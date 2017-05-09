"""Models and database functions for Ariel's project - db Rendezvous."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of Rendezvous website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return "<User user_id=%s name=%s>" % (self.user_id, self.name)

    invites = db.relationship("Invitation",
                              secondary="users_invites",
                              backref="users")

    waypts = db.relationship("Waypoint")


class Invitation(db.Model):
    """Create invitations table"""

    __tablename__ = "invitations"

    invite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    destination_lat = db.Column(db.Integer, nullable=False)
    destination_long = db.Column(db.Integer, nullable=False)
    rendezvous_date = db.Column(db.DateTime, nullable=False)

    invite_users = db.relationship("User",
                            secondary="users_invites",
                            backref="invitations")

    def __repr__(self):
        return "<Invitation invite_id=%s destination_lat=%s\
                 destination_long=%s>" % (self.invite_id, self.destination_lat,
                                          self.destination_long)


class UserInvite(db.Model):
    """Relate users to invitations"""

    __tablename__ = "users_invites"

    ui_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    invite_id = db.Column(db.Integer, db.ForeignKey('invitations.invite_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return "<UsersInvites ui_id=%s invite_id=%s user_id=%s>" % (self.ui_id,
                                                                    self.invite_id,
                                                                    self.user_id)


class Waypoint(db.Model):
    """ Waypoints in database. """

    __tablename__ = "waypoints"

    waypoint_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    invite_id = db.Column(db.Integer, db.ForeignKey('invitations.invite_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    current_time = db.Column(db.DateTime, nullable=False)
    waypoint_lat = db.Column(db.Integer, nullable=False)
    waypoint_long = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Waypoint waypoint_id=%s user_id=%s waypoint_lat=%s \
            waypoint_long=%s current_time=%s>" % (self.waypoint_id, self.user_id, self.waypoint_lat,
                                                  self.waypoint_long, self.current_time)

    waypoint_user = db.relationship('User')

    invites = db.relationship('Invitation')


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///rendezvous'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
