"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User



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

    return redirect("/users")


@app.get("/users")
def show_users():

    users = User.get_all_users()

    return render_template("/users.html", users=users)


@app.get("/users/new")
def show_add_user_form():

    return render_template("/new_user.html")


@app.post("/users/new")
def handle_add_user():

    first_name = request.form['first-name-input']
    last_name = request.form['last-name-input']
    image_url = request.form['image-url-input']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.get("/users/<int:user_id>")
def show_user_detail(user_id):
    user = db.session.query(User).get(user_id)

    first_name = user.first_name
    last_name = user.last_name
    image_url = user.image_url

    return render_template(
        "user_detail.html",
        first_name=first_name,
        last_name=last_name,
        image_url=image_url,
        user_id=user_id)


# @app.post("/users/<user_id>/edit")
# def handle_edit_user():


# @app.post("/users/<user_id>/delete")
# def delete_user():