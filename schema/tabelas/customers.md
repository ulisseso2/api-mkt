# `customers`

Linhas (estimativa do information_schema): **~673.506**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna              | tipo                         | nulo   | chave   |   padrao | comentario         |
|:--------------------|:-----------------------------|:-------|:--------|---------:|:-------------------|
| id                  | bigint unsigned              | NO     | PRI     |      nan |                    |
| uuid                | char(36)                     | YES    |         |      nan |                    |
| full_name           | varchar(255)                 | NO     | MUL     |      nan |                    |
| first_name          | varchar(255)                 | YES    |         |      nan |                    |
| email               | varchar(255)                 | YES    | MUL     |      nan |                    |
| phone               | varchar(255)                 | YES    |         |      nan |                    |
| cellphone           | varchar(255)                 | YES    |         |      nan |                    |
| cpf                 | varchar(255)                 | YES    |         |      nan |                    |
| active              | varchar(255)                 | NO     |         |      nan |                    |
| origin_id           | bigint unsigned              | YES    | MUL     |      nan |                    |
| password            | varchar(255)                 | NO     |         |      nan |                    |
| school_id           | bigint unsigned              | YES    | MUL     |      nan |                    |
| created_at          | timestamp                    | YES    |         |      nan |                    |
| updated_at          | timestamp                    | YES    |         |      nan |                    |
| birth               | date                         | YES    |         |      nan |                    |
| gender              | enum('masculino','feminino') | YES    |         |      nan |                    |
| token_remember      | varchar(245)                 | YES    |         |      nan |                    |
| external_id         | varchar(255)                 | YES    |         |      nan |                    |
| scholarity_id       | int unsigned                 | YES    | MUL     |      nan |                    |
| rg                  | varchar(255)                 | YES    |         |      nan |                    |
| done                | tinyint(1)                   | YES    |         |      nan |                    |
| old_id              | int                          | YES    |         |      nan |                    |
| cellphone_2         | varchar(100)                 | YES    |         |      nan |                    |
| passport            | tinyint(1)                   | YES    |         |        0 |                    |
| trail               | tinyint(1)                   | YES    |         |        0 |                    |
| external_id_2       | varchar(255)                 | YES    |         |      nan | Vindi - Presencial |
| octadesk_contact_id | varchar(254)                 | YES    |         |      nan |                    |

## Chaves estrangeiras (esta tabela → outra)

| coluna        | referencia          |
|:--------------|:--------------------|
| origin_id     | customer_origins.id |
| scholarity_id | scholarities.id     |
| school_id     | schools.id          |

## Referenciada por (outra tabela → esta)

| origem                                        | coluna   |
|:----------------------------------------------|:---------|
| api_customer_tokens.customer_id               | id       |
| approved_students.customer_id                 | id       |
| carts.customer_id                             | id       |
| classroom_notification_recipients.customer_id | id       |
| classroom_transfers.customer_id               | id       |
| course_leaderboard.customer_id                | id       |
| customer_achievements.customer_id             | id       |
| customer_addresses.customer_id                | id       |
| customer_call_histories.customer_id           | id       |
| customer_follows.customer_id                  | id       |
| customer_logs.customer_id                     | id       |
| customer_note_teachers.customer_id            | id       |
| customer_notes.customer_id                    | id       |
| customer_schools.customer_id                  | id       |
| customer_xp.customer_id                       | id       |
| customer_xp_events.customer_id                | id       |
| grid_lesson_finish.customer_id                | id       |
| grid_lesson_notes.customer_id                 | id       |
| interesteds.customer_id                       | id       |
| lesson_finisheds.customer_id                  | id       |
| lesson_ratings.customer_id                    | id       |
| letter_credits.customer_id                    | id       |
| order_comments.customer_id                    | id       |
| order_discount_requests.customer_id           | id       |
| order_payment_attempts.customer_id            | id       |
| orders.customer_id                            | id       |
| school_warning_reads.customer_id              | id       |
| teacher_evaluates.customer_id                 | id       |
| unit_calendars.customer_id                    | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                          | colunas               |   unico |
|:--------------------------------|:----------------------|--------:|
| customers_origin_id_foreign     | origin_id             |       0 |
| customers_scholarity_id_foreign | scholarity_id         |       0 |
| ft_customers_email              | email                 |       0 |
| ft_customers_fullname           | full_name             |       0 |
| idx_customers_school_cellphone  | school_id,cellphone   |       0 |
| idx_customers_school_cellphone2 | school_id,cellphone_2 |       0 |
| idx_customers_school_cpf        | school_id,cpf         |       0 |
| idx_customers_school_email      | school_id,email       |       0 |
| idx_customers_school_uuid       | school_id,uuid        |       0 |
| PRIMARY                         | id                    |       1 |
