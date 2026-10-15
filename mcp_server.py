#!/usr/bin/env python3
"""Servidor MCP do api-mkt — dá ao Claude Desktop acesso SOMENTE LEITURA ao banco Seducar.

Usa as mesmas travas do q.py (db.py): só SELECT/WITH/SHOW/DESCRIBE/EXPLAIN, uma
instrução por vez, sessão READ ONLY, timeout por consulta.

Dois modos:
  .venv/bin/python mcp_server.py           # stdio: local, iniciado pelo Claude Desktop
  .venv/bin/python mcp_server.py --http    # HTTP: remoto (Render), em /mcp/<MCP_TOKEN>

Credenciais do banco: .env na pasta do projeto ou variáveis de ambiente (ver .env.example).
No modo HTTP, MCP_TOKEN é obrigatório e a URL do conector é
  <PUBLIC_URL ou RENDER_EXTERNAL_URL>/mcp/<MCP_TOKEN>
Quem tem a URL tem acesso: trate-a como senha. Para revogar, troque MCP_TOKEN.
IMPORTANTE: em stdio, nada pode ser impresso em stdout — use stderr para depurar.
"""

import os
import re
import secrets
import shutil
import sys
import tempfile
import threading
import time
from datetime import date
from pathlib import Path

import pandas as pd
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, PlainTextResponse

from db import RAIZ, aplicar_limite, conectar, consultar, exportar, parametros_usados

CONSULTAS = RAIZ / "consultas"
SCHEMA = RAIZ / "schema"

# Modo HTTP: planilhas ficam num diretório temporário e saem por link de download
# (chave aleatória por arquivo, expira em ARQUIVOS_TTL segundos).
MODO_HTTP = "--http" in sys.argv
ARQUIVOS = Path(tempfile.gettempdir()) / "api-mkt-arquivos"
ARQUIVOS_TTL = 24 * 3600

LIMITE_EXPORTACAO = 100_000
MAX_LINHAS_RESPOSTA = 500

INSTRUCOES = """\
Banco MySQL do CRM Seducar (marcas Degrau Cultural e Central de Concursos), acesso somente leitura.
Use para análises de marketing: leads, campanhas/UTM, qualificação do bot (P1/P2/tier), funil e vendas.

Fluxo: 1) listar_consultas e prefira rodar_consulta (já trazem as regras de negócio);
2) para SQL novo, leia ler_documentacao("visao-geral") e descrever_tabela antes; 3) agregue no banco.

Regras que NÃO podem ser esquecidas:
- school_id 1 = Degrau, 2 = Central; 3, 4 e 5 são teste: sempre filtre school_id IN (1, 2).
- Lead = interesteds (data: created_at). Exclua opportunity_origin_id 14 (Upsell Passaport).
- Venda = orders, data = paid_at, mas quem define pago é o status: líquida = order_status_id 2;
  bruta = IN (2, 3, 10, 14, 15). paid_at vem preenchido até em pedido não pago.
- Etapa Vendido = opportunity_step_id 12 (Degrau) / 20 (Central). Perdido = 11 / 19.
- interested_pontuations pode ter mais de uma linha por lead: use a de maior id.
- orders × order_items é 1:N: pré-agregue itens para não duplicar valores.
- Fuso: a sessão lê as datas como gravadas. created_at/updated_at já estão em horário de Brasília;
  orders.paid_at está em UTC (use DATE_SUB(paid_at, INTERVAL 3 HOUR)). Não use NOW()/CURDATE() (UTC).
- Sempre filtre por período (banco de produção; orders não tem índice de data).
- Não traga dados pessoais (nome, CPF, e-mail, telefone, endereço) em análises.
"""

mcp = MCPServer(name="api-mkt", title="Análises de marketing Seducar", instructions=INSTRUCOES)

LEITURA = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)

# Uma conexão reaproveitada entre chamadas (abrir conexão custa ~2s).
_conn = None
_trava = threading.Lock()


