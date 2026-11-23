---
name: "seducar-analise-financeira"
description: "Análise financeira da Degrau e Central no banco Seducar (MCP mkt-seducar / api-mkt): vendas, matrículas, turmas, custo de professor, cancelamentos, despesas, contas a pagar e caixa. Conhece o fluxo de pagamentos do dashboard (pedido de compra, aprovação, lote de pagamento, baixa, competência, rateio, documentos, recorrência e clones). Use para DRE, despesa por competência, resultado de unidade ou turma, fornecedores, pagamentos do mês, atrasos, pendências de documento e contas que se repetem."
---

# Análise financeira Seducar (Degrau e Central)

Use esta skill para qualquer pergunta financeira sobre a Degrau Cultural e a Central de Concursos feita sobre o banco Seducar pelo MCP `mkt-seducar`. Exemplos:

- receita, ticket e mix de produtos;
- cancelamentos e devoluções;
- turma que se paga ou não e custo de professor por turma, curso ou unidade;
- despesas por centro de custo;
- receita e despesa de uma unidade física;
- DRE gerencial, contas a pagar e fluxo de caixa ou de recebíveis.

O banco é de produção e o acesso é só leitura (`consulta_sql`). Toda consulta deve ter filtro de período e escola, e deve agregar no banco.

## Como trabalhar

1. **Entenda a pergunta financeira.** Defina o regime (competência ou caixa), o período, a escola e o nível de análise: pedido, turma, curso, unidade ou centro de custo. Se o regime não estiver claro, use competência para receita e caixa (data de pagamento) para despesa, e diga isso na resposta.
2. **Vendas e leads simples:** use primeiro as consultas prontas (`listar_consultas` / `rodar_consulta`: `vendas`, `vendas_por_dia`, `funil_lead_venda`). Elas já aplicam as regras de data e status.
3. **Análises cruzadas:** parta dos modelos SQL abaixo. Antes de usar uma tabela que não está aqui, rode `descrever_tabela`.
4. **Valide antes de concluir.** Confira os totais contra uma visão independente. Exemplos:
   - receita por turma somada contra a receita total do período;
   - despesas rateadas somadas contra a soma das parcelas.
5. **Volume grande:** use `exportar_planilha` e trabalhe a planilha. Não pagine linha a linha pela conversa.
6. **Na resposta:**
   - mostre o número;
   - diga a definição usada (status, data, regime);
   - aponte as limitações de dado que afetam aquele número (veja "Armadilhas").

## Mapa do modelo de dados

```
VENDAS / MATRÍCULAS
orders ──< order_items >── products ── product_categories
  │            └── classroom_id ──> classrooms ──> courses ──> course_sales
  │                                     │            └── scholarity_id (médio/superior)
  │                                     ├── units, shifts, classroom_modalities
  │                                     └── start_type ('mother' | 'cyclical' | NULL)
  ├── order_status, payment_methods, order_cancelation_types, return_methods
  ├── unit_id (unidade do pedido) e seller_unit_id (unidade do vendedor)
  ├── order_installments (agenda de recebíveis por parcela)
  ├── order_refunds / purchase_orders.cancellation_order_id (devolução paga)
  ├── order_id (pedido pai) e letter_credit_id (carta de crédito)
  └── customers

PEDAGÓGICO (CUSTO DE AULA)
classrooms ──< grids ──< grid_x_lessons >── grid_lessons ──> teachers (value_higher / value_lower)
                                              ├── grid_lesson_status, grid_lesson_categories
                                              └── teacher_points_report_id ──> teacher_points_reports ──< teacher_points_report_items

DESPESAS (CONTAS A PAGAR)
purchase_orders ──< purchase_order_installments (vencimento = date, pagamento = completed, valor = total_final)
  ├── order_plans (plano de contas) ──> cost_centers (centro de custo)
  ├── purchase_order_categories, suppliers, order_document_types, purchase_order_status
  └──< purchase_order_strategic_units ──< business_x_strategics (rateio %) ──> business_units, strategic_units

CAIXA
bank_accounts (saldo), cash_flows (entradas manuais), transfers, bank_account_logs
```

## Regras que não podem ser esquecidas

### Gerais
- `school_id` 1 = Degrau e 2 = Central. Os ids 3, 4 e 5 são teste: sempre filtre `school_id IN (1,2)` em todas as tabelas da consulta.
- Não use `NOW()`/`CURDATE()` porque devolvem UTC. Passe as datas explícitas.
- `UNION` entre tabelas diferentes pode dar "Illegal mix of collations". Converta as colunas de texto com `CONVERT(col USING utf8mb4) COLLATE utf8mb4_unicode_ci`.
- Subconsulta correlacionada sobre `customers` (cerca de 670 mil linhas) estoura o tempo limite. Prefira JOIN por coluna indexada (`school_id, cpf` / `school_id, email`) ou `UNION ALL` de JOINs.
- O MCP bloqueia como "comando de escrita" qualquer SQL que contenha palavras como `REPLACE`, mesmo sendo a função de texto. Use `CASE` no lugar (ex.: `CASE WHEN TRIM(LOWER(cc.name)) = 'cancelamentos de vendas' THEN 'cancelamento de vendas' ELSE TRIM(LOWER(cc.name)) END`).

### Vendas
- **Data da venda:** é `orders.paid_at`. Desde a correção de 20/10/2026, `orders.paid_at`, `orders.request_date` e `transactions.paid_at` estão em **horário de Brasília** (todo o histórico foi convertido; os valores antigos em UTC ficaram em `*_tz_original`). Use direto, **sem `DATE_SUB` de 3h**: `o.paid_at >= 'AAAA-MM-01' AND o.paid_at < 'AAAA-MM+1-01'`. Se uma consulta pronta ou instrução antiga mandar descontar 3h, ela está desatualizada.
- **Status é o que define a venda**, e não o `paid_at`, que vem preenchido até em pedido não pago.
  - Líquida: `order_status_id = 2`.
  - Bruta: `IN (2,3,10,14,15)`.
