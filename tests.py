import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        Post.query.delete()

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()


        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id


        test_post = Post(
            title="Test Title",
            content="Test content",
            user_id=test_user.id,
            created_at=None
        )

        db.session.add(test_post)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_list_users(self):
        """Test page showing list of users"""

        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)


    def test_new_user_page(self):
        """Test new user page is displayed"""

        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Create a user", html)


    def test_create_new_user(self):
        """Test creating a new user"""

        with self.client as c:
            resp = c.post(
                "/users/new",
                data={
                "first-name-input": "John",
                "last-name-input": "Wick",
                "image-url-input": f"{DEFAULT_IMAGE_URL}"
                }
            )
            self.assertEqual(resp.status_code, 302)
            jw = User.query.filter_by(first_name="John").one_or_none()
            self.assertEqual(jw.last_name, "Wick")
            self.assertEqual(jw.image_url, f"{DEFAULT_IMAGE_URL}")


    def test_show_user_detail(self):
        """Test display the user detail page"""

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- Test: user detail page -->", html)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)


    def test_user_edit_page(self):
        """Test user edit page is displayed"""

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("<h1>Edit a user</h1>", html)


    def test_edit_user(self):
        """Test handling edit user"""

        with self.client as c:
            resp = c.post(
                f"users/{self.user_id}/edit",
                data={
                    "first-name-input": "changed_first",
                    "last-name-input": "changed_last",
                    "image-url-input": ""
                })
            user = db.session.query(User).get(self.user_id)
            self.assertEqual(user.first_name, "changed_first")
            self.assertEqual(user.last_name, "changed_last")
            self.assertEqual(user.image_url, DEFAULT_IMAGE_URL)


    def test_delete_user(self):
        """Test deleting a user"""

        Post.query.delete()

        with self.client as c:
            resp = c.post(f"/users/{self.user_id}/delete")

            self.assertEqual(len(User.query.all()), 0)


    """TESTS FOR BLOG POST ROUTES"""

    def test_add_post_form(self):
        """Test displaying the add post form"""

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/posts/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Add Post for", html)


    def test_handle_add_form(self):
        """Test adding post to db"""

        with self.client as c:
            resp = c.post(
                f"/users/{self.user_id}/posts/new",
                data={
                "title-input": "Hai",
                "content-input": "Hello world!"
                }
            )
            self.assertEqual(resp.status_code, 302)
            test_post = Post.query.filter_by(title="Hai").one_or_none()
            self.assertEqual(test_post.content, "Hello world!")


    def test_show_post(self):
        """Test showing post on page"""

        first_post_id = Post.query.first().id

        with self.client as c:
            resp = c.get(f"/posts/{first_post_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Post Detail", html)


    def test_show_edit_post(self):
        """Test showing edit post form"""

        first_post_id = Post.query.first().id

        with self.client as c:
            resp = c.get(f"/posts/{first_post_id}/edit")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit Post", html)


    def test_edit_post(self):
        """Test editing a post in db"""

        first_post_id = Post.query.first().id

        with self.client as c:
            resp = c.post(
                f"posts/{first_post_id}/edit",
                data={
                    "title-input": "Edited Title",
                    "content-input": "Edited content",
                })

        post = Post.query.get(first_post_id)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(post.title, "Edited Title")
        self.assertEqual(post.content, "Edited content")

    def test_delete_post(self):
        """Test deleting a post from db"""

        first_post_id = Post.query.first().id

        with self.client as c:
            resp = c.post(
                f"/posts/{first_post_id}/delete",
                follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(Post.query.all()), 0)


