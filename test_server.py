"""Tests for Rendezvous Flask app."""

import unittest
from model import connect_to_db, db#, example_data
from server import app
from flask import session


class TestsBasic(unittest.TestCase):
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

    def test_user_landing(self):
        """Does a user make it to their profile page after logging in?"""

        #FIXME:  this is going to need session data in the setup
        # to test logged in versus not logged in, right?

    def test_registration_route(self):
        """Do users make it to registration page when clicking registration link?"""

        # Question:  Think I need to add GET something to this test
        # since the same route is used for POST of registration
        result = self.client.get("/register")
        self.assertIn("Registration Form", str(result.data))

    def test_rendezvous_map_route(self):
        """Do users make it to the rendezvous map page from link?"""

        #FIXME -- make this a POST and it will work
        result = self.client.get("/rendezvous-map-v3")
        self.assertIn("Rendezvous Map", str(result.data))

        #This is going to have to be a lot more complex in future
        #since I only want users on an invitation to be able to see
        #shared map


class TestsLoggedIn(unittest.TestCase):
    """Tests for Rendezvous site app routes by logged in user."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        with self.client as c:
            with c.session_transaction() as sess:
                # sess['user_id'] = 1
                #pretty sure i need to use the session variable i set in server.py:
                sess['login'] = 1

    def test_logged_in(self):
        """Do logged-in users see the correct view on login?"""

        #FIXME:  need to figure out what pages to test
        #to make sure logged in users DO see them, and not-logged-in
        #users do not see them.

        #here is how we handled RSVP-ing in the testing exercise:
        # rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        # result = self.client.post("/rsvp", data=rsvp_info,
        #                           follow_redirects=True)
        # self.assertNotIn("<h2>Please RSVP</h2>", str(result.data))

        # self.assertIn("<h2>Party Details</h2>", str(result.data))



class TestsNotLoggedIn(unittest.TestCase):
    """Tests for Rendezvous site app routes by not-logged in user."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_not_logged_in(self):
        """Do users who are not logged in see the correct view?"""

        result = self.client.get("/")
        self.assertIn("Click here to log in.", str(result.data))


class TestsLogInLogOut(unittest.TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_login(self):
        """Test log in form."""

        login_info = {'email': "user1@email.com", 'password': "pass"}

        with self.client as c:
            result = c.post('/login',
                            data=login_info,
                            follow_redirects=True
                            )
            self.assertEqual(session['login'], '1')
            self.assertIn("Your User Profile", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['login'] = '1'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn('login', session)
            self.assertIn('You are logged out', result.data)


if __name__ == "__main__":
    unittest.main()
