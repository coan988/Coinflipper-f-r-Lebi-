# db.py
from __future__ import annotations
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
PORT = int(os.getenv("MYSQL_PORT", "3306"))
USER = os.getenv("MYSQL_USER", "root")
PWD  = os.getenv("MYSQL_PASSWORD", "")
DB   = os.getenv("MYSQL_DATABASE", "casino")

CFG = {
    "host": HOST,
    "port": PORT,
    "user": USER,
    "password": PWD,
    "database": DB,
    "autocommit": True
}

def get_conn():
    return mysql.connector.connect(**CFG)

def init_db():
    return

def ensure_user(user_id: str):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("SELECT balance FROM users WHERE user_id=%s", (user_id,))
        row = cur.fetchone()
        if not row:
            cur.execute("INSERT INTO users(user_id, balance) VALUES(%s, %s)", (user_id, 0)), (user_id, 500)

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

def log_bet(user_id: str, choice: str, outcome: str, wager: int, balance_after: int):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO bets(user_id, choice, outcome, wager, balance_after) VALUES(%s,%s,%s,%s,%s)",
            (user_id, choice, outcome, wager, balance_after)
        )
