import time
import pyperclip
import sqlite3
import keyboard
from playsound import playsound


#Initialize the sqlite3 database
def init_db():
    # This function initializes the SQLite database and creates a table for clipboard history
    print("Initializing database...")
    # Connect to the SQLite database (it will be created if it doesn't exist)
    # The database file will be named "clipboard.db"
    conn = sqlite3.connect("clipboard.db")
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create a table named "clipboard_history" if it doesn't already exist
    # The table will have three columns: id, content, and timestamp
    # id is an auto-incrementing primary key
    # content will store the clipboard content as text
    # timestamp will store the time when the content was copied
    # The timestamp will be stored as text in a human-readable format
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clipboard_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)

    # Commit the changes and close the connection to the database
    conn.commit()
    conn.close()


# Function to save clipboard content to the database
# This function takes the content and timestamp as parameters
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
    playsound("watching.mp3")
    # Announce that the program is running using text-to-speech
    print("Clipboard Manager is running. Press Ctrl+Shift+Q to exit.")
    last_content = ""
    # Start the monitoring loop
    while True:
        # Check if the user has pressed the exit key combination (Ctrl+Shift+Q)
        # If so, break the loop and exit the program
        if keyboard.is_pressed("ctrl+shift+q"):
            playsound("done.mp3")
            print("Exiting program")
            break
        # Check the clipboard content
        current_content = pyperclip.paste()
        # If the content has changed, print it
        if current_content != last_content and current_content.strip():
            # If the content is different from the last recorded content and is not empty
            # Update the last_content variable to the new content
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