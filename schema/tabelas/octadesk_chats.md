# `octadesk_chats`

Linhas (estimativa do information_schema): **~37.298**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna                 | tipo            | nulo   | chave   | padrao   | comentario   |
|:-----------------------|:----------------|:-------|:--------|:---------|:-------------|
| id                     | bigint unsigned | NO     | PRI     |          |              |
| uuid                   | char(36)        | NO     | UNI     |          |              |
| chat_id                | varchar(255)    | YES    | UNI     |          |              |
| school_id              | bigint unsigned | YES    | MUL     |          |              |
| created_at             | timestamp       | YES    |         |          |              |
| status                 | varchar(50)     | YES    | MUL     |          |              |
| updated_at_octa        | datetime        | YES    |         |          |              |
| closed_at              | datetime        | YES    |         |          |              |
| phone                  | varchar(100)    | YES    | MUL     |          |              |
| contact_name           | varchar(150)    | YES    |         |          |              |
| agent_name             | varchar(150)    | YES    |         |          |              |
| channel                | varchar(50)     | YES    |         |          |              |
| tags                   | text            | YES    |         |          |              |
| group                  | varchar(150)    | YES    |         |          |              |
| origin                 | varchar(100)    | YES    |         |          |              |
| bot_name               | varchar(150)    | YES    |         |          |              |
| survey_response        | text            | YES    |         |          |              |
| raw_json               | longtext        | YES    |         |          |              |
| cached_at              | datetime        | YES    |         |          |              |
| synced_at              | datetime        | YES    |         |          |              |
| avaliavel              | tinyint         | YES    |         |          |              |
| avaliabilidade_motivo  | varchar(255)    | YES    |         |          |              |
| avaliabilidade_calc_at | datetime        | YES    |         |          |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna    | referencia   |
|:----------|:-------------|
| school_id | schools.id   |

## Referenciada por (outra tabela → esta)

_(vazio)_

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                           | colunas   |   unico |
|:---------------------------------|:----------|--------:|
| idx_octadesk_chats_phone         | phone     |       0 |
| idx_octadesk_chats_status        | status    |       0 |
| octadesk_chats_school_id_foreign | school_id |       0 |
| octadesk_chats_uuid_unique       | uuid      |       1 |
| PRIMARY                          | id        |       1 |
| uq_octadesk_chats_chat_id        | chat_id   |       1 |
