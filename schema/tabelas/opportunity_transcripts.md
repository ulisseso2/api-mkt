# `opportunity_transcripts`

Linhas (estimativa do information_schema): **~45.132**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna              | tipo                       | nulo   | chave   | padrao   | comentario   |
|:--------------------|:---------------------------|:-------|:--------|:---------|:-------------|
| id                  | bigint unsigned            | NO     | PRI     |          |              |
| uuid                | char(36)                   | NO     | UNI     |          |              |
| transcript          | text                       | YES    |         |          |              |
| opportunity_id      | bigint unsigned            | YES    | MUL     |          |              |
| original_transcript | json                       | YES    |         |          |              |
| insight_ia          | mediumtext                 | YES    |         |          |              |
| evaluation_ia       | text                       | YES    |         |          |              |
| date                | date                       | YES    |         |          |              |
| time                | time                       | YES    |         |          |              |
| school_id           | bigint unsigned            | NO     | MUL     |          |              |
| created_at          | timestamp                  | NO     |         |          |              |
| origin              | enum('receptive','active') | YES    |         |          |              |
| agent               | varchar(255)               | YES    |         |          |              |
| duration            | int                        | YES    |         |          |              |
| phone               | varchar(255)               | YES    |         |          |              |
| type                | varchar(255)               | YES    |         |          |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna         | referencia     |
|:---------------|:---------------|
| opportunity_id | interesteds.id |
| school_id      | schools.id     |

## Referenciada por (outra tabela → esta)

| origem                                      | coluna   |
|:--------------------------------------------|:---------|
| transcription_ai_summaries.transcription_id | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                         | colunas        |   unico |
|:-----------------------------------------------|:---------------|--------:|
| opportunity_transcripts_opportunity_id_foreign | opportunity_id |       0 |
| opportunity_transcripts_school_id_foreign      | school_id      |       0 |
| opportunity_transcripts_uuid_unique            | uuid           |       1 |
| PRIMARY                                        | id             |       1 |
