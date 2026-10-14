# `courses`

Linhas (estimativa do information_schema): **~2.208**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna          | tipo            | nulo   | chave   |   padrao | comentario   |
|:----------------|:----------------|:-------|:--------|---------:|:-------------|
| id              | bigint unsigned | NO     | PRI     |      nan |              |
| uuid            | char(36)        | YES    |         |      nan |              |
| title           | varchar(255)    | YES    |         |      nan |              |
| title_contract  | varchar(255)    | YES    |         |      nan |              |
| display_panel   | tinyint(1)      | YES    |         |        0 |              |
| status          | tinyint(1)      | YES    |         |        0 |              |
| user_id         | bigint unsigned | YES    | MUL     |      nan |              |
| media_id        | bigint unsigned | YES    | MUL     |      nan |              |
| datasheet_id    | bigint unsigned | YES    | MUL     |      nan |              |
| course_sale_id  | bigint unsigned | YES    | MUL     |      nan |              |
| scholarity_id   | int unsigned    | YES    | MUL     |      nan |              |
| course_type_id  | bigint unsigned | YES    | MUL     |      nan |              |
| school_id       | bigint unsigned | YES    | MUL     |      nan |              |
| created_at      | timestamp       | YES    |         |      nan |              |
| updated_at      | timestamp       | YES    |         |      nan |              |
| migration       | tinyint(1)      | YES    |         |        0 |              |
| product_id      | bigint unsigned | YES    | MUL     |      nan |              |
| old_id          | varchar(100)    | YES    |         |      nan |              |
| product_live_id | bigint unsigned | YES    | MUL     |      nan |              |
| mother_value    | decimal(12,2)   | YES    |         |      nan |              |
| cyclical_value  | decimal(12,2)   | YES    |         |      nan |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna          | referencia      |
|:----------------|:----------------|
| course_sale_id  | course_sales.id |
| course_type_id  | course_types.id |
| datasheet_id    | datasheets.id   |
| media_id        | medias.id       |
| product_id      | products.id     |
| product_live_id | products.id     |
| scholarity_id   | scholarities.id |
| school_id       | schools.id      |
| user_id         | users.id        |

## Referenciada por (outra tabela → esta)

| origem                         | coluna   |
|:-------------------------------|:---------|
| classrooms.course_id           | id       |
| course_classrooms.course_id    | id       |
| course_installments.course_id  | id       |
| course_products.course_id      | id       |
| discipline_workloads.course_id | id       |
| sales_panel_sorts.course_id    | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                          | colunas         |   unico |
|:--------------------------------|:----------------|--------:|
| courses_course_sale_id_foreign  | course_sale_id  |       0 |
| courses_course_type_id_foreign  | course_type_id  |       0 |
| courses_datasheet_id_foreign    | datasheet_id    |       0 |
| courses_media_id_foreign        | media_id        |       0 |
| courses_product_id_foreign      | product_id      |       0 |
| courses_product_live_id_foreign | product_live_id |       0 |
| courses_scholarity_id_foreign   | scholarity_id   |       0 |
| courses_school_id_foreign       | school_id       |       0 |
| courses_user_id_foreign         | user_id         |       0 |
| PRIMARY                         | id              |       1 |
