# `interested_x_orders`

Linhas (estimativa do information_schema): **~1.566**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna        | tipo            | nulo   | chave   | padrao            | comentario   |
|:--------------|:----------------|:-------|:--------|:------------------|:-------------|
| id            | bigint unsigned | NO     | PRI     | nan               |              |
| uuid          | char(36)        | NO     | UNI     | nan               |              |
| interested_id | bigint unsigned | NO     | MUL     | nan               |              |
| order_id      | bigint unsigned | NO     | MUL     | nan               |              |
| created_at    | timestamp       | NO     |         | CURRENT_TIMESTAMP |              |
| updated_at    | timestamp       | NO     |         | CURRENT_TIMESTAMP |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna        | referencia     |
|:--------------|:---------------|
| interested_id | interesteds.id |
| order_id      | orders.id      |

## Referenciada por (outra tabela → esta)

_(vazio)_

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                    | colunas       |   unico |
|:------------------------------------------|:--------------|--------:|
| interested_x_orders_interested_id_foreign | interested_id |       0 |
| interested_x_orders_order_id_foreign      | order_id      |       0 |
| interested_x_orders_uuid_unique           | uuid          |       1 |
| PRIMARY                                   | id            |       1 |
