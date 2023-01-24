from flask_app import app
# import the class from friend.py
from flask_app.controllers import users, messages


if __name__ == "__main__":
    app.run(debug=True)