- **Pedido de valor zero não é receita, mas é matrícula.** Os pagamentos Carta de Crédito (8), Bônus (14), Cortesia (5), Experimental (13) e Migração (4) geram pedidos de valor zero ou simbólico. Exemplo: na Degrau, no 3º trimestre de 2026, cerca de 7 mil dos 10 mil pedidos pagos tinham total zero.
  - Para receita: some `orders.total`.
  - Para contar alunos na turma: conte todos os pedidos pagos com o item na turma e separe em "pagantes" (`total > 0`) e "não pagantes".
- **Passaporte e carta de crédito:**
  - O aluno paga o Passaporte (categoria 7) uma vez e recebe uma carta de crédito em horas (`letter_credits`: `total`, `price_hour`, `passport = 1`).
  - Depois ele se matricula nas turmas por pedidos filhos de valor zero, pagos com Carta de Crédito (`orders.order_id` = pedido pai).
  - Por isso, a receita de uma turma **não inclui** o valor do Passaporte desses alunos. Quando a pergunta for rentabilidade por turma, mostre separado quantos matriculados vieram de Passaporte ou carta. Se o usuário quiser imputar receita, uma estimativa possível é horas consumidas × `price_hour`. Deixe claro que é estimativa.
- **Pedido com vários itens:** `order_items.price - discount` nem sempre fecha com `orders.total`. Para atribuir receita a turma ou produto, rateie o total do pedido pelo peso do `price` de cada item: `o.total * i.price / SUM(i.price) OVER (PARTITION BY o.id)`. Nunca some `orders.total` depois de juntar com `order_items` sem esse rateio, porque o pedido duplica.
- **Rótulo de categoria e curso** (padrão do relatório de pedidos): item sem turma com categoria 7 = "Passaporte"; categoria 10 = "Degrau Smart" ou "Central Smart". Unidade do pedido sem turma: categoria 3 = Live, 10 = Smart, 2 = EAD.
- **Recebíveis:** `order_installments` tem o calendário das parcelas (`date`, `amount`), com datas até 2028. A soma das parcelas bate com o total em mais de 85% dos pedidos de cartão. O `paid_at` das parcelas **não é preenchido**, então use a tabela como projeção de entrada de caixa, não como baixa.

### Cancelamentos
- **Status:** 3 Cancelado e 15 Em cancelamento. Os status 11 (Estorno Total) e 21 (Estorno Parcial) aparecem quase só na Central.
- **Data do cancelamento:** `orders.request_date` (solicitação). O relatório de pedidos usa `COALESCE(request_date, paid_at)` como data de referência.
- **Valores:**
  - `orders.total_refund` = valor devolvido;
  - `orders.fine` = % de multa;
  - retido = `total - total_refund`.
- **Tipo** (`order_cancelation_types`):

  | id | Tipo | Multa |
  |---|---|---|
  | 1 | Dentro do Prazo | 10% |
  | 2 | Fora do Prazo | 30% |
  | 3 | Turma Cancelada | — |
  | 4 | Devolução Proporcional | — |
  | 5 | Migração Passaporte | — |
  | 6 | Alteração no início da turma | — |

  Os tipos 3 e 6 são **cancelamentos causados pela operação**, não pelo aluno. Analise-os separadamente.
- **Como a devolução sai do caixa:** `return_methods` (1 Estorno no cartão, 2 Depósito). A devolução por depósito vira conta a pagar no centro de custo "Cancelamento de Vendas" (cc 7 na Degrau, 58 na Central), ligada por `purchase_orders.cancellation_order_id` e `order_refunds.purchase_order_id`.
  - **Não some** `total_refund` com essas despesas na mesma DRE: é o mesmo dinheiro contado duas vezes. Na DRE, cancelamento é dedução da receita (`total_refund` por `request_date`), e o centro de custo de cancelamento sai das despesas.
- **Carta de crédito gerada por cancelamento:** fica em `letter_credits`. O valor vira crédito para uso futuro, não sai do caixa.

### Turmas e pedagógico
- **Valor para iniciar a turma:** é a meta de faturamento definida no curso. Para `start_type = 'mother'` (turma mãe) use `courses.mother_value`; para `'cyclical'` (turma cíclica) use `courses.cyclical_value`. Turma com `start_type` NULL não tem meta: deixe fora da análise "atingiu o valor para iniciar".
- **Data de início da turma:** `classrooms` não tem data de início. Use `MIN(grid_lessons.date)` da grade (e `MAX` para o fim). `classrooms.date_end` existe, mas nem sempre vem preenchido.
- **Aula → turma:** sempre por `grids.classroom_id` → `grid_x_lessons` → `grid_lessons`. A coluna `grid_lessons.grid_id` nunca vem preenchida.
- **Aula compartilhada:** uma mesma aula pode estar na grade de várias turmas, o que vale para mais da metade das aulas. O custo dela deve ser **rateado** por `COUNT(DISTINCT grid_id)` em `grid_x_lessons`. Sem o rateio, o custo por turma infla.
- **Custo estimado da aula:** `(TIME_TO_SEC(workload) - 900)/3600` horas (desconta 15 min de intervalo, com mínimo de 0) × taxa do professor ÷ turmas que compartilham a aula.
  - Taxa = `teachers.value_higher` quando `courses.scholarity_id IN (5,7,10,13,18,19)` (superior, licenciatura, pós, mestrado).
  - Nos outros casos, taxa = `teachers.value_lower`.
- **Que aulas contar:** só as de `grid_lesson_status_id = 1` (Ativo). Status 2 Inativo, 3 Cancelado, 4 Faltou e 5 Adiado não geram custo. Categorias da aula: 1 Normal, 2 Bônus, 3 Extra, 4 Gratuita, 5 Correção.
- **Custo real pago ao professor:**
  - Degrau: `teacher_points_reports` / `teacher_points_report_items` (relatórios quinzenais, com `total_to_pay` e horas médio/superior). Cada `grid_lessons.teacher_points_report_id` liga a aula ao relatório. A Central não usa essa tabela.
  - Nas duas escolas, o pagamento aparece em contas a pagar, no centro de custo "Pedagógico" (Pagto de Professor e "500. Pagamento de Professores").
  - Para comparar estimado com real, use o mesmo período de aula.

