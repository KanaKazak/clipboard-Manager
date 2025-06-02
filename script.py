import time
import pyperclip
import json
import sqlite3

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


# Initialize a dictionary to store clipboard history

def load_history():
    """Load clipboard history from a file."""
    try:
        with open('clipboard_history.json', 'r') as file:
            content = file.read().strip()
            if not content:
                print("History file was empty. Starting fresh.")
                return {}
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        print("History file missing or corrupted. Starting fresh.")
        return {}

def save_history(history: dict) -> None:
    """Save clipboard history to a file."""
    with open('clipboard_history.json', 'w') as file:
        json.dump(history, file, indent=4)

def main():
    clipboard_history = load_history()
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
            if current_content not in clipboard_history:
                clipboard_history[current_content] = time.ctime()
                print(f"Saved new clipboard entry at {time.ctime()}")
                save_history(clipboard_history)
        # Sleep for a short duration to avoid busy waiting
        time.sleep(1)
# A good practice to ensure the script runs only when executed directly
# This allows the script to be imported without running the main loop
if __name__ == "__main__":
    main()