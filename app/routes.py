from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
from app import password_holder

main = Blueprint("main", __name__)

# 🔐 Middleware to enforce login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("main.login"))
    return decorated_function

# 🔑 Login route
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_password = request.form.get("password", "")
        stored_password = password_holder.get()
        if user_password == stored_password:
            session["logged_in"] = True
            return redirect(url_for("main.index"))
        return render_template("login.html", error="❌ Incorrect password")
    return render_template("login.html")

# 💬 Main chatroom page
@main.route("/")
@login_required
def index():
    return render_template("index.html")

# 🚪 Logout
@main.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("main.login"))
