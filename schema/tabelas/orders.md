# `orders`

Linhas (estimativa do information_schema): **~386.317**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna               | tipo            | nulo   | chave   | padrao            | comentario           |
|:---------------------|:----------------|:-------|:--------|:------------------|:---------------------|
| id                   | bigint unsigned | NO     | PRI     | nan               |                      |
| uuid                 | char(36)        | YES    |         | nan               |                      |
| school_id            | bigint unsigned | YES    | MUL     | nan               |                      |
| created_at           | timestamp       | YES    |         | nan               |                      |
| updated_at           | timestamp       | YES    | MUL     | nan               |                      |
| total_discount       | decimal(11,2)   | YES    |         | 0.00              |                      |
| customer_id          | bigint unsigned | YES    | MUL     | nan               |                      |
| coupon_id            | bigint unsigned | YES    | MUL     | nan               |                      |
| total                | decimal(11,2)   | YES    |         | 0.00              |                      |
| paid_at              | timestamp       | YES    |         | CURRENT_TIMESTAMP |                      |
| gateway_id           | bigint unsigned | YES    | MUL     | nan               |                      |
| order_status_id      | bigint unsigned | YES    | MUL     | nan               |                      |
| payment_method_id    | bigint unsigned | YES    | MUL     | nan               |                      |
| external_id          | varchar(255)    | YES    |         | nan               |                      |
| shipping_price       | decimal(11,2)   | YES    |         | nan               |                      |
| shipping_days        | int             | YES    |         | nan               |                      |
| shipping_service     | varchar(255)    | YES    |         | nan               |                      |
| shipping_code_track  | varchar(255)    | YES    |         | nan               |                      |
| note                 | varchar(255)    | YES    |         | nan               |                      |
| note_user            | varchar(255)    | YES    |         | nan               |                      |
| user_id              | bigint unsigned | YES    | MUL     | nan               |                      |
| sync                 | tinyint(1)      | YES    |         | 0                 |                      |
| done                 | tinyint(1)      | YES    |         | nan               |                      |
| old_id               | varchar(250)    | YES    | MUL     | nan               |                      |
| unit_id              | bigint unsigned | YES    | MUL     | nan               |                      |
| migration_lives      | tinyint(1)      | YES    |         | 0                 |                      |
| order_origin_id      | bigint unsigned | YES    | MUL     | nan               |                      |
| discount_note        | varchar(255)    | YES    |         | nan               |                      |
| seller_unit_id       | bigint unsigned | YES    | MUL     | nan               |                      |
| letter_credit_id     | bigint unsigned | YES    | MUL     | nan               |                      |
| total_refund         | decimal(11,2)   | YES    |         | 0.00              |                      |
| geolocation          | json            | YES    |         | nan               |                      |
| json_consys          | json            | YES    |         | nan               |                      |
| request_date         | timestamp       | YES    |         | nan               |                      |
| completion_date      | timestamp       | YES    |         | nan               |                      |
| step_id              | bigint unsigned | YES    | MUL     | nan               |                      |
| return_method_id     | bigint unsigned | YES    | MUL     | nan               |                      |
| fine                 | decimal(5,2)    | YES    |         | 0.00              | Porcentagem de multa |
| letter_credit_hours  | varchar(100)    | YES    |         | nan               |                      |
| matricula            | varchar(100)    | YES    |         | nan               |                      |
| migrado              | tinyint(1)      | YES    |         | 0                 |                      |
| vinculado            | tinyint(1)      | YES    |         | 0                 |                      |
| opportunity_id       | bigint unsigned | YES    | MUL     | nan               |                      |
| contract_id          | bigint unsigned | YES    | MUL     | nan               |                      |
| letter_credit_total  | decimal(11,2)   | YES    |         | 0.00              |                      |
| contract_accepted    | tinyint(1)      | YES    |         | 0                 |                      |
| date_acceptance      | datetime        | YES    |         | nan               |                      |
| cancelation_type_id  | bigint unsigned | YES    | MUL     | nan               |                      |
| order_id             | bigint unsigned | YES    | MUL     | nan               |                      |
| consumed_value       | decimal(12,2)   | YES    |         | nan               |                      |
| enrollment_lock_date | timestamp       | YES    |         | nan               |                      |
| owner_id             | bigint unsigned | YES    | MUL     | nan               | Dono do pedido       |

