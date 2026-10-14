# Tabelas de domínio (valores id → nome)

> Gerado por `scripts/gerar_schema.py`. Use estes ids em filtros e CASEs.

## `schools`

|   id | company_name         | trading_name                 | document           | domain                            | background   | sales_force_oid   | sales_force_record_type   |
|-----:|:---------------------|:-----------------------------|:-------------------|:----------------------------------|:-------------|:------------------|:--------------------------|
|    1 | Degrau Cultural      | Editora Degrau Cultural      | 28.060.747/0001-54 | degraucultural.com.br             | #009c73      | 00D5f000006qsAK   | 0125f000000ZvUO           |
|    2 | Central de Concursos | Editora Central de Concursos | 61.632.659/0001-55 | centraldeconcursos.com.br         | #031af5      | 00D5f000006qsAK   | 0125f000000ZvUN           |
|    3 | Degrau Cultural      |                              | 28.060.747/0001-54 | homolog.degraucultural.com.br     | nan          | nan               | nan                       |
|    4 | Central de Concursos |                              | 61.632.659/0001-55 | homolog.centraldeconcursos.com.br | nan          | nan               | nan                       |
|    5 | Vercel - Development |                              | 61.632.659/0001-55 | front-site-liard.vercel.app       | nan          | nan               | nan                       |

## `opportunity_steps`

|   id | name                      |   sort |   active | template_email_code   |   school_octadesk_template_id |   school_id | modalities                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|-----:|:--------------------------|-------:|---------:|:----------------------|------------------------------:|------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|    1 | Contato urgente           |      0 |        1 |                       |                            56 |           1 | [{"modality": "c41d8e83-b3a5-4ff2-b15f-4e1ffc897363", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 56}, {"modality": "1141844f-836b-4713-a1bf-b57baaf16fef", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 56}]                                                                                                                                                                                            |
|   13 | Contato urgente           |      0 |        1 |                       |                            55 |           2 | [{"modality": "ed2ad9d7-b6c8-4e10-9441-8c63649e22c2", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 55}, {"modality": "d1a8c295-8525-41e4-824e-0cdaf84a4f54", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 55}]                                                                                                                                                                                            |
|    2 | 2ª Tentativa de conexão   |      1 |        1 |                       |                           nan |           1 | [{"modality": "1141844f-836b-4713-a1bf-b57baaf16fef", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 33}, {"modality": "c41d8e83-b3a5-4ff2-b15f-4e1ffc897363", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 33}, {"modality": "b40abacd-9604-47e2-9cd9-11d9a223ccdf", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 33}] |
|   37 | 2ª Tentativa de Conexão   |      1 |        1 |                       |                           nan |           2 | [{"modality": "ed2ad9d7-b6c8-4e10-9441-8c63649e22c2", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 23}, {"modality": "d1a8c295-8525-41e4-824e-0cdaf84a4f54", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 23}]                                                                                                                                                                                            |
|    4 | 3ª tentativa de conexão   |      2 |        1 |                       |                           nan |           1 | [{"modality": "1141844f-836b-4713-a1bf-b57baaf16fef", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 37}, {"modality": "c41d8e83-b3a5-4ff2-b15f-4e1ffc897363", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 37}, {"modality": "b40abacd-9604-47e2-9cd9-11d9a223ccdf", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 37}] |
|   24 | 3ª Tentativa de Conexão   |      2 |        1 |                       |                           nan |           2 | [{"modality": "ed2ad9d7-b6c8-4e10-9441-8c63649e22c2", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 41}, {"modality": "d1a8c295-8525-41e4-824e-0cdaf84a4f54", "sundaySchedule": "00:01 - 23:59", "weekdaySchedule": "00:01 - 23:59", "weekendSchedule": "00:01 - 23:59", "templateOctadeskId": 41}]                                                                                                                                                                                            |
|   14 | Conectado                 |      3 |        1 |                       |                           nan |           1 | nan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|   25 | Conectado                 |      3 |        1 |                       |                           nan |           2 | nan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|    8 | Proposta enviada          |      4 |        1 |                       |                           nan |           1 | nan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|   26 | Qualificação              |      4 |        1 |                       |                           nan |           2 | nan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|    9 | 2ª tentativa de proposta  |      5 |        1 |                       |                           nan |           1 | [{"modality": "c41d8e83-b3a5-4ff2-b15f-4e1ffc897363", "sundaySchedule": "10:00 - 23:59", "weekdaySchedule": "09:00 - 19:30", "weekendSchedule": "09:00 - 14:00", "templateOctadeskId": 22}, {"modality": "1141844f-836b-4713-a1bf-b57baaf16fef", "sundaySchedule": "10:00 - 23:59", "weekdaySchedule": "09:00 - 19:30", "weekendSchedule": "09:00 - 14:00", "templateOctadeskId": 22}, {"modality": "b40abacd-9604-47e2-9cd9-11d9a223ccdf", "sundaySchedule": "10:00 - 23:59", "weekdaySchedule": "09:00 - 19:30", "weekendSchedule": "09:00 - 14:00", "templateOctadeskId": 22}] |
|   31 | Fup 1                     |      5 |        1 |                       |                           nan |           2 | nan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|   40 | Upsell Passaport          |      6 |        1 |                       |                           nan |           1 | []                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|   52 | Fup 2                     |      6 |        1 |                       |                           nan |           2 | []                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|   50 | Upsell - Negociando       |      7 |        1 |                       |                           nan |           1 | []                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|   53 | Fup 3                     |      7 |        1 |                       |                           nan |           2 | []                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|   51 | Upsell - Proposta enviada |      8 |        1 |                       |                           nan |           1 | []                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|   54 | Negociação                |      8 |        1 |                       |                           nan |           2 | []                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|   10 | Encerrado                 |      9 |        1 |                       |                           nan |           1 | nan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|   28 | Link enviado              |      9 |        1 |                       |                           nan |           2 | nan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|   11 | Perdido                   |     10 |        0 |                       |                           nan |           1 | nan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|   41 | Upsell Passaport          |     10 |        0 |                       |                           nan |           2 | []                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|   12 | Vendido                   |     11 |        0 |                       |                           nan |           1 | nan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|   33 | Encerrado                 |     11 |        1 |                       |                           nan |           2 | nan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|   19 | Perdido                   |     12 |        0 |                       |                           nan |           2 | nan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|   20 | Vendido                   |     13 |        0 |                       |                           nan |           2 | nan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

