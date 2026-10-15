# Instalação no Claude Desktop: conector api-mkt + skill de análise

> **Para o Claude Code:** este arquivo é um roteiro para você executar junto com a usuária.
> Ela trabalha com marketing e **não tem perfil técnico**. Faça você tudo o que for terminal.
> Para o que for clique na interface do Claude Desktop (que você não controla), dê **um passo
> por vez**, em linguagem simples, e espere ela confirmar antes de seguir. Não mostre
> comandos nem saídas técnicas sem necessidade. Diga só o que ela precisa fazer ou saber.

O resultado final é ela abrir o Claude Desktop e perguntar coisas como *"quantos leads o Google
trouxe em setembro na Degrau?"*, com o Claude consultando o banco do CRM (somente leitura) e
seguindo as regras de negócio da skill.

São duas peças:

| Peça | O que é | Onde fica |
|---|---|---|
| **Conector `api-mkt`** | dá acesso ao banco (somente leitura) | servidor no Render. Ela só cola uma URL |
| **Skill `analise-marketing-seducar`** | ensina as regras de negócio e como apresentar análises | arquivo `skill/analise-marketing-seducar.zip` deste repositório |

---

## Antes de começar: confira com ela

1. **Claude Desktop instalado e logado.** Se não tiver, oriente a baixar em https://claude.ai/download.
2. **A URL do conector**, enviada pelo Ulisses por mensagem. Tem o formato
   `https://....onrender.com/mcp/<código-longo>`.
   - Essa URL **é uma senha**. Não a escreva em arquivos, não faça commit e não a repita na
     conversa além do necessário. Se ela colar a URL no chat, tudo bem usar, mas não guarde.
   - Se ela não tiver a URL, pare aqui e peça que solicite ao Ulisses.
3. **Plano do Claude:** conectores personalizados exigem plano pago (Pro, Max, Team ou Enterprise).
   Em Team/Enterprise, talvez só o administrador da organização possa adicionar conectores.
   Se a opção não aparecer para ela, é esse o motivo: oriente a falar com o administrador.

---

## Parte 1: baixar a skill

Você (Claude Code) faz isso. O repositório é privado, e ela foi adicionada como colaboradora.

1. Se a pasta do projeto ainda não existir na máquina, clone:
   ```bash
   git clone https://github.com/ulisseso2/api-mkt.git ~/api-mkt
   ```
   - Se pedir login: com `gh` instalado, peça para ela rodar `! gh auth login` aqui no prompt
     (GitHub.com → HTTPS → login pelo navegador) e tente de novo. No Windows, o Git Credential
     Manager costuma abrir o navegador sozinho.
   - Se der "Repository not found", o convite de colaboradora ainda não foi aceito. Peça para ela
     abrir o e-mail do GitHub ou https://github.com/ulisseso2/api-mkt/invitations e aceitar.
   - Já existe? Atualize com `git -C ~/api-mkt pull`.
2. Copie o zip para um lugar fácil de achar e diga a ela onde está:
   - macOS/Linux: `cp ~/api-mkt/skill/analise-marketing-seducar.zip ~/Downloads/`
   - Windows (PowerShell): `Copy-Item $HOME\api-mkt\skill\analise-marketing-seducar.zip $HOME\Downloads\`

   **Não descompacte**: o Claude Desktop recebe o `.zip` como está.

---

## Parte 2: adicionar o conector (ela faz, você guia)

Guie um passo por vez. Os nomes de menu podem variar um pouco entre versões. Se ela não achar,
peça que descreva o que vê na tela.

1. Abra o **Claude Desktop** → menu de perfil (canto inferior esquerdo) → **Configurações** (Settings).
2. Vá em **Conectores** (Connectors) → **Adicionar conector personalizado** (Add custom connector).
3. Preencha:
   - **Nome:** `api-mkt`
   - **URL:** a URL que o Ulisses enviou (inteira, incluindo o código depois de `/mcp/`)
   - Deixe as opções avançadas (OAuth) **em branco**.
4. Clique em **Adicionar**. O conector deve aparecer na lista, **ativado**.
5. Em uma conversa nova, no botão de ferramentas (ícone de controles, perto do campo de mensagem),
   confirme que **api-mkt** aparece e está ligado. Ao abrir, devem aparecer 6 ferramentas:
   `listar_consultas`, `rodar_consulta`, `consulta_sql`, `descrever_tabela`, `buscar_tabelas`, `ler_documentacao`.

**Se der erro ao adicionar ou o conector aparecer desconectado:**
- Confira se a URL foi colada inteira, sem espaço no fim.
- Você pode testar se o servidor está no ar sem expor a URL na conversa. Pegue só a parte antes
  de `/mcp/` (ex.: `https://api-mkt-mcp.onrender.com`) e rode `curl -s <base>/health`. A resposta
  esperada é `{"ok":true}`. Se não responder, o servidor está fora do ar: avise o Ulisses.