### Despesas (contas a pagar)
- **Unidade de análise:** a parcela (`purchase_order_installments`).
  - Valor = `total_final` (valor final, com juros ou desconto). `total` é o valor original.
  - Vencimento = `date`. Pagamento = `completed`. `paid_at` quase nunca vem preenchido.
- **Status da parcela:** 1 A pagar, 2 Análise, 3 Aprovado, 4 Pago, 5 Cancelado. **Sempre exclua o 5.** Existem pedidos com parcelas canceladas e substituídas, e somar tudo dá mais que o total do pedido.
  - Pago (regime de caixa) = `status 4` com `completed` no período.
  - Despesa por competência = `competence` no período, status diferente de 5 (veja "Competência" abaixo).
- **Rateio:** cada pedido de compra tem 1 unidade estratégica (`purchase_order_strategic_units`, 100%) e N unidades de negócio em `business_x_strategics.percent`, que somam 100 por pedido. O valor rateado é `total_final * bxs.percent / 100`.
  - Juntar com `business_x_strategics` **sem** multiplicar pelo percentual duplica a despesa.
  - Para total sem rateio, não junte essas tabelas.
- **Unidades estratégicas:** 1 Degrau Cultural, 2 Conselho, 3 Editora Azul, 4 Central de Concursos, 5 Central Administradora, 6 Gestão administrativa, 7 Gerencial.
  - Na Degrau, parte relevante das despesas é do Conselho ou da Editora Azul.
  - Para o resultado operacional da escola, filtre a unidade estratégica da própria escola e mostre as demais à parte.
- **Unidades de negócio:** prefixo DC = Degrau (Alfândega, Campo Grande, Madureira, Niterói, Taquara, Live, Virtual, Questões, Corporativo); CC = Central (República, Live, Questões, Santo André, Santo Amaro, Osasco, Paulista, Guarulhos, EAD). Use-as para despesa por unidade física.
- **Dois planos de contas:**
  - A Degrau usa o plano antigo (centros de custo 6 a 33, nomes sem número).
  - A Central usa o plano novo (centros de custo 34 a 60, planos numerados como "500. Pagamento de Professores").
  - Os nomes quase coincidem. Para comparar as escolas, agrupe por `TRIM(LOWER(cost_centers.name))` e normalize "cancelamentos de vendas" = "cancelamento de vendas" com `CASE`.
- **Fora das despesas operacionais:**
  - "Partida Dupla - Despesa" (59) e "Partida Dupla - Receita" (60): lançamentos contábeis, empréstimo de capital de giro, transferências;
  - "Receitas" (34);
  - "Investimentos" (44): CAPEX, mostrar separado;
  - "Retirada dos sócios" (45);
  - "Cancelamento de Vendas" (7/58): já está na dedução da receita.
- **Período com dado:** contas a pagar existe na Degrau desde dez/2024 e na Central desde dez/2025. Antes disso, "sem despesa" significa sem registro.
- **Tipo do pedido de compra:** `purchase_orders.order_type` 'normal' ou 'avulso'. Status do pedido: 1 Lançado, 2 Aprovado Pgto, 3 Gerado Pgto, 4 Pago, 5 Reprovado, 6 Cancelado.

### Fluxo de pagamentos (como o dashboard cria e paga uma conta)

Tela: Financeiro → Pedidos de compra / Pagamentos. Tudo fica em `purchase_orders` (o "pedido") e
`purchase_order_installments` (as parcelas). Saber o caminho explica os status que aparecem no banco.

**Dois jeitos de lançar** (`purchase_orders.order_type`):

| Tipo | Como nasce | Situação hoje |
|---|---|---|
| `normal` | Pedido de compra que passa pelas etapas Lançado (1) → Unidade (2) → Financeiro (3), com aprovação em cada uma | Quase parou: na Degrau são 0 a 15 por mês desde mai/2026; a Central não usa desde dez/2025 |
| `avulso` | "Criar pagamento" direto na tela de Pagamentos, já na etapa Financeiro (3) e status Gerado Pgto (3) | É o caminho real: ~350–390/mês na Degrau, ~40–90/mês na Central |

Por isso quase todo pedido está em `purchase_order_step_id = 3`. "Pedido sem aprovação" não é anomalia:
o Financeiro lança direto. Quem tem acesso aos botões é definido por permissão de perfil no dashboard.

**Status do pedido × status da parcela.** Quem diz se o dinheiro saiu é a **parcela**:
- parcela `status 4` (Pago) com `completed` = data da baixa. `paid_at` da parcela **nunca** vem preenchido;
- o pedido só vira status 4 (Pago) quando **todas** as parcelas foram pagas. Um pedido em 2 (Aprovado Pgto)
  ou 3 (Gerado Pgto) pode ter parcelas já pagas: na Central, 1.764 parcelas pagas estão em pedidos ainda "Gerado Pgto";
- pedido 6 (Cancelado) tem todas as parcelas em 5. Pedido 5 (Reprovado) só existe no fluxo `normal`;
- parcela 3 (Aprovado) = liberada para pagar e ainda não baixada. Parcela 2 (Análise) praticamente não é usada.
- `purchase_orders.completed`, `hours`, `fine`, `workload`, `total_refund` e `order_id` existem, mas **não são usados**
  (vazios ou zero). Não tire conclusão deles.

**Valores e datas da parcela:** `total` = valor original lançado; `total_final` = valor efetivamente pago (com juros,
multa ou desconto). Use `total_final`. Na Central, mais da metade das parcelas pagas tem `total_final ≠ total`.
`date` = vencimento; `completed` = pagamento. `bank_account_id` na parcela = conta de onde saiu.
Em jul–out/2026, 35% das parcelas pagas da Degrau saíram depois do vencimento (média de 3,8 dias); na Central, 19%.