## `opportunity_origins`

|   id | name                 |
|-----:|:---------------------|
|    1 | Busca Orgânica       |
|    2 | Chat                 |
|    3 | Google AdWords       |
|    4 | Marketing            |
|    5 | Outros               |
|    6 | Receptivo telefônico |
|    7 | Site                 |
|    8 | WhatsApp             |
|    9 | Receptivo presencial |
|   10 | Whats sem URA        |
|   11 | Instagram            |
|   13 | Whatsapp Site        |
|   14 | Upsell Passaport     |
|   15 | Area do Aluno        |

## `opportunity_modalities`

|   id | name       |   user_id |   school_id |   sort |   active |
|-----:|:-----------|----------:|------------:|-------:|---------:|
|    1 | Presencial |        38 |           1 |      1 |        1 |
|    4 | Presencial |        38 |           2 |      1 |        1 |
|    2 | Online     |        38 |           1 |      2 |        1 |
|    5 | Online     |        38 |           2 |      2 |        1 |
|    3 | Live       |        38 |           1 |      3 |        1 |
|    6 | Live       |        38 |           2 |      3 |        1 |

## `opportunity_statuses`

|   id | slug         | name                    |   active |
|-----:|:-------------|:------------------------|---------:|
|    1 | normal       | Normal                  |        1 |
|    2 | multiplicity | Multiplicidade de Venda |        1 |

## `order_status`

