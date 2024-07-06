'''Helper functions for web app'''
import database

import sys
import hashlib

from flask import Flask, session

def hash(text):
    hash = hashlib.new("sha512")
    hash.update(text.encode())
    text = hash.hexdigest()
    
    return text

def store_id(email):
    user_id = database.get_id(email=email)
    if not user_id:
        print("Unable to get I.D")
        sys.exit()

    session["user_id"] = user_id[0]