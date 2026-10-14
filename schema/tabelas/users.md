# `users`

Linhas (estimativa do information_schema): **~207**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna              | tipo            | nulo   | chave   |   padrao | comentario   |
|:--------------------|:----------------|:-------|:--------|---------:|:-------------|
| id                  | bigint unsigned | NO     | PRI     |      nan |              |
| uuid                | char(36)        | YES    |         |      nan |              |
| full_name           | varchar(255)    | NO     |         |      nan |              |
| first_name          | varchar(255)    | NO     |         |      nan |              |
| email               | varchar(255)    | NO     |         |      nan |              |
| phone               | varchar(255)    | YES    |         |      nan |              |
| cellphone           | varchar(255)    | YES    |         |      nan |              |
| cpf                 | varchar(255)    | YES    |         |      nan |              |
| active              | varchar(255)    | NO     |         |        0 |              |
| token_remember      | varchar(245)    | YES    |         |      nan |              |
| password            | varchar(200)    | NO     |         |      nan |              |
| created_at          | timestamp       | YES    |         |      nan |              |
| updated_at          | timestamp       | YES    |         |      nan |              |
| user_permission_id  | bigint unsigned | YES    | MUL     |      nan |              |
| unit_id             | bigint unsigned | YES    | MUL     |      nan |              |
| crm                 | tinyint(1)      | YES    |         |        0 |              |
| opportunity_list_id | bigint unsigned | YES    | MUL     |      nan |              |
| last_access         | datetime        | YES    |         |      nan |              |
| seller              | tinyint(1)      | NO     |         |        0 |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna              | referencia           |
|:--------------------|:---------------------|
| opportunity_list_id | opportunity_lists.id |
| unit_id             | units.id             |
| user_permission_id  | user_permissions.id  |

## Referenciada por (outra tabela → esta)

| origem                                 | coluna   |
|:---------------------------------------|:---------|
| acquirers.user_id                      | id       |
| api_tokens.tokenable_id                | id       |
| api_tokens.user_id                     | id       |
| approved_students.user_id              | id       |
| auth_access_tokens.tokenable_id        | id       |
| bank_account_categories.user_id        | id       |
| bank_account_logs.user_id              | id       |
| bank_account_types.user_id             | id       |
| bank_accounts.user_id                  | id       |
| banners.user_id                        | id       |
| business_unit_categories.user_id       | id       |
| business_units.user_id                 | id       |
| card_networks.user_id                  | id       |
| cash_flows.user_id                     | id       |
| classroom_days.user_id                 | id       |
| classroom_notification_logs.user_id    | id       |
| classroom_notifications.user_id        | id       |
| classroom_postponements.user_id        | id       |
| classroom_transfers.responsible_id     | id       |
| classroom_transfers.user_id            | id       |
| classrooms.confirmed_user_id           | id       |
| classrooms.user_id                     | id       |
| client_categories.user_id              | id       |
| clients.user_id                        | id       |
| companies.user_id                      | id       |
| contest_sorts.user_id                  | id       |
| contests.user_id                       | id       |
| contracts.user_id                      | id       |
| cost_centers.user_id                   | id       |
| coupons.user_id                        | id       |
| course_installments.user_id            | id       |
| course_sale_types.user_id              | id       |
| course_sales.user_id                   | id       |
| course_types.user_id                   | id       |
| courses.user_id                        | id       |
| customer_call_histories.user_id        | id       |
| customer_follows.user_id               | id       |
| datasheet_contract_models.user_id      | id       |
| disciplines.user_id                    | id       |
| email_template_categories.user_id      | id       |
| email_templates.user_id                | id       |
| grid_lesson_categories.user_id         | id       |
| grid_lesson_status.user_id             | id       |
| grid_lessons.user_id                   | id       |
| grid_lessons.user_signature_id         | id       |
| grid_logs.user_id                      | id       |
| grids.user_id                          | id       |
| interesteds.owner_id                   | id       |
| interesteds.user_id                    | id       |
| lessons.user_id                        | id       |
| letter_credit_logs.user_id             | id       |
| letter_credits.user_id                 | id       |
| manager_discounts.manager_id           | id       |
| manager_discounts.user_id              | id       |
| mcp_access_tokens.user_id              | id       |
| mcp_usage_logs.user_id                 | id       |
| medias.user_id                         | id       |
| news.user_id                           | id       |
| news_curations.published_by            | id       |
| notas_fiscais.user_id                  | id       |
| opportunity_calls.user_id              | id       |
| opportunity_follows.user_id            | id       |
| opportunity_follows_upsell.user_id     | id       |
| opportunity_list_users.user_id         | id       |
| opportunity_lists.user_id              | id       |
| opportunity_logs.user_id               | id       |
| opportunity_modalities.user_id         | id       |
| opportunity_user_favorites.user_id     | id       |
| order_comments.user_id                 | id       |
| order_contracts.user_id                | id       |
| order_discount_requests.manager_id     | id       |
| order_discount_requests.user_id        | id       |
| order_notes.user_id                    | id       |
| order_operations.user_id               | id       |
| order_plans.user_id                    | id       |
| order_refunds.user                     | id       |
| order_release_types.user_id            | id       |
| orders.owner_id                        | id       |
| orders.user_id                         | id       |
| partners.user_id                       | id       |
| payment_movements.user_id              | id       |
| posts.user_id                          | id       |
| product_cycles.user_id                 | id       |
| product_installments.user_id           | id       |
| product_types.user_id                  | id       |
| products.user_id                       | id       |
| purchase_order_categories.user_id      | id       |
| purchase_order_movements.user_id       | id       |
| purchase_order_step_users.user_id      | id       |
| purchase_orders.user_id                | id       |
| remittances.user_id                    | id       |
| request_discounts.user_id              | id       |
| sales_order_categories.user_id         | id       |
| sales_orders.user_id                   | id       |
| sales_panel_sorts.user_id              | id       |
| school_discounts.user_id               | id       |
| school_esteira_settings.system_user_id | id       |
| school_faqs.user_id                    | id       |
| school_gateways.user_id                | id       |
| school_octadesk_templates.user_id      | id       |
| school_permissions.user_id             | id       |
| school_privacy_policies.user_id        | id       |
| school_sendgrid_templates.user_id      | id       |
| school_team_users.user_id              | id       |
| school_teams.user_id                   | id       |
| school_warnings.user_id                | id       |
| strategic_unit_categories.user_id      | id       |
| strategic_units.user_id                | id       |
| supplier_bank_accounts.user_id         | id       |
| supplier_categories.user_id            | id       |
| suppliers.user_id                      | id       |
| tags.user_id                           | id       |
| teacher_notes.user_id                  | id       |
| teacher_points_reports.user_id         | id       |
| teacher_unavailabilities.user_id       | id       |
| transfers.user_id                      | id       |
| unit_calendars.user_id                 | id       |
| units.user_id                          | id       |
| user_discount_categories.user_id       | id       |
| user_logs.user_id                      | id       |
| user_schools.user_id                   | id       |
| weekdays.user_id                       | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                            | colunas             |   unico |
|:----------------------------------|:--------------------|--------:|
| PRIMARY                           | id                  |       1 |
| users_opportunity_list_id_foreign | opportunity_list_id |       0 |
| users_unit_id_foreign             | unit_id             |       0 |
| users_user_permission_id_foreign  | user_permission_id  |       0 |
