# `order_refunds`

Linhas (estimativa do information_schema): **~136**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna            | tipo            | nulo   | chave   | padrao            | comentario   |
|:------------------|:----------------|:-------|:--------|:------------------|:-------------|
| id                | bigint unsigned | NO     | PRI     | nan               |              |
| uuid              | char(36)        | NO     | UNI     | nan               |              |
| order_id          | bigint unsigned | YES    | MUL     | nan               |              |
| purchase_order_id | bigint unsigned | YES    | MUL     | nan               |              |
| refund_date       | date            | NO     |         | nan               |              |
| user              | bigint unsigned | YES    | MUL     | nan               |              |
| note              | text            | YES    |         | nan               |              |
| created_at        | timestamp       | YES    |         | CURRENT_TIMESTAMP |              |
| updated_at        | timestamp       | YES    |         | CURRENT_TIMESTAMP |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna            | referencia         |
|:------------------|:-------------------|
| order_id          | orders.id          |
| purchase_order_id | purchase_orders.id |
| user              | users.id           |

## Referenciada por (outra tabela → esta)

| origem                             | coluna   |
|:-----------------------------------|:---------|
| order_refund_files.order_refund_id | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                  | colunas           |   unico |
|:----------------------------------------|:------------------|--------:|
| order_refunds_order_id_foreign          | order_id          |       0 |
| order_refunds_purchase_order_id_foreign | purchase_order_id |       0 |
| order_refunds_user_foreign              | user              |       0 |
| order_refunds_uuid_unique               | uuid              |       1 |
| PRIMARY                                 | id                |       1 |
