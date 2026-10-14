# `products`

Linhas (estimativa do information_schema): **~772**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna                 | tipo            | nulo   | chave   |   padrao | comentario                                 |
|:-----------------------|:----------------|:-------|:--------|---------:|:-------------------------------------------|
| id                     | bigint unsigned | NO     | PRI     |      nan |                                            |
| uuid                   | char(36)        | YES    |         |      nan |                                            |
| title                  | varchar(255)    | NO     |         |      nan |                                            |
| cost                   | decimal(8,2)    | YES    |         |      nan |                                            |
| price                  | decimal(11,2)   | YES    |         |      nan |                                            |
| sale                   | decimal(11,2)   | YES    |         |      nan |                                            |
| video_url              | varchar(255)    | YES    |         |      nan |                                            |
| description            | longtext        | YES    |         |      nan |                                            |
| about                  | text            | YES    |         |      nan |                                            |
| title_seo              | varchar(255)    | YES    |         |      nan |                                            |
| description_seo        | varchar(255)    | YES    |         |      nan |                                            |
| disable_store_discount | tinyint(1)      | YES    |         |        0 |                                            |
| disable_billet         | tinyint(1)      | YES    |         |        0 |                                            |
| disable_popup          | tinyint(1)      | YES    |         |        0 |                                            |
| slug                   | varchar(255)    | YES    |         |      nan |                                            |
| external_id            | varchar(255)    | YES    |         |      nan |                                            |
| media_id               | bigint unsigned | YES    | MUL     |      nan |                                            |
| product_category_id    | bigint unsigned | YES    | MUL     |      nan |                                            |
| school_id              | bigint unsigned | YES    | MUL     |      nan |                                            |
| user_id                | bigint unsigned | YES    | MUL     |      nan |                                            |
| created_at             | timestamp       | YES    |         |      nan |                                            |
| updated_at             | timestamp       | YES    |         |      nan |                                            |
| datasheet_id           | bigint unsigned | YES    | MUL     |      nan |                                            |
| label_image            | varchar(255)    | YES    |         |      nan |                                            |
| id_old                 | varchar(255)    | YES    |         |      nan |                                            |
| validity               | int             | YES    |         |      365 |                                            |
| class_id               | varchar(255)    | YES    |         |      nan |                                            |
| grid_id                | varchar(255)    | YES    |         |      nan |                                            |
| live_link              | varchar(255)    | YES    |         |      nan |                                            |
| tags                   | longtext        | YES    |         |      nan |                                            |
| status                 | tinyint(1)      | YES    |         |      nan |                                            |
| banner_id              | bigint unsigned | YES    | MUL     |      nan |                                            |
| sales_force_id         | bigint unsigned | YES    | MUL     |      nan |                                            |
| disable_form_contact   | tinyint(1)      | YES    |         |      nan |                                            |
| product_subcategory_id | bigint unsigned | YES    | MUL     |      nan |                                            |
| program_content        | longtext        | YES    |         |      nan |                                            |
| max_installments       | int             | YES    |         |      nan |                                            |
| promotion_date         | date            | YES    |         |      nan |                                            |
| sort                   | int             | YES    |         |      nan |                                            |
| plataforma_questoes    | tinyint(1)      | YES    |         |        0 |                                            |
| title_contract         | varchar(255)    | YES    |         |      nan |                                            |
| display_panel          | tinyint(1)      | YES    |         |        0 |                                            |
| course                 | tinyint(1)      | YES    |         |        0 |                                            |
| course_sale_id         | bigint unsigned | YES    | MUL     |      nan |                                            |
| scholarity_id          | int unsigned    | YES    | MUL     |      nan |                                            |
| product_type_id        | bigint unsigned | YES    | MUL     |      nan |                                            |
| disable_whatsapp       | tinyint(1)      | YES    |         |        0 |                                            |
| api_questoes_area      | varchar(255)    | YES    |         |      nan |                                            |
| api_questoes_edital    | varchar(255)    | YES    |         |      nan |                                            |
| migration              | tinyint(1)      | YES    |         |        0 |                                            |
| sales_force_positions  | tinyint(1)      | YES    |         |        0 |                                            |
| label_positions        | varchar(255)    | YES    |         |      nan |                                            |
| api_questoes_dias      | int             | YES    |         |       30 |                                            |
| workload               | varchar(10)     | YES    |         |        0 |                                            |
| active_in_trail        | tinyint(1)      | NO     |         |        1 | Indica se o produto está ativo para trilha |
| show_datasheet         | tinyint(1)      | NO     |         |        1 |                                            |
| faqs                   | json            | YES    |         |      nan |                                            |
| teaches                | json            | YES    |         |      nan |                                            |
| units                  | text            | YES    |         |      nan |                                            |

