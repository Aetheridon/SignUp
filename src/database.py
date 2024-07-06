import sqlite3
import sys

connection = sqlite3.connect("user-accounts.db", check_same_thread=False)
cursor = connection.cursor()

def initialise_db():
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS accounts(id integer primary key autoincrement, email, name, password)")
    except Exception as e: 
        print(f"Failed to initialise table, got error: {e}")
        sys.exit()

def write_to_db(email: str, name: str, password: str):
    try:
        cursor.execute("INSERT INTO accounts (email, name, password) VALUES (?, ?, ?)", (email, name, password))
        connection.commit()

    except Exception as e:
        return e

def is_existing_email(email):
    cursor.execute("""SELECT email FROM accounts WHERE email=?""", (email, ))
    result = cursor.fetchone()

    if result:
        return True
    
    return False

def get_hashed_password(email):
    try:
        cursor.execute("""SELECT password FROM accounts WHERE email=?""", (email, ))
        result = cursor.fetchone()

        if result:
            return result
        
    except Exception as e:
        print("got errror whilst trying to fetch hashed password: {e}")
        return None
            
def get_name(email):
    try:
        cursor.execute("""SELECT name FROM accounts WHERE email=?""", (email, ))
        result = cursor.fetchone()

        if result:
            return result
        
    except Exception as e:
        print(f"got error fetching name: {e}")
        return None

def get_id(email):
    try:
        cursor.execute("""SELECT id FROM accounts WHERE email=?""", (email, ))
        result = cursor.fetchone()

        if result:
            return result
    
    except Exception as e:
        print("got error fetching I.D: {e}")
        return None