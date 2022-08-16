from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
from flask_app.models import user

bcrypt = Bcrypt(app)

class Recipe:

    DB = "recipes"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description= data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30_min = data['under_30_min']
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data['user_id']
        self.creator = None

    def cook_time_to_string_yes_no (self):
        if self.under_30_min == 1:
            return "Yes"
        else:
            return "No"
        
#Model - Recipes - Create
    @classmethod
    def create_recipe(cls,data):
        if not cls.validate_recipe_data(data):
            return False
        query = """
        INSERT INTO recipes (name, description, instructions, date_cooked, under_30_min, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s,%(date_cooked)s,%(under_30_min)s, %(user_id)s)
        ;"""
        recipe_id = connectToMySQL(cls.DB).query_db(query,data)
        session['recipe_id'] = recipe_id
        session['recipe_name'] = f"{data['name']}"
        return True

#Model - Recipes - Read
    @classmethod
    def recipe_with_creator(cls, id):
        data = { 'id' : id }
        query = """
        SELECT *
        FROM recipes
        JOIN users
        ON recipes.user_id = users.id
        WHERE recipes.id = %(id)s
        ;"""
        result = connectToMySQL(cls.DB).query_db(query, data)

        if result:
            row = result[0]
            this_recipe = cls(row)
            creator_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            this_recipe.creator = user.User(creator_data)
        return this_recipe
    
    @classmethod
    def all_recipes_with_creator(cls):
        query = """
        SELECT *
        FROM recipes
        JOIN users
        ON recipes.user_id = users.id
        ;"""
        result = connectToMySQL(cls.DB).query_db(query)

        all_recipes = []

        if result:
            for a_recipe in result:
                this_recipe = cls(a_recipe)
                creator_data = {
                    'id' : a_recipe['users.id'],
                    'first_name' : a_recipe['first_name'],
                    'last_name' : a_recipe['last_name'],
                    'email' : a_recipe['email'],
                    'password' : a_recipe['password'],
                    'created_at' : a_recipe['users.created_at'],
                    'updated_at' : a_recipe['users.updated_at']
                }
                this_recipe.creator = user.User(creator_data)
                all_recipes.append(this_recipe)
        return all_recipes

#Model - Recipes - Update
    @classmethod
    def update_recipe(cls, data):
        if not cls.validate_recipe_data(data):
            return False
        query = """
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_cooked=%(date_cooked)s, under_30_min = %(under_30_min)s
        WHERE id = %(id)s
        ;"""
        result =  connectToMySQL(cls.DB).query_db(query, data)
        return result != False

#Model - Recipes - Delete
    @classmethod
    def delete_recipe(cls, id):
        data = {'id' : id}
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db(query, data)

#Static Methods
    @staticmethod 
    def validate_recipe_data(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Your recipe name needs to be at least 3 characters.', 'recipe')
            is_valid=False
        if len(data['description']) < 3:
            flash('Your recipe description needs to be at least 3 characters.', 'recipe')
            is_valid=False
        if len(data['instructions']) < 3:
            flash('Your recipe instructions need to be at least 3 characters.', 'recipe')
            is_valid=False
        if len(data['date_cooked']) < 10:
            flash('You must enter a date cooked.', 'recipe')
            is_valid=False
        return is_valid
        