- Se o `/health` responde mas o conector falha, provavelmente o código da URL está errado ou foi
  trocado: peça uma URL nova ao Ulisses.

---

## Parte 3: instalar a skill (ela faz, você guia)

1. **Configurações** → **Capacidades** (Capabilities).
2. Ative **Execução de código e criação de arquivos** (Code execution and file creation).
   As skills dependem disso.
3. Na seção **Skills**, clique em **Enviar skill** (Upload skill) e escolha
   `Downloads/analise-marketing-seducar.zip`.
4. A skill **analise-marketing-seducar** deve aparecer na lista, **ativada**.

---

## Parte 4: teste final (ela faz)

Peça para ela abrir uma **conversa nova** no Claude Desktop e mandar:

> Quantos leads cada marca recebeu em setembro de 2026, e qual a taxa de venda?

O esperado: o Claude pede permissão para usar a ferramenta do **api-mkt** (ela pode clicar em
"Permitir sempre"), consulta e responde com números das duas marcas (Degrau e Central),
dizendo o período e o critério de venda usados.

Depois, um teste de planilha:

> Me gera uma planilha com as vendas pagas da Degrau de 01/10/2026 até ontem.

O esperado é um **link de download** de um arquivo `.xlsx`, válido por 24 horas.

Se responder sem consultar o banco ("não tenho acesso a esses dados"), o conector não está
ativo naquela conversa: volte à Parte 2, passo 5.

Pronto. Explique a ela, em duas linhas, que é só abrir o Claude Desktop e perguntar em português.
Planilhas chegam por link.

---

## Alternativa: MCP local (só se o conector remoto não for possível)

Use **apenas** se o Ulisses pedir, por exemplo se o plano dela não permitir conectores
personalizados. Aqui o servidor roda na máquina dela e as credenciais do banco ficam num
arquivo `.env` local.

1. **Python 3.10+ via uv** (o uv instala o Python sozinho):
   - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
2. **Ambiente do projeto** (na pasta `~/api-mkt` da Parte 1):
   ```bash
   cd ~/api-mkt && uv venv --python 3.12 .venv && uv pip install -p .venv -r requirements.txt
   ```
3. **Arquivo `.env`:** o Ulisses envia o arquivo separadamente. Peça para ela salvá-lo na pasta
   `~/api-mkt` com o nome exato `.env`.
   - Ele costuma chegar como `env`, `env.txt` ou `.env.txt` (navegadores e e-mail renomeiam).
     Localize em Downloads e mova/renomeie para `~/api-mkt/.env` **sem abrir nem mostrar o conteúdo**.
   - **Nunca** peça a senha no chat, nem imprima o `.env`.
   - Opcional: acrescente a linha `SAIDAS_DIR=~/Downloads/api-mkt` ao `.env` para as planilhas
     irem para Downloads (use `echo 'SAIDAS_DIR=~/Downloads/api-mkt' >> .env`, sem ler o arquivo).
4. **Teste o servidor:**
   - macOS/Linux: `.venv/bin/python scripts/testar_mcp.py`
   - Windows: `.venv\Scripts\python.exe scripts\testar_mcp.py`

   Precisa terminar com **TUDO OK**. Erro de conexão (`Can't connect`, `Access denied`, timeout)
   é rede ou credencial: avise que é preciso falar com o Ulisses.
5. **Registrar no Claude Desktop.** Edite o arquivo de configuração. Se ele já existir,
   **acrescente** dentro de `mcpServers` sem apagar o que houver:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

   macOS/Linux (troque `<HOME>` pelo caminho real, ex.: `/Users/maria`):
   ```json
   {
     "mcpServers": {
       "api-mkt": {
         "command": "<HOME>/api-mkt/.venv/bin/python",
         "args": ["<HOME>/api-mkt/mcp_server.py"]
       }
     }
   }
   ```
   Windows (barras normais funcionam e evitam erro de escape):
   ```json
   {
     "mcpServers": {
       "api-mkt": {
         "command": "C:/Users/<usuario>/api-mkt/.venv/Scripts/python.exe",
         "args": ["C:/Users/<usuario>/api-mkt/mcp_server.py"]
       }
     }
   }
   ```
   Valide o JSON depois de editar (ex.: `python3 -m json.tool <arquivo>`).
6. Peça para ela **fechar o Claude Desktop por completo** (no macOS, Cmd+Q; no Windows, sair pelo
   ícone da bandeja) e abrir de novo. Siga então as Partes 3 e 4. No modo local, as planilhas são
   salvas na pasta indicada na resposta, em vez de virem por link.
   - Se o conector não aparecer, veja os logs: macOS `~/Library/Logs/Claude/mcp-server-api-mkt.log`,
     Windows `%APPDATA%\Claude\logs\`.
   - Atualizações futuras: `git -C ~/api-mkt pull` e reiniciar o Claude Desktop.
