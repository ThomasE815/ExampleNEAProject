from flask import Blueprint, get_flashed_messages, redirect, render_template, session, url_for
from scripts.isAuthorised import isAuthorised

pages = Blueprint("pages", __name__)


@pages.route("/")
def signin():
    if isAuthorised():
        return redirect(url_for("pages.dashboard"))
    return render_template("signin.html")

@pages.route("/dashboard")
def dashboard():
    if not isAuthorised():
        return redirect(url_for("pages.signin"))
    
    currentUser = session["currentUser"]
    return render_template("dashboard.html", currentUser = currentUser)

@pages.route("/signup")
def signup():
    messages = get_flashed_messages()
    return render_template("signup.html", messages = messages)