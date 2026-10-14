# `sales_force`

Linhas (estimativa do information_schema): **~287**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna     | tipo            | nulo   | chave   | padrao   | comentario   |
|:-----------|:----------------|:-------|:--------|:---------|:-------------|
| id         | bigint unsigned | NO     | PRI     |          |              |
| uuid       | char(36)        | YES    |         |          |              |
| name       | varchar(255)    | YES    |         |          |              |
| status     | tinyint(1)      | YES    |         |          |              |
| school_id  | bigint unsigned | YES    | MUL     |          |              |
| created_at | timestamp       | YES    |         |          |              |
| alias      | varchar(255)    | NO     |         |          |              |
| area_id    | bigint unsigned | YES    | MUL     |          |              |
| octadesk   | varchar(24)     | YES    |         |          |              |
| campaign   | text            | YES    |         |          |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna    | referencia   |
|:----------|:-------------|
| area_id   | areas.id     |
| school_id | schools.id   |

## Referenciada por (outra tabela → esta)

| origem                             | coluna   |
|:-----------------------------------|:---------|
| contest_sales_force.sales_force_id | id       |
| contests.sales_force_id            | id       |
| interesteds.sales_force_id         | id       |
| product_sales_force.sales_force_id | id       |
| products.sales_force_id            | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                        | colunas   |   unico |
|:------------------------------|:----------|--------:|
| PRIMARY                       | id        |       1 |
| rd_stations_school_id_foreign | school_id |       0 |
| sales_force_area_id_foreign   | area_id   |       0 |
