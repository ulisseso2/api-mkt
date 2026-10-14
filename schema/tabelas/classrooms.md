# `classrooms`

Linhas (estimativa do information_schema): **~9.462**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna                | tipo            | nulo   | chave   |   padrao | comentario   |
|:----------------------|:----------------|:-------|:--------|---------:|:-------------|
| id                    | bigint unsigned | NO     | PRI     |      nan |              |
| uuid                  | char(36)        | YES    |         |      nan |              |
| name                  | varchar(255)    | NO     |         |      nan |              |
| start_time            | time            | YES    |         |      nan |              |
| end_time              | time            | YES    |         |      nan |              |
| link                  | varchar(255)    | YES    |         |      nan |              |
| display_panel         | tinyint(1)      | YES    |         |        0 |              |
| status                | tinyint(1)      | YES    |         |        0 |              |
| max_students          | int             | YES    |         |      nan |              |
| course_id             | bigint unsigned | YES    | MUL     |      nan |              |
| unit_id               | bigint unsigned | YES    | MUL     |      nan |              |
| shift_id              | int unsigned    | YES    | MUL     |      nan |              |
| classroom_modality_id | bigint unsigned | YES    | MUL     |      nan |              |
| user_id               | bigint unsigned | YES    | MUL     |      nan |              |
| school_id             | bigint unsigned | YES    | MUL     |      nan |              |
| created_at            | timestamp       | YES    |         |      nan |              |
| updated_at            | timestamp       | YES    |         |      nan |              |
| consys_grid           | varchar(255)    | YES    |         |      nan |              |
| migration             | tinyint(1)      | YES    |         |        0 |              |
| interval              | time            | YES    |         |      nan |              |
| confirmed_date        | datetime        | YES    |         |      nan |              |
| confirmed_user_id     | bigint unsigned | YES    | MUL     |      nan |              |
| date_end              | date            | YES    |         |      nan |              |
| old_id                | varchar(100)    | YES    |         |      nan |              |
| streaming_id          | int unsigned    | YES    | MUL     |        1 |              |
| start_type            | varchar(255)    | YES    |         |      nan |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna                | referencia              |
|:----------------------|:------------------------|
| classroom_modality_id | classroom_modalities.id |
| confirmed_user_id     | users.id                |
| course_id             | courses.id              |
| school_id             | schools.id              |
| shift_id              | shifts.id               |
| streaming_id          | streamings.id           |
| unit_id               | units.id                |
| user_id               | users.id                |

## Referenciada por (outra tabela → esta)

| origem                                   | coluna   |
|:-----------------------------------------|:---------|
| cart_products.classroom_id               | id       |
| classroom_consys.classroom_id            | id       |
| classroom_days.classroom_id              | id       |
| classroom_materials.classroom_id         | id       |
| classroom_notification_logs.classroom_id | id       |
| classroom_notifications.classroom_id     | id       |
| classroom_postponements.classroom_id     | id       |
| classroom_transfers.classroom_from_id    | id       |
| classroom_transfers.classroom_to_id      | id       |
| classroom_warnings.classroom_id          | id       |
| course_classrooms.classroom_id           | id       |
| grids.classroom_id                       | id       |
| interesteds.classroom_id                 | id       |
| order_discount_requests.classroom_id     | id       |
| order_items.classroom_id                 | id       |
| product_classrooms.classroom_id          | id       |
| school_warnings.classroom_id             | id       |
| teacher_evaluates.classroom_id           | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                   | colunas               |   unico |
|:-----------------------------------------|:----------------------|--------:|
| classrooms_classroom_modality_id_foreign | classroom_modality_id |       0 |
| classrooms_confirmed_user_id_foreign     | confirmed_user_id     |       0 |
| classrooms_course_id_foreign             | course_id             |       0 |
| classrooms_school_id_foreign             | school_id             |       0 |
| classrooms_shift_id_foreign              | shift_id              |       0 |
| classrooms_streaming_id_foreign          | streaming_id          |       0 |
| classrooms_unit_id_foreign               | unit_id               |       0 |
| classrooms_user_id_foreign               | user_id               |       0 |
| PRIMARY                                  | id                    |       1 |
