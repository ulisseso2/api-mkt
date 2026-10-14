#!/usr/bin/env python3
"""Testa o servidor MCP como o Claude Desktop faria (sobe mcp_server.py via stdio).

  .venv/bin/python scripts/testar_mcp.py          (Windows: .venv\\Scripts\\python.exe scripts\\testar_mcp.py)

Para testar o servidor REMOTO (Render), passe a URL do conector por variável de ambiente
(ela não é impressa):
  MCP_URL="https://.../mcp/<token>" .venv/bin/python scripts/testar_mcp.py

Termina com "TUDO OK" quando o servidor sobe, lista as ferramentas, consulta o
banco e bloqueia escrita. Não imprime credenciais.
"""

import asyncio
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

RAIZ = Path(__file__).resolve().parent.parent
ESPERADAS = {"listar_consultas", "rodar_consulta", "consulta_sql", "descrever_tabela", "buscar_tabelas", "ler_documentacao"}


def texto(resultado) -> str:
    return "\n".join(getattr(c, "text", "") for c in resultado.content)


@asynccontextmanager
async def conectar_servidor():
    url = os.getenv("MCP_URL")
    if url:
        print("Testando servidor REMOTO (MCP_URL)")
        async with streamable_http_client(url) as streams:
            yield streams[0], streams[1]
    else:
        print("Testando servidor LOCAL (mcp_server.py via stdio)")
        params = StdioServerParameters(command=sys.executable, args=[str(RAIZ / "mcp_server.py")], cwd=str(RAIZ))
        async with stdio_client(params) as (leitura, escrita):
            yield leitura, escrita


async def main() -> int:
    falhas = 0
    async with conectar_servidor() as (leitura, escrita):
        async with ClientSession(leitura, escrita) as sessao:
            await sessao.initialize()
            print("✓ servidor iniciou")

            nomes = {t.name for t in (await sessao.list_tools()).tools}
            faltando = ESPERADAS - nomes
            print(("✓" if not faltando else "✗") + f" ferramentas: {', '.join(sorted(nomes))}")
            falhas += bool(faltando)

            r = await sessao.call_tool("consulta_sql", {"sql": "SELECT CURRENT_USER() AS usuario, NOW() AS agora"})
            ok = not r.is_error and "usuario" in texto(r)
            print(("✓" if ok else "✗") + " conexão com o banco" + ("" if ok else f": {texto(r)}"))
            falhas += not ok

            r = await sessao.call_tool(
                "rodar_consulta",
                {"consulta": "etapas_crm", "inicio": "2026-09-01", "fim": "2026-09-30", "escola": 1},
            )
            ok = not r.is_error and "leads" in texto(r)
            print(("✓" if ok else "✗") + " consulta pronta (etapas_crm)" + ("" if ok else f": {texto(r)}"))
            falhas += not ok

            r = await sessao.call_tool("consulta_sql", {"sql": "DELETE FROM interesteds WHERE id = 0"})
            ok = r.is_error
            print(("✓" if ok else "✗") + " escrita bloqueada")
            falhas += not ok

    print("\nTUDO OK" if not falhas else f"\n{falhas} FALHA(S)")
    return 1 if falhas else 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except BaseException as e:  # noqa: BLE001 — falha de conexão vira mensagem curta
        if isinstance(e, SystemExit):
            raise
        print(f"\n✗ Não foi possível conectar ao servidor: {type(e).__name__}")
        if os.getenv("MCP_URL"):
            print("  Confira a URL inteira (deve terminar em /mcp/<token>) e se o token é o mesmo do Render.")
        else:
            print("  Confira o .env e a conexão de rede com o banco.")
        sys.exit(1)
