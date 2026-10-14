# `opportunity_steps`

Linhas (estimativa do information_schema): **~26**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna                      | tipo            | nulo   | chave   |   padrao | comentario   |
|:----------------------------|:----------------|:-------|:--------|---------:|:-------------|
| id                          | bigint unsigned | NO     | PRI     |      nan |              |
| uuid                        | char(36)        | NO     | UNI     |      nan |              |
| name                        | varchar(255)    | NO     |         |      nan |              |
| sort                        | int             | NO     |         |      nan |              |
| active                      | tinyint(1)      | NO     |         |      nan |              |
| template_email_code         | varchar(255)    | YES    |         |      nan |              |
| school_octadesk_template_id | bigint unsigned | YES    | MUL     |      nan |              |
| school_id                   | bigint unsigned | NO     | MUL     |      nan |              |
| created_at                  | timestamp       | YES    |         |      nan |              |
| modalities                  | json            | YES    |         |      nan |              |
| weekday_schedule            | varchar(255)    | YES    |         |      nan |              |
| weekend_schedule            | varchar(255)    | YES    |         |      nan |              |
| amber_after_hours           | int unsigned    | YES    |         |      nan |              |
| red_after_hours             | int unsigned    | YES    |         |      nan |              |
| is_terminal                 | tinyint(1)      | NO     |         |        0 |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna                      | referencia                   |
|:----------------------------|:-----------------------------|
| school_id                   | schools.id                   |
| school_octadesk_template_id | school_octadesk_templates.id |

## Referenciada por (outra tabela → esta)

| origem                                             | coluna   |
|:---------------------------------------------------|:---------|
| interesteds.opportunity_step_id                    | id       |
| opportunity_step_esteira_rules.opportunity_step_id | id       |
| opportunity_step_esteira_rules.target_step_id      | id       |

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                                | colunas                     |   unico |
|:------------------------------------------------------|:----------------------------|--------:|
| opportunity_steps_school_id_foreign                   | school_id                   |       0 |
| opportunity_steps_school_octadesk_template_id_foreign | school_octadesk_template_id |       0 |
| opportunity_steps_uuid_unique                         | uuid                        |       1 |
| PRIMARY                                               | id                          |       1 |
