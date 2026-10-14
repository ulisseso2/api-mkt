# `course_sales`

Linhas (estimativa do information_schema): **~905**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna              | tipo            | nulo   | chave   |   padrao | comentario   |
|:--------------------|:----------------|:-------|:--------|---------:|:-------------|
| id                  | bigint unsigned | NO     | PRI     |      nan |              |
| uuid                | char(36)        | YES    |         |      nan |              |
| name                | varchar(255)    | NO     |         |      nan |              |
| status              | tinyint(1)      | YES    |         |        0 |              |
| course_sale_type_id | bigint unsigned | YES    | MUL     |      nan |              |
| user_id             | bigint unsigned | YES    | MUL     |      nan |              |
| school_id           | bigint unsigned | YES    | MUL     |      nan |              |
| created_at          | timestamp       | YES    |         |      nan |              |
| updated_at          | timestamp       | YES    |         |      nan |              |
| migration           | varchar(100)    | YES    |         |        0 |              |
| old_id              | varchar(255)    | YES    |         |      nan |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna              | referencia           |
|:--------------------|:---------------------|
| course_sale_type_id | course_sale_types.id |
| school_id           | schools.id           |
| user_id             | users.id             |

## Referenciada por (outra tabela → esta)

| origem                  | coluna   |
|:------------------------|:---------|
| courses.course_sale_id  | id       |
| products.course_sale_id | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                   | colunas             |   unico |
|:-----------------------------------------|:--------------------|--------:|
| course_sales_course_sale_type_id_foreign | course_sale_type_id |       0 |
| course_sales_school_id_foreign           | school_id           |       0 |
| course_sales_user_id_foreign             | user_id             |       0 |
| PRIMARY                                  | id                  |       1 |
