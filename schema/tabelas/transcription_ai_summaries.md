# `transcription_ai_summaries`

Linhas (estimativa do information_schema): **~4.300**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna                 | tipo            | nulo   | chave   | padrao            | comentario   |
|:-----------------------|:----------------|:-------|:--------|:------------------|:-------------|
| id                     | bigint unsigned | NO     | PRI     | nan               |              |
| transcription_id       | bigint unsigned | NO     | UNI     | nan               |              |
| uuid                   | varchar(64)     | YES    |         | nan               |              |
| created_at             | timestamp       | NO     |         | CURRENT_TIMESTAMP |              |
| updated_at             | timestamp       | YES    |         | nan               |              |
| ai_insight             | longtext        | YES    |         | nan               |              |
| ai_evaluation          | int             | YES    |         | nan               |              |
| lead_score             | int             | YES    |         | nan               |              |
| lead_classification    | varchar(8)      | YES    |         | nan               |              |
| strengths              | text            | YES    |         | nan               |              |
| improvements           | text            | YES    |         | nan               |              |
| most_expensive_mistake | varchar(255)    | YES    |         | nan               |              |
| main_pain_points       | text            | YES    |         | nan               |              |
| restrictions           | text            | YES    |         | nan               |              |
| contest_area           | varchar(255)    | YES    |         | nan               |              |
| main_product           | varchar(100)    | YES    |         | nan               |              |
| vendedor_disclaimer    | text            | YES    |         | nan               |              |
| lead_disclaimer        | text            | YES    |         | nan               |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna           | referencia                 |
|:-----------------|:---------------------------|
| transcription_id | opportunity_transcripts.id |

## Referenciada por (outra tabela → esta)

_(vazio)_

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                             | colunas          |   unico |
|:---------------------------------------------------|:-----------------|--------:|
| PRIMARY                                            | id               |       1 |
| transcription_ai_summaries_transcription_id_unique | transcription_id |       1 |
