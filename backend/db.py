from __future__ import annotations
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

CFG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME"),
    "autocommit": True,
}

def get_conn():
    if not CFG["user"] or not CFG["database"]:
        raise RuntimeError("DB-Config unvollständig (DB_USER/DB_NAME fehlen).")
    return mysql.connector.connect(**CFG)

def init_db():
    return

def ensure_user(user_id: str, start_balance: int = 100):
    with get_conn() as con, con.cursor() as cur:
        cur.execute("SELECT balance FROM `users` WHERE user_id=%s", (user_id,))
        row = cur.fetchone()
        if not row:
            cur.execute("INSERT INTO `users` (user_id, balance) VALUES (%s, %s)",(user_id, int(start_balance)),
            )

def get_balance(user_id: str) -> int:
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("SELECT balance FROM users WHERE user_id=%s", (user_id,))
        row = cur.fetchone()
        return int(row[0]) if row else 0

def set_balance(user_id: str, new_balance: int) -> int:
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET balance=%s WHERE user_id=%s", (int(new_balance), user_id))
    return int(new_balance)

def add_balance(user_id: str, delta: int) -> int:
    bal = get_balance(user_id)
    return set_balance(user_id, bal + int(delta))

def log_bet(user_id: str, game: str, choice: str, dealer: str, bet: int, new_balance: int):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO bets(user_id, game, choice, dealer, bet, new_balance) VALUES(%s,%s,%s,%s,%s,%s)",
            (user_id, game, choice, dealer, bet, new_balance)
        )
