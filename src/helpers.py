'''Helper functions for web app'''
import hashlib

def hash(text):
    hash = hashlib.new("sha512")
    hash.update(text.encode())
    text = hash.hexdigest()
    
    return text