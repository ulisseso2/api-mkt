# `interested_pontuations`

Linhas (estimativa do information_schema): **~41.355**

> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.

## Colunas

| coluna             | tipo                  | nulo   | chave   |   padrao | comentario   |
|:-------------------|:----------------------|:-------|:--------|---------:|:-------------|
| id                 | bigint unsigned       | NO     | PRI     |      nan |              |
| uuid               | char(36)              | NO     |         |      nan |              |
| interested_id      | bigint unsigned       | NO     | MUL     |      nan |              |
| school_id          | bigint unsigned       | NO     |         |      nan |              |
| p1_answer          | varchar(255)          | YES    |         |      nan |              |
| p1_score           | int unsigned          | NO     |         |        0 |              |
| p2_answer          | varchar(255)          | YES    |         |      nan |              |
| p2_score           | int unsigned          | NO     |         |        0 |              |
| total_score        | int unsigned          | NO     |         |        0 |              |
| tier               | enum('A','B','C','D') | YES    |         |      nan |              |
| conversion_sent    | tinyint               | NO     |         |        0 |              |
| conversion_value   | int unsigned          | YES    |         |      nan |              |
| octadesk_chat_id   | varchar(150)          | YES    |         |      nan |              |
| created_at         | timestamp             | NO     |         |      nan |              |
| updated_at         | timestamp             | NO     |         |      nan |              |
| conversion_sent_at | timestamp             | YES    |         |      nan |              |
| p2_answered_at     | timestamp             | YES    |         |      nan |              |
| p2_timed_out_at    | timestamp             | YES    | MUL     |      nan |              |
| send_status        | varchar(24)           | YES    | MUL     |      nan |              |
| delivery_status    | varchar(24)           | YES    | MUL     |      nan |              |
| delivery_detail    | varchar(120)          | YES    |         |      nan |              |
| delivered_at       | timestamp             | YES    |         |      nan |              |

## Chaves estrangeiras (esta tabela → outra)

| coluna        | referencia     |
|:--------------|:---------------|
| interested_id | interesteds.id |

## Referenciada por (outra tabela → esta)

_(vazio)_

## Índices (filtre/junte preferencialmente por colunas indexadas)

| indice                                       | colunas                                    |   unico |
|:---------------------------------------------|:-------------------------------------------|--------:|
| idx_ip_delivery_status                       | delivery_status                            |       0 |
| idx_ip_p2_timeout                            | p2_timed_out_at,conversion_sent,created_at |       0 |
| idx_ip_send_status                           | send_status                                |       0 |
| interested_pontuations_interested_id_foreign | interested_id                              |       0 |
| PRIMARY                                      | id                                         |       1 |
