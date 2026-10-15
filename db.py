"""Conexão somente leitura com o MySQL `seducar` (mesmo banco do CRM).

Credenciais vêm do .env (MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD,
MYSQL_DB_NAME). Senhas com `#` precisam estar entre aspas duplas no .env,
senão o dotenv trunca a senha no `#`.
"""

import os
import re
from pathlib import Path

import pandas as pd
import pymysql
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent
load_dotenv(RAIZ / ".env")

# Pasta das planilhas exportadas (SAIDAS_DIR no .env; padrão: saidas/ do projeto).
_SAIDAS_PADRAO = RAIZ / "saidas"

# Tempo máximo de uma consulta no servidor (ms). O banco é de produção.
TIMEOUT_MS = int(os.getenv("QUERY_TIMEOUT_MS", "60000"))

_PERMITIDO = re.compile(r"^\s*(SELECT|WITH|SHOW|DESCRIBE|DESC|EXPLAIN)\b", re.IGNORECASE)
_PROIBIDO = re.compile(
    r"\b(INSERT|UPDATE|DELETE|REPLACE|DROP|ALTER|CREATE|TRUNCATE|GRANT|REVOKE|"
    r"RENAME|LOCK|UNLOCK|CALL|LOAD|HANDLER|SET\s+GLOBAL|INTO\s+OUTFILE|INTO\s+DUMPFILE)\b",
    re.IGNORECASE,
)


def _sem_comentarios_e_strings(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)
    sql = re.sub(r"(--|#)[^\n]*", " ", sql)
    sql = re.sub(r"'(?:[^'\\]|\\.)*'", "''", sql)
    sql = re.sub(r'"(?:[^"\\]|\\.)*"', '""', sql)
    return sql


def validar_somente_leitura(sql: str) -> None:
    """Recusa qualquer coisa que não seja leitura. Defesa extra além do usuário readonly."""
    limpo = _sem_comentarios_e_strings(sql).strip().rstrip(";").strip()
    if ";" in limpo:
        raise ValueError("Só uma instrução por vez (encontrei ';' no meio da consulta).")
    if not _PERMITIDO.match(limpo):
        raise ValueError("Só são permitidas consultas SELECT / WITH / SHOW / DESCRIBE / EXPLAIN.")
    if _PROIBIDO.search(limpo):
        raise ValueError("A consulta contém um comando de escrita/DDL — bloqueado.")


def parametros_usados(sql: str) -> set[str]:
    """Nomes `:param` presentes no SQL (fora de comentários e strings)."""
    return set(re.findall(r"(?<![:\w]):([a-zA-Z_]\w*)", _sem_comentarios_e_strings(sql)))


def _parametros_nomeados(sql: str, params: dict) -> str:
    """Converte `:nome` → `%(nome)s` e escapa os demais `%` (LIKE, DATE_FORMAT)."""
    faltando = parametros_usados(sql) - set(params)
    if faltando:
        raise ValueError(f"Faltou informar parâmetro(s): {', '.join(sorted(faltando))} (use -p nome=valor)")
    sql = sql.replace("%", "%%")
    for nome in sorted(params, key=len, reverse=True):
        sql = re.sub(rf"(?<![:\w]):{nome}\b", f"%({nome})s", sql)
    return sql


def conectar() -> pymysql.connections.Connection:
    faltando = [v for v in ("MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DB_NAME") if not os.getenv(v)]
    if faltando:
        raise RuntimeError(f"Variáveis ausentes no .env: {', '.join(faltando)}")
    conn = pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DB_NAME"],
        charset="utf8mb4",
        # Sem autocommit, a conexão reaproveitada pelo MCP fica presa numa transação e
        # passa a ver uma "foto" antiga do banco (REPEATABLE READ): leads novos não aparecem.
        autocommit=True,
        connect_timeout=15,
        read_timeout=max(TIMEOUT_MS // 1000 + 30, 60),
        cursorclass=pymysql.cursors.DictCursor,
    )
    with conn.cursor() as cur:
        cur.execute("SET SESSION TRANSACTION READ ONLY")
        # Sessão em UTC = lê as colunas como estão gravadas. created_at/updated_at já estão em
        # horário de Brasília; só orders.paid_at está em UTC (descontar 3h nas consultas).
        cur.execute("SET time_zone = '+00:00'")
        cur.execute(f"SET SESSION max_execution_time = {TIMEOUT_MS}")
    return conn


def consultar(
    sql: str,
    params: dict | list | None = None,
    conn: pymysql.connections.Connection | None = None,
) -> pd.DataFrame:
    """Executa uma consulta de leitura e devolve um DataFrame.

    Passe `conn` (de `conectar()`) para reaproveitar a conexão em várias consultas.
    """
    validar_somente_leitura(sql)
    if isinstance(params, dict):
        sql = _parametros_nomeados(sql, params)
    propria = conn is None
    conn = conn or conectar()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            linhas = cur.fetchall()
            colunas = [d[0] for d in cur.description] if cur.description else []
        return pd.DataFrame(linhas, columns=colunas)
    finally:
        if propria:
            conn.close()


def aplicar_limite(sql: str, limite: int) -> str:
    corpo = sql.strip().rstrip(";")
    if not re.match(r"^\s*(SELECT|WITH)\b", re.sub(r"--[^\n]*", "", corpo).strip(), re.I):
        return corpo
    # Já tem LIMIT no final? respeita.
    if re.search(r"\bLIMIT\s+\d+(\s*,\s*\d+|\s+OFFSET\s+\d+)?\s*$", corpo, re.I):
        return corpo
    return f"{corpo}\nLIMIT {limite}"


def pasta_saidas() -> Path:
    destino = Path(os.path.expanduser(os.getenv("SAIDAS_DIR", ""))) if os.getenv("SAIDAS_DIR") else _SAIDAS_PADRAO
    destino.mkdir(parents=True, exist_ok=True)
    return destino


def exportar(df: pd.DataFrame, nome: str, formato: str = "xlsx") -> Path:
    """Salva o DataFrame em SAIDAS_DIR/nome.xlsx|csv e devolve o caminho."""
    nome = re.sub(r"[^\w\-]+", "_", nome.strip()).strip("_") or "consulta"
    destino = pasta_saidas() / f"{nome}.{formato}"
    if formato == "csv":
        df.to_csv(destino, index=False, encoding="utf-8-sig", sep=";", decimal=",")
    else:
        df.to_excel(destino, index=False)
    return destino
