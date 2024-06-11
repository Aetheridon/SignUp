from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def landing_page():
    return render_template("landing.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)