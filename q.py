#!/usr/bin/env python3
"""Runner de consultas — única porta de entrada para o banco.

Exemplos:
  python q.py "SELECT COUNT(*) FROM interesteds WHERE created_at >= '2026-10-01'"
  python q.py consultas/leads_por_campanha.sql -p inicio=2026-10-01 -p fim=2026-10-13 -p escola=1
  python q.py consultas/vendas.sql -p inicio=2026-09-01 -p fim=2026-09-30 -p escola=0 --xlsx vendas_setembro
  python q.py "SHOW COLUMNS FROM orders"

Parâmetros: escreva :nome no SQL e passe -p nome=valor.
Sem --sem-limite, consultas SELECT recebem LIMIT automático (padrão 500).
"""

import argparse
import sys
import time
from pathlib import Path

import pandas as pd

from db import aplicar_limite, consultar, exportar, parametros_usados

def carregar_sql(arg: str) -> str:
    caminho = Path(arg)
    if not caminho.is_absolute():
        caminho = Path(__file__).resolve().parent / caminho
    if arg.lower().endswith(".sql"):
        if not caminho.exists():
            sys.exit(f"Arquivo não encontrado: {arg}")
        return caminho.read_text(encoding="utf-8")
    return arg


def parse_params(itens: list[str]) -> dict:
    params = {}
    for item in itens:
        if "=" not in item:
            sys.exit(f"Parâmetro inválido '{item}' — use nome=valor")
        k, v = item.split("=", 1)
        params[k.strip()] = v
    return params


def main() -> None:
    ap = argparse.ArgumentParser(description="Consulta somente leitura no banco seducar.")
    ap.add_argument("sql", help="SQL entre aspas ou caminho de um arquivo .sql")
    ap.add_argument("-p", "--param", action="append", default=[], help="nome=valor (para :nome no SQL)")
    ap.add_argument("-l", "--limite", type=int, default=500, help="LIMIT automático (padrão 500)")
    ap.add_argument("--sem-limite", action="store_true", help="não adiciona LIMIT (use com filtro de período!)")
    ap.add_argument("--csv", metavar="NOME", help="salva em saidas/NOME.csv")
    ap.add_argument("--xlsx", metavar="NOME", help="salva em saidas/NOME.xlsx")
    ap.add_argument("--mostrar", type=int, default=50, help="quantas linhas imprimir (padrão 50)")
    args = ap.parse_args()

    sql = carregar_sql(args.sql)
    if not args.sem_limite:
        sql = aplicar_limite(sql, args.limite)
    params = parse_params(args.param)
    if not params and not parametros_usados(sql):
        params = None

    inicio = time.time()
    try:
        df = consultar(sql, params)
    except Exception as e:  # noqa: BLE001 — mensagem amigável para o terminal
        sys.exit(f"ERRO: {e}")
    duracao = time.time() - inicio
    df = df.convert_dtypes()  # ids com vazios continuam inteiros (não 1.6e+06)

    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 50)
    pd.set_option("display.max_colwidth", 60)
    if df.empty:
        print("(nenhuma linha)")
    else:
        print(df.head(args.mostrar).to_markdown(index=False))
    aviso_limite = "" if args.sem_limite else f" (LIMIT {args.limite})"
    print(f"\n{len(df)} linha(s){aviso_limite} em {duracao:.1f}s")
    if not args.sem_limite and len(df) == args.limite:
        print("⚠️  Resultado bateu no LIMIT — pode haver mais linhas. Agregue no SQL ou use --sem-limite.")

    if args.csv:
        print(f"CSV salvo em {exportar(df, args.csv, 'csv')}")
    if args.xlsx:
        print(f"XLSX salvo em {exportar(df, args.xlsx, 'xlsx')}")

if __name__ == "__main__":
    main()
