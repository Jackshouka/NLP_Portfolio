import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect("guilty_gear_data.db")
cursor = connection.cursor()

# Create the characters table
cursor.execute("""
CREATE TABLE characters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
""")

# Create the moves table
cursor.execute("""
CREATE TABLE moves (
    id INTEGER PRIMARY KEY,
    character_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    move_type TEXT,
    description TEXT,
    FOREIGN KEY (character_id) REFERENCES characters (id)
);
""")

# Create the frame_data table
cursor.execute("""
CREATE TABLE frame_data (
    id INTEGER PRIMARY KEY,
    move_id INTEGER NOT NULL,
    startup INTEGER,
    active INTEGER,
    recovery INTEGER,
    on_block INTEGER,
    on_hit INTEGER,
    FOREIGN KEY (move_id) REFERENCES moves (id)
);
""")

# Commit the changes and close the connection
connection.commit()
cursor.close()
connection.close()
