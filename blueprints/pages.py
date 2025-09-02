from flask import Blueprint, get_flashed_messages, redirect, render_template, session, url_for
from database import DatabaseHandler
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
    userID = session["userID"]

    db = DatabaseHandler()
    success, tasks = db.fetchAllTasks(userID)

    messages = get_flashed_messages()

    return render_template("dashboard.html", currentUser = currentUser, tasks = tasks, messages = messages)

@pages.route("/signup")
def signup():
    messages = get_flashed_messages()
    return render_template("signup.html", messages = messages)


@pages.route("/createTask")
def createTask():
    messages = get_flashed_messages()
    return render_template("createTask.html", messages = messages)