import sqlite3
import csv

def export_to_csv(db_path="clipboard.db", output_file="clipboard_export.csv"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clipboard_history")
    rows = cursor.fetchall()

    with open(output_file, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Content", "Timestamp"])  # Header
        writer.writerows(rows)

    conn.close()
    print(f"Exported {len(rows)} entries to {output_file}")

if __name__ == "__main__":
    export_to_csv()
