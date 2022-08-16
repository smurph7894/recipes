from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class User:

    DB = "recipes"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name= data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipes = []

#Model SQL - Create
    @classmethod
    def create_user(cls,data):
        if not cls.validate_user_reg_data(data):
            return False
        data = cls.parse_registration_data(data)
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL(cls.DB).query_db(query,data)
        session['user_id'] = user_id
        session['user_name'] = f"{data['first_name']}"
        return True

#Model SQL - Read
    @classmethod
    def get_user_by_email(cls, email):
        data = { 'email' : email }
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            result = cls(result[0])
        return result

#Model SQL - Update


#Model SQL - Delete


#Static Methods
    @staticmethod
    def validate_user_reg_data(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2:
            flash ('Your first name needs to be at least two characters long.', 'registration')
            is_valid = False
        if len(data['last_name']) < 2:
            flash ('Your first name needs to be at least two characters long.', 'registration')
            is_valid = False
        if len(data['password']) < 8 : 
            flash('Your password needs to be at least eight characters long.', 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('please use a valid email address.', 'registration')
            is_valid = False
        if User.get_user_by_email(data['email'].lower().strip()):
            flash('that email is already in use.', 'registration')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash ("Your passwords don't match.", 'registration')
            is_valid = False
        return is_valid
        

    @staticmethod
    def parse_registration_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['email'] = data['email']
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data


    @staticmethod
    def login_user(data):
        this_user = User.get_user_by_email(data['email'])
        if this_user:
            print("got to this_user")
            print(this_user.password, data['password'])
            if bcrypt.check_password_hash(this_user.password, data['password']):
                print(this_user.password, data['password'])
                session['user_id'] = this_user.id
                session['user_name'] = f"{this_user.first_name}"
                return True
        flash('Your login failed.', 'login')
        return False