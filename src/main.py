import database
import helpers
import events_db

import sys

from flask import Flask, render_template, url_for, request, flash, redirect, session

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

        helpers.store_id(email=email)

        return redirect(url_for("dashboard", name=name[0]))
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
                    print("Successful login!") #TODO: work on redirection to dashboard, some type of session checking

                    name = database.get_name(email=email)
                    if not name:
                        print("Unable to get name")
                        sys.exit()

                    helpers.store_id(email=email)
                    
                    return redirect(url_for("dashboard", name=name[0])) #TODO: bug with how the name is displayed

                else:
                    flash("Incorrect password!", "password_error")

            if not hashed_account_password:
                print("Unable to get password")
                sys.exit()

        else:
            flash("Email does not exist!", "email_error")

    return render_template("login.html")

@app.route(f"/dashboard/<name>")
def dashboard(name):
    return render_template("dashboard.html", name=name)

@app.route("/create-event", methods=["GET", "POST"])
def create_event():
    if request.method == "POST":
        user_id = session.get("user_id")
        if not user_id:
            print(f"user_id is None")
            sys.exit()

        event_name = request.form["event_name"]
        start_datetime = request.form["start_datetime"]
        end_datetime = request.form["end_datetime"]
        primary_list = request.form["primary_list"]
        reserve_list = request.form["reserve_list"]
        location = request.form["location"]

        events_db.initialise_events()
        
        write_status = events_db.write_to_events(event_name, start_datetime, end_datetime, primary_list, reserve_list, location, user_id)

        if write_status:
            print(write_status)

        return render_template("create_event.html")

    else:
        return render_template("create_event.html")

@app.route("/view-events")
def view_events():
    user_id = session.get("user_id")
    if not user_id:
        print(f"user_id is None")
        sys.exit()

    events = events_db.get_user_events(user_id)
    print(events)

    return render_template("view_events.html", events=events)

@app.route("/about")
def about_page():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)