#!/usr/bin/env python3
"""
Script per ispezionare il database e vedere le colonne delle tabelle.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path("data/fairs.db")

def inspect_db():
    if not DB_PATH.exists():
        print("Database non trovato.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    try:
        # Ottieni tutte le tabelle
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table_name, in tables:
            print(f"\nTabella: {table_name}")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[1]} ({col[2]}) {'PRIMARY KEY' if col[5] else ''}")

    except Exception as e:
        print(f"Errore: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    inspect_db()