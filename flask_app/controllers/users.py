from flask_app import app
from flask import render_template, redirect, request
from flask_app.models import user, recipe
from flask_app.controllers import recipes
from flask import session


@app.route('/users/register', methods=["POST"])
def register_user():
    if user.User.create_user(request.form):
        return redirect('/recipes')
    return redirect ('/')

@app.route('/')
def login_page():
    return render_template ("index.html")


@app.route('/users/login', methods=['POST'])
def login_user():
    if user.User.login_user(request.form):
        return redirect ('/recipes')
    return redirect ('/')

@app.route('/users/logout')
def logout_user():
    session.clear()
    return redirect('/')