**Competência** (`purchase_order_installments.competence`, desde 23/11/2026): o mês a que a despesa se
refere, separado do vencimento (`date`) e do pagamento (`completed`).
- Gravada como o **1º dia do mês** (`2026-11-01`). Filtre por intervalo de meses:
  `i.competence >= '2026-10-01' AND i.competence <= '2026-12-01'`. Mostre como `MM/AAAA`.
- É **por parcela**: num parcelado, cada parcela tem a sua (padrão: avança 1 mês por parcela).
- **Sempre preenchida.** Quem lança pode informar; se não informar, vale o mês do vencimento. Devolução de
  cancelamento = mês em que foi processada. Clone = competência da origem + 1 mês (editável no modal).
- **Histórico preenchido por regra** (migration de 23/11/2026), não por pessoa: pedido de 1 parcela com mês/ano
  escrito na descrição ("ref 10/26") a até 6 meses do vencimento → esse mês; senão, e em parcelados, o mês do
  vencimento. Resultado: na Degrau, ~3.100 de ~14.200 parcelas ficaram com competência diferente do mês do
  vencimento (quase sempre 1 mês antes: conta de outubro paga em novembro); na Central, nenhuma (a Central
  quase não escreve o mês na descrição). Para períodos antigos, avise que a competência é inferida.
- A descrição continua com o mês escrito; não a use mais para competência.
- No Dashboard Financeiro, a aba "Despesas pagas" tem o regime Pagamento/Competência; o regime Competência
  conta só parcelas pagas cuja competência cai no período.

**Lotes de aprovação e de pagamento** (`purchase_order_movements` + `purchase_order_movement_items`):
cada clique de aprovar ou pagar em lote grava um movimento com `user_id`, `total_value` e os pedidos do lote.
- `old_status 1 → 2` (etapa 1 → 2 ou 3): aprovação de pedido `normal`; `1 → 5`: reprovação.
- `old_status 2 → NULL` na etapa 3, com `bank_id` preenchido: **pagamento em lote** pelo Financeiro (o grosso dos
  movimentos da Degrau). `movement_items.value` = valor pago daquele pedido no lote.
- A Central praticamente não usa lotes desde dez/2025. Para "quem pagou/aprovou e quando", use essas tabelas e
  `users.full_name`; para "quanto saiu", use as parcelas (`completed`), não os movimentos.

**Rateio** (resumo do que está em Despesas): o lançamento escolhe 1 unidade estratégica e 1 ou mais unidades
de negócio com percentual. O dashboard grava a unidade estratégica em `purchase_order_strategic_units` e o
rateio em `business_x_strategics` (`percent` soma 100).

**Parcelamento:** `purchase_orders.installments` = nº de parcelas. 91% dos pedidos da Degrau têm 1 parcela;
os demais (3, 10, 12x...) são acordos, empréstimos e compras parceladas, com parcelas que vencem meses à frente.
Uma conta mensal recorrente costuma ser **um pedido novo por mês** com 1 parcela, não um pedido de 12 parcelas.

**Documentos** (obrigatórios para pagar, mas chegam depois):
- número do documento: `purchase_orders.document_number` (nota, boleto); tipo em `order_document_types`;
- anexos: `purchase_order_files` (por pedido) e `purchase_order_installment_medias` (por parcela).
  Uma parcela "tem documento anexado" se existir arquivo no pedido **ou** na parcela;
- a Degrau quase não preenche o número (82% das pagas de jul–out/2026 sem número); a Central preenche quase sempre.
  Anexo falta em cerca de metade (Degrau) a 80% (Central) das parcelas pagas. Pendência de documento é rotina,
  não exceção: apresente como lista de trabalho, não como irregularidade.

**Clonar pagamentos** (botão na tela de Pagamentos, desde 11/2026, permissão "Pagamento - Clonar"):
- clona contas que se repetiram nos dois últimos meses (mesma escola + fornecedor + categoria + rateio);
- o clone nasce `avulso`, etapa 3, status 3, 1 parcela A pagar (1), vencimento no mesmo dia do mês seguinte,
  competência = a da origem + 1 mês (editável no modal), descrição com o mês escrito avançado
  (ex.: "10/26" → "11/26"), **sem número de documento e sem anexos**;
- `purchase_orders.cloned_from_purchase_order_id` aponta para o pedido de origem. Use para medir adoção
  ("quantos pagamentos do mês vieram de clone") e para cobrar documentos dos clones;
- no dashboard, aparecem os selos "clonado" e "sem documento".

### Caixa
- **`bank_accounts.saldo` não é o saldo real**, principalmente na Degrau: as entradas de vendas não são lançadas lá, então os saldos ficam negativos. Não apresente esse campo como caixa disponível.
- **`cash_flows` (entradas manuais):** só a Central usa. A Degrau não tem lançamentos.
- **Movimento de caixa** (como na query de referência):
  - entradas `cash_flows`;
  - pagamentos = parcelas com `completed` (valor negativo);
  - transferências em `transfers` (uma saída na conta de origem e uma entrada na conta de destino);
  - ajustes manuais em `bank_account_logs` (`operation_type = 'manual_adjustment'`).

  Transferências antigas estão em `bank_account_logs` com `operation_type = 'transfer'` até 25/12/2025. Depois dessa data estão em `transfers`. Não conte as duas fontes no mesmo período.
- **Para a Degrau, a entrada de caixa vem dos pedidos:**
  - à vista (Pix/dinheiro/débito) no `paid_at`;
  - cartão e Princípia pela agenda de `order_installments`, como projeção.

## Métricas padrão

