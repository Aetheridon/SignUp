import database

import hashlib
import random
import sys

from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)
database.initialise_db()
app.secret_key = sys.argv[1]

@app.route("/")
def landing_page():
    return render_template("landing.html")

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":

        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]

        id = random.randint(1000000000, 9999999999)
        id_check = database.is_id_duplicate(id=id)

        if id_check:
            id = random.randint(1000000000, 9999999999)
            id_check = database.is_id_duplicate(id=id)
            
        email_check = database.is_email_duplicate(email=email)
        
        if email_check:
            flash("Email is already in use, please use another one!", "error")
        else:
            hash = hashlib.new("sha512")
            hash.update(password.encode())
            password = hash.hexdigest()
            database.write_to_db(id=id, email=email, name=name, password=password)

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if database.is_existing_email(email=email): 
            hashed_account_password = database.get_hashed_password(email=email) # Returns a tuple
            
            if hashed_account_password:
                hash = hashlib.new("sha512")
                hash.update(password.encode())
                password = hash.hexdigest()

                if password == hashed_account_password[0]:
                    print("Successful login!") #TODO: work on redirection to dashboard

                else:
                    flash("Incorrect password!", "password_error")

        else:
            flash("Email does not exist in database!", "email_error")

    return render_template("login.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)