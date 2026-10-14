# `transactions`

Linhas (estimativa do information_schema): **~65.184**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna            | tipo            | nulo   | chave   | padrao            | comentario   |
|:------------------|:----------------|:-------|:--------|:------------------|:-------------|
| id                | bigint unsigned | NO     | PRI     | nan               |              |
| uuid              | char(36)        | YES    |         | nan               |              |
| transaction_id    | varchar(255)    | YES    |         | nan               |              |
| gateway_id        | bigint unsigned | YES    | MUL     | nan               |              |
| order_id          | bigint unsigned | YES    | MUL     | nan               |              |
| paid_at           | datetime        | YES    |         | nan               |              |
| created_at        | timestamp       | YES    |         | CURRENT_TIMESTAMP |              |
| updated_at        | timestamp       | YES    |         | nan               |              |
| order_status_id   | bigint unsigned | YES    | MUL     | nan               |              |
| payment_method_id | bigint unsigned | YES    | MUL     | nan               |              |
| bank_agency       | varchar(255)    | YES    |         | nan               |              |
| bank_account      | varchar(255)    | YES    |         | nan               |              |
| bank_name         | varchar(255)    | YES    |         | nan               |              |
| check_number      | varchar(255)    | YES    |         | nan               |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna            | referencia         |
|:------------------|:-------------------|
| gateway_id        | gateways.id        |
| order_id          | orders.id          |
| order_status_id   | order_status.id    |
| payment_method_id | payment_methods.id |

## Referenciada por (outra tabela → esta)

| origem                                  | coluna   |
|:----------------------------------------|:---------|
| billet_transactions.transaction_id      | id       |
| boleto_transactions.transaction_id      | id       |
| credit_card_transactions.transaction_id | id       |
| pix_transactions.transaction_id         | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                 | colunas           |   unico |
|:---------------------------------------|:------------------|--------:|
| PRIMARY                                | id                |       1 |
| transactions_gateway_id_foreign        | gateway_id        |       0 |
| transactions_order_id_foreign          | order_id          |       0 |
| transactions_order_status_id_foreign   | order_status_id   |       0 |
| transactions_payment_method_id_foreign | payment_method_id |       0 |
