import sqlite3
import sys

connection = sqlite3.connect("events.db", check_same_thread=False)
cursor = connection.cursor()

def initialise_events():
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                event_name TEXT, 
                start_datetime TEXT, 
                end_datetime TEXT, 
                primary_list INTEGER, 
                reserve_list INTEGER, 
                location TEXT,
                user_id INTEGER
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS primary_list(
                event_id INTEGER, 
                user_id INTEGER, 
                position INTEGER,
                FOREIGN KEY(event_id) REFERENCES events(id),
                PRIMARY KEY(event_id, user_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reserve_list(
                event_id INTEGER, 
                user_id INTEGER, 
                position INTEGER,
                FOREIGN KEY(event_id) REFERENCES events(id),
                PRIMARY KEY(event_id, user_id)
            )
        """)

    except Exception as e:
        print(f"Failed to initialise events or lists table, got error: {e}")
        sys.exit()

def write_to_events(event_name: str, start_datetime: str, end_datetime: str, primary_list: int, reserve_list: int, location: str, user_id: int):
    try:
        cursor.execute("""
            INSERT INTO events (
                event_name, 
                start_datetime,
                end_datetime,
                primary_list,
                reserve_list,
                location,
                user_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (event_name, start_datetime, end_datetime, primary_list, reserve_list, location, user_id))

        connection.commit()
    except Exception as e:
        return e

def get_user_events(user_id):
    cursor.execute("SELECT * FROM events WHERE user_id = ?", (user_id,))
    events = cursor.fetchall()

    return events

def get_event_by_id(event_id):
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()

    return event

def get_primary_list_count(event_id):
    cursor.execute("SELECT COUNT(*) FROM primary_list WHERE event_id = ?", (event_id,))
    count = cursor.fetchone()[0]

    return count

def get_reserve_list_count(event_id):
    cursor.execute("SELECT COUNT(*) FROM reserve_list WHERE event_id = ?", (event_id,))
    count = cursor.fetchone()[0]

    return count

def add_to_primary_list(event_id, user_id, position):
    try:
        cursor.execute("""
            INSERT INTO primary_list (event_id, user_id, position)
            VALUES (?, ?, ?)
        """, (event_id, user_id, position))

        connection.commit()

    except Exception as e:
        return e

def add_to_reserve_list(event_id, user_id, position):
    try:
        cursor.execute("""
            INSERT INTO reserve_list (event_id, user_id, position)
            VALUES (?, ?, ?)
        """, (event_id, user_id, position))

        connection.commit()
        
    except Exception as e:
        return e
