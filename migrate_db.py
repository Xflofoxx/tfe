#!/usr/bin/env python3
"""
Script per migrare il database aggiungendo colonne mancanti.
"""
import sqlite3
from pathlib import Path

# Percorso del database
DB_PATH = Path("data/fairs.db")

def migrate_database():
    if not DB_PATH.exists():
        print("Database non trovato, nessuna migrazione necessaria.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    try:
        # Verifica se la colonna ai_analysis_enabled esiste
        cursor.execute("PRAGMA table_info(fairs)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'ai_analysis_enabled' not in columns:
            print("Aggiunta colonna ai_analysis_enabled...")
            cursor.execute("ALTER TABLE fairs ADD COLUMN ai_analysis_enabled TEXT DEFAULT 'no'")
            print("Colonna ai_analysis_enabled aggiunta.")

        if 'ai_last_updated' not in columns:
            print("Aggiunta colonna ai_last_updated...")
            cursor.execute("ALTER TABLE fairs ADD COLUMN ai_last_updated TEXT")
            print("Colonna ai_last_updated aggiunta.")

        if 'previous_editions' not in columns:
            print("Aggiunta colonna previous_editions...")
            cursor.execute("ALTER TABLE fairs ADD COLUMN previous_editions TEXT")
            print("Colonna previous_editions aggiunta.")

        conn.commit()
        print("Migrazione completata con successo!")

    except Exception as e:
        print(f"Errore durante la migrazione: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()