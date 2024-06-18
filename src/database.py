import sqlite3
import sys

connection = sqlite3.connect("user-accounts.db", check_same_thread=False)
cursor = connection.cursor()

def initialise_db():
    res = cursor.execute("SELECT name FROM sqlite_master")
    
    if not res.fetchone(): # checks for existing D.B, if not we create the D.B and Table
        try:
            cursor.execute("CREATE TABLE accounts(id, email, name, password)")
        except Exception as e:
            print(f"encountered err trying to initialise database\nErr: {e}")
            sys.exit()

def write_to_db(id: int, email: str, name: str, password: str):
    cursor.execute("INSERT INTO accounts (id, email, name, password) VALUES (?, ?, ?, ?)", (id, email, name, password))

    connection.commit()

def is_id_duplicate(id):
    cursor.execute("""SELECT id FROM accounts WHERE id=?""", (id, ))
    result = cursor.fetchone()
    
    if result:
        return True
    
    return False

def is_email_duplicate(email):
    cursor.execute("""SELECT email FROM accounts WHERE email=?""", (email, ))
    result = cursor.fetchone()

    if result:
        return True
    
    return False
