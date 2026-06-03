# ============================================================
# database.py — Модуль работы с БД (без изменений)
# ============================================================
import sqlite3
from config import DB_PATH, TABLE_USERS
import random

def get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def init_system_tables():
    conn = get_connection()
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS ГруппыПользователей (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        name            TEXT UNIQUE NOT NULL
    );
    """)
    
    for g in ["Администратор", "Пользователь"]:
        conn.execute("INSERT OR IGNORE INTO ГруппыПользователей (name) VALUES (?)", (g,))
        
    query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_USERS} (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        login           TEXT UNIQUE NOT NULL,
        password        TEXT NOT NULL,
        role            TEXT NOT NULL DEFAULT 'Пользователь',
        is_blocked      INTEGER DEFAULT 0,
        failed_attempts INTEGER DEFAULT 0
    );
    """
    conn.executescript(query)
    
    count = conn.execute(f"SELECT COUNT(*) FROM {TABLE_USERS}").fetchone()[0]
    if count == 0:
        conn.execute(
            f"INSERT INTO {TABLE_USERS} (login, password, role) VALUES (?,?,?)",
            ("admin", "admin", "Администратор")
        )
    
    conn.commit()
    conn.close()

def check_login(login, password):
    conn = get_connection()
    row = conn.execute(f"SELECT * FROM {TABLE_USERS} WHERE login = ?", (login,)).fetchone()
    if not row:
        conn.close()
        return None, "not_found"
    if row["is_blocked"]:
        conn.close()
        return None, "blocked"
    if row["password"] != password:
        attempts = row["failed_attempts"] + 1
        if attempts >= 3:
            conn.execute(f"UPDATE {TABLE_USERS} SET is_blocked=1, failed_attempts=? WHERE id=?",
                         (attempts, row["id"]))
        else:
            conn.execute(f"UPDATE {TABLE_USERS} SET failed_attempts=? WHERE id=?",
                         (attempts, row["id"]))
        conn.commit()
        conn.close()
        if attempts >= 3:
            return None, "blocked"
        return None, "wrong_password"
    
    conn.execute(f"UPDATE {TABLE_USERS} SET failed_attempts=0 WHERE id=?", (row["id"],))
    conn.commit()
    user = dict(row)
    conn.close()
    return user, None

def get_all_users():
    conn = get_connection()
    rows = conn.execute(f"SELECT id, login, role, is_blocked FROM {TABLE_USERS}").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_user(login, password, role):
    conn = get_connection()
    existing = conn.execute(f"SELECT id FROM {TABLE_USERS} WHERE login=?", (login,)).fetchone()
    if existing:
        conn.close()
        return False, "exists"
    conn.execute(f"INSERT INTO {TABLE_USERS} (login, password, role) VALUES (?,?,?)",
                 (login, password, role))
    conn.commit()
    conn.close()
    return True, "ok"

def update_user(user_id, login=None, password=None, role=None, is_blocked=None):
    conn = get_connection()
    fields, values = [], []
    if login is not None:
        fields.append("login=?"); values.append(login)
    if password is not None:
        fields.append("password=?"); values.append(password)
    if role is not None:
        fields.append("role=?"); values.append(role)
    if is_blocked is not None:
        fields.append("is_blocked=?"); values.append(is_blocked)
        if is_blocked == 0:
            fields.append("failed_attempts=0")
    
    if fields:
        values.append(user_id)
        conn.execute(f"UPDATE {TABLE_USERS} SET {', '.join(fields)} WHERE id=?", values)
        conn.commit()
    conn.close()

def get_user_groups():
    conn = get_connection()
    rows = conn.execute("SELECT name FROM ГруппыПользователей").fetchall()
    conn.close()
    return [r["name"] for r in rows]

def add_user_group(name):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO ГруппыПользователей (name) VALUES (?)", (name,))
        conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_user_group(name):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM ГруппыПользователей WHERE name = ?", (name,))
        conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_table_names():
    conn = get_connection()
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    conn.close()
    return [r["name"] for r in rows]

def get_table_data(table_name, limit=1000):
    conn = get_connection()
    try:
        rows = conn.execute(f"SELECT * FROM [{table_name}] LIMIT ?", (limit,)).fetchall()
        cols = [desc[0] for desc in conn.execute(f"SELECT * FROM [{table_name}] LIMIT 0").description]
        return cols, [dict(r) for r in rows]
    except Exception:
        return [], []
    finally:
        conn.close()

def get_primary_key(table_name):
    conn = get_connection()
    try:
        rows = conn.execute(f"PRAGMA table_info([{table_name}])").fetchall()
        for r in rows:
            if r["pk"] > 0:
                return r["name"]
        return "rowid"
    except Exception:
        return None
    finally:
        conn.close()

def get_table_columns_info(table_name):
    conn = get_connection()
    try:
        rows = conn.execute(f"PRAGMA table_info([{table_name}])").fetchall()
        return [dict(r) for r in rows]
    except Exception:
        return []
    finally:
        conn.close()

def insert_row(table_name, data):
    conn = get_connection()
    try:
        cols = list(data.keys())
        placeholders = ", ".join(["?"] * len(cols))
        query = f"INSERT INTO [{table_name}] ({', '.join(f'[{c}]' for c in cols)}) VALUES ({placeholders})"
        conn.execute(query, list(data.values()))
        conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def update_row(table_name, pk_col, pk_val, data):
    conn = get_connection()
    try:
        sets = [f"[{k}] = ?" for k in data.keys()]
        vals = list(data.values())
        vals.append(pk_val)
        query = f"UPDATE [{table_name}] SET {', '.join(sets)} WHERE [{pk_col}] = ?"
        conn.execute(query, vals)
        conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_row(table_name, pk_col, pk_val):
    conn = get_connection()
    try:
        query = f"DELETE FROM [{table_name}] WHERE [{pk_col}] = ?"
        conn.execute(query, (pk_val,))
        conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def execute_query(query):
    conn = get_connection()
    try:
        cursor = conn.execute(query)
        if cursor.description:
            cols = [d[0] for d in cursor.description]
            rows = [list(r) for r in cursor.fetchall()]
            conn.commit()
            return cols, rows, None
        else:
            conn.commit()
            return [], [], "Запрос выполнен успешно (без возврата данных)"
    except Exception as e:
        return None, None, str(e)
    finally:
        conn.close()