from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/sendmessage", methods=["POST"])
def sendmessage():
    if 'user_id' not in session:
        return redirect('/')
    if not Message.validate_send(request.form):
        return redirect("/dojo_wall")
    Message.save(request.form)
    return redirect("/dojo_wall")

@app.route("/destroy/message/<int:message_id>")
def deletepost(message_id):
    Message.delete(message_id)
    return redirect("/dojo_wall")

# @app.route("/post/newcomment", methods=["POST"])
# def newcomment():
#     if not Post.validate_comment(request.form):
#         return redirect("/dojo_wall")
#     Post.save_comment(request.form)
#     return redirect("/dojo_wall")