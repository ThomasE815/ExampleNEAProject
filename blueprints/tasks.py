from flask import Blueprint, flash, redirect, request, session, url_for

from database import DatabaseHandler

tasks = Blueprint("tasks",__name__,url_prefix="/tasks")

@tasks.route("/create", methods = ["post"])
def createTask():
    #get the task name and description from the form
    formDetails = request.form
    taskName = formDetails.get("taskName")
    description = formDetails.get("description")
    #get the userID - from session
    userID = session["userID"]
    errors = False

    #validate data to be added
    if len(taskName) < 3:
        errors = True
        flash("Invalid task name.")

    if len(description) < 1:
        errors = True
        flash("Invalid task description.")

    if errors:
        return redirect(url_for("pages.createTask"))
    
    #if valid - add to database
    db = DatabaseHandler()
    success, errorType = db.createTask(taskName, description, userID)

    if success:
        return redirect(url_for("pages.dashboard")) #for now....
    
    #handle errors and redirect appropriately
    flash("An error occured making the task.")
    return redirect(url_for("pages.createTask"))

@tasks.route("/get/<int:taskID>")
def getTaskByID(taskID):
    return "getting tasks for task ID" + str(taskID)

@tasks.route("/updateStatus/<int:taskID>", methods = ["post"])
def updateStatus(taskID):
    db = DatabaseHandler()
    userID = session["userID"]
    formData = request.form
    status = formData.get("status")

    if status == "incomplete":
        newStatus = "complete"
    else:
        newStatus = "incomplete"

    success = db.updateStatus(taskID, userID, newStatus)
    if not success:
        flash("Task not updated successfully.")

    return redirect(url_for("pages.dashboard"))

@tasks.route("/delete/<int:taskID>", methods = ["post"])
def deleteTask(taskID):

    db = DatabaseHandler()
    userID = session["userID"]
    success  = db.deleteTask(taskID, userID)

    if not success:
        flash("Task not deleted")
    else:
        flash("Task deleted successfully!")
    
    return redirect(url_for("pages.dashboard"))

