"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from sqlalchemy import update
#delete above import


app = Flask(__name__)
app.config["SECRET_KEY"] = 'ihbdsfihabsf'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.get("/")
def homepage():
    """Redirect to users list"""

    return redirect("/users")


@app.get("/users")
def show_users():
    """Show list of users"""

    users = User.get_all_users()

    return render_template("/users.html", users=users)


@app.get("/users/new")
def show_add_user_form():
    """Show page with form to create new user"""

    return render_template("/new_user.html")


@app.post("/users/new")
def handle_add_user():
    """Process new user request"""

    first_name = request.form['first-name-input']
    last_name = request.form['last-name-input']
    image_url = request.form['image-url-input']
    #implement conditional logic to catch empty string
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.get("/users/<int:user_id>")
def show_user_detail(user_id):
    """Show page with user details"""
    #implement get or 404 below
    user = db.session.query(User).get(user_id)
    print("TEST user", user)

    first_name = user.first_name
    last_name = user.last_name
    image_url = user.image_url

    return render_template(
        "user_detail.html",
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
        user_id=user_id)


@app.get("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Show page with user edit"""
    #get or 404
    user = db.session.query(User).get(user_id)

    return render_template(
        "edit_user.html",
        user=user)


@app.post("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Process edit user details"""

    user = db.session.query(User).get(user_id)

    user.first_name = request.form['first-name-input']
    user.last_name = request.form['last-name-input']
    user.image_url = request.form['image-url-input']

    db.session.commit()

    return redirect('/users')


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete user"""

    db.session.query(User).filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')



