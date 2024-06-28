'''Helper functions for web app'''
from database import is_id_duplicate

import random
import hashlib

def generate_id():
    while True:
        id = random.randint(1000000000, 9999999999)
        if not is_id_duplicate(id=id):
            return id

def hash(text):
    hash = hashlib.new("sha512")
    hash.update(text.encode())
    text = hash.hexdigest()
    
    return text