## Chaves estrangeiras (esta tabela → outra)

| coluna                 | referencia               |
|:-----------------------|:-------------------------|
| banner_id              | banners.id               |
| course_sale_id         | course_sales.id          |
| datasheet_id           | datasheets.id            |
| media_id               | medias.id                |
| product_category_id    | product_categories.id    |
| product_subcategory_id | product_subcategories.id |
| product_type_id        | product_types.id         |
| sales_force_id         | sales_force.id           |
| scholarity_id          | scholarities.id          |
| school_id              | schools.id               |
| user_id                | users.id                 |

## Referenciada por (outra tabela → esta)

| origem                                      | coluna   |
|:--------------------------------------------|:---------|
| cart_products.product_id                    | id       |
| contest_product_book_digitals.product_id    | id       |
| contest_product_book_impress.product_id     | id       |
| contest_product_books.product_id            | id       |
| contest_product_fast.product_id             | id       |
| contest_product_free.product_id             | id       |
| contest_product_lives.product_id            | id       |
| contest_product_online.product_id           | id       |
| contest_product_presencials.product_id      | id       |
| contracts.product_id                        | id       |
| coupon_products.product_id                  | id       |
| course_products.product_id                  | id       |
| courses.product_id                          | id       |
| courses.product_live_id                     | id       |
| interesteds.product_id                      | id       |
| lesson_finisheds.product_id                 | id       |
| post_products.product_id                    | id       |
| product_approveds.product_id                | id       |
| product_areas.product_id                    | id       |
| product_book_infos.product_id               | id       |
| product_classrooms.product_id               | id       |
| product_cycles.product_id                   | id       |
| product_disciplines.product_id              | id       |
| product_installments.product_id             | id       |
| product_landing_pages.product_id            | id       |
| product_list_subcategories.product_id       | id       |
| product_live_disciplines.product_id         | id       |
| product_presencial_disciplines.product_id   | id       |
| product_products.product_id                 | id       |
| product_products.product_product_id         | id       |
| product_recommendeds.product_id             | id       |
| product_recommendeds.recommended_product_id | id       |
| product_sales_force.product_id              | id       |
| product_warnings.product_id                 | id       |
| products_related.product_id                 | id       |
| products_related.product_related_id         | id       |
| school_warnings.product_id                  | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                  | colunas                            |   unico |
|:----------------------------------------|:-----------------------------------|--------:|
| PRIMARY                                 | id                                 |       1 |
| products_banner_id_foreign              | banner_id                          |       0 |
| products_course_sale_id_foreign         | course_sale_id                     |       0 |
| products_datasheet_id_foreign           | datasheet_id                       |       0 |
| products_media_id_foreign               | media_id                           |       0 |
| products_product_category_id_foreign    | product_category_id                |       0 |
| products_product_subcategory_id_foreign | product_subcategory_id             |       0 |
| products_product_type_id_foreign        | product_type_id                    |       0 |
| products_public_presencial_slug_idx     | school_id,product_category_id,slug |       0 |
| products_sales_force_id_foreign         | sales_force_id                     |       0 |
| products_scholarity_id_foreign          | scholarity_id                      |       0 |
| products_user_id_foreign                | user_id                            |       0 |