|   id | name                 | code             | color   |
|-----:|:---------------------|:-----------------|:--------|
|    1 | Pendente             | pending          | #00cfe8 |
|    2 | Pago                 | paid             | #28c76f |
|    3 | Cancelado            | canceled         | #ea5455 |
|    4 | Processando          | processing       | #0875d6 |
|    5 | Revisão de Fraude    | review_fraud     | #ea5455 |
|    6 | Aguardando Pagamento | waiting          | #0875d6 |
|    7 | Sucesso              | success          | #28c76f |
|    8 | Rejeitado            | rejected         | #ea5455 |
|    9 | Linha de Crédito     | credit-line      | #0875d6 |
|   10 | Expirada             | expired          | #ea5455 |
|   11 | Estorno Total        | refund           | #ea5455 |
|   12 | Inadimplente         | defaulter        | #ea5455 |
|   13 | Pendente de desconto | pending-discount | #00cfe8 |
|   14 | Trancada             | locked           | #ea5455 |
|   15 | Em cancelamento      | canceling        | #0875d6 |
|   16 | Inativo              | inactive         | #ea5455 |
|   17 | Inválido             | invalid          | #ea5455 |
|   18 | Finalizada           | finished         | #ea5455 |
|   19 | Transferida          | transfered       | #ea5455 |
|   20 | Agendada             | scheduled        | #00cfe8 |
|   21 | Estorno Parcial      | refund_partial   | #ea5455 |

## `payment_methods`

|   id | name              | code         | icon                    |   conventional |
|-----:|:------------------|:-------------|:------------------------|---------------:|
|    1 | Cartão de Crédito | card_credit  | bi-credit-card-2-front  |              1 |
|    2 | Boleto            | bank_slip    | bi-upc-scan             |              1 |
|    3 | Pix               | pix          | bi-qr-code              |              1 |
|    4 | Migração          | migracao     | bi-arrow-down-up        |              0 |
|    5 | Cortesia          | cortesia     | bi-gift                 |              0 |
|    6 | Unidade           | unit         | bi-building             |              0 |
|    7 | Cartão de Débito  | card_debit   | bi-credit-card-2-front  |              1 |
|    8 | Carta de Crédito  | letter       | bi-file-earmark-medical |              0 |
|    9 | Cheque            | check        | bi-card-text            |              0 |
|   10 | Dinheiro          | money        | bi-cash                 |              0 |
|   11 | Princípia         | principia    | bi-flag                 |              0 |
|   12 | Ciclo             | cycle        | bi-arrow-clockwise      |              0 |
|   13 | Experimental      | experimental | bi-flask                |              0 |
|   14 | Bônus             | bonus        | bi-gift                 |              0 |
|   15 | Wazapi            | wazapi       | bi-whatsapp             |              0 |

## `product_categories`

|   id | name             | initials   |   active | slug               | color   | icon   |
|-----:|:-----------------|:-----------|---------:|:-------------------|:--------|:-------|
|    1 | Curso Presencial | CP         |        1 | cursos/presenciais |         |        |
|    2 | Curso Online     | CO         |        1 | cursos/online      |         |        |
|    3 | Curso Live       | CL         |        1 | cursos/lives       |         |        |
|    4 | Curso Rápido     | CR         |        1 | cursos/rapidos     |         |        |
|    5 | Curso Grátis     | CG         |        1 | cursos/gratis      |         |        |
|    6 | Apostila         | AP         |        1 | apostilas          |         |        |
|    7 | Passaporte       | PS         |        1 | passaporte         |         |        |
|    8 | Questões         | Q          |        1 | questoes           |         |        |
|    9 | Combo Questões   | CQ         |        1 | maisquestoes       |         |        |
|   10 | Smart            | SM         |        1 | jornada            |         |        |
|   11 | Trilha           | TRI        |        1 | trilha             |         |        |

## `units`

