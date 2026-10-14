# `opportunity_modalities`

Linhas (estimativa do information_schema): **~6**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna     | tipo            | nulo   | chave   |   padrao | comentario   |
|:-----------|:----------------|:-------|:--------|---------:|:-------------|
| id         | bigint unsigned | NO     | PRI     |      nan |              |
| uuid       | char(36)        | NO     | UNI     |      nan |              |
| name       | varchar(255)    | NO     |         |      nan |              |
| user_id    | bigint unsigned | NO     | MUL     |      nan |              |
| school_id  | bigint unsigned | NO     | MUL     |      nan |              |
| sort       | int             | NO     |         |      nan |              |
| active     | tinyint(1)      | NO     |         |        1 |              |
| created_at | timestamp       | YES    |         |      nan |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna    | referencia   |
|:----------|:-------------|
| school_id | schools.id   |
| user_id   | users.id     |

## Referenciada por (outra tabela → esta)

| origem                                         | coluna   |
|:-----------------------------------------------|:---------|
| interesteds.opportunity_modality_id            | id       |
| school_team_modalities.opportunity_modality_id | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                   | colunas   |   unico |
|:-----------------------------------------|:----------|--------:|
| opportunity_modalities_school_id_foreign | school_id |       0 |
| opportunity_modalities_user_id_foreign   | user_id   |       0 |
| opportunity_modalities_uuid_unique       | uuid      |       1 |
| PRIMARY                                  | id        |       1 |