| Métrica | Definição |
|---|---|
| Receita bruta | Soma de `orders.total` com status IN (2,3,10,14,15) por `paid_at` |
| Receita líquida de vendas | Soma de `orders.total` com status 2 |
| Cancelamentos (dedução) | Soma de `total_refund` com status IN (3,15) por `request_date` |
| Valor retido em cancelamentos | Soma de `total - total_refund` dos cancelados |
| Taxa de cancelamento | Cancelados do período ÷ vendas brutas da mesma safra (por `paid_at`). Diga se é por quantidade ou por valor |
| Ticket médio | Receita ÷ pedidos com `total > 0` |
| Matrículas na turma | Pedidos status 2 com item na turma. Separe pagantes (`total > 0`) e Passaporte/carta/bônus |
| Atingiu o valor para iniciar | Receita da turma ≥ `mother_value`/`cyclical_value` |
| Custo de professor por turma | Soma do custo das aulas ativas com rateio de aulas compartilhadas |
| Margem de contribuição da turma | Receita da turma − custo de professor (antes de despesas fixas) |
| Despesa paga | Soma de `total_final × percentual` das parcelas status 4 por `completed` |
| Margem da unidade | Receita líquida da unidade − devoluções da unidade − despesas diretas pagas da unidade (antes do rateio corporativo) |
| Resultado gerencial | Receita líquida − cancelamentos − despesas operacionais pagas (sem partida dupla, investimento e cancelamento) |

## Modelos SQL (validados no banco)

Troque as datas e a escola. Todos rodam dentro do limite de tempo para um trimestre.

### 1. Economia da turma: receita, matrículas, valor para iniciar e custo de professor

```sql
WITH turmas AS (
  SELECT c.id, c.school_id, c.name, c.start_type, c.unit_id, cu.title curso, cu.scholarity_id,
    CASE c.start_type WHEN 'mother' THEN cu.mother_value WHEN 'cyclical' THEN cu.cyclical_value END valor_iniciar
  FROM classrooms c JOIN courses cu ON cu.id = c.course_id
  WHERE c.school_id IN (1,2) AND c.created_at >= '2026-04-01'          -- recorte das turmas
),
itens AS (
  SELECT i.classroom_id, o.id order_id, o.order_status_id, o.payment_method_id, o.total, i.price,
    SUM(i.price) OVER (PARTITION BY o.id) soma_price_pedido
  FROM order_items i JOIN orders o ON o.id = i.order_id
  WHERE i.classroom_id IN (SELECT id FROM turmas)
),
vendas AS (
  SELECT classroom_id,
    COUNT(DISTINCT CASE WHEN order_status_id = 2 THEN order_id END) matriculas,
    COUNT(DISTINCT CASE WHEN order_status_id = 2 AND total > 0 THEN order_id END) pagantes,
    COUNT(DISTINCT CASE WHEN order_status_id = 2 AND payment_method_id IN (8,14) THEN order_id END) via_carta_bonus,
    COUNT(DISTINCT CASE WHEN order_status_id IN (3,15) THEN order_id END) canceladas,
    ROUND(SUM(CASE WHEN order_status_id = 2 THEN total * price / NULLIF(soma_price_pedido,0) END),2) receita
  FROM itens GROUP BY classroom_id
),
aulas AS (
  SELECT g.classroom_id, MIN(gl.date) inicio, MAX(gl.date) fim, COUNT(*) n_aulas,
    ROUND(SUM(GREATEST((TIME_TO_SEC(gl.workload) - 900)/3600, 0)
      * CASE WHEN t.scholarity_id IN (5,7,10,13,18,19) THEN te.value_higher ELSE te.value_lower END
      / sh.n), 2) custo_prof
  FROM grids g
  JOIN grid_x_lessons x ON x.grid_id = g.id
  JOIN grid_lessons gl ON gl.id = x.grid_lesson_id AND gl.grid_lesson_status_id = 1
  JOIN turmas t ON t.id = g.classroom_id
  LEFT JOIN teachers te ON te.id = gl.teacher_id
  JOIN (SELECT grid_lesson_id, COUNT(DISTINCT grid_id) n FROM grid_x_lessons GROUP BY grid_lesson_id) sh
    ON sh.grid_lesson_id = gl.id
  GROUP BY g.classroom_id
)
SELECT t.id turma_id, t.name turma, IF(t.school_id=1,'Degrau','Central') escola, t.curso, u.name unidade,
  t.start_type, t.valor_iniciar, a.inicio, a.fim, a.n_aulas,
  v.matriculas, v.pagantes, v.via_carta_bonus, v.canceladas, v.receita,
  (v.receita >= t.valor_iniciar) atingiu_valor_iniciar,
  a.custo_prof, ROUND(v.receita - a.custo_prof, 2) margem_contribuicao
FROM turmas t
LEFT JOIN units u ON u.id = t.unit_id
LEFT JOIN vendas v ON v.classroom_id = t.id
LEFT JOIN aulas a ON a.classroom_id = t.id
ORDER BY margem_contribuicao;
```

### 2. Cancelamentos por tipo, com valor devolvido e retido

```sql
SELECT IF(o.school_id=1,'Degrau','Central') escola, DATE_FORMAT(o.request_date,'%Y-%m') mes,
  COALESCE(oct.name,'Sem tipo') tipo, rm.name metodo_devolucao,
  COUNT(*) pedidos, ROUND(SUM(o.total)) valor_vendido, ROUND(SUM(o.total_refund)) devolvido,
  ROUND(SUM(o.total - o.total_refund)) retido, ROUND(AVG(o.fine),1) multa_media_pct,
  ROUND(AVG(DATEDIFF(o.request_date, o.paid_at))) dias_ate_cancelar
FROM orders o
LEFT JOIN order_cancelation_types oct ON oct.id = o.cancelation_type_id
LEFT JOIN return_methods rm ON rm.id = o.return_method_id
WHERE o.school_id IN (1,2) AND o.order_status_id IN (3,15)
  AND o.request_date >= '2026-01-01' AND o.request_date < '2026-10-01'
GROUP BY escola, mes, tipo, rm.name ORDER BY escola, mes, devolvido DESC;
```

Para cancelamento por curso ou turma, junte `order_items` → `classrooms` → `courses`, usando o rateio de valor por item do modelo 1.

### 3. Despesas pagas por centro de custo, plano e unidade (com rateio)

