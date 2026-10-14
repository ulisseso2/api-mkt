# `interested_pontuations_answers`

Linhas (estimativa do information_schema): **~16**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna          | tipo            | nulo   | chave   | padrao   | comentario   |
|:----------------|:----------------|:-------|:--------|:---------|:-------------|
| id              | bigint unsigned | NO     | PRI     |          |              |
| uuid            | char(36)        | NO     | UNI     |          |              |
| question        | int             | NO     |         |          |              |
| question_number | int             | NO     |         |          |              |
| text            | varchar(255)    | NO     |         |          |              |
| school_id       | bigint unsigned | YES    | MUL     |          |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna    | referencia   |
|:----------|:-------------|
| school_id | schools.id   |

## Referenciada por (outra tabela → esta)

_(vazio)_

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                           | colunas   |   unico |
|:-------------------------------------------------|:----------|--------:|
| interested_pontuations_answers_school_id_foreign | school_id |       0 |
| interested_pontuations_answers_uuid_unique       | uuid      |       1 |
| PRIMARY                                          | id        |       1 |
