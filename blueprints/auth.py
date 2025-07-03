from flask import Blueprint, flash, redirect, request, session, url_for

from database import DatabaseHandler

auth = Blueprint("auth",__name__, url_prefix="/auth")

@auth.route("/authoriseuser", methods = ["POST"])
def authoriseUser():
    formDetails = request.form
    username = formDetails.get("username")
    password = formDetails.get("password")

    db = DatabaseHandler()
    success = db.authoriseUser(username, password)
    if success:
        session["currentUser"] = username
        return redirect(url_for("pages.dashboard"))
    
    return redirect(url_for("pages.signin"))

@auth.route("/createuser", methods = ["POST"])
def createUser():
    formDetails = request.form
    username = formDetails.get("username")
    password = formDetails.get("password")
    repassword = formDetails.get("repassword")
    errors = False

    if password != repassword:
        flash("Passwords do not match")
        errors = True

    if len(password) < 8:
        flash("Password must be 8 or more characters.")
        errors = True

    if len(username) < 3:
        flash("Username must be 3 or more characters.")
        errors = True

    if errors:
        return redirect(url_for("pages.signup"))
        
    db = DatabaseHandler()
    success, errorType = db.createUser(username, password)
    if success:
        return redirect(url_for("pages.dashboard"))

    if errorType == "integrity-error":    
        flash("Invalid data has been entered. Please try again.")
    elif errorType == "unique-error":
        flash("Username taken. Please use another.")

    else:
        flash("An unknown error has occured")
    return redirect(url_for("pages.signup"))

@auth.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("pages.signin"))