```sql
SELECT IF(po.school_id=1,'Degrau','Central') escola, DATE_FORMAT(i.completed,'%Y-%m') mes,
  CASE WHEN TRIM(LOWER(cc.name)) = 'cancelamentos de vendas' THEN 'cancelamento de vendas'
       ELSE TRIM(LOWER(cc.name)) END centro_custo,
  op.name plano_contas, su.company_name unidade_estrategica, bu.company_name unidade_negocio,
  ROUND(SUM(i.total_final * bxs.percent / 100), 2) valor_pago
FROM purchase_order_installments i
JOIN purchase_orders po ON po.id = i.purchase_order_id
JOIN purchase_order_strategic_units pos ON pos.purchase_order_id = po.id
JOIN business_x_strategics bxs ON bxs.po_strategic_unit_id = pos.id
LEFT JOIN strategic_units su ON su.id = bxs.strategic_unit_id
LEFT JOIN business_units bu ON bu.id = bxs.business_unit_id
LEFT JOIN order_plans op ON op.id = po.order_plan_id
LEFT JOIN cost_centers cc ON cc.id = op.cost_center_id
WHERE po.school_id IN (1,2)
  AND i.purchase_order_installment_status_id = 4
  AND i.completed BETWEEN '2026-07-01' AND '2026-09-30'
GROUP BY escola, mes, centro_custo, op.name, su.company_name, bu.company_name
ORDER BY escola, mes, valor_pago DESC;
```

Para competência, troque o filtro por `i.competence BETWEEN '2026-07-01' AND '2026-09-01'` (1º dia de cada mês) e `i.purchase_order_installment_status_id <> 5`, e agrupe por `DATE_FORMAT(i.competence,'%Y-%m')`. Para "o que foi pago referente a esses meses", mantenha também `status = 4`.

### 4. Contas a pagar: situação e vencimentos

```sql
SELECT IF(po.school_id=1,'Degrau','Central') escola,
  CASE WHEN i.completed IS NULL AND i.date < '2026-10-29' THEN 'Em atraso'
       WHEN i.completed IS NOT NULL AND i.completed > i.date THEN 'Pago atrasado'
       WHEN i.completed IS NOT NULL THEN 'Pago em dia'
       ELSE 'A vencer' END situacao,
  DATE_FORMAT(i.date,'%Y-%m') mes_vencimento, COUNT(*) parcelas, ROUND(SUM(i.total_final)) valor
FROM purchase_order_installments i JOIN purchase_orders po ON po.id = i.purchase_order_id
WHERE po.school_id IN (1,2) AND i.purchase_order_installment_status_id <> 5
  AND i.date BETWEEN '2026-07-01' AND '2026-12-31'
GROUP BY escola, situacao, mes_vencimento ORDER BY escola, mes_vencimento, situacao;
```

Passe a data de hoje explicitamente no lugar de `'2026-10-29'`.

### 5. DRE gerencial mensal (receita, cancelamentos, despesas)

Rode em três consultas agregadas por mês e escola e monte a DRE na planilha ou na resposta:

1. Receita: modelo `vendas_por_dia` ou soma de `orders.total` por mês de `paid_at`, bruta e líquida.
2. Cancelamentos: modelo 2 agregado por mês (`devolvido`).
3. Despesas: modelo 3 agregado por mês e centro de custo, sem os centros 7, 58, 59, 60, 34, 44 e 45 (cancelamento, partida dupla, receitas, investimentos, retirada dos sócios). Mostre Investimentos e Retirada dos sócios em linhas abaixo do resultado.

Agrupe os centros de custo assim:

| Grupo da DRE | Centros de custo |
|---|---|
| Custo direto | Pedagógico, Educação à Distância, Editoração, Serviços Prestados (MEIs) |
| Pessoal | Folha Salarial, Departamento de Pessoal, Encargos, Gestão |
| Comercial e Marketing | Marketing, Comercial |
| Ocupação | Custos sobre Imóveis, Estrutura Predial |
| Administrativo | Administrativo, TI/Telefonia, Contabilidade, Despesas Jurídicas, Logística, Outras Despesas |
| Financeiro | Financeiro (tarifas, juros, antecipação de cartão) |
| Impostos | Impostos |

### 6. Custo de professor: estimado × pago (Degrau)

```sql
SELECT DATE_FORMAT(r.created_at,'%Y-%m') mes_relatorio, COUNT(DISTINCT r.id) relatorios,
  ROUND(SUM(i.hours_level_medium)) horas_medio, ROUND(SUM(i.hours_level_higher)) horas_superior,
  ROUND(SUM(i.total_to_pay)) total_a_pagar
FROM teacher_points_reports r JOIN teacher_points_report_items i ON i.teacher_points_report_id = r.id
WHERE r.school_id = 1 AND r.created_at >= '2026-07-01' AND r.created_at < '2026-10-01'
GROUP BY mes_relatorio;
```

Compare com o custo estimado das aulas do mesmo período (bloco `aulas` do modelo 1, por mês de `gl.date`) e com o centro de custo "Pedagógico" do modelo 3.

### 7. Recebíveis projetados (entrada de caixa futura das vendas)

```sql
SELECT IF(o.school_id=1,'Degrau','Central') escola, DATE_FORMAT(oi.date,'%Y-%m') mes_recebimento,
  pm.name metodo, ROUND(SUM(oi.amount)) valor
FROM order_installments oi JOIN orders o ON o.id = oi.order_id
LEFT JOIN payment_methods pm ON pm.id = o.payment_method_id
WHERE o.school_id IN (1,2) AND o.order_status_id = 2 AND o.total > 0
  AND o.paid_at >= '2026-01-01'
  AND oi.date >= '2026-11-01'
GROUP BY escola, mes_recebimento, pm.name ORDER BY escola, mes_recebimento;
```

É uma projeção bruta: não desconta taxa de cartão (MDR) nem antecipação, que aparecem como despesa no centro de custo Financeiro.

### 8. Receita e despesa de uma unidade física (ex.: "receita e despesa de Campo Grande nos últimos 60 dias")

