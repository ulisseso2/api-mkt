#!/usr/bin/env python3
"""Gera a documentação de schema em schema/ a partir do banco real.

  python scripts/gerar_schema.py

Produz:
  schema/tabelas/<tabela>.md   colunas, tipos, chaves, FKs e índices das tabelas-chave
  schema/dominios.md           valores das tabelas de domínio (etapas, status, origens...)
  schema/indice_tabelas.md     todas as tabelas do banco com volume estimado

Rodar de novo quando o schema mudar. schema/visao-geral.md é escrito à mão
(regras de negócio) e NÃO é sobrescrito.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db import RAIZ, conectar, consultar as _consultar  # noqa: E402

_CONN = None


def consultar(sql, params=None):
    global _CONN
    if _CONN is None:
        _CONN = conectar()
    return _consultar(sql, params, conn=_CONN)

SCHEMA = RAIZ / "schema"
TABELAS_DIR = SCHEMA / "tabelas"

# Tabelas documentadas em detalhe (as que o marketing usa).
TABELAS_CHAVE = [
    "interesteds",
    "interested_pontuations",
    "interested_pontuations_answers",
    "interested_x_orders",
    "orders",
    "order_items",
    "order_attributions",
    "order_refunds",
    "transactions",
    "customers",
    "products",
    "product_categories",
    "classrooms",
    "courses",
    "course_sales",
    "sales_force",
    "contests",
    "units",
    "users",
    "opportunity_steps",
    "opportunity_origins",
    "opportunity_modalities",
    "opportunity_logs",
    "opportunity_transcripts",
    "transcription_ai_summaries",
    "chat_ai_evaluations",
    "octadesk_chats",
    "preleads",
]

# Tabelas pequenas cujos valores vale exportar inteiros (id → nome).
DOMINIOS = [
    "schools",
    "opportunity_steps",
    "opportunity_origins",
    "opportunity_modalities",
    "opportunity_statuses",
    "order_status",
    "payment_methods",
    "product_categories",
    "units",
    "shifts",
    "time_to_calls",
    "areas",
    "reason_for_losses",
    "order_cancelation_types",
]

COLUNAS_RUIDO = {"created_at", "updated_at", "deleted_at", "uuid"}


def esc(v) -> str:
    s = "" if v is None else str(v)
    return s.replace("|", "\\|").replace("\n", " ")


def tabela_md(df) -> str:
    if df.empty:
        return "_(vazio)_\n"
    return df.to_markdown(index=False) + "\n"


def documentar_tabela(nome: str) -> str | None:
    info = consultar(
        "SELECT table_rows, table_comment FROM information_schema.tables "
        "WHERE table_schema = DATABASE() AND table_name = :t",
        {"t": nome},
    )
    if info.empty:
        print(f"  - {nome}: não existe, pulando")
        return None

    cols = consultar(
        "SELECT column_name AS coluna, column_type AS tipo, is_nullable AS nulo, "
        "column_key AS chave, column_default AS padrao, column_comment AS comentario "
        "FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = :t "
        "ORDER BY ordinal_position",
        {"t": nome},
    )
    fks_saida = consultar(
        "SELECT column_name AS coluna, CONCAT(referenced_table_name, '.', referenced_column_name) AS referencia "
        "FROM information_schema.key_column_usage WHERE table_schema = DATABASE() AND table_name = :t "
        "AND referenced_table_name IS NOT NULL ORDER BY column_name",
        {"t": nome},
    )
    fks_entrada = consultar(
        "SELECT CONCAT(table_name, '.', column_name) AS origem, referenced_column_name AS coluna "
        "FROM information_schema.key_column_usage WHERE table_schema = DATABASE() "
        "AND referenced_table_name = :t ORDER BY table_name",
        {"t": nome},
    )
    indices = consultar(
        "SELECT index_name AS indice, GROUP_CONCAT(column_name ORDER BY seq_in_index) AS colunas, "
        "MIN(non_unique) = 0 AS unico FROM information_schema.statistics "
        "WHERE table_schema = DATABASE() AND table_name = :t GROUP BY index_name",
        {"t": nome},
    )

    for df in (cols, fks_saida, fks_entrada, indices):
        for c in df.columns:
            df[c] = df[c].map(esc)

    linhas = int(info.iloc[0]["TABLE_ROWS"] or 0)
    partes = [
        f"# `{nome}`\n",
        f"Linhas (estimativa do information_schema): **~{linhas:,}**".replace(",", "."),
    ]
    if info.iloc[0]["TABLE_COMMENT"]:
        partes.append(f"\nComentário: {info.iloc[0]['TABLE_COMMENT']}")
    partes += [
        "\n> Gerado por `scripts/gerar_schema.py`. Regras de negócio estão em `schema/visao-geral.md`.\n",
        "## Colunas\n",
        tabela_md(cols),
        "## Chaves estrangeiras (esta tabela → outra)\n",
        tabela_md(fks_saida),
        "## Referenciada por (outra tabela → esta)\n",
        tabela_md(fks_entrada),
        "## Índices (filtre/junte preferencialmente por colunas indexadas)\n",
        tabela_md(indices),
    ]
    return "\n".join(partes)


def documentar_dominios() -> str:
    partes = [
        "# Tabelas de domínio (valores id → nome)\n",
        "> Gerado por `scripts/gerar_schema.py`. Use estes ids em filtros e CASEs.\n",
    ]
    for nome in DOMINIOS:
        cols = consultar(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() "
            "AND table_name = :t ORDER BY ordinal_position",
            {"t": nome},
        )
        if cols.empty:
            continue
        uteis = [c for c in cols["COLUMN_NAME"] if c not in COLUNAS_RUIDO][:8]
        lista = ", ".join(f"`{c}`" for c in uteis)
        ordem = "sort, id" if "sort" in uteis else "id"
        df = consultar(f"SELECT {lista} FROM `{nome}` ORDER BY {ordem} LIMIT 200")
        for c in df.columns:
            df[c] = df[c].map(esc)
        partes += [f"## `{nome}`\n", tabela_md(df)]
    return "\n".join(partes)


def documentar_indice() -> str:
    df = consultar(
        "SELECT table_name AS tabela, table_rows AS linhas_estimadas "
        "FROM information_schema.tables WHERE table_schema = DATABASE() ORDER BY table_name"
    )
    return (
        "# Todas as tabelas do banco `seducar`\n\n"
        "> Gerado por `scripts/gerar_schema.py`. Para ver colunas de uma tabela fora de `schema/tabelas/`:\n"
        "> `python q.py \"SHOW COLUMNS FROM nome_da_tabela\"`\n\n" + tabela_md(df)
    )


def main() -> None:
    TABELAS_DIR.mkdir(parents=True, exist_ok=True)
    print("Documentando tabelas-chave...")
    for nome in TABELAS_CHAVE:
        md = documentar_tabela(nome)
        if md:
            (TABELAS_DIR / f"{nome}.md").write_text(md, encoding="utf-8")
            print(f"  ✓ {nome}")
    print("Exportando domínios...")
    (SCHEMA / "dominios.md").write_text(documentar_dominios(), encoding="utf-8")
    print("Gerando índice de tabelas...")
    (SCHEMA / "indice_tabelas.md").write_text(documentar_indice(), encoding="utf-8")
    print("Pronto.")


if __name__ == "__main__":
    main()
