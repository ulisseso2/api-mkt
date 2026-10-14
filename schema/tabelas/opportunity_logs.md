# `opportunity_logs`

Linhas (estimativa do information_schema): **~1.544.676**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna                      | tipo            | nulo   | chave   | padrao   | comentario   |
|:----------------------------|:----------------|:-------|:--------|:---------|:-------------|
| id                          | bigint unsigned | NO     | PRI     |          |              |
| uuid                        | char(36)        | NO     | UNI     |          |              |
| title                       | varchar(255)    | NO     |         |          |              |
| text                        | varchar(255)    | YES    |         |          |              |
| data                        | longtext        | YES    |         |          |              |
| opportunity_log_category_id | bigint unsigned | NO     | MUL     |          |              |
| user_id                     | bigint unsigned | YES    | MUL     |          |              |
| opportunity_id              | bigint unsigned | NO     | MUL     |          |              |
| created_at                  | timestamp       | YES    |         |          |              |
| data_uuid                   | varchar(254)    | YES    |         |          |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna                      | referencia                    |
|:----------------------------|:------------------------------|
| opportunity_id              | interesteds.id                |
| opportunity_log_category_id | opportunity_log_categories.id |
| user_id                     | users.id                      |

## Referenciada por (outra tabela → esta)

_(vazio)_

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                               | colunas                     |   unico |
|:-----------------------------------------------------|:----------------------------|--------:|
| opportunity_logs_opportunity_id_foreign              | opportunity_id              |       0 |
| opportunity_logs_opportunity_log_category_id_foreign | opportunity_log_category_id |       0 |
| opportunity_logs_user_id_foreign                     | user_id                     |       0 |
| opportunity_logs_uuid_unique                         | uuid                        |       1 |
| PRIMARY                                              | id                          |       1 |
