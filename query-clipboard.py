import sqlite3
from tabulate import tabulate  # Optional for pretty tables

def query_clipboard(limit=50):
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, content, timestamp 
        FROM clipboard_history 
        ORDER BY id DESC 
        LIMIT ?
    """, (limit,))
    results = cursor.fetchall()
    conn.close()

    if results:
        print(tabulate(results, headers=["ID", "Content", "Timestamp"], tablefmt="fancy_grid"))
    else:
        print("No clipboard history found.")

if __name__ == "__main__":
    query_clipboard()
