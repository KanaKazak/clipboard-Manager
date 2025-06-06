import time
import pyperclip
import json
import sqlite3

#Initialize the sqlite3 database
def init_db():
    conn = sqlite3.connect("clipboard.db")  # creates file if not exists
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clipboard_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

#Function to commit clipboard history to the database
def save_to_db(content: str, timestamp: str) -> None:
    conn = sqlite3.connect("clipboard.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clipboard_history (content, timestamp) VALUES (?, ?)", (content, timestamp))
    conn.commit()
    conn.close()
    print(f"Inserted into DB at {timestamp}")

def main():
    init_db()
    # Set up the clipboard monitoring
    print("Monitoring clipboard for changes...")
    last_content = ""
    # Start the monitoring loop
    while True:
        # Check the clipboard content
        current_content = pyperclip.paste()
        # If the content has changed, print it
        if current_content != last_content:
            # Print the new content
            print(f"Clipboard updated: {current_content}")
            last_content = current_content
            # Store the new content in the history
            save_to_db(current_content, time.ctime())
        # Sleep for a short duration to avoid busy waiting
        time.sleep(1)
# A good practice to ensure the script runs only when executed directly
# This allows the script to be imported without running the main loop
if __name__ == "__main__":
    main()