"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, DEFAULT_IMAGE_URL


app = Flask(__name__)
app.config["SECRET_KEY"] = 'ihbdsfihabsf'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


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
    image_url = (request.form['image-url-input']
        if request.form['image-url-input']
        else None)

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.get("/users/<int:user_id>")
def show_user_detail(user_id):
    """Show page with user details"""

    user = db.session.query(User).get_or_404(user_id)
    print("TEST user", user)

    return render_template(
        "user_detail.html",
        user=user,
        posts=user.posts)


@app.get("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Show page with user edit"""

    user = db.session.query(User).get_or_404(user_id)

    return render_template(
        "edit_user.html",
        user=user,
        posts=user.posts
    )


@app.post("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Process edit user details"""

    user = db.session.query(User).get(user_id)

    user.first_name = request.form['first-name-input']
    user.last_name = request.form['last-name-input']
    user.image_url = (request.form['image-url-input']
        if request.form['image-url-input']
        else DEFAULT_IMAGE_URL)

    db.session.commit()

    return redirect('/users')

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete user"""

    db.session.query(User).filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')


"""BLOG POST ROUTES"""


@app.get("/users/<int:user_id>/posts/new")
def show_add_post_form(user_id):
    """Show form to add new post"""

    user = db.session.query(User).get(user_id)

    return render_template('new_post.html', user=user)


@app.post("/users/<int:user_id>/posts/new")
def handle_add_form(user_id):
    """Add post to database and redirect to user detail"""

    title = request.form["title-input"]
    content = request.form["content-input"]

    new_post = Post(
        title=title,
        content=content,
        user_id=user_id,
        created_at=None)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """Show post on page"""

    post = db.session.query(Post).get(post_id)

    return render_template('post_detail.html', post=post)


@app.get('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """Show page with edit post form"""

    post = db.session.query(Post).get(post_id)

    return render_template('edit_post.html', post=post)


@app.post("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Process edit to post and redirect to post detail page"""

    post = db.session.query(Post).get(post_id)

    post.title = request.form['title-input']
    post.content = request.form['content-input']

    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.post("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete post"""

    post = db.session.query(Post).get(post_id)
    author_id = post.author.id

    db.session.query(Post).filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f"/users/{author_id}")
