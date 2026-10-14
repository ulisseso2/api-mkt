# `product_categories`

Linhas (estimativa do information_schema): **~11**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna   | tipo            | nulo   | chave   |   padrao | comentario   |
|:---------|:----------------|:-------|:--------|---------:|:-------------|
| id       | bigint unsigned | NO     | PRI     |      nan |              |
| uuid     | char(36)        | YES    |         |      nan |              |
| name     | varchar(255)    | NO     |         |      nan |              |
| initials | text            | YES    |         |      nan |              |
| active   | tinyint(1)      | YES    |         |        0 |              |
| slug     | varchar(255)    | YES    |         |      nan |              |
| color    | varchar(255)    | YES    |         |      nan |              |
| icon     | varchar(255)    | YES    |         |      nan |              |

## Chaves estrangeiras (esta tabela → outra)

_(vazio)_

## Referenciada por (outra tabela → esta)

| origem                                          | coluna   |
|:------------------------------------------------|:---------|
| contracts.product_category_id                   | id       |
| coupon_product_categories.product_category_id   | id       |
| manager_discount_categories.product_category_id | id       |
| product_category_warnings.product_category_id   | id       |
| product_recommendeds.product_category_id        | id       |
| product_subcategories.product_category_id       | id       |
| products.product_category_id                    | id       |
| school_discounts.product_category_id            | id       |
| user_discount_categories.product_category_id    | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice   | colunas   |   unico |
|:---------|:----------|--------:|
| PRIMARY  | id        |       1 |
