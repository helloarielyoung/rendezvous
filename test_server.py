"""Tests for Rendezvous Flask app."""

from unittest import TestCase
from model import connect_to_db, db, example_data
from server import app, hash_pass
from flask import session


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
        """Do users make it to login page when clicking login link?"""

        result = self.client.get("/login")
        self.assertIn("Login Form", str(result.data))

    def test_registration_route(self):
        """Do users make it to registration page when clicking registration link?"""

        # Question:  Think I need to add GET something to this test
        # since the same route is used for POST of registration
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

        if not logged in, confirm cannot get to map

        """
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


class TestsLogInLogOut(TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

#Trouble:  cannot test login without a hashed password saved in example_data()
#but could not hash data in model.py because cross imports broke all...
    # def test_login(self):
    #     """Test log in form."""

    #     login_info = {'email': "user1@email.com", 'password': ("pass")}

    #     with self.client as c:
    #         result = c.post('/login',
    #                         data=login_info,
    #                         follow_redirects=True
    #                         )
    #         self.assertEqual(session['user_id'], '1')
    #         self.assertIn("Your User Profile", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['user_name'] = 'Test User 1'

            result = self.client.get('/logout',
                                     follow_redirects=True)

            self.assertNotIn('user_id', session)
            self.assertIn('You have logged out', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
