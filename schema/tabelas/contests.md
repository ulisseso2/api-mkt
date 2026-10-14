# `contests`

Linhas (estimativa do information_schema): **~120**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna                | tipo            | nulo   | chave   |   padrao | comentario                              |
|:----------------------|:----------------|:-------|:--------|---------:|:----------------------------------------|
| id                    | bigint unsigned | NO     | PRI     |      nan |                                         |
| uuid                  | char(36)        | YES    |         |      nan |                                         |
| title                 | varchar(255)    | NO     |         |      nan |                                         |
| subtitle              | text            | YES    |         |      nan |                                         |
| video_url             | varchar(255)    | YES    |         |      nan |                                         |
| label_image           | varchar(255)    | YES    |         |      nan |                                         |
| description           | longtext        | YES    |         |      nan |                                         |
| about                 | text            | YES    |         |      nan |                                         |
| display_home          | tinyint(1)      | YES    |         |        0 |                                         |
| display_passport      | tinyint(1)      | YES    |         |        0 |                                         |
| display_subscription  | tinyint(1)      | YES    |         |        0 |                                         |
| status                | tinyint(1)      | YES    |         |        0 |                                         |
| banner_id             | bigint unsigned | YES    | MUL     |      nan |                                         |
| datasheet_id          | bigint unsigned | YES    | MUL     |      nan |                                         |
| approved_student_id   | bigint unsigned | YES    | MUL     |      nan |                                         |
| media_id              | bigint unsigned | YES    | MUL     |      nan |                                         |
| user_id               | bigint unsigned | YES    | MUL     |      nan |                                         |
| school_id             | bigint unsigned | YES    | MUL     |      nan |                                         |
| title_seo             | varchar(255)    | YES    |         |      nan |                                         |
| description_seo       | varchar(255)    | YES    |         |      nan |                                         |
| created_at            | timestamp       | YES    |         |      nan |                                         |
| updated_at            | timestamp       | YES    |         |      nan |                                         |
| tags                  | longtext        | YES    |         |      nan |                                         |
| slug                  | varchar(255)    | YES    |         |      nan |                                         |
| sales_force_id        | bigint unsigned | YES    | MUL     |      nan |                                         |
| sort                  | int             | YES    |         |      nan |                                         |
| sort_home             | int             | YES    |         |      nan |                                         |
| done                  | tinyint(1)      | YES    |         |      nan |                                         |
| disable_whatsapp      | tinyint(1)      | YES    |         |        0 |                                         |
| sales_force_positions | tinyint(1)      | YES    |         |        0 |                                         |
| label_positions       | varchar(255)    | YES    |         |      nan |                                         |
| form_presencial       | tinyint(1)      | YES    |         |        1 |                                         |
| form_online           | tinyint(1)      | YES    |         |        1 |                                         |
| form_live             | tinyint(1)      | YES    |         |        1 |                                         |
| show_relateds         | tinyint(1)      | NO     |         |        1 |                                         |
| show_datasheet        | tinyint(1)      | NO     |         |        1 |                                         |
| landing_page_config   | json            | YES    |         |      nan |                                         |
| weight_a              | int unsigned    | NO     |         |       50 | Peso da variante A no Teste A/B (0–100) |
| weight_b              | int unsigned    | NO     |         |       50 | Peso da variante B no Teste A/B (0–100) |
| enable_new_lp         | tinyint(1)      | YES    |         |        0 |                                         |
| published             | tinyint(1)      | YES    |         |        0 |                                         |
| faqs                  | json            | YES    |         |      nan |                                         |

## Chaves estrangeiras (esta tabela → outra)

| coluna              | referencia           |
|:--------------------|:---------------------|
| approved_student_id | approved_students.id |
| banner_id           | banners.id           |
| datasheet_id        | datasheets.id        |
| media_id            | medias.id            |
| sales_force_id      | sales_force.id       |
| school_id           | schools.id           |
| user_id             | users.id             |

## Referenciada por (outra tabela → esta)

| origem                                   | coluna   |
|:-----------------------------------------|:---------|
| banners.contest_id                       | id       |
| contest_access_logs.contest_id           | id       |
| contest_approveds.contest_id             | id       |
| contest_areas.contest_id                 | id       |
| contest_drafts.contest_id                | id       |
| contest_product_book_digitals.contest_id | id       |
| contest_product_book_impress.contest_id  | id       |
| contest_product_books.contest_id         | id       |
| contest_product_fast.contest_id          | id       |
| contest_product_free.contest_id          | id       |
| contest_product_lives.contest_id         | id       |
| contest_product_online.contest_id        | id       |
| contest_product_presencials.contest_id   | id       |
| contest_sales_force.contest_id           | id       |
| contest_sorts.contest_id                 | id       |
| interesteds.contest_id                   | id       |
| post_contests.contest_id                 | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                               | colunas             |   unico |
|:-------------------------------------|:--------------------|--------:|
| contests_approved_student_id_foreign | approved_student_id |       0 |
| contests_banner_id_foreign           | banner_id           |       0 |
| contests_datasheet_id_foreign        | datasheet_id        |       0 |
| contests_media_id_foreign            | media_id            |       0 |
| contests_sales_force_id_foreign      | sales_force_id      |       0 |
| contests_school_slug_idx             | school_id,slug      |       0 |
| contests_user_id_foreign             | user_id             |       0 |
| PRIMARY                              | id                  |       1 |
