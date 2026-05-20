from __future__ import annotations
import base64
import json
import os
import shutil
import sqlite3
from datetime import datetime, date, timedelta
from typing import Any

import pandas as pd

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except Exception:  # pragma: no cover
    psycopg2 = None
    RealDictCursor = None

try:
    import streamlit as st
except Exception:  # pragma: no cover
    st = None

import hashlib
from .calculations import action_priority, default_action_deadline_days


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
from .config import DB_PATH, DEFAULT_USERS, FORM_SECTIONS, STORES, UPLOAD_DIR


def get_database_url() -> str | None:
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return env_url.strip()
    if st is not None:
        try:
            if "DATABASE_URL" in st.secrets:
                return str(st.secrets["DATABASE_URL"]).strip()
            if "database" in st.secrets and "url" in st.secrets["database"]:
                return str(st.secrets["database"]["url"]).strip()
        except Exception:
            return None
    return None


def is_postgres() -> bool:
    url = get_database_url()
    return bool(url and url.startswith(("postgres://", "postgresql://")))


def database_mode_label() -> str:
    return "Supabase/PostgreSQL" if is_postgres() else "SQLite local"


def _ph(sql: str) -> str:
    return sql.replace("?", "%s") if is_postgres() else sql


def get_conn():
    url = get_database_url()
    if url and is_postgres():
        if psycopg2 is None:
            raise RuntimeError("psycopg2-binary não está instalado. Rode: pip install -r requirements.txt")
        return psycopg2.connect(url)
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    return conn


def _exec(cur, sql: str, params: tuple | list = ()):  # compatibilidade SQLite/Postgres
    cur.execute(_ph(sql), params)


def _fetchone_dict(cur) -> dict | None:
    row = cur.fetchone()
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    if isinstance(row, sqlite3.Row):
        return dict(row)
    cols = [d[0] for d in cur.description]
    return dict(zip(cols, row))


def _create_tables_sqlite(cur) -> None:
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            store TEXT,
            name TEXT,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS stores (
            name TEXT PRIMARY KEY,
            active INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            evaluation_date TEXT NOT NULL,
            supervisor TEXT NOT NULL,
            manager TEXT NOT NULL,
            store TEXT NOT NULL,
            scores_json TEXT NOT NULL,
            observations_json TEXT NOT NULL,
            strategic_json TEXT NOT NULL,
            section_scores_json TEXT NOT NULL,
            weighted_score REAL NOT NULL,
            overall_status TEXT NOT NULL,
            bonus_json TEXT NOT NULL,
            grave_disciplinary_issue INTEGER NOT NULL DEFAULT 0,
            photo_vm_path TEXT,
            created_by TEXT
        );
        CREATE TABLE IF NOT EXISTS action_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evaluation_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            store TEXT NOT NULL,
            section TEXT NOT NULL,
            question_key TEXT NOT NULL,
            question_label TEXT NOT NULL,
            score REAL NOT NULL,
            priority TEXT NOT NULL,
            responsible TEXT,
            deadline TEXT,
            status TEXT NOT NULL DEFAULT 'Aberto',
            notes TEXT,
            FOREIGN KEY(evaluation_id) REFERENCES evaluations(id)
        );
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            filename TEXT NOT NULL,
            mime_type TEXT,
            content_base64 TEXT NOT NULL
        );
        """
    )


def _create_tables_postgres(cur) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            store TEXT,
            name TEXT,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS stores (
            name TEXT PRIMARY KEY,
            active INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
            created_at TEXT NOT NULL,
            evaluation_date TEXT NOT NULL,
            supervisor TEXT NOT NULL,
            manager TEXT NOT NULL,
            store TEXT NOT NULL,
            scores_json TEXT NOT NULL,
            observations_json TEXT NOT NULL,
            strategic_json TEXT NOT NULL,
            section_scores_json TEXT NOT NULL,
            weighted_score DOUBLE PRECISION NOT NULL,
            overall_status TEXT NOT NULL,
            bonus_json TEXT NOT NULL,
            grave_disciplinary_issue INTEGER NOT NULL DEFAULT 0,
            photo_vm_path TEXT,
            created_by TEXT
        );
        CREATE TABLE IF NOT EXISTS action_plans (
            id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
            evaluation_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            store TEXT NOT NULL,
            section TEXT NOT NULL,
            question_key TEXT NOT NULL,
            question_label TEXT NOT NULL,
            score DOUBLE PRECISION NOT NULL,
            priority TEXT NOT NULL,
            responsible TEXT,
            deadline TEXT,
            status TEXT NOT NULL DEFAULT 'Aberto',
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
            created_at TEXT NOT NULL,
            filename TEXT NOT NULL,
            mime_type TEXT,
            content_base64 TEXT NOT NULL
        );
        """
    )