def _executar(sql: str, params: dict | None = None) -> pd.DataFrame:
    global _conn
    with _trava:
        if _conn is not None:
            try:
                _conn.ping(reconnect=False)
            except Exception:  # noqa: BLE001 — conexão caiu: abre outra com as travas da sessão
                try:
                    _conn.close()
                except Exception:  # noqa: BLE001
                    pass
                _conn = None
        try:
            if _conn is None:
                _conn = conectar()
            return consultar(sql, params, conn=_conn).convert_dtypes()
        except Exception as e:  # noqa: BLE001 — a mensagem (sintaxe, coluna, trava) volta para o Claude corrigir
            raise ToolError(str(e)) from e


def _formatar(df: pd.DataFrame, limite: int | None, linhas_na_resposta: int, arquivo: str | None) -> str:
    partes = []
    total = len(df)
    if df.empty:
        partes.append("(nenhuma linha)")
    else:
        mostrar = df.head(linhas_na_resposta).copy()
        for c in mostrar.columns:
            if mostrar[c].dtype == object or str(mostrar[c].dtype) == "string":
                mostrar[c] = mostrar[c].map(lambda v: v if not isinstance(v, str) or len(v) <= 80 else v[:77] + "...")
        partes.append(mostrar.to_markdown(index=False))
        if total > linhas_na_resposta:
            partes.append(f"\n(mostrando {linhas_na_resposta} de {total} linhas)")
    partes.append(f"\nTotal: {total} linha(s).")
    if limite is not None and total == limite:
        partes.append(
            f"⚠️ O resultado bateu no limite de {limite} linhas: pode haver mais. "
            "Agregue no SQL, aumente `limite` ou exporte uma planilha."
        )
    if arquivo and MODO_HTTP:
        partes.append(f"Planilha pronta para download (link válido por 24h): {arquivo}")
    elif arquivo:
        partes.append(f"Planilha salva em: {arquivo}")
    return "\n".join(partes)


def _url_publica() -> str:
    return (os.getenv("PUBLIC_URL") or os.getenv("RENDER_EXTERNAL_URL") or "http://localhost:8000").rstrip("/")


def _limpar_arquivos_expirados() -> None:
    if not ARQUIVOS.exists():
        return
    limite = time.time() - ARQUIVOS_TTL
    for pasta in ARQUIVOS.iterdir():
        if pasta.stat().st_mtime < limite:
            shutil.rmtree(pasta, ignore_errors=True)


def _salvar_planilha(df: pd.DataFrame, nome: str) -> str:
    """Local: salva em SAIDAS_DIR. HTTP: salva em temp e devolve o link de download."""
    if not MODO_HTTP:
        return str(exportar(df, nome))
    _limpar_arquivos_expirados()
    nome_limpo = re.sub(r"[^\w\-]+", "_", nome.strip()).strip("_") or "consulta"
    chave = secrets.token_urlsafe(24)
    pasta = ARQUIVOS / chave
    pasta.mkdir(parents=True)
    df.to_excel(pasta / f"{nome_limpo}.xlsx", index=False)
    return f"{_url_publica()}/arquivos/{chave}/{nome_limpo}.xlsx"


def _validar_data(valor: str, nome: str) -> str:
    try:
        return date.fromisoformat(valor).isoformat()
    except ValueError:
        raise ToolError(f"`{nome}` deve estar no formato AAAA-MM-DD (recebi {valor!r}).") from None


def _cabecalho_sql(caminho: Path) -> str:
    linhas = []
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if not linha.startswith("--"):
            break
        linhas.append(linha[2:].strip())
    return " ".join(linhas)


@mcp.tool(annotations=LEITURA)
def listar_consultas() -> str:
    """Lista as consultas prontas (já com as regras de negócio) e os parâmetros de cada uma.

    Prefira estas consultas a escrever SQL do zero.
    """
    itens = []
    for arq in sorted(CONSULTAS.glob("*.sql")):
        params = sorted(parametros_usados(arq.read_text(encoding="utf-8")))
        itens.append(f"- **{arq.stem}** (parâmetros: {', '.join(params) or 'nenhum'}): {_cabecalho_sql(arq)}")
    return "\n".join(itens)


