import database
import helpers
import events_db

import sys

from flask import Flask, render_template, url_for, request, flash, redirect, session

app = Flask(__name__)

database.initialise_db()
events_db.initialise_events()

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
        
        if database.is_existing_email(email=email):
            flash("Email is already in use, please use another one!", "error")

        else:
            write_to_db_status = database.write_to_db(email=email, name=name, password=helpers.hash(password))

            if isinstance(write_to_db_status, Exception): # Checks if write_to_db_status threw an exception
                flash(f"Error whilst creating account: {write_to_db_status}", "error")

            else:
                helpers.store_id(email=email) 

                return redirect(url_for("dashboard", name=name))
        
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
                    print("Successful login!")

                    name = database.get_name(email=email)

                    if not name:
                        name = "<Unknown>"

                    helpers.store_id(email=email)
                    
                    return redirect(url_for("dashboard", name=name[0]))

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
        
        write_status = events_db.write_to_events(event_name, start_datetime, end_datetime, primary_list, reserve_list, location, user_id)

        if write_status: # write_status true when exception thrown.
            print(write_status) 

        return redirect(url_for("view_events"))

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

@app.route("/events/<int:event_id>")
def view_event(event_id):
    event = events_db.get_event_by_id(event_id)

    if event:
        primary_list_count = events_db.get_primary_list_count(event_id)
        reserve_list_count = events_db.get_reserve_list_count(event_id)
        return render_template("view_event.html", event=event, primary_list_count=primary_list_count, reserve_list_count=reserve_list_count)
    
    else:
        return "Event not found", 404

@app.route("/sign-up-primary/<int:event_id>", methods=["POST"])
def sign_up_primary(event_id):
    user_id = session.get("user_id")
    primary_list_count = events_db.get_primary_list_count(event_id)
    event = events_db.get_event_by_id(event_id)

    if primary_list_count < event[4]:
        position = primary_list_count + 1
        events_db.add_to_primary_list(event_id, user_id, position)
        flash("Successfully signed up for the primary list!", "success")

    else:
        flash("The primary list is full!", "error")

    return redirect(url_for("view_event", event_id=event_id))

@app.route("/sign-up-reserve/<int:event_id>", methods=["POST"])
def sign_up_reserve(event_id):
    user_id = session.get("user_id")
    reserve_list_count = events_db.get_reserve_list_count(event_id)
    event = events_db.get_event_by_id(event_id)

    if reserve_list_count < event[5]:
        position = reserve_list_count + 1
        events_db.add_to_reserve_list(event_id, user_id, position)
        flash("Successfully signed up for the reserve list!", "success")
        
    else:
        flash("The reserve list is full!", "error")
        
    return redirect(url_for("view_event", event_id=event_id))

@app.route("/about")
def about_page():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)