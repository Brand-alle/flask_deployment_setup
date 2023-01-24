# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
from flask_bcrypt import Bcrypt
from flask_app.models import message
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
bcrypt = Bcrypt(app)

class User:
    db = "private_wall_schema"
    def __init__(self,user):
        self.id = user["id"]
        self.first_name = user["first_name"]
        self.last_name = user["last_name"]
        self.email = user["email"]
        self.created_at = user["created_at"]
        self.updated_at = user["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        user_data = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in user_data:
            users.append( cls(user) )
        return users

    @classmethod 
    def get_by_id(cls,user_id): 
        data = {"id" : user_id}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email,password) VALUES ( %(first_name)s , %(last_name)s , %(email)s, %(password)s);"
        # data is a dictionary that will be passed into the save method from server.py
        endresult = connectToMySQL(cls.db).query_db(query, data)
        return endresult


    @classmethod
    def get_by_email(cls,email):
        data = {"log_email": email}
        query = "SELECT * FROM users WHERE email = %(log_email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    # fetches an existing user after authenticating
    def authenticated_user_by_input(cls, user_input):
        valid = True
        existing_user = cls.get_by_email(user_input["log_email"])
        password_valid = True
        if not existing_user:
            valid = False
        else:
            # Retrieve the hashed password to compare
            data = {
                "email": user_input["log_email"]
            }
            query = "SELECT password FROM users WHERE email = %(email)s;"
            hashed_pw = connectToMySQL(cls.db).query_db(query,data)[0]["password"]
            password_valid = bcrypt.check_password_hash(hashed_pw, user_input['password'])
            if not password_valid:
                valid = False
        if not valid:
            flash("That email & password combination does not match our records.", "login")
            return False
        return existing_user
    
    @classmethod
    def create_valid_user(cls, user):
        # Validate user
        if not cls.is_valid(user):
            return False
        # Hash password
        pw_hash = bcrypt.generate_password_hash(user['password'])
        user = user.copy()
        user["password"] = pw_hash
        print("User after adding pw: ", user)
        # Insert user into DB
        query = """
                INSERT into users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        new_user_id = connectToMySQL(cls.db).query_db(query, user)
        new_user = cls.get_by_id(new_user_id)
        return new_user


    @classmethod
    def is_valid(cls, user):
        is_valid = True # we assume this is true
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, user)
        if len(user["first_name"]) <= 0 or len(user["last_name"]) <= 0 or len(user["email"]) <= 0 or len(user["password"]) <= 0 or len(user["confirm_password"]) <= 0:
            flash("All fields are required, registration incomplete!", "registration")
            is_valid = False
        if (user['email']) == results:
            flash("Email already in use, registration incomplete", "registration")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("Please enter a Name with atleast 2 characters, registration incomplete!", "registration")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Please enter a Last Name with atleast 2 characters, registration incomplete!", "registration")
            is_valid = False
        if len(user['password']) < 8:
            flash("Please enter a password with atleast 8 characters, registration incomplete!", "registration")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email format, registration incomplete!", "registration")
            is_valid = False
        if len(user['email']) <= 0:
            flash("Please enter an email, registration incomplete!", "registration")
            is_valid = False
        if user["password"] != user["confirm_password"]:
            flash("Passwords do not match, please try registration again!", "registration")
            is_valid = False
        if not any(char.isupper() for char in user["password"]):
            flash("Password should have at least one uppercase letter!", "registration")
            is_valid = False
        if not any(char.isdigit() for char in user["password"]):
            flash("Password should have at least one number!", "registration")
            is_valid = False
        return is_valid