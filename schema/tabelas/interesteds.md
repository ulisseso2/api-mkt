# `interesteds`

Linhas (estimativa do information_schema): **~511.252**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna                           | tipo                        | nulo   | chave   |   padrao | comentario                               |
|:---------------------------------|:----------------------------|:-------|:--------|---------:|:-----------------------------------------|
| id                               | bigint unsigned             | NO     | PRI     |      nan |                                          |
| uuid                             | char(36)                    | YES    |         |      nan |                                          |
| page_title                       | varchar(255)                | YES    |         |      nan |                                          |
| page_type                        | varchar(255)                | YES    |         |      nan |                                          |
| first_name                       | varchar(255)                | YES    | MUL     |      nan |                                          |
| last_name                        | varchar(255)                | YES    |         |      nan |                                          |
| phone                            | varchar(255)                | YES    |         |      nan |                                          |
| email                            | varchar(255)                | YES    | MUL     |      nan |                                          |
| popup                            | tinyint(1)                  | YES    |         |        0 |                                          |
| prefer_to_study                  | varchar(255)                | YES    |         |      nan |                                          |
| previous_contest                 | varchar(10)                 | YES    |         |      nan | Já estudou pra concurso antes? (Sim/Não) |
| unit                             | varchar(255)                | YES    |         |      nan |                                          |
| shift                            | varchar(255)                | YES    |         |      nan |                                          |
| time                             | varchar(255)                | YES    |         |      nan |                                          |
| status                           | tinyint(1)                  | YES    |         |      nan |                                          |
| prelead                          | tinyint(1)                  | NO     |         |        0 |                                          |
| variant                          | varchar(255)                | YES    | MUL     |      nan | Variante A/B do formulário (A ou B)      |
| finished                         | tinyint(1)                  | NO     | MUL     |        0 | Indica se o fluxo de lead foi concluído  |
| origin                           | varchar(255)                | YES    |         |      nan |                                          |
| school_id                        | bigint unsigned             | YES    | MUL     |      nan |                                          |
| created_at                       | timestamp                   | YES    |         |      nan |                                          |
| updated_at                       | timestamp                   | YES    |         |      nan |                                          |
| contest_id                       | bigint unsigned             | YES    | MUL     |      nan |                                          |
| product_id                       | bigint unsigned             | YES    | MUL     |      nan |                                          |
| customer_id                      | bigint unsigned             | YES    | MUL     |      nan |                                          |
| position                         | varchar(255)                | YES    |         |      nan |                                          |
| external_id                      | varchar(100)                | YES    |         |      nan |                                          |
| phone_2                          | varchar(255)                | YES    |         |      nan |                                          |
| age                              | int                         | YES    |         |      nan |                                          |
| were_you_a_student               | tinyint(1)                  | YES    |         |      nan |                                          |
| held_a_contest                   | tinyint(1)                  | YES    |         |      nan |                                          |
| checkout_sent                    | tinyint(1)                  | YES    |         |      nan |                                          |
| link                             | varchar(255)                | YES    |         |      nan |                                          |
| gclid                            | varchar(255)                | YES    |         |      nan |                                          |
| fbclid                           | varchar(255)                | YES    |         |      nan |                                          |
| tiktok                           | varchar(255)                | YES    |         |      nan |                                          |
| email_marketing                  | varchar(255)                | YES    |         |      nan |                                          |
| utm_source                       | varchar(255)                | YES    |         |      nan |                                          |
| utm_medium                       | varchar(255)                | YES    |         |      nan |                                          |
| utm_campaign                     | varchar(255)                | YES    |         |      nan |                                          |
| utm_content                      | varchar(255)                | YES    |         |      nan |                                          |
| level                            | enum('1','2','3','4','5')   | YES    |         |        1 |                                          |
| interest_contest_id              | bigint unsigned             | YES    |         |      nan |                                          |
| opportunity_step_id              | bigint unsigned             | YES    | MUL     |      nan |                                          |
| user_id                          | bigint unsigned             | YES    | MUL     |      nan |                                          |
| reason_for_losse_id              | bigint unsigned             | YES    | MUL     |      nan |                                          |
| owner_id                         | bigint unsigned             | YES    | MUL     |      nan |                                          |
| area_id                          | bigint unsigned             | YES    | MUL     |      nan |                                          |
| opportunity_origin_id            | bigint unsigned             | YES    | MUL     |      nan |                                          |
| scholarity_id                    | int unsigned                | YES    | MUL     |      nan |                                          |
| unit_calendar_id                 | bigint unsigned             | YES    | MUL     |      nan |                                          |
| sales_force_id                   | bigint unsigned             | YES    | MUL     |      nan |                                          |
| opportunity_modality_id          | bigint unsigned             | YES    | MUL     |      nan |                                          |
| time_to_call_id                  | int unsigned                | YES    | MUL     |      nan |                                          |
| shift_id                         | int unsigned                | YES    | MUL     |      nan |                                          |
| unit_id                          | bigint unsigned             | YES    | MUL     |      nan |                                          |
| chat_id                          | varchar(150)                | YES    |         |      nan |                                          |
| last_step_updated_at             | datetime                    | YES    | MUL     |      nan |                                          |
| checkout_link                    | varchar(255)                | YES    |         |      nan |                                          |
| classroom_id                     | bigint unsigned             | YES    | MUL     |      nan |                                          |
| instagram_username               | varchar(100)                | YES    |         |      nan |                                          |
| origin_information               | varchar(100)                | YES    |         |      nan |                                          |
| calls_count                      | int                         | YES    |         |        0 |                                          |
| pretension                       | varchar(255)                | YES    |         |      nan |                                          |
| challenge                        | varchar(255)                | YES    |         |      nan |                                          |
| user_ip                          | varchar(255)                | YES    |         |      nan |                                          |
| city                             | varchar(255)                | YES    |         |      nan |                                          |
| state                            | varchar(255)                | YES    |         |      nan |                                          |
| user_agent                       | text                        | YES    |         |      nan |                                          |
| form_step                        | int                         | YES    |         |      nan |                                          |
| opportunity_status_id            | bigint unsigned             | YES    | MUL     |        1 |                                          |
| has_contest_familiarity          | tinyint(1)                  | YES    |         |      nan |                                          |
| tired_of_private_sector          | tinyint(1)                  | YES    |         |      nan |                                          |
| interested_in_active_interaction | tinyint(1)                  | YES    |         |      nan |                                          |
| last_evaluated_band              | enum('green','amber','red') | YES    |         |      nan |                                          |
| event_id                         | varchar(64)                 | YES    | MUL     |      nan |                                          |
| last_inbound_message_at          | datetime                    | YES    | MUL     |      nan |                                          |
| gbraid                           | varchar(255)                | YES    |         |      nan |                                          |
| wbraid                           | varchar(255)                | YES    |         |      nan |                                          |

