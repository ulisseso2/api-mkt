# api-mkt

Análises de marketing (leads, pontuação do bot, vendas) direto no banco do CRM Seducar,
feitas pelo Claude Code em linguagem natural.

## Como usar

1. Abra esta pasta no Claude Code (terminal: `cd api-mkt && claude`, ou pelo VS Code).
2. Peça o que precisa em português, por exemplo:
   - "Quantos leads cada campanha do Google trouxe em setembro na Degrau?"
   - "Qual a taxa de venda dos leads tier A comparada com tier D no último mês?"
   - "Gera uma planilha com as vendas pagas de 01/10 até ontem, das duas marcas."
   - "Quais origens de lead mais viraram venda nos últimos 30 dias?"
3. As planilhas geradas ficam na pasta `saidas/`.

Na primeira vez, o Claude instala as dependências sozinho. Você só precisa do arquivo `.env`
(credenciais do banco), que o Ulisses envia separadamente. Não compartilhe esse arquivo.

## O que tem aqui

- `CLAUDE.md`: instruções e regras de negócio que o Claude segue.
- `q.py`: executor de consultas **somente leitura** (bloqueia qualquer alteração no banco).
- `consultas/`: consultas prontas e testadas.
- `schema/`: documentação das tabelas, gerada do banco real.
- `saidas/`: planilhas exportadas.

O acesso ao banco é somente leitura. Mesmo assim, o banco é o de produção do CRM, então
prefira análises de períodos de até alguns meses.
