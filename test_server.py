"""Tests for Rendezvous Flask app."""

from unittest import TestCase
from model import User, connect_to_db, db, example_data, hash_pass, compare_hash
from server import app
from flask import session

# app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False


class TestsBasic(TestCase):
    """Basic tests for my Rendezvous site app routes."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn("Rendezvous Home", str(result.data))

    def test_login_route(self):
        """Can users make it to login page?"""

        result = self.client.get("/login")
        self.assertIn("Login Form", str(result.data))

    def test_registration_route(self):
        """Do users make it to registration page when clicking registration link?"""

        result = self.client.get("/register")
        self.assertIn("Registration Form", str(result.data))


class TestsLoggedIn(TestCase):
    """Tests app routes by logged in user."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
        app.config['SECRET_KEY'] = 'key'
        app.config['TESTING'] = True

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_rendezvous_map_route(self):
        """Do logged-in users make it to the rendezvous map page from link?

        if logged in, confirm can get to map

        """

        #without session user_id set above, this will fail
        map_data = {'center':  "{'lat': 37.7881866, 'lng': -122.4168552}",
                    'invite_id': 1,
                    'user_id': 1}

        with self.client as c:
            result = c.post('/rendezvous-map-v3',
                            data=map_data,
                            follow_redirects=True
                            )
        self.assertIn("Rendezvous Map", str(result.data))

    def test_other(self):
        """Test other routes that are different when logged in vs not-logged-in"""

        #FIXME:  need to figure out what pages to test
        #to make sure logged in users DO see them, and not-logged-in
        #users do not see them.

        #here is how we handled RSVP-ing in the testing exercise:
        # rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        # result = self.client.post("/rsvp", data=rsvp_info,
        #                           follow_redirects=True)
        # self.assertNotIn("<h2>Please RSVP</h2>", str(result.data))

        # self.assertIn("<h2>Party Details</h2>", str(result.data))


class TestsNotLoggedIn(TestCase):
    """Test app routes by not-logged in user."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_not_logged_in(self):
        """Do users who are not logged in see the correct view?"""

        result = self.client.get("/")
        self.assertIn("Click here to log in.", str(result.data))

    def test_rendezvous_map_route(self):
        """Can not-logged-in users make it to the rendezvous map page?

        if not logged in, confirm cannot get to map & are redirected home

        """

        #without session user_id set above, this will fail
        map_data = {'center':  "{'lat': 37.7881866, 'lng': -122.4168552}",
                    'invite_id': 1,
                    'user_id': 1}

        with self.client as c:
            result = c.post('/rendezvous-map-v3',
                            data=map_data,
                            follow_redirects=True
                            )

        self.assertNotIn("Rendezvous Map", str(result.data))
        self.assertIn("Rendezvous Home", str(result.data))

    def test_user_page(self):
        """Can not-logged-in users make it to Users page?

        If not logged in, confirm cannot get to /Users & are redirected home

        """

        #NEED TO MODIFY /login before this will be accurate
        #it should check that session data matches what is passed in post!
        login_info = {'email': "user1@email.com", 'password': "pass"}

        with self.client as c:
            result = c.post('/login',
                            data=login_info,
                            follow_redirects=True
                            )
            #add asserts here - NOT users, and IS homepage


class TestsLogInLogOut(TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """Test log in form."""

        # pswd = hash_pass("pass")
        login_info = {'email': "user1@email.com", 'password': "pass"}

        with self.client as c:
            result = c.post('/login',
                            data=login_info,
                            follow_redirects=True
                            )
            with c.session_transaction() as sess:
                # import pdb; pdb.set_trace()

                self.assertIn("Your User Profile", result.data)
                self.assertEqual(sess['user_id'], 1)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['user_name'] = 'Test User 1'

            result = self.client.get('/logout',
                                     follow_redirects=True)

            self.assertNotIn('user_id', session)
            self.assertNotIn('user_name', session)
            self.assertIn('You have logged out', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