@mcp.tool(annotations=LEITURA)
def rodar_consulta(
    consulta: str,
    inicio: str,
    fim: str,
    escola: int = 0,
    janela_dias: int = 30,
    limite: int = 500,
    linhas_na_resposta: int = 100,
    exportar_planilha: str | None = None,
) -> str:
    """Executa uma consulta pronta de `listar_consultas`.

    Args:
        consulta: nome da consulta (ex.: "leads_por_campanha").
        inicio: data inicial, AAAA-MM-DD.
        fim: data final INCLUSIVA, AAAA-MM-DD.
        escola: 1 = Degrau, 2 = Central, 0 = as duas.
        janela_dias: só para funil_lead_venda (dias após o lead para contar a compra do cliente).
        limite: máximo de linhas trazidas do banco (ignorado quando exporta planilha).
        linhas_na_resposta: quantas linhas mostrar aqui (o resto vai só para a planilha).
        exportar_planilha: se informado, salva o resultado COMPLETO em XLSX com este nome
            (ex.: "vendas_setembro_degrau") e devolve o caminho do arquivo ou o link de download.
    """
    nome = re.sub(r"\.sql$", "", consulta.strip())
    if not re.fullmatch(r"[a-z0-9_]+", nome) or not (CONSULTAS / f"{nome}.sql").exists():
        disponiveis = ", ".join(sorted(p.stem for p in CONSULTAS.glob("*.sql")))
        raise ToolError(f"Consulta '{consulta}' não existe. Disponíveis: {disponiveis}")
    if escola not in (0, 1, 2):
        raise ToolError("`escola` deve ser 0 (as duas), 1 (Degrau) ou 2 (Central).")

    sql = (CONSULTAS / f"{nome}.sql").read_text(encoding="utf-8")
    valores = {
        "inicio": _validar_data(inicio, "inicio"),
        "fim": _validar_data(fim, "fim"),
        "escola": escola,
        "janela": int(janela_dias),
    }
    params = {k: v for k, v in valores.items() if k in parametros_usados(sql)}
    teto = LIMITE_EXPORTACAO if exportar_planilha else max(1, int(limite))
    df = _executar(aplicar_limite(sql, teto), params)
    arquivo = _salvar_planilha(df, exportar_planilha) if exportar_planilha else None
    return _formatar(df, teto, min(linhas_na_resposta, MAX_LINHAS_RESPOSTA), arquivo)


@mcp.tool(annotations=LEITURA)
def consulta_sql(
    sql: str,
    limite: int = 500,
    linhas_na_resposta: int = 100,
    exportar_planilha: str | None = None,
) -> str:
    """Executa um SQL de LEITURA (SELECT/WITH/SHOW/DESCRIBE/EXPLAIN) no banco seducar.

    Escrita e DDL são bloqueadas. Uma instrução por vez. Timeout de 60s.
    Antes de escrever SQL, leia ler_documentacao("visao-geral") e descrever_tabela.
    Sempre filtre por período e por school_id IN (1, 2). Agregue no banco.

    Args:
        sql: a consulta. `%` pode ser usado normalmente (LIKE '%x%', DATE_FORMAT).
        limite: LIMIT automático quando o SQL não tem LIMIT (ignorado quando exporta planilha).
        linhas_na_resposta: quantas linhas mostrar aqui.
        exportar_planilha: se informado, salva o resultado completo em XLSX com este nome.
    """
    teto = LIMITE_EXPORTACAO if exportar_planilha else max(1, int(limite))
    df = _executar(aplicar_limite(sql, teto))
    arquivo = _salvar_planilha(df, exportar_planilha) if exportar_planilha else None
    return _formatar(df, teto, min(linhas_na_resposta, MAX_LINHAS_RESPOSTA), arquivo)


@mcp.tool(annotations=LEITURA)
def descrever_tabela(tabela: str) -> str:
    """Colunas, tipos, chaves estrangeiras e índices de uma tabela do banco."""
    nome = tabela.strip().strip("`").lower()
    if not re.fullmatch(r"[a-z0-9_]+", nome):
        raise ToolError("Nome de tabela inválido.")
    doc = SCHEMA / "tabelas" / f"{nome}.md"
    if doc.exists():
        return doc.read_text(encoding="utf-8")
    cols = _executar(
        "SELECT column_name AS coluna, column_type AS tipo, is_nullable AS nulo, column_key AS chave "
        "FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = :t "
        "ORDER BY ordinal_position",
        {"t": nome},
    )
    if cols.empty:
        raise ToolError(f"A tabela '{nome}' não existe. Use buscar_tabelas para procurar.")
    fks = _executar(
        "SELECT column_name AS coluna, CONCAT(referenced_table_name, '.', referenced_column_name) AS referencia "
        "FROM information_schema.key_column_usage WHERE table_schema = DATABASE() AND table_name = :t "
        "AND referenced_table_name IS NOT NULL",
        {"t": nome},
    )
    md = f"# `{nome}`\n\n## Colunas\n\n{cols.to_markdown(index=False)}\n"
    if not fks.empty:
        md += f"\n## Chaves estrangeiras\n\n{fks.to_markdown(index=False)}\n"
    return md


