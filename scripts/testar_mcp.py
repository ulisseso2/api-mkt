#!/usr/bin/env python3
"""Testa o servidor MCP como o Claude Desktop faria (sobe mcp_server.py via stdio).

  .venv/bin/python scripts/testar_mcp.py          (Windows: .venv\\Scripts\\python.exe scripts\\testar_mcp.py)

Termina com "TUDO OK" quando o servidor sobe, lista as ferramentas, consulta o
banco e bloqueia escrita. Não imprime credenciais.
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

RAIZ = Path(__file__).resolve().parent.parent
ESPERADAS = {"listar_consultas", "rodar_consulta", "consulta_sql", "descrever_tabela", "buscar_tabelas", "ler_documentacao"}


def texto(resultado) -> str:
    return "\n".join(getattr(c, "text", "") for c in resultado.content)


async def main() -> int:
    params = StdioServerParameters(command=sys.executable, args=[str(RAIZ / "mcp_server.py")], cwd=str(RAIZ))
    falhas = 0
    async with stdio_client(params) as (leitura, escrita):
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
    sys.exit(asyncio.run(main()))
