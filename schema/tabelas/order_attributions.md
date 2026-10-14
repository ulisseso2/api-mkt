# `order_attributions`

Linhas (estimativa do information_schema): **~395**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna            | tipo            | nulo   | chave   | padrao            | comentario   |
|:------------------|:----------------|:-------|:--------|:------------------|:-------------|
| id                | bigint unsigned | NO     | PRI     | nan               |              |
| uuid              | varchar(36)     | NO     | UNI     | nan               |              |
| order_id          | bigint unsigned | NO     | UNI     | nan               |              |
| school_id         | bigint unsigned | NO     | MUL     | nan               |              |
| event_id          | varchar(64)     | NO     |         | nan               |              |
| browser_event_id  | varchar(64)     | YES    |         | nan               |              |
| ga_client_id      | varchar(64)     | YES    |         | nan               |              |
| ga_session_id     | varchar(64)     | YES    |         | nan               |              |
| ga_session_number | int unsigned    | YES    |         | nan               |              |
| fbp               | varchar(255)    | YES    |         | nan               |              |
| fbc               | varchar(255)    | YES    |         | nan               |              |
| gclid             | varchar(255)    | YES    |         | nan               |              |
| gbraid            | varchar(255)    | YES    |         | nan               |              |
| wbraid            | varchar(255)    | YES    |         | nan               |              |
| ttclid            | varchar(255)    | YES    |         | nan               |              |
| fbclid            | varchar(255)    | YES    |         | nan               |              |
| utm_source        | varchar(100)    | YES    |         | nan               |              |
| utm_medium        | varchar(100)    | YES    |         | nan               |              |
| utm_campaign      | varchar(160)    | YES    |         | nan               |              |
| utm_content       | varchar(160)    | YES    |         | nan               |              |
| utm_term          | varchar(160)    | YES    |         | nan               |              |
| consent_status    | varchar(16)     | YES    |         | nan               |              |
| consent_analytics | tinyint(1)      | YES    |         | nan               |              |
| consent_marketing | tinyint(1)      | YES    |         | nan               |              |
| client_ip         | varchar(45)     | YES    |         | nan               |              |
| user_agent        | text            | YES    |         | nan               |              |
| page_location     | varchar(500)    | YES    |         | nan               |              |
| referrer          | varchar(500)    | YES    |         | nan               |              |
| origem            | varchar(100)    | YES    |         | nan               |              |
| modalidade        | varchar(20)     | YES    |         | nan               |              |
| new_user          | tinyint(1)      | YES    |         | nan               |              |
| ltv_value         | decimal(12,2)   | YES    |         | nan               |              |
| created_at        | timestamp       | NO     |         | CURRENT_TIMESTAMP |              |
| cityads_click_id  | varchar(255)    | YES    |         | nan               |              |

## Chaves estrangeiras (esta tabela → outra)

_(vazio)_

## Referenciada por (outra tabela → esta)

_(vazio)_

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                  | colunas                    |   unico |
|:----------------------------------------|:---------------------------|--------:|
| order_attributions_browser_event_index  | school_id,browser_event_id |       0 |
| order_attributions_order_unique         | order_id                   |       1 |
| order_attributions_school_created_index | school_id,created_at,id    |       0 |
| order_attributions_school_event_unique  | school_id,event_id         |       1 |
| order_attributions_uuid_unique          | uuid                       |       1 |
| PRIMARY                                 | id                         |       1 |
