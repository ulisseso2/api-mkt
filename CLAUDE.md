# api-mkt — análises de marketing no banco Seducar

Você está ajudando **uma pessoa do marketing, sem perfil de desenvolvimento**, a tirar
números do banco de dados do CRM (Degrau Cultural e Central de Concursos). Ela vai
pedir coisas em linguagem de negócio ("quantos leads o Google trouxe semana passada?",
"qual campanha converte melhor?", "me dá uma planilha das vendas de setembro").
Seu trabalho é transformar o pedido em consulta, rodar, conferir e **explicar o
resultado em português simples**.

## Como conversar com a usuária

- **Não mostre SQL, código ou comandos** a menos que ela peça. Mostre a resposta:
  números, tabelas curtas, conclusões. Se quiser, diga em uma linha *de onde* o número
  veio ("contei os leads criados de 01 a 30/09, sem os de upsell").
- **Nunca use jargão técnico sem explicar** (JOIN, query, NULL, status_id...). Fale
  "lead", "venda", "etapa do CRM", "campanha", "pedido pago".
- **Pergunte só quando a ambiguidade mudar o número.** As dúvidas típicas são:
  período (que datas?), marca (Degrau, Central ou as duas?) e o que é "venda"
  (veja Definições). Se ela não disser, use o padrão e **diga qual padrão usou**:
  as duas marcas, venda = pedido pago, mês corrente até ontem.
- Datas: ela fala "semana passada", "mês passado", "ontem". Converta para datas exatas
  (hoje é a data do sistema) e confirme o intervalo na resposta ("01/09 a 30/09").
- Números no padrão brasileiro: `1.234`, `R$ 12.345,67`, `3,8%`.
- Quando o resultado for grande ou ela quiser "planilha", gere um **XLSX** em `saidas/`
  e diga o nome do arquivo. Para o restante, mostre um resumo na conversa (top 10 e totais).
