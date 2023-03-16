"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

DEFAULT_IMAGE_URL = "http://joelburton.com/joel-burton.jpg"

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Class to contain user info"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    first_name = db.Column(
        db.String(50),
        nullable = False
    )

    last_name = db.Column(
        db.String(50),
        nullable = False
    )

    image_url = db.Column(
        db.String(100),
        nullable = False,
        default = DEFAULT_IMAGE_URL
    )

    posts = db.relationship("Post", backref="author")

    @classmethod
    def get_all_users(cls):
        """Returns a list of all User instances"""

        return User.query.all()


class Post(db.Model):
    """Class to contain blog post info"""
    """Backref to User is 'author'"""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    title = db.Column(
        db.String(50),
        nullable = False
    )

    content = db.Column(
        db.Text,
        nullable = False
    )

    created_at = db.Column(
        db.DateTime,
        nullable = False,
        default = db.func.now()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )
