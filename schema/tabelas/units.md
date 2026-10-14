# `units`

Linhas (estimativa do information_schema): **~20**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna       | tipo            | nulo   | chave   |   padrao | comentario   |
|:-------------|:----------------|:-------|:--------|---------:|:-------------|
| id           | bigint unsigned | NO     | PRI     |      nan |              |
| uuid         | char(36)        | YES    |         |      nan |              |
| name         | varchar(255)    | NO     |         |      nan |              |
| email        | varchar(255)    | NO     |         |      nan |              |
| phone_1      | varchar(255)    | NO     |         |      nan |              |
| phone_2      | varchar(255)    | YES    |         |      nan |              |
| address      | varchar(255)    | NO     |         |      nan |              |
| neighborhood | varchar(255)    | NO     |         |      nan |              |
| complement   | varchar(255)    | YES    |         |      nan |              |
| number       | varchar(255)    | YES    |         |      nan |              |
| city         | varchar(255)    | NO     |         |      nan |              |
| uf           | varchar(255)    | NO     |         |      nan |              |
| cep          | varchar(255)    | NO     |         |      nan |              |
| slug         | varchar(255)    | NO     |         |      nan |              |
| status       | tinyint(1)      | YES    |         |        0 |              |
| school_id    | bigint unsigned | YES    | MUL     |      nan |              |
| user_id      | bigint unsigned | YES    | MUL     |      nan |              |
| created_at   | timestamp       | YES    |         |      nan |              |
| media_id     | bigint unsigned | YES    | MUL     |      nan |              |
| id_old       | varchar(255)    | YES    |         |      nan |              |
| is_live      | tinyint(1)      | YES    |         |        0 |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna    | referencia   |
|:----------|:-------------|
| media_id  | medias.id    |
| school_id | schools.id   |
| user_id   | users.id     |

## Referenciada por (outra tabela → esta)

| origem                              | coluna   |
|:------------------------------------|:---------|
| acquirer_units.unit_id              | id       |
| business_units.unit_id              | id       |
| classrooms.unit_id                  | id       |
| customer_follows.unit_id            | id       |
| interesteds.unit_id                 | id       |
| manager_discount_units.unit_id      | id       |
| orders.seller_unit_id               | id       |
| orders.unit_id                      | id       |
| school_team_units.unit_id           | id       |
| teacher_points_report_items.unit_id | id       |
| unit_calendars.unit_id              | id       |
| users.unit_id                       | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                  | colunas   |   unico |
|:------------------------|:----------|--------:|
| PRIMARY                 | id        |       1 |
| units_media_id_foreign  | media_id  |       0 |
| units_school_id_foreign | school_id |       0 |
| units_user_id_foreign   | user_id   |       0 |