**Período relativo:** converta para datas explícitas a partir da data de hoje, em dias completos (ex.: 60 dias até ontem). Diga as datas na resposta.

**Mapeie a unidade nos dois lados:**

| Unidade | `units.id` (vendas) | `business_units.id` (despesas) |
|---|---|---|
| Alfândega / Centro (Degrau) | 2 | 1 DC Alfândega |
| Campo Grande | 4 | 2 DC Campo Grande |
| Madureira | 3 | 3 DC Madureira |
| Niterói | 5 | 4 DC Niterói |
| Taquara | 6 | 5 DC Taquara |
| Live Degrau / Central | 22 / 24 | 6 DC Live / 15 CC Live |
| EAD Degrau / Central | 23 / 25 | 7 DC Virtual / 24 CC EAD |
| Metrô República | 10 | 13 CC República |
| Santo Amaro | 12 | 18 CC Santo Amaro |

**Receita da unidade:** atribua cada item à unidade por esta ordem: `classrooms.unit_id` da turma do item → `orders.unit_id` (é onde cai o Passaporte vendido na unidade) → `orders.seller_unit_id`. Rateie o total do pedido pelos itens. Mostre a receita separada por origem (turma × Passaporte/pedido), porque o Passaporte vendido na unidade costuma ser parte grande da receita dela.

```sql
WITH it AS (
  SELECT o.id, o.order_status_id, o.total,
    COALESCE(c.unit_id, o.unit_id, o.seller_unit_id) unidade_id,
    CASE WHEN c.unit_id IS NOT NULL THEN 'turma' WHEN o.unit_id IS NOT NULL THEN 'pedido (Passaporte etc.)'
         WHEN o.seller_unit_id IS NOT NULL THEN 'unidade do vendedor' ELSE 'sem unidade' END origem,
    i.price, SUM(i.price) OVER (PARTITION BY o.id) sp, COUNT(*) OVER (PARTITION BY o.id) n
  FROM orders o JOIN order_items i ON i.order_id = o.id
  LEFT JOIN classrooms c ON c.id = i.classroom_id
  WHERE o.school_id = 1 AND o.order_status_id IN (2,3,10,14,15)
    AND o.paid_at >= '2026-08-30' AND o.paid_at < '2026-10-29'
)
SELECT origem,
  COUNT(DISTINCT CASE WHEN order_status_id = 2 AND total > 0 THEN id END) pedidos_pagantes,
  ROUND(SUM(CASE WHEN order_status_id = 2 THEN total * COALESCE(price / NULLIF(sp,0), 1/n) END)) receita_liquida,
  ROUND(SUM(total * COALESCE(price / NULLIF(sp,0), 1/n))) receita_bruta
FROM it WHERE unidade_id = 4 GROUP BY origem;
```

**Cancelamentos da unidade:** mesma atribuição de unidade, com status IN (3,15) e `request_date` no período, somando `total_refund`.

**Despesa da unidade:** parcelas pagas (status 4, `completed` no período) com `bxs.business_unit_id` da unidade, valor `total_final * bxs.percent / 100`, abertas por centro de custo. Tire "cancelamento de vendas" (já está na dedução) e mostre quanto veio de rateio (`bxs.percent < 100`).

**O que dizer sempre:** a despesa direta da unidade é só uma parte do custo. Marketing, a maior parte da folha e a estrutura central ficam em "DC Corporativo" e "Conselho ADM" e não são rateados para as unidades no banco. Por isso o resultado da unidade é **margem antes do rateio corporativo**, não lucro. Mostre também o total corporativo do período para dar a dimensão. Se o usuário quiser rateio, proponha um critério (por receita ou por número de alunos) e deixe claro que é uma premissa.

### 9. Pagamentos do período por fornecedor (o que saiu, de onde e quanto atrasou)

```sql
SELECT IF(po.school_id=1,'Degrau','Central') escola, s.company_name fornecedor, poc.name categoria,
  ba.name conta_saida, COUNT(*) parcelas, ROUND(SUM(i.total_final),2) pago,
  ROUND(SUM(i.total_final - i.total),2) juros_desconto, SUM(i.completed > i.date) pagas_atrasadas,
  ROUND(AVG(DATEDIFF(i.completed, i.date)),1) dias_medio_vs_vencimento
FROM purchase_order_installments i
JOIN purchase_orders po ON po.id = i.purchase_order_id
LEFT JOIN suppliers s ON s.id = po.supplier_id
LEFT JOIN purchase_order_categories poc ON poc.id = po.purchase_order_category_id
LEFT JOIN bank_accounts ba ON ba.id = i.bank_account_id
WHERE po.school_id IN (1,2) AND i.purchase_order_installment_status_id = 4
  AND i.completed >= '2026-10-01' AND i.completed < '2026-11-01'
GROUP BY escola, s.company_name, poc.name, ba.name ORDER BY pago DESC;
```

### 10. Contas recorrentes (o que se repete todo mês)

Mesma ideia do botão Clonar: fornecedor + categoria com parcela em todos os meses da janela.

```sql
SELECT IF(po.school_id=1,'Degrau','Central') escola, s.company_name fornecedor, poc.name categoria,
  COUNT(DISTINCT DATE_FORMAT(i.date,'%Y-%m')) meses, COUNT(*) parcelas,
  ROUND(AVG(i.total_final)) media, ROUND(MIN(i.total_final)) minimo, ROUND(MAX(i.total_final)) maximo,
  MAX(i.date) ultimo_vencimento
FROM purchase_order_installments i
JOIN purchase_orders po ON po.id = i.purchase_order_id
LEFT JOIN suppliers s ON s.id = po.supplier_id
LEFT JOIN purchase_order_categories poc ON poc.id = po.purchase_order_category_id
WHERE po.school_id IN (1,2) AND po.purchase_order_status_id <> 6
  AND i.purchase_order_installment_status_id <> 5
  AND i.date >= '2026-08-01' AND i.date < '2026-11-01'          -- 3 meses fechados
GROUP BY escola, s.company_name, poc.name
HAVING meses = 3
ORDER BY media DESC;
```

