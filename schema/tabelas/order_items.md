# `order_items`

Linhas (estimativa do information_schema): **~395.113**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna              | tipo            | nulo   | chave   |   padrao | comentario   |
|:--------------------|:----------------|:-------|:--------|---------:|:-------------|
| id                  | bigint unsigned | NO     | PRI     |      nan |              |
| uuid                | char(36)        | YES    |         |      nan |              |
| title               | varchar(255)    | YES    |         |      nan |              |
| quantity            | int             | YES    |         |      nan |              |
| price               | decimal(11,2)   | YES    |         |        0 |              |
| discount            | decimal(11,2)   | YES    |         |        0 |              |
| product_id          | bigint          | YES    |         |      nan |              |
| product_category_id | bigint          | YES    |         |      nan |              |
| validity            | int             | YES    |         |      nan |              |
| start               | date            | YES    |         |      nan |              |
| end                 | date            | YES    |         |      nan |              |
| order_id            | bigint unsigned | YES    | MUL     |      nan |              |
| created_at          | timestamp       | YES    |         |      nan |              |
| updated_at          | timestamp       | YES    |         |      nan |              |
| active              | tinyint(1)      | YES    |         |        1 |              |
| classroom_id        | bigint unsigned | YES    | MUL     |      nan |              |
| classroom_full      | tinyint(1)      | YES    |         |        0 |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna       | referencia    |
|:-------------|:--------------|
| classroom_id | classrooms.id |
| order_id     | orders.id     |

## Referenciada por (outra tabela → esta)

| origem                               | coluna   |
|:-------------------------------------|:---------|
| order_item_disciplines.order_item_id | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                           | colunas      |   unico |
|:---------------------------------|:-------------|--------:|
| order_items_classroom_id_foreign | classroom_id |       0 |
| order_items_order_id_foreign     | order_id     |       0 |
| PRIMARY                          | id           |       1 |