def init_db() -> None:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    conn = get_conn()
    cur = conn.cursor()
    if is_postgres():
        _create_tables_postgres(cur)
    else:
        _create_tables_sqlite(cur)

    now = datetime.now().isoformat(timespec="seconds")
    for store in STORES:
        _exec(cur, "SELECT name FROM stores WHERE name = ?", (store,))
        if _fetchone_dict(cur) is None:
            _exec(cur, "INSERT INTO stores (name, active) VALUES (?, 1)", (store,))
    for user in DEFAULT_USERS:
        _exec(cur, "SELECT username FROM users WHERE username = ?", (user["username"],))
        if _fetchone_dict(cur) is None:
            _exec(
                cur,
                "INSERT INTO users (username, password_hash, role, store, name, active, created_at) VALUES (?, ?, ?, ?, ?, 1, ?)",
                (user["username"], hash_password(user["password"]), user["role"], user["store"], user["name"], now),
            )
    conn.commit()
    conn.close()


def get_user_by_username(username: str) -> dict | None:
    conn = get_conn()
    if is_postgres():
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT username, password_hash, role, store, name FROM users WHERE username = %s AND active = 1", (username,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None
    cur = conn.cursor()
    cur.execute("SELECT username, password_hash, role, store, name FROM users WHERE username = ? AND active = 1", (username,))
    row = _fetchone_dict(cur)
    conn.close()
    return row


def save_uploaded_file(uploaded_file, prefix: str) -> str | None:
    if not uploaded_file:
        return None
    safe_name = uploaded_file.name.replace(" ", "_").replace("/", "_").replace("\\", "_")
    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_name}"

    if is_postgres():
        content = uploaded_file.getvalue()
        encoded = base64.b64encode(content).decode("ascii")
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO uploaded_files (created_at, filename, mime_type, content_base64) VALUES (%s, %s, %s, %s) RETURNING id",
            (datetime.now().isoformat(timespec="seconds"), filename, getattr(uploaded_file, "type", None), encoded),
        )
        file_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return f"db://uploaded_files/{file_id}/{filename}"

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path