- `parcelas > meses` = mais de um lançamento por mês (ex.: várias notas do mesmo fornecedor). Não é uma conta só.
- Valor que oscila mais de 10% entre mínimo e máximo é conta variável (anúncio, juros de antecipação): projete pela média e diga isso.
- Para "o que ainda não foi lançado para o mês que vem", compare `ultimo_vencimento` com o mês seguinte.
- Para recorrência por mês de referência (e não de vencimento), troque `i.date` por `i.competence` no filtro e no
  `COUNT(DISTINCT ...)`; útil quando a conta às vezes vence no próprio mês e às vezes no seguinte.

### 11. Contas em aberto do mês e pendências de documento

```sql
SELECT IF(po.school_id=1,'Degrau','Central') escola, i.date vencimento,
  DATE_FORMAT(i.competence,'%m/%Y') competencia, s.company_name fornecedor,
  po.description, i.total_final valor,
  CASE i.purchase_order_installment_status_id WHEN 1 THEN 'A pagar' WHEN 3 THEN 'Aprovado' END situacao,
  (po.document_number IS NULL OR po.document_number = '') sem_numero_documento,
  (NOT EXISTS (SELECT 1 FROM purchase_order_files f WHERE f.purchase_order_id = po.id)
   AND NOT EXISTS (SELECT 1 FROM purchase_order_installment_medias m WHERE m.purchase_order_installment_id = i.id)) sem_anexo,
  (po.cloned_from_purchase_order_id IS NOT NULL) clonado
FROM purchase_order_installments i
JOIN purchase_orders po ON po.id = i.purchase_order_id
LEFT JOIN suppliers s ON s.id = po.supplier_id
WHERE po.school_id IN (1,2) AND i.purchase_order_installment_status_id IN (1,3)
  AND i.date >= '2026-11-01' AND i.date < '2026-12-01'
ORDER BY escola, vencimento;
```

Para o resumo, agregue por escola (parcelas, valor, quantas sem número, sem anexo e clonadas). Em aberto e
vencida antes de hoje = atraso: passe a data de hoje explicitamente.

### 12. Quem aprovou ou pagou em lote

```sql
SELECT IF(m.school_id=1,'Degrau','Central') escola, DATE(m.created_at) dia, u.full_name usuario,
  CASE WHEN m.new_status IS NULL AND m.bank_id IS NOT NULL THEN 'Pagamento em lote'
       WHEN m.old_status = 1 AND m.new_status = 2 THEN 'Aprovação'
       WHEN m.new_status = 5 THEN 'Reprovação' ELSE 'Outro' END acao,
  COUNT(DISTINCT m.id) lotes, COUNT(x.id) pedidos, ROUND(SUM(x.value)) valor
FROM purchase_order_movements m
JOIN purchase_order_movement_items x ON x.movement_id = m.id
LEFT JOIN users u ON u.id = m.user_id
WHERE m.school_id IN (1,2) AND m.created_at >= '2026-10-01' AND m.created_at < '2026-11-01'
GROUP BY escola, dia, u.full_name, acao ORDER BY dia, valor DESC;
```

## Armadilhas que já distorceram números

1. **Contar despesa sem o rateio, ou juntar o rateio sem o percentual:** isso duplica valores. Sempre use `total_final * bxs.percent / 100`, ou não junte as tabelas de rateio.
2. **Somar parcelas canceladas** (status 5): infla a despesa.
3. **Contar a devolução duas vezes:** `orders.total_refund` e o centro de custo "Cancelamento de Vendas" são o mesmo dinheiro.
4. **Receita de turma sem o rateio por item:** pedido com vários itens duplica o total.
5. **Turma "deficitária" porque os alunos vieram de Passaporte ou carta:** a receita deles está no pedido do Passaporte, não na turma.
6. **Custo de professor sem o rateio de aulas compartilhadas:** mais da metade das aulas são compartilhadas.
7. **`grid_lessons.grid_id` vazio:** use `grid_x_lessons`.
8. **Saldo bancário negativo na Degrau:** o campo `saldo` não reflete as entradas de vendas.
9. **Comparar Degrau e Central antes de dez/2025 em despesas:** a Central não tem contas a pagar nesse período.
10. **Usar `paid_at` sem filtrar o status**, ou descontar 3h dele (regra antiga, anterior a 20/10/2026).
11. **Apresentar a margem da unidade como lucro:** as despesas corporativas (DC Corporativo, Conselho ADM) não estão rateadas para as unidades.
12. **Usar o status do pedido de compra para dizer se foi pago:** pedidos em 2 ou 3 podem ter parcelas pagas. Use a parcela (status 4 + `completed`).
13. **Usar `purchase_order_installments.paid_at` ou `purchase_orders.completed`:** nunca são preenchidos. A data do pagamento é `completed` da parcela.
14. **Somar `total` em vez de `total_final`:** ignora juros, multa e desconto da baixa.
15. **Somar `purchase_order_movement_items.value` como despesa:** um pedido pode aparecer em mais de um lote (aprovação e depois pagamento). Para valor pago, use as parcelas.
16. **Tratar a ausência de documento como irregularidade:** o documento chega depois do lançamento, e clones nascem sem documento por desenho.
17. **Usar o vencimento como competência, ou ler o mês da descrição,** depois de 23/11/2026: existe a coluna `competence`. E não apresente a competência de lançamentos antigos como informada pelo Financeiro: ela foi inferida.

## Formato da resposta

- Comece pelo achado principal com o número. Em seguida, diga a definição usada em uma linha: regime, status, período e escola.
- Quando a análise cruzar fontes, mostre a reconciliação: o total da visão detalhada contra o total da visão agregada.
- Use tabela quando houver comparação entre escolas, unidades, cursos ou meses. Para o detalhe completo, exporte planilha com `exportar_planilha`.
- Não exponha dados pessoais de alunos (nome, CPF, e-mail, telefone) em análises financeiras agregadas. Traga essas colunas só quando a pessoa pedir uma lista nominal.