from flask_app import app
from flask import render_template, redirect, request
from flask_app.models import user, recipe
from flask_app.controllers import users
from flask import session

@app.route('/recipes')
def all_recipes():
    if not 'user_id' in session:
        return redirect('/')
    all_recipes = recipe.Recipe.all_recipes_with_creator()
    return render_template('recipes.html', all_recipes=all_recipes)

@app.route('/recipes/create', methods=["POST"])
def create_new_recipe():
    if recipe.Recipe.create_recipe(request.form):
        return redirect('/recipes')
    return redirect ('/recipes/new')

@app.route('/recipes/<int:id>')
def show_one_recipe(id):
    if not 'user_id' in session:
        return redirect('/')
    one_recipe = recipe.Recipe.recipe_with_creator(id)
    return render_template("show_recipe.html", one_recipe=one_recipe)

@app.route('/recipes/new')
def add_recipe():
    if not 'user_id' in session:
        return redirect('/')
    return render_template("add_recipe.html")

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if not 'user_id' in session:
        return redirect('/')
    recipe_info = recipe.Recipe.recipe_with_creator(id)
    return render_template("edit_recipe.html", recipe_info=recipe_info)

@app.route('/recipes/update', methods=["POST"])
def update_recipe():
    if recipe.Recipe.update_recipe(request.form):
        return redirect ('/recipes')
    return redirect (f"/recipes/edit/{request.form['id']}")

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    recipe.Recipe.delete_recipe(id)
    return redirect('/recipes')