def insert_evaluation(data: dict[str, Any]) -> int:
    conn = get_conn()
    cur = conn.cursor()
    values = (
        datetime.now().isoformat(timespec="seconds"),
        data["evaluation_date"],
        data["supervisor"],
        data["manager"],
        data["store"],
        json.dumps(data["scores"], ensure_ascii=False),
        json.dumps(data["observations"], ensure_ascii=False),
        json.dumps(data["strategic"], ensure_ascii=False),
        json.dumps(data["section_scores"], ensure_ascii=False),
        data["weighted_score"],
        data["overall_status"],
        json.dumps(data["bonus"], ensure_ascii=False),
        1 if data.get("grave_disciplinary_issue") else 0,
        data.get("photo_vm_path"),
        data.get("created_by"),
    )
    if is_postgres():
        cur.execute(
            """
            INSERT INTO evaluations (
                created_at, evaluation_date, supervisor, manager, store, scores_json,
                observations_json, strategic_json, section_scores_json, weighted_score,
                overall_status, bonus_json, grave_disciplinary_issue, photo_vm_path, created_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            values,
        )
        evaluation_id = int(cur.fetchone()[0])
    else:
        cur.execute(
            """
            INSERT INTO evaluations (
                created_at, evaluation_date, supervisor, manager, store, scores_json,
                observations_json, strategic_json, section_scores_json, weighted_score,
                overall_status, bonus_json, grave_disciplinary_issue, photo_vm_path, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            values,
        )
        evaluation_id = int(cur.lastrowid)

    for item in build_action_plan_items(evaluation_id, data):
        _exec(
            cur,
            """
            INSERT INTO action_plans (
                evaluation_id, created_at, store, section, question_key, question_label,
                score, priority, responsible, deadline, status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Aberto', ?)
            """,
            (
                item["evaluation_id"], item["created_at"], item["store"], item["section"], item["question_key"],
                item["question_label"], item["score"], item["priority"], item["responsible"], item["deadline"], item["notes"],
            ),
        )
    conn.commit()
    conn.close()
    return evaluation_id


def build_action_plan_items(evaluation_id: int, data: dict[str, Any]) -> list[dict[str, Any]]:
    items = []
    scores = data["scores"]
    now = datetime.now().isoformat(timespec="seconds")
    for section in FORM_SECTIONS:
        for q in section["questions"]:
            key = q["key"]
            score = float(scores.get(key, 10))
            is_binary = q["type"] in {"binary", "binary_inverse"}
            if score < 7 or (is_binary and score == 0):
                days = default_action_deadline_days(score, is_binary)
                items.append({
                    "evaluation_id": evaluation_id,
                    "created_at": now,
                    "store": data["store"],
                    "section": section["name"],
                    "question_key": key,
                    "question_label": q["label"],
                    "score": score,
                    "priority": action_priority(score, is_binary),
                    "responsible": data.get("manager") or "Gerente de Loja",
                    "deadline": (date.today() + timedelta(days=days)).isoformat(),
                    "notes": "Plano de ação gerado automaticamente por nota abaixo do padrão.",
                })
    return items


def evaluations_df() -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM evaluations ORDER BY evaluation_date DESC, id DESC", conn)
    conn.close()
    if df.empty:
        return df
    df["evaluation_date"] = pd.to_datetime(df["evaluation_date"], errors="coerce")
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    for col in ["scores_json", "observations_json", "strategic_json", "section_scores_json", "bonus_json"]:
        df[col] = df[col].apply(lambda x: json.loads(x) if isinstance(x, str) and x else {})
    df["bonus_level"] = df["bonus_json"].apply(lambda x: x.get("level", ""))
    df["manager_bonus"] = df["bonus_json"].apply(lambda x: x.get("manager_bonus", 0.0))
    for section in FORM_SECTIONS:
        df[f"media_{section['name'].lower().replace(' ', '_').replace('&','e')}"] = df["section_scores_json"].apply(lambda x, s=section["name"]: x.get(s, 0.0))
    return df


def action_plans_df() -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM action_plans ORDER BY deadline ASC, id DESC", conn)
    conn.close()
    if not df.empty:
        df["deadline"] = pd.to_datetime(df["deadline"], errors="coerce")
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    return df


def update_action_plan(plan_id: int, status: str, responsible: str, deadline: str, notes: str) -> None:
    conn = get_conn()
    cur = conn.cursor()
    _exec(cur, "UPDATE action_plans SET status = ?, responsible = ?, deadline = ?, notes = ? WHERE id = ?", (status, responsible, deadline, notes, plan_id))
    conn.commit()
    conn.close()


def export_flattened_evaluations(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    rows = []
    for _, row in df.iterrows():
        base = {
            "id": row["id"],
            "data": row["evaluation_date"].date().isoformat() if pd.notna(row["evaluation_date"]) else "",
            "loja": row["store"],
            "supervisora": row["supervisor"],
            "gerente": row["manager"],
            "media_ponderada": row["weighted_score"],
            "status": row["overall_status"],
            "nivel_bonus": row["bonus_level"],
            "bonus_gerente": row["manager_bonus"],
        }
        scores = row["scores_json"] if isinstance(row["scores_json"], dict) else {}
        sections = row["section_scores_json"] if isinstance(row["section_scores_json"], dict) else {}
        obs = row["observations_json"] if isinstance(row["observations_json"], dict) else {}
        strategic = row["strategic_json"] if isinstance(row["strategic_json"], dict) else {}
        base.update({f"nota_{k}": v for k, v in scores.items()})
        base.update({f"media_{k}": v for k, v in sections.items()})
        base.update(obs)
        base.update(strategic)
        rows.append(base)
    return pd.DataFrame(rows)


def list_users_df() -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql_query("SELECT username, role, store, name, active, created_at FROM users ORDER BY role, username", conn)
    conn.close()
    return df


def update_user_password(username: str, new_password: str) -> None:
    if not username or not new_password:
        raise ValueError("Usuário e nova senha são obrigatórios.")
    if len(new_password) < 6:
        raise ValueError("A nova senha precisa ter pelo menos 6 caracteres.")
    conn = get_conn()
    cur = conn.cursor()
    _exec(cur, "UPDATE users SET password_hash = ? WHERE username = ? AND active = 1", (hash_password(new_password), username))
    if cur.rowcount == 0:
        conn.close()
        raise ValueError("Usuário não encontrado ou inativo.")
    conn.commit()
    conn.close()


def backup_database() -> str | None:
    if is_postgres():
        return None
    if not os.path.exists(DB_PATH):
        return None
    os.makedirs("backups", exist_ok=True)
    dest = os.path.join("backups", f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
    shutil.copy2(DB_PATH, dest)
    return dest
