from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models import message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if "log_email" not in session:
        session["log_email"] = ""
    if "first_name" and "last_name" and "email" not in session:
        session["first_name"] = ""
        session["last_name"] = ""
        session["email"] = ""
    return render_template("reg_log.html")

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        session["log_email"] = request.form["log_email"]
    # see if the username provided exists in the database
    valid_user = User.authenticated_user_by_input(request.form)
    if not valid_user:
        return redirect("/")
    session["user_id"] = valid_user.id
    return redirect("/dojo_wall")

@app.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        session["first_name"] = request.form["first_name"]
        session["last_name"] = request.form["last_name"]
        session["email"] = request.form["email"]
    valid_user = User.create_valid_user(request.form)
    if not valid_user:
        return redirect("/")
    session["user_id"] = valid_user.id
    return redirect("/dojo_wall")


@app.route("/dojo_wall")
def users():
    if "user_id" not in session:
        return redirect("/logout")
    # data = {
    #     "id" : session["user_id"]
    # }
    user = User.get_by_id(session["user_id"])
    users = User.get_all() 
    messages = message.Message.get_messages(session["user_id"])
    sent_amount = message.Message.get_sent_messages(session["user_id"])
    return render_template("dojo_wall.html", user = user ,users=users, messages = messages, sent_amount = sent_amount)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")







