# `preleads`

Linhas (estimativa do information_schema): **~6.113**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna       | tipo            | nulo   | chave   | padrao            | comentario   |
|:-------------|:----------------|:-------|:--------|:------------------|:-------------|
| id           | bigint unsigned | NO     | PRI     | nan               |              |
| uuid         | char(36)        | NO     |         | [object Object]   |              |
| school_id    | bigint unsigned | NO     | MUL     | nan               |              |
| cellphone    | varchar(20)     | YES    |         | nan               |              |
| page_url     | varchar(512)    | YES    |         | nan               |              |
| utm_source   | varchar(128)    | YES    |         | nan               |              |
| utm_medium   | varchar(128)    | YES    |         | nan               |              |
| utm_campaign | varchar(128)    | YES    |         | nan               |              |
| utm_term     | varchar(128)    | YES    |         | nan               |              |
| utm_content  | varchar(128)    | YES    |         | nan               |              |
| created_at   | timestamp       | YES    |         | CURRENT_TIMESTAMP |              |
| updated_at   | timestamp       | YES    |         | CURRENT_TIMESTAMP |              |

## Chaves estrangeiras (esta tabela → outra)

_(vazio)_

## Referenciada por (outra tabela → esta)

_(vazio)_

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                   | colunas   |   unico |
|:-------------------------|:----------|--------:|
| preleads_school_id_index | school_id |       0 |
| PRIMARY                  | id        |       1 |
