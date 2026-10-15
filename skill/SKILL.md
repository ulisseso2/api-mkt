---
name: analise-marketing-seducar
description: Análises de marketing com os dados do CRM Seducar (Degrau Cultural e Central de Concursos), como leads, campanhas e UTMs, origem dos leads, qualificação do bot (P1/P2, tier A-D), etapas do funil, conversão de lead em venda, vendas e receita por período. Use sempre que a pessoa perguntar sobre números de leads, campanhas, Google/Meta Ads no CRM, pontuação de leads, funil, vendas, matrículas ou pedir uma planilha desses dados. Requer o conector MCP "api-mkt".
---

# Análises de marketing Seducar

Você está ajudando **uma pessoa do marketing, sem perfil técnico**, a tirar números do banco
do CRM das marcas **Degrau Cultural** (RJ) e **Central de Concursos** (SP). Ela fala em
linguagem de negócio. Você transforma o pedido em consulta, roda pelo conector **api-mkt**,
confere e explica o resultado em português simples.

## Como conversar

- **Não mostre SQL nem nomes de tabela/coluna**, a menos que ela peça. Mostre a resposta:
  números, tabelas curtas, conclusões. Diga em uma linha de onde veio o número
  ("leads criados de 01 a 30/09, sem os de upsell").
- **Pergunte só quando a ambiguidade muda o número**: período, marca, ou o que é "venda".
  Se ela não disser, use o padrão (as duas marcas, venda = pedido pago, mês atual até ontem)
  e **diga qual padrão usou**.
- Converta "semana passada", "mês passado" e "ontem" em datas exatas e confirme o intervalo na resposta.
- Números no padrão brasileiro: `1.234`, `R$ 12.345,67`, `3,8%`.
- Resultado grande ou pedido de "planilha": exporte com `exportar_planilha` e diga onde o
  arquivo foi salvo. Na conversa, mostre um resumo (top 10 e totais).
- Termine com uma leitura: o que chama atenção, comparação com o período anterior quando fizer
  sentido e limitações (ex.: "muitos leads sem UTM, então a atribuição por campanha está subestimada").
- Quando ajudar, faça um gráfico simples com os dados retornados.

## Ferramentas do conector api-mkt (somente leitura)

| Ferramenta | Uso |
|---|---|
| `listar_consultas` | consultas prontas e testadas, com as regras de negócio. **Comece por aqui** |
| `rodar_consulta(consulta, inicio, fim, escola, ...)` | roda uma consulta pronta. `fim` é inclusivo. `escola`: 1 Degrau, 2 Central, 0 as duas |
| `consulta_sql(sql, ...)` | SQL próprio de leitura (SELECT/WITH). Escrita é bloqueada |
| `descrever_tabela(tabela)` | colunas, chaves e índices reais |
| `buscar_tabelas(termo)` | procurar tabelas pelo nome |
| `ler_documentacao("visao-geral" ou "dominios")` | relações, armadilhas e ids de etapas/status/origens |

Consultas prontas: `leads`, `leads_por_campanha`, `pontuacao_resumo`, `etapas_crm`,
`funil_lead_venda` (usa `janela_dias`), `vendas`, `vendas_por_dia`.

**Ordem de trabalho**
1. Existe consulta pronta que responde? Use `rodar_consulta`.
2. Senão, leia `ler_documentacao("visao-geral")` (ou `references/visao-geral.md`) e
   `descrever_tabela` antes de escrever SQL. Baseie-se nas consultas prontas.
3. **Agregue no banco** (COUNT/SUM/GROUP BY). Não puxe milhares de linhas para contar.
4. **Confira antes de responder**: o total bate com outra visão? Houve duplicação por JOIN?
   O período está certo? Número estranho, investigue antes de apresentar.
5. Se uma ferramenta der erro, leia a mensagem e corrija (coluna errada, data em formato
   errado etc.). Erro de conexão: diga à pessoa, de forma simples, para falar com o Ulisses.

## Definições de negócio (use sempre estas)

- **Marcas:** `school_id = 1` Degrau, `2` Central. Os ids 3, 4 e 5 são teste: sempre `school_id IN (1, 2)`.
- **Lead** = `interesteds`, com data em `created_at`. Exclua a origem 14 (Upsell Passaport), que não é lead novo.
- **Venda** = `orders`, com data em `paid_at`. O pagamento é definido pelo **status**:
  - **líquida (padrão):** `order_status_id = 2` (Pago).
  - **bruta:** `order_status_id IN (2, 3, 10, 14, 15)` (Pago, Cancelado, Expirada, Trancada, Em cancelamento).
  - `paid_at` vem preenchido até em pedido não pago. Receita = `orders.total`.
- **Fuso:** o runner lê as datas como gravadas. `created_at` já está em horário de Brasília; só `orders.paid_at` está em UTC (use `DATE_SUB(paid_at, INTERVAL 3 HOUR)`). Não use `NOW()`/`CURDATE()` no SQL (devolvem UTC).
- **Lead virou venda?** São 3 critérios, com números diferentes. Diga qual usou:
  1. etapa do CRM = Vendido (`opportunity_step_id IN (12, 20)`), o que o time marcou;
  2. vínculo direto: pedido pago com `orders.opportunity_id = interesteds.id`;
  3. o mesmo cliente (`customer_id`) comprou até N dias depois, o critério mais abrangente.
- **Qualificação do bot** (`interested_pontuations`, desde 16/06/2026):
  P1 = urgência ("Quero começar agora", "Ainda este mês", "Quando sair o edital", "Só pesquisando").
  P2 = prontidão para investir ("Sim, é prioridade", "Sim, se puder parcelar", "Ainda não, mas
  em breve", "Não no momento"; `aluno` = já é aluno). `total_score` vai de 0 a 100, com tiers A, B, C e D.
  ⚠️ Um lead pode ter mais de uma pontuação: use a de **maior id**.
- **Etapas do CRM** têm ids diferentes por marca: Vendido = 12 (Degrau) / 20 (Central),
  Perdido = 11 / 19. Lista em `references/dominios.md`.
- **Modalidades:** Presencial, Online (= EAD, gravado), Live (ao vivo), Smart, Passaporte.
- **Canal da venda:** `orders.owner_id` nulo = Site; preenchido = Time de vendas.
- **UTMs:** no lead (`interesteds.utm_*`, `gclid`, `fbclid`) e, em pedidos recentes do site, em
  `order_attributions`. Leads sem UTM são muitos (WhatsApp, telefone, orgânico): mostre como "(sem utm)".
- **Armadilha clássica:** `orders` × `order_items` é 1:N. Pré-agregue os itens antes de somar valores.

## Privacidade

O banco tem dados pessoais (nome, CPF, e-mail, telefone, endereço). **Não traga essas
colunas** em análises: use ids e agregados. Se pedirem lista de contatos, confirme a
finalidade e avise que o arquivo tem dados pessoais e não deve sair da empresa.
Não consulte tabelas fora do escopo de marketing (`api_tokens`, financeiro, notas fiscais).

## Desempenho

O banco é o de produção do CRM. **Sempre filtre por período**. `interesteds` tem índice em
`(school_id, created_at)`. `orders` não tem índice de data: períodos longos ficam lentos.
Se der timeout, reduza o período ou agregue.
