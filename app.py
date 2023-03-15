"""Blogly application."""

import os

from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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


# @app.post("/users/new")
# def handle_add_user():


# @app.get("users/<user_id>")
# def show_user_detail():

#     return render_template("user_detail.html", user_id=user_id)


# @app.post("/users/<user_id>/edit")
# def handle_edit_user():


# @app.post("/users/<user_id>/delete")
# def delete_user():