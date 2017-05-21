"""Tests for Rendezvous Flask app."""

import unittest
import server


class RendezvousTests(unittest.TestCase):
    """Basic tests for my Rendezvous site app routes."""

    def setUp(self):
        """Code to run before every test."""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn("Rendezvous Home", str(result.data))

    def test_not_logged_in(self):
        """Do users who are not logged in see the correct view?"""

        result = self.client.get("/")
        self.assertIn("Click here to log in.", str(result.data))

    def test_logged_in(self):
        """Do logged-in users see the correct view?"""

        #FIXME:  need to figure out how to identify landing page when logged in

        #here is how we handled RSVP-ing in the testing exercise:
        # rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        # result = self.client.post("/rsvp", data=rsvp_info,
        #                           follow_redirects=True)
        # self.assertNotIn("<h2>Please RSVP</h2>", str(result.data))

        # self.assertIn("<h2>Party Details</h2>", str(result.data))

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

if __name__ == "__main__":
    unittest.main()
