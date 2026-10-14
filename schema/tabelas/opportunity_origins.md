# `opportunity_origins`

Linhas (estimativa do information_schema): **~14**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna     | tipo            | nulo   | chave   | padrao   | comentario   |
|:-----------|:----------------|:-------|:--------|:---------|:-------------|
| id         | bigint unsigned | NO     | PRI     |          |              |
| uuid       | char(36)        | NO     | UNI     |          |              |
| name       | varchar(255)    | NO     |         |          |              |
| created_at | timestamp       | YES    |         |          |              |

## Chaves estrangeiras (esta tabela → outra)

_(vazio)_

## Referenciada por (outra tabela → esta)

| origem                            | coluna   |
|:----------------------------------|:---------|
| interesteds.opportunity_origin_id | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                          | colunas   |   unico |
|:--------------------------------|:----------|--------:|
| opportunity_origins_uuid_unique | uuid      |       1 |
| PRIMARY                         | id        |       1 |