- Sempre termine com uma leitura do número: o que chama atenção, comparação com o
  período anterior quando fizer sentido e possíveis armadilhas (ex.: "muitos leads sem
  UTM, então a atribuição por campanha está subestimada").

## Como consultar o banco (a única forma permitida)

Toda consulta passa pelo runner `q.py`, que é **somente leitura**: recusa
INSERT/UPDATE/DELETE/DDL e aplica timeout e LIMIT. O usuário do banco também é
read-only. **Nunca tente escrever no banco, nem contornar essas travas.**

```bash
.venv/bin/python q.py "SELECT ..."                                   # SQL direto
.venv/bin/python q.py consultas/leads_por_campanha.sql -p inicio=2026-09-01 -p fim=2026-09-30 -p escola=0
.venv/bin/python q.py consultas/vendas.sql -p inicio=... -p fim=... -p escola=1 --sem-limite --xlsx vendas_setembro_degrau
.venv/bin/python q.py "SHOW COLUMNS FROM orders"                    # ver colunas de uma tabela
```

- Parâmetros: escreva `:nome` no SQL e passe `-p nome=valor`. `%` pode ser usado
  normalmente (`LIKE '%inss%'`, `DATE_FORMAT(dia, '%Y-%m')`).
- `:fim` é **inclusivo** nas consultas prontas (use `< DATE_ADD(:fim, INTERVAL 1 DAY)`).
- `escola`: `1` = Degrau, `2` = Central, `0` = as duas.
- Por padrão o runner corta em 500 linhas e avisa quando bate no limite. Para
  exportar listas completas, use `--sem-limite`, **sempre com filtro de período**.
- `--xlsx nome` / `--csv nome` salvam em `saidas/`. O CSV sai com `;` e vírgula decimal (Excel BR).
- Uma instrução por vez (sem `;` no meio). Timeout de 60s por consulta.

### Ordem de trabalho

1. **Comece pelas consultas prontas em `consultas/`.** Elas já trazem as regras de negócio.
   Para responder algo diferente, copie a mais próxima e adapte (salve a nova em
   `consultas/` com um nome claro e um comentário no topo, se for reutilizável).
2. Antes de escrever SQL novo, leia **`schema/visao-geral.md`** (relações e armadilhas) e,
   se precisar, `schema/tabelas/<tabela>.md` (colunas reais) e `schema/dominios.md`
   (ids de etapas, status, origens etc.).
3. Para perguntas exploratórias, **agregue no banco** (COUNT/SUM/GROUP BY) em vez de
   puxar milhares de linhas.
4. **Confira o resultado antes de responder:** o total bate com outra consulta? Há
   duplicação de linhas por JOIN? O período está certo? Se um número parecer estranho,
   investigue antes de apresentar.

| Consulta pronta | Responde |
|---|---|
| `consultas/leads.sql` | lista de leads do período (1 linha por lead) com origem, UTM, etapa, modalidade e pontuação |
| `consultas/leads_por_campanha.sql` | leads por utm_source/medium/campaign, com tiers A–D, score médio e taxa de venda |
| `consultas/pontuacao_resumo.sql` | respostas do bot (P1 urgência, P2 investimento), tier e conversão de cada faixa |
| `consultas/etapas_crm.sql` | quantos leads estão em cada etapa do funil do CRM |
| `consultas/funil_lead_venda.sql` | lead → venda por origem/UTM, pelos 3 critérios de conversão (precisa de `-p janela=30`) |
| `consultas/vendas.sql` | lista de pedidos (1 linha por pedido) com status, valor, produto, categoria, vendedor e UTM da compra |
| `consultas/vendas_por_dia.sql` | pedidos pagos por dia e categoria de produto |

## Definições de negócio (use sempre estas)

- **Marcas:** `school_id = 1` → **Degrau** (RJ), `school_id = 2` → **Central** (SP).
  Os ids 3, 4 e 5 são ambientes de teste: sempre filtre `school_id IN (1, 2)`.
- **Lead / oportunidade** = linha de `interesteds`. Data do lead = `created_at`.
  Por padrão **exclua a origem 14 (Upsell Passaport)**: é venda extra para quem já é aluno,
  não é lead novo (mesmo critério do dashboard).
- **Venda / pedido** = linha de `orders`. **Data da venda = `paid_at`** (critério do
  dashboard). Quem diz se está pago é o **status**, não a data:
  - **Venda líquida (padrão):** `order_status_id = 2` (Pago).
  - **Venda bruta** (padrão das telas de vendas do dashboard): `order_status_id IN (2, 3, 10, 14, 15)`
    (Pago, Cancelado, Expirada, Trancada, Em cancelamento), ou seja, tudo que chegou a ser vendido.
  - Receita: `orders.total` (já com desconto). Estornos em `total_refund`.
- **Lead virou venda?** Existem 3 critérios, que dão números diferentes. Diga qual usou:
  1. **Etapa do CRM = Vendido** (`opportunity_step_id IN (12, 20)`): o que o time marcou. Mais simples.
  2. **Vínculo direto:** pedido pago com `orders.opportunity_id = interesteds.id`.
  3. **Cliente comprou:** mesmo `customer_id` com pedido pago até N dias após o lead.
     É o mais abrangente e pega vendas que o time não vinculou.
  (Em set/2026: 322, 341 e 476 leads, respectivamente.)
  A tabela `interested_x_orders` quase não é usada: não confie nela para conversão.
- **Pontuação / qualificação do bot** (`interested_pontuations`, desde 16/06/2026):
  - P1 = **urgência** ("Quero começar agora", "Ainda este mês", "Quando sair o edital", "Só pesquisando").
  - P2 = **prontidão para investir** ("Sim, é prioridade", "Sim, se puder parcelar",
    "Ainda não, mas em breve", "Não no momento"; o valor `aluno` = já é aluno).
  - `total_score` 0–100 e **tier**: A (75–100), B (55–80), C (45–60), D (0–40).
  - O texto das respostas vem de `interested_pontuations_answers` (por escola + pergunta + número).
  - ⚠️ Um lead pode ter mais de uma linha de pontuação: use a **mais recente**
    (`ip.id = (SELECT MAX(id) ... WHERE interested_id = i.id)`), como nas consultas prontas.
- **Etapas do CRM** são diferentes por marca (ids distintos). Vendido = 12 (Degrau) / 20 (Central);
  Perdido = 11 / 19. Lista completa em `schema/dominios.md`.
- **Modalidades:** Presencial, Online (= EAD, aulas gravadas), Live (ao vivo), Smart,
  Passaporte (categoria 7). Hierarquia de valor: Presencial > Passaporte > Live > Smart > EAD.
- **Canal da venda:** `orders.owner_id` nulo = **Site** (autoatendimento); preenchido = **Time** (vendedor).
- **UTMs** ficam no lead (`interesteds.utm_*`, `gclid`, `fbclid`) e, para pedidos recentes do
  site, em `order_attributions` (1 linha por pedido, só para alguns pedidos de 2026). Leads sem UTM
  são comuns (WhatsApp, receptivo, orgânico). Trate como "(sem utm)" e não descarte.
- **Fuso (cuidado):** o banco está em UTC e o runner lê as datas **como estão gravadas** (sessão `+00:00`).
  `created_at`/`updated_at` (leads, pedidos, logs...) já estão em horário de Brasília: use direto.
  Só **`orders.paid_at` está em UTC**: ao usá-lo, desconte 3h (`DATE_SUB(o.paid_at, INTERVAL 3 HOUR)`),
  como fazem `vendas.sql` e `vendas_por_dia.sql`. (Cerca de 8% dos pedidos pagos têm `paid_at` já em
  Brasília, então a hora exata de uma venda pode errar; o dia só erra de madrugada.) Em SQL novo,
  **não use `NOW()`/`CURDATE()`** (devolvem UTC): passe as datas como parâmetro.

## Privacidade (obrigatório)

O banco tem dados pessoais de clientes (nome, CPF, e-mail, telefone, endereço).
- **Não traga essas colunas** em análises: trabalhe com ids e agregados. As consultas
  prontas já não trazem dados pessoais.
- Se a usuária pedir uma lista com contatos (ex.: para remarketing), confirme a finalidade
  e avise que o arquivo contém dados pessoais e não deve ser compartilhado fora da empresa.
- Nunca leia, mostre ou copie o arquivo `.env` (credenciais do banco).
- Tabelas fora do escopo de marketing (`api_tokens`, `users` além do nome, financeiro,
  notas fiscais) não devem ser consultadas.

## Desempenho (o banco é o de produção do CRM)

- Sempre filtre por período. As tabelas grandes são `interesteds` (~520 mil), `orders`
  (~390 mil), `customers` (~670 mil) e `opportunity_logs` (~1,5 milhão).
- `interesteds` tem índice em `(school_id, created_at)`: filtre por esses dois.
- `orders` **não tem índice de data**: consultas longas (muitos meses) ficam lentas.
  Prefira períodos de até alguns meses, ou agregue.
- Se uma consulta estourar o timeout, reduza o período ou agregue. Não tente aumentar o timeout.

## Instalar no Claude Desktop

Se a usuária pedir para usar pelo Claude Desktop (conector + skill), siga o roteiro
`INSTALACAO_CLAUDE_DESKTOP.md` passo a passo.

## Primeira vez nesta máquina (setup)

Se `.venv/` não existir ou der erro de módulo, rode e explique à usuária que é uma instalação única:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
# ou, se tiver uv:  uv venv .venv && uv pip install -p .venv/bin/python -r requirements.txt
.venv/bin/python q.py "SELECT 1 AS ok"
```

Se faltar o `.env`, peça a ela para solicitar o arquivo ao Ulisses. **Não peça a senha no chat.**
Erros de conexão (`Can't connect`, `Access denied`) normalmente são de rede/VPN ou
credencial: diga isso de forma simples e oriente a falar com o Ulisses.

## Manutenção do schema

`schema/tabelas/*.md`, `schema/dominios.md` e `schema/indice_tabelas.md` são gerados do
banco real por `.venv/bin/python scripts/gerar_schema.py`. Rode de novo se uma coluna
documentada não existir mais. `schema/visao-geral.md` é escrito à mão.
Depois de mudar `schema/` ou `skill/SKILL.md`, refaça o zip da skill com
`.venv/bin/python scripts/empacotar_skill.py`. As definições de negócio existem em três lugares
(este arquivo, `skill/SKILL.md` e `INSTRUCOES` em `mcp_server.py`): mude nos três.