## Chaves estrangeiras (esta tabela → outra)

| coluna              | referencia                 |
|:--------------------|:---------------------------|
| cancelation_type_id | order_cancelation_types.id |
| contract_id         | medias.id                  |
| coupon_id           | coupons.id                 |
| customer_id         | customers.id               |
| gateway_id          | gateways.id                |
| letter_credit_id    | letter_credits.id          |
| opportunity_id      | interesteds.id             |
| order_id            | orders.id                  |
| order_origin_id     | order_origins.id           |
| order_status_id     | order_status.id            |
| owner_id            | users.id                   |
| payment_method_id   | payment_methods.id         |
| return_method_id    | return_methods.id          |
| school_id           | schools.id                 |
| seller_unit_id      | units.id                   |
| step_id             | steps.id                   |
| unit_id             | units.id                   |
| user_id             | users.id                   |

## Referenciada por (outra tabela → esta)

| origem                                | coluna   |
|:--------------------------------------|:---------|
| classroom_transfers.order_id          | id       |
| interested_x_orders.order_id          | id       |
| letter_credit_logs.order_id           | id       |
| letter_credits.order_id               | id       |
| letter_credits.order_old_id           | id       |
| notas_fiscais.order_id                | id       |
| order_comments.order_id               | id       |
| order_contracts.order_id              | id       |
| order_cycles.order_id                 | id       |
| order_discount_requests.order_id      | id       |
| order_enrollments.order_id            | id       |
| order_installments.order_id           | id       |
| order_items.order_id                  | id       |
| order_logs.order_id                   | id       |
| order_notes.order_id                  | id       |
| order_payment_attempts.order_id       | id       |
| order_refunds.order_id                | id       |
| order_shippings.order_id              | id       |
| orders.order_id                       | id       |
| payment_fulfillment_steps.order_id    | id       |
| purchase_orders.cancellation_order_id | id       |
| purchase_orders.order_id              | id       |
| remittance_orders.order_id            | id       |
| transactions.order_id                 | id       |
| wazapi_store_orders.order_id          | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                             | colunas             |   unico |
|:-----------------------------------|:--------------------|--------:|
| idx_orders_old_id                  | old_id              |       0 |
| idx_orders_opportunity_id          | opportunity_id      |       0 |
| idx_orders_updated_at              | updated_at          |       0 |
| orders_cancelation_type_id_foreign | cancelation_type_id |       0 |
| orders_contract_id_foreign         | contract_id         |       0 |
| orders_coupon_id_foreign           | coupon_id           |       0 |
| orders_customer_id_foreign         | customer_id         |       0 |
| orders_gateway_id_foreign          | gateway_id          |       0 |
| orders_letter_credit_id_foreign    | letter_credit_id    |       0 |
| orders_order_id_foreign            | order_id            |       0 |
| orders_order_origin_id_foreign     | order_origin_id     |       0 |
| orders_order_status_id_foreign     | order_status_id     |       0 |
| orders_owner_id_foreign            | owner_id            |       0 |
| orders_payment_method_id_foreign   | payment_method_id   |       0 |
| orders_return_method_id_foreign    | return_method_id    |       0 |
| orders_school_id_foreign           | school_id           |       0 |
| orders_seller_unit_id_foreign      | seller_unit_id      |       0 |
| orders_step_id_foreign             | step_id             |       0 |
| orders_unit_id_foreign             | unit_id             |       0 |
| orders_user_id_foreign             | user_id             |       0 |
| PRIMARY                            | id                  |       1 |
