# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask_app.models import user
from flask import flash, session
import re	# the regex module
# create a regular expression object that we'll use later
import math 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Message:
    db = "private_wall_schema"
    def __init__(self,db_data):
        self.id = db_data["id"]
        self.content = db_data["content"]
        self.sender = db_data["sender_id"]
        self.recipient = db_data["recipient_id"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]

    @classmethod
    def get_messages(cls,user_id):
        recipient = user.User.get_by_id(user_id)
        query = "SELECT messages.*, first_name, last_name, email, senders.created_at as sender_created_at, senders.updated_at as sender_updated_at FROM messages JOIN users as senders on messages.sender_id = senders.id WHERE recipient_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,{"id": user_id})
        print(results)
        # all_the_messages = cls(results[0])
        messages = []
        for message in results:
            # Create a Tweet class instance from the information from each db row
            sender_data = {
                "id": message["sender_id"],
                "first_name": message["first_name"],
                "last_name": message["last_name"],
                "email": message["email"],
                "created_at": message["sender_created_at"],
                "updated_at": message["sender_updated_at"]
            }
            sender = user.User(sender_data)
            message = {
                "id": message["id"],
                "content": message["content"],
                "sender_id": sender,
                "recipient_id": recipient,
                "created_at": message["created_at"],
                "updated_at": message["updated_at"],
            }
            # Prepare to make a User class instance, looking at the class in models/user.py
            # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
            # Create the User class instance that's in the user.py model file
            # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
            # Append the Tweet containing the associated User to your list of tweets
            messages.append(cls(message))
        return messages

    @classmethod
    def get_sent_messages(cls,user_id):
        query ="SELECT * FROM messages WHERE sender_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,{"id": user_id})
        print(results)
        return results


    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (content, created_at, sender_id, recipient_id, user_id) VALUES ( %(content)s , NOW(), %(sender_id)s, %(recipient_id)s, %(user_id)s);"
        # data is a dictionary that will be passed into the save method from server.py
        endresult = connectToMySQL(cls.db).query_db(query, data)
        return endresult

    @classmethod
    def delete(cls,message_id):
        query  = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, {"message_id" : message_id})

    @classmethod
    def validate_send(cls,post):
        is_valid = True # we assume this is true
        if len(post['content']) <= 0:
            flash("Message may not be blank!", "sendmessage")
            is_valid = False
        return is_valid
    @classmethod
    def validate_comment(cls,post):
        is_valid = True # we assume this is true
        if len(post['content']) <= 0:
            flash("Post may not be blank!", "newcomment")
            is_valid = False
        return is_valid

    def time_span(self):
        print(self.created_at)
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"