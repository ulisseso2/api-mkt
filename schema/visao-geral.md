# Visão geral do schema para marketing

Banco MySQL `seducar` (CRM compartilhado de Degrau e Central). São 500 tabelas. Para marketing,
importa este núcleo:

```
                       interested_pontuations_answers (texto das respostas P1/P2)
                                   ▲
interested_pontuations ──interested_id──► interesteds ◄──opportunity_id── orders ──► order_items ──► products
  (P1, P2, score, tier)                   (LEAD)                          (PEDIDO)        │            product_categories
                                            │  │                             │  │         └──► classrooms ──► courses ──► course_sales
                       opportunity_steps ◄──┘  └──► customers ◄──customer_id─┘  │                    │
                       opportunity_origins      (cliente/aluno)                 │                    └──► units, shifts
                       opportunity_modalities                                   ├──► order_status
                       units, areas, sales_force (concurso)                     ├──► payment_methods
                       users (dono/vendedor)                                    ├──► users (vendedor: user_id / owner_id)
                                                                                └──► order_attributions (UTM/click ids da compra)
```

## Tabelas principais

| Tabela | O que é | Chave de data | Observações |
|---|---|---|---|
| `interesteds` | Lead/oportunidade do CRM | `created_at` | UTMs, gclid, fbclid, página de captura, etapa, dono. Índice `(school_id, created_at)` |
| `interested_pontuations` | Qualificação do bot de WhatsApp (P1/P2) | `created_at` | Desde 16/06/2026. **Pode haver mais de uma por lead**: use a de maior `id` |
| `interested_pontuations_answers` | Texto das alternativas P1/P2 | — | Junte por `school_id` + `question` (1/2) + `question_number` = `p1_answer`/`p2_answer` |
| `orders` | Pedido de compra | `paid_at` | Status em `order_status_id`. `owner_id` nulo = venda pelo site. Sem índice de data |
| `order_items` | Itens do pedido | — | Um pedido pode ter vários itens/categorias. **Agregue antes de juntar com orders** |
| `order_attributions` | Atribuição de marketing do pedido (site) | `created_at` | 1 por pedido, só pedidos recentes do site. utm_*, gclid, fbclid, fbp, ttclid, ltv_value |
| `customers` | Cliente/aluno | — | **Dados pessoais**: não traga colunas de contato |
| `opportunity_steps` | Etapas do funil do CRM | — | Ids diferentes por marca |
| `opportunity_origins` | Origem do lead | — | Site, WhatsApp, Google AdWords, Instagram etc. 14 = Upsell |
| `opportunity_logs` | Histórico de ações no lead | `created_at` | ~1,5 mi linhas: filtre bem |
| `transcription_ai_summaries`, `chat_ai_evaluations` | Avaliações de IA de ligações/chats | — | Do projeto api-analises |

## Armadilhas que distorcem números

1. **Duplicação por JOIN 1:N.** Juntar `orders` com `order_items` multiplica os pedidos.
   Some `orders.total` só com `COUNT(DISTINCT o.id)` e sem itens, ou pré-agregue os itens em
   subconsulta (como em `consultas/vendas.sql`). O mesmo vale para pontuações duplicadas.
2. **Escolas de teste.** `school_id` 3, 4 e 5 são homologação: filtre `IN (1, 2)`.
3. **`paid_at` vem preenchido até em pedido não pago.** O status decide se é venda.
4. **Fuso das datas.** O banco roda em UTC e o runner lê as datas como gravadas. `created_at` e
   `updated_at` já estão em horário de Brasília. `orders.paid_at` está em UTC: desconte 3h
   (`DATE_SUB(o.paid_at, INTERVAL 3 HOUR)`) antes de agrupar por dia/hora ou comparar com `created_at`.
   Não use `NOW()`/`CURDATE()` no SQL (devolvem UTC).
5. **Etapas por marca.** "Vendido" é 12 na Degrau e 20 na Central. Nunca filtre por um id só
   quando a pergunta envolve as duas marcas.
6. **Leads sem UTM** são a maior fatia (WhatsApp, telefone, orgânico). Não os descarte. Mostre
   como "(sem utm)".
7. **Upsell (origem 14)** infla leads se não for excluído.
8. **Pontuação só existe desde 16/06/2026.** Antes disso, "sem tier" não quer dizer lead ruim.
9. **Regras de unidade/modalidade:** quando o lead não tem unidade, ela é derivada da modalidade
   (ver CASE em `consultas/leads.sql`). Units 22/24 = Live, 23/25 = EAD, 26/27 = Smart.

## Status de pedido (resumo; lista completa em dominios.md)

| id | status | conta como |
|---|---|---|
| 2 | Pago | venda líquida e bruta |
| 3 | Cancelado | venda bruta |
| 10 | Expirada | venda bruta |
| 14 | Trancada | venda bruta |
| 15 | Em cancelamento | venda bruta |
| 11, 21 | Estorno total/parcial | — |
| 1, 6, 13 | Pendente / Aguardando pagamento / Pendente de desconto | não é venda |
| 8, 17 | Rejeitado / Inválido | não é venda |
