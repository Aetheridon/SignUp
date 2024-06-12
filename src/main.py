from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def landing_page():
    return render_template("landing.html")

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"] #TODO: store these fields in a database

        print(f"email: {email}\nname: {name}\npassword: {password}\n")
        
        return "<h1>Sign up completed</h1>" #TODO: redirection to homepage for website

    else:
        return render_template("signup.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)