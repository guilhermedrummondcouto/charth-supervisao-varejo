from __future__ import annotations
import argparse
import os
import sqlite3
from pathlib import Path

import psycopg2

# Permite importar src/db.py quando rodar pela raiz do projeto.
from src.db import init_db

TABLES = ["stores", "users", "evaluations", "action_plans", "uploaded_files"]


def rows_from_sqlite(sqlite_path: str, table: str) -> tuple[list[str], list[tuple]]:
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
    except sqlite3.OperationalError:
        conn.close()
        return [], []
    if not rows:
        conn.close()
        return [], []
    columns = rows[0].keys()
    data = [tuple(row[col] for col in columns) for row in rows]
    conn.close()
    return list(columns), data


def insert_rows_pg(database_url: str, table: str, columns: list[str], rows: list[tuple]) -> int:
    if not rows:
        return 0
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
    placeholders = ", ".join(["%s"] * len(columns))
    col_sql = ", ".join(columns)
    conflict = ""
    if table == "users":
        conflict = " ON CONFLICT (username) DO NOTHING"
    elif table == "stores":
        conflict = " ON CONFLICT (name) DO NOTHING"
    elif table in {"evaluations", "action_plans", "uploaded_files"} and "id" in columns:
        conflict = " ON CONFLICT (id) DO NOTHING"
    sql = f"INSERT INTO {table} ({col_sql}) VALUES ({placeholders}){conflict}"
    cur.executemany(sql, rows)
    inserted = cur.rowcount if cur.rowcount is not None else 0
    if table in {"evaluations", "action_plans", "uploaded_files"}:
        try:
            cur.execute(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), COALESCE((SELECT MAX(id) FROM {table}), 1), true)")
        except Exception:
            pass
    conn.commit()
    conn.close()
    return inserted


def main() -> None:
    parser = argparse.ArgumentParser(description="Migra dados do SQLite local do app CHARTH para Supabase/PostgreSQL.")
    parser.add_argument("--sqlite", default="charth_supervisao_v6.db", help="Caminho do banco SQLite local.")
    parser.add_argument("--database-url", default=os.getenv("DATABASE_URL"), help="Connection string PostgreSQL/Supabase.")
    args = parser.parse_args()

    sqlite_path = Path(args.sqlite)
    if not sqlite_path.exists():
        raise SystemExit(f"Banco SQLite não encontrado: {sqlite_path}")
    if not args.database_url:
        raise SystemExit("Informe DATABASE_URL via variável de ambiente ou parâmetro --database-url.")

    os.environ["DATABASE_URL"] = args.database_url
    init_db()

    print("Migrando dados...")
    for table in TABLES:
        columns, rows = rows_from_sqlite(str(sqlite_path), table)
        if not rows:
            print(f"- {table}: sem registros")
            continue
        count = insert_rows_pg(args.database_url, table, columns, rows)
        print(f"- {table}: {len(rows)} registros lidos, {count} inserções/ignorados conforme conflito")
    print("Migração concluída.")


if __name__ == "__main__":
    main()