@mcp.tool(annotations=LEITURA)
def buscar_tabelas(termo: str) -> str:
    """Procura tabelas do banco pelo nome (ex.: "refund", "coupon", "octadesk")."""
    df = _executar(
        "SELECT table_name AS tabela, table_rows AS linhas_estimadas FROM information_schema.tables "
        "WHERE table_schema = DATABASE() AND table_name LIKE :termo ORDER BY table_name",
        {"termo": f"%{termo.strip()}%"},
    )
    return df.to_markdown(index=False) if not df.empty else "(nenhuma tabela encontrada)"


DOCUMENTOS = {
    "visao-geral": SCHEMA / "visao-geral.md",
    "dominios": SCHEMA / "dominios.md",
}


@mcp.tool(annotations=LEITURA)
def ler_documentacao(documento: str = "visao-geral") -> str:
    """Documentação do banco para marketing.

    Args:
        documento: "visao-geral" (relações entre tabelas, armadilhas, status de pedido) ou
            "dominios" (ids → nomes de etapas do CRM, status, origens, unidades, categorias).
    """
    caminho = DOCUMENTOS.get(documento.strip().lower())
    if not caminho:
        raise ToolError(f"Documento inválido. Opções: {', '.join(DOCUMENTOS)}")
    return caminho.read_text(encoding="utf-8")


@mcp.custom_route("/health", methods=["GET"])
async def health(_: Request) -> JSONResponse:
    return JSONResponse({"ok": True})


@mcp.custom_route("/arquivos/{chave}/{nome}", methods=["GET"])
async def baixar_arquivo(request: Request):
    chave, nome = request.path_params["chave"], request.path_params["nome"]
    if not re.fullmatch(r"[\w\-]{20,}", chave) or not re.fullmatch(r"[\w\-]+\.xlsx", nome):
        return PlainTextResponse("Não encontrado", status_code=404)
    arquivo = ARQUIVOS / chave / nome
    if not arquivo.is_file() or arquivo.stat().st_mtime < time.time() - ARQUIVOS_TTL:
        return PlainTextResponse("Link expirado ou inexistente. Peça a planilha de novo ao Claude.", status_code=404)
    return FileResponse(
        arquivo,
        filename=nome,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def _rodar_http() -> None:
    import uvicorn
    from mcp.server.transport_security import TransportSecuritySettings

    token = os.getenv("MCP_TOKEN", "")
    if not re.fullmatch(r"[A-Za-z0-9_\-]{32,}", token):
        sys.exit(
            "MCP_TOKEN ausente ou fraco: use 32+ caracteres [A-Za-z0-9_-]. Gere com:\n"
            "  python3 -c \"import secrets; print(secrets.token_urlsafe(32))\""
        )
    host_publico = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    seguranca = (
        TransportSecuritySettings(allowed_hosts=[host_publico, "localhost:*", "127.0.0.1:*"])
        if host_publico
        else TransportSecuritySettings(enable_dns_rebinding_protection=False)
    )
    app = mcp.streamable_http_app(
        streamable_http_path=f"/mcp/{token}",
        stateless_http=True,
        json_response=True,
        transport_security=seguranca,
    )
    porta = int(os.getenv("PORT", "8000"))
    print(f"api-mkt MCP (HTTP) na porta {porta}; endpoint /mcp/<MCP_TOKEN>", file=sys.stderr)
    # access_log desligado: a URL contém o token e não pode ir para os logs do Render.
    uvicorn.run(app, host="0.0.0.0", port=porta, access_log=False, proxy_headers=True, forwarded_allow_ips="*")


if __name__ == "__main__":
    if MODO_HTTP:
        _rodar_http()
    else:
        mcp.run("stdio")
