import sqlite3
import sys

connection = sqlite3.connect("events.db", check_same_thread=False)
cursor = connection.cursor()

def initialise_events():
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS events(id integer primary key autoincrement, 
            event_name, 
            start_datetime, 
            end_datetime, 
            primary_list, 
            reserve_list, 
            location,
            user_id
            )"""
        )

    except Exception as e:
        print(f"Failed to initialise events table, got error: {e}")
        sys.exit()

def write_to_events(event_name: str, start_datetime: str, end_datetime: str, primary_list: int, reserve_list: int, location: str, user_id: int):
    try:
        #TODO: function call to generate unique url for each event here

        cursor.execute("""INSERT INTO events (event_name, 
        start_datetime,
        end_datetime,
        primary_list,
        reserve_list,
        location,
        user_id
        )
                       
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (event_name, start_datetime, end_datetime, primary_list, reserve_list, location, user_id)) 
        connection.commit()

    except Exception as e:
        return e
    
def get_user_events(user_id):
    try:
        cursor.execute("SELECT * FROM events WHERE user_id = ?", (user_id,))
        events = cursor.fetchall()

        return events
    
    except Exception as e:
        print(f"Failed to get events for user_id {user_id}, got error: {e}")
        return None
