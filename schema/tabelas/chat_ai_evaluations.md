# `chat_ai_evaluations`

Linhas (estimativa do information_schema): **~3.586**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna                | tipo         | nulo   | chave   | padrao   | comentario   |
|:----------------------|:-------------|:-------|:--------|:---------|:-------------|
| id                    | int unsigned | NO     | PRI     |          |              |
| uuid                  | char(36)     | NO     | UNI     |          |              |
| opportunity_id        | int          | YES    |         |          |              |
| chat_id               | varchar(100) | NO     |         |          |              |
| classification        | varchar(50)  | NO     |         |          |              |
| classification_reason | text         | YES    |         |          |              |
| transcript            | text         | YES    |         |          |              |
| ai_evaluation         | json         | YES    |         |          |              |
| lead_score            | int          | YES    |         |          |              |
| vendor_score          | int          | YES    |         |          |              |
| main_product          | varchar(255) | YES    |         |          |              |
| octa_agent            | varchar(150) | YES    |         |          |              |
| octa_channel          | varchar(50)  | YES    |         |          |              |
| octa_status           | varchar(50)  | YES    |         |          |              |
| octa_tags             | text         | YES    |         |          |              |
| octa_group            | varchar(150) | YES    |         |          |              |
| octa_origin           | varchar(100) | YES    |         |          |              |
| octa_contact_name     | varchar(150) | YES    |         |          |              |
| octa_contact_phone    | varchar(50)  | YES    |         |          |              |
| octa_bot_name         | varchar(150) | YES    |         |          |              |
| octa_created_at       | varchar(50)  | YES    |         |          |              |
| octa_closed_at        | varchar(50)  | YES    |         |          |              |
| octa_survey_response  | varchar(50)  | YES    |         |          |              |
| created_at            | timestamp    | YES    |         |          |              |
| updated_at            | timestamp    | YES    |         |          |              |
| vendedor_disclaimer   | text         | YES    |         |          |              |
| lead_disclaimer       | text         | YES    |         |          |              |

## Chaves estrangeiras (esta tabela → outra)

_(vazio)_

## Referenciada por (outra tabela → esta)

_(vazio)_

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                          | colunas   |   unico |
|:--------------------------------|:----------|--------:|
| chat_ai_evaluations_uuid_unique | uuid      |       1 |
| PRIMARY                         | id        |       1 |
