import database
import helpers

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

        email_check = database.is_existing_email(email=email)
        
        if email_check:
            flash("Email is already in use, please use another one!", "error")

        else:
            password = helpers.hash(password)
            write_to_db_status = database.write_to_db(email=email, name=name, password=password)

            if isinstance(write_to_db_status, Exception):
                flash(f"Error whilst creating account: {write_to_db_status}", "error")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if database.is_existing_email(email=email): 
            hashed_account_password = database.get_hashed_password(email=email) # Returns a tuple
            
            if hashed_account_password:
                password = helpers.hash(password)

                if password == hashed_account_password[0]:
                    print("Successful login!") #TODO: work on redirection to dashboard

                else:
                    flash("Incorrect password!", "password_error")

        else:
            flash("Email does not exist!", "email_error")

    return render_template("login.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)