## Chaves estrangeiras (esta tabela → outra)

| coluna                  | referencia                |
|:------------------------|:--------------------------|
| area_id                 | areas.id                  |
| classroom_id            | classrooms.id             |
| contest_id              | contests.id               |
| customer_id             | customers.id              |
| opportunity_modality_id | opportunity_modalities.id |
| opportunity_origin_id   | opportunity_origins.id    |
| opportunity_status_id   | opportunity_statuses.id   |
| opportunity_step_id     | opportunity_steps.id      |
| owner_id                | users.id                  |
| product_id              | products.id               |
| reason_for_losse_id     | reason_for_losses.id      |
| sales_force_id          | sales_force.id            |
| scholarity_id           | scholarities.id           |
| school_id               | schools.id                |
| shift_id                | shifts.id                 |
| time_to_call_id         | time_to_calls.id          |
| unit_calendar_id        | unit_calendars.id         |
| unit_id                 | units.id                  |
| user_id                 | users.id                  |

## Referenciada por (outra tabela → esta)

| origem                                     | coluna   |
|:-------------------------------------------|:---------|
| interested_pontuations.interested_id       | id       |
| interested_x_orders.interested_id          | id       |
| opportunity_calls.opportunity_id           | id       |
| opportunity_esteira_actions.opportunity_id | id       |
| opportunity_follows.opportunity_id         | id       |
| opportunity_follows_upsell.opportunity_id  | id       |
| opportunity_logs.opportunity_id            | id       |
| opportunity_stage_history.opportunity_id   | id       |
| opportunity_transcripts.opportunity_id     | id       |
| opportunity_user_favorites.opportunity_id  | id       |
| orders.opportunity_id                      | id       |
| stage_time_events.opportunity_id           | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                      | colunas                                            |   unico |
|:--------------------------------------------|:---------------------------------------------------|--------:|
| ft_interesteds_email                        | email                                              |       0 |
| ft_interesteds_name                         | first_name,last_name                               |       0 |
| idx_finished                                | finished                                           |       0 |
| idx_interesteds_school_challenge            | school_id,challenge                                |       0 |
| idx_interesteds_school_chat                 | school_id,chat_id                                  |       0 |
| idx_interesteds_school_city                 | school_id,city                                     |       0 |
| idx_interesteds_school_created_at           | school_id,created_at                               |       0 |
| idx_interesteds_school_email                | school_id,email                                    |       0 |
| idx_interesteds_school_phone_created        | school_id,phone,created_at                         |       0 |
| idx_interesteds_school_prelead_created      | school_id,prelead,created_at                       |       0 |
| idx_interesteds_school_prelead_id           | school_id,prelead,id                               |       0 |
| idx_interesteds_school_pretension           | school_id,pretension                               |       0 |
| idx_interesteds_school_state                | school_id,state                                    |       0 |
| idx_interesteds_school_step_stagetime       | school_id,opportunity_step_id,last_step_updated_at |       0 |
| idx_interesteds_school_uuid                 | school_id,uuid                                     |       0 |
| idx_variant                                 | variant                                            |       0 |
| interesteds_area_id_foreign                 | area_id                                            |       0 |
| interesteds_classroom_id_foreign            | classroom_id                                       |       0 |
| interesteds_contest_id_foreign              | contest_id                                         |       0 |
| interesteds_customer_id_foreign             | customer_id                                        |       0 |
| interesteds_event_id_index                  | event_id                                           |       0 |
| interesteds_last_inbound_message_at_index   | last_inbound_message_at                            |       0 |
| interesteds_last_step_updated_at_index      | last_step_updated_at                               |       0 |
| interesteds_opportunity_modality_id_foreign | opportunity_modality_id                            |       0 |
| interesteds_opportunity_origin_id_foreign   | opportunity_origin_id                              |       0 |
| interesteds_opportunity_status_id_foreign   | opportunity_status_id                              |       0 |
| interesteds_opportunity_step_id_foreign     | opportunity_step_id                                |       0 |
| interesteds_owner_id_foreign                | owner_id                                           |       0 |
| interesteds_product_id_foreign              | product_id                                         |       0 |
| interesteds_reason_for_losse_id_foreign     | reason_for_losse_id                                |       0 |
| interesteds_sales_force_id_foreign          | sales_force_id                                     |       0 |
| interesteds_scholarity_id_foreign           | scholarity_id                                      |       0 |
| interesteds_shift_id_foreign                | shift_id                                           |       0 |
| interesteds_time_to_call_id_foreign         | time_to_call_id                                    |       0 |
| interesteds_unit_calendar_id_foreign        | unit_calendar_id                                   |       0 |
| interesteds_unit_id_foreign                 | unit_id                                            |       0 |
| interesteds_user_id_foreign                 | user_id                                            |       0 |
| PRIMARY                                     | id                                                 |       1 |