|   id | name            | email                                 | phone_1         | phone_2   | address                   | neighborhood   | complement   |
|-----:|:----------------|:--------------------------------------|:----------------|:----------|:--------------------------|:---------------|:-------------|
|    2 | Centro          | faleconosco@degrauculcural.com.br     | (21) 3970-1015  | (         | R. da Alfândega           | Centro         | - 2º Andar   |
|    3 | Madureira       | faleconosco@degraucultural.com.br     | (21) 3970-1015  | null      | Rua Américo Brasiliense   | Madureira      | null         |
|    4 | Campo Grande    | faleconosco@degraucultural.com.br     | (21) 3970-1015  | null      | Avenida Cesário de Melo   | Campo Grande   | null         |
|    5 | Niterói         | faleconosco@degraucultural.com.br     | (21) 3970-1015  | null      | Rua São Pedro             | Centro         | Sobreloja    |
|    6 | Taquara         | faleconosco@degraucultural.com.br     | (21) 3970-1015  | (         | Estrada do Tindiba        | Taquara        | 2º andar     |
|   10 | Metrô República | faleconosco@centraldeconcursos.com.br | (11) 3017-8800  | (         | Rua Barão de Itapetininga | República      | 6º andar     |
|   12 | Santo Amaro     | faleconosco@centraldeconcursos.com.br | (11) 3017-8800  | (         | Avenida Adolfo Pinheiro   | Santo Amaro    | null         |
|   13 | ABC             | faleconosco@centraldeconcursos.com.br | (11) 3017-8800  | nan       | Avenida José Caballero    | Vila Bastos    | nan          |
|   14 | Bonsucesso      | faleconosco@degrauculcural.com.br     | (21) 3970-1015  | null      | R. Dona Isabel            | Bonsucesso     | null         |
|   15 | Copacabana      | faleconosco@degrauculcural.com.br     | (21) 3970-1015  | null      | R. Dona Isabel            | Bonsucesso     | null         |
|   16 | Rio Branco      | faleconosco@degrauculcural.com.br     | (21) 3970-1015  | null      | R. Dona Isabel            | Bonsucesso     | null         |
|   17 | Meier           | faleconosco@degrauculcural.com.br     | (21) 3970-1015  | null      | R. Dona Isabel            | Bonsucesso     | null         |
|   18 | Caxias          | faleconosco@degrauculcural.com.br     | (21) 3970-1015  | null      | R. Dona Isabel            | Bonsucesso     | null         |
|   19 | Alcântara       | faleconosco@degrauculcural.com.br     | (21) 3970-1015  | null      | R. Dona Isabel            | Bonsucesso     | null         |
|   20 | Nova Iguaçu     | faleconosco@degrauculcural.com.br     | (21) 3970-1015  | null      | R. Dona Isabel            | Bonsucesso     | null         |
|   21 | Guarulhos       | guarulhos@guarulhos.com               | (11) 11111-1111 | nan       | Rua da Alfândega          | Centro         | nan          |
|   22 | Live            | igor.velazquez@degraucultural.com.br  | (21) 3970-1015  | (         | Rua da Alfândega          | Centro         | sobre loja   |
|   23 | EAD             | igor.velazquez@degraucultural.com.br  | (21) 3970-1015  | nan       | Rua da Alfândega          | Centro         | sobreloja    |
|   24 | Live            | igor.velazquez@degraucultural.com.br  | (11) 3017-8800  | nan       | Rua da Alfândega          | Centro         | nan          |
|   25 | EAD             | igor.velazquez@degraucultural.com.br  | (11) 3017-8800  | null      | Rua da Alfândega          | Centro         | null         |
|   26 | Smart           | ulisses@maisquestoes.com.br           | (21) 3970-1015  | (         | Rua da Alfândega          | Centro         | null         |
|   27 | Smart           | ulisses@maisquestoes.com.br           | (21) 9648-5080  | nan       | Rua da Alfândega          | Centro         | nan          |

## `shifts`

|   id | name           |   school_id |   sort |
|-----:|:---------------|------------:|-------:|
|    1 | Manhã          |           2 |      1 |
|    5 | Manhã          |           1 |      1 |
|    2 | Tarde          |           2 |      2 |
|    8 | Tarde          |           1 |      2 |
|    3 | Noite          |           2 |      3 |
|    7 | Noite          |           1 |      3 |
|    4 | Fins de Semana |           2 |      4 |
|    6 | Fins de Semana |           1 |      4 |

## `time_to_calls`

|   id | name               |   school_id |   active |
|-----:|:-------------------|------------:|---------:|
|    1 | Manhã (08h às 12h) |           2 |        1 |
|    2 | Tarde (12h às 17h) |           2 |        1 |
|    3 | Noite (17h às 21h) |           2 |        1 |
|    4 | Agora              |           2 |        0 |
|    5 | Agora              |           1 |        0 |
|    6 | Manhã (08h às 12h) |           1 |        1 |
|    7 | Noite (17h às 21h) |           1 |        1 |
|    8 | Tarde (12h às 17h) |           1 |        1 |

## `areas`

|   id | name                      |   active |   school_id | slug                      |   display_blog_home |   sort_blog_home |   layout_blog_home |
|-----:|:--------------------------|---------:|------------:|:--------------------------|--------------------:|-----------------:|-------------------:|
|    6 | Jurídica                  |        1 |           2 | juridica                  |                   0 |                3 |                  1 |
|    7 | Segurança                 |        1 |           2 | seguranca                 |                   1 |                2 |                  2 |
|    8 | Saúde                     |        1 |           2 | saude                     |                 nan |                6 |                nan |
|    9 | Administrativa            |        1 |           2 | administrativa            |                   1 |                0 |                  2 |
|   10 | Educação                  |        1 |           2 | educacao                  |                 nan |                5 |                nan |
|   11 | Fiscal                    |        1 |           2 | fiscal                    |                 nan |                4 |                nan |
|   12 | Bancária                  |        1 |           2 | bancaria                  |                   1 |                1 |                  2 |
|   13 | Administrativa            |        1 |           1 | administrativa            |                   1 |                4 |                  2 |
|   14 | Bancária                  |        1 |           1 | bancaria                  |                   1 |               11 |                  2 |
|   15 | Educação                  |        1 |           1 | educacao                  |                 nan |               12 |                nan |
|   16 | Fiscal                    |        1 |           1 | fiscal                    |                 nan |               13 |                nan |
|   17 | Jurídica                  |        1 |           1 | juridica                  |                 nan |               10 |                nan |
|   18 | Saúde                     |        1 |           1 | saude                     |                 nan |               14 |                nan |
|   19 | Segurança                 |        1 |           1 | seguranca                 |                   1 |                8 |                  1 |
|   20 | Tribunais                 |        1 |           1 | tribunais                 |                 nan |                9 |                nan |
|   21 | Militar                   |        1 |           1 | militar                   |                 nan |               15 |                nan |
|   22 | Dicas                     |        1 |           2 | dicas                     |                 nan |              nan |                nan |
|   23 | Prefeituras               |        1 |           2 | prefeituras               |                 nan |              nan |                nan |
|   24 | Tribunais                 |        1 |           2 | tribunais                 |                 nan |              nan |                nan |
|   25 | Prefeitura                |        1 |           1 | prefeituras               |                 nan |               16 |                nan |
|   26 | Dicas                     |        1 |           1 | dicas                     |                 nan |               17 |                nan |
|   27 | Limpeza                   |        1 |           1 | limpeza                   |                 nan |                0 |                nan |
|   28 | CNU                       |        1 |           1 | cnu                       |                 nan |                6 |                nan |
|   29 | Passaporte para Aprovação |        1 |           1 | passaporte-para-aprovacao |                 nan |                3 |                nan |
|   30 | Eventos                   |        1 |           1 | eventos                   |                 nan |                7 |                nan |
|   31 | Passaporte da Aprovação   |        1 |           2 | passaporte-da-aprovacao   |                 nan |              nan |                nan |
|   32 | CNU                       |        1 |           2 | cnu                       |                 nan |              nan |                nan |
|   33 | Jornada                   |        1 |           1 | jornada-da-aprovacao      |                 nan |                5 |                nan |
|   34 | Jornada                   |        1 |           2 | jornada-da-aprovacao      |                 nan |              nan |                nan |
|   35 | Trilha                    |        1 |           1 | trilha-do-aluno           |                 nan |                1 |                nan |
|   36 | Trilha                    |        1 |           2 | trilha-do-aluno           |                 nan |              nan |                nan |
|   37 | Tecnologia                |        1 |           2 | tecnologia                |                 nan |              nan |                nan |
|   38 | Tecnologia                |        1 |           1 | tecnologia                |                 nan |                2 |                nan |

## `reason_for_losses`

|   id | name                                           |   school_id |
|-----:|:-----------------------------------------------|------------:|
|    1 | Abandonado pelo Time                           |           1 |
|    2 | Achou que era Grátis                           |           1 |
|    4 | Comprou na concorrência (EAD)                  |           1 |
|    5 | Comprou na concorrência (Presencial)           |           1 |
|    6 | Sem Contato                                    |           1 |
|    7 | Comprou no Agora eu Passo                      |           1 |
|    8 | Comprou no Alfacon                             |           1 |
|    9 | Comprou no Cejuris                             |           1 |
|   10 | Comprou no Estratégia                          |           1 |
|   11 | Comprou no Gran                                |           1 |
|   12 | Comprou no Progressão                          |           1 |
|   13 | Desempregado                                   |           1 |
|   14 | Desistiu de estudar agora                      |           1 |
|   15 | Duplicidade                                    |           1 |
|   16 | Duplicidade - vendido                          |           1 |
|   17 | Interesse exclusivo em Online                  |           1 |
|   18 | Não consegue assistir na hora da live          |           1 |
|   19 | Não consegue estar na hora da aula             |           1 |
|   20 | Não se inscreveu no concurso                   |           1 |
|   21 | Não tem cartão, nem cheque                     |           1 |
|   22 | Não tem dinheiro                               |           1 |
|   23 | Não tem forma de pagamento                     |           1 |
|   24 | Não tem interesse                              |           1 |
|   25 | Não tem limite                                 |           1 |
|   26 | Não tem tempo                                  |           1 |
|   27 | Não temos o Curso desse Concurso               |           1 |
|   28 | Nível fundamental                              |           1 |
|   29 | Nunca conseguimos contato                      |           1 |
|   30 | Outro                                          |           1 |
|   31 | Preço, achou o concorrente mais barato         |           1 |
|   32 | Preço, achou o nosso caro                      |           1 |
|   33 | Problemas de saúde                             |           1 |
|   34 | Resiliência - duplicidade                      |           1 |
|   35 | Interesse futuro                               |           1 |
|   36 | Telefone inexistente                           |           1 |
|   37 | Tem cartão, mas não tem limite                 |           1 |
|   38 | Multiplicidade de vendido                      |           1 |
|   40 | Achou que era Grátis                           |           2 |
|   41 | Abandonado pelo Time                           |           2 |
|   42 | Comprou na concorrência (EAD)                  |           2 |
|   43 | Comprou na concorrência (Presencial)           |           2 |
|   44 | Desempregado                                   |           2 |
|   45 | Desistiu de estudar agora                      |           2 |
|   46 | Duplicidade                                    |           2 |
|   47 | Duplicidade - vendido                          |           2 |
|   48 | Interesse exclusivo em Online                  |           2 |
|   49 | Indisponibilidade de horário                   |           2 |
|   50 | Não se inscreveu no concurso                   |           2 |
|   51 | Não tem forma de pagamento                     |           2 |
|   52 | Não tem interesse                              |           2 |
|   53 | Não tem tempo                                  |           2 |
|   54 | Não temos o Curso desse Concurso               |           2 |
|   55 | Cadastro inconsistente                         |           2 |
|   56 | Nunca interagiu                                |           2 |
|   57 | Interagiu e parou                              |           2 |
|   58 | Preço, achou o concorrente mais barato         |           2 |
|   59 | Preço, achou o nosso caro                      |           2 |
|   60 | Problemas de saúde                             |           2 |
|   62 | Outro                                          |           2 |
|   63 | Multiplicidade de vendido                      |           2 |
|   64 | Respondeu ao Bot, mas não interagiu com humano |           2 |

## `order_cancelation_types`

|   id | name                         |   fine |
|-----:|:-----------------------------|-------:|
|    1 | Dentro do Prazo              |     10 |
|    2 | Fora do Prazo                |     30 |
|    3 | Turma Cancelada              |      0 |
|    4 | Devolução Proporcional       |      0 |
|    5 | Migração Passaporte          |      0 |
|    6 | Alteração no inicio da turma |      0 |
