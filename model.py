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
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    origin_lat = db.Column(db.String(12))
    origin_long = db.Column(db.String(12))

    def __repr__(self):
        return "<User user_id=%s name=%s>" % (self.user_id, self.name)

    #get all invitations for this user
    invites = db.relationship("Invitation",
                              secondary="users_invites",
                              backref="users")

# FIX ME!
    # pending_invites = db.relationship("Invitation",
    #                                   secondary="and (User.user_id == UserInvite.user_id, "
    #                                   "UserInvite.status=='pen')",
    #                                   backref="users")

    #get all waypoints for this user - this is useless w/out invite info, right?
    waypts = db.relationship("Waypoint")

    # #get all my friends of any status
    all_relationships = db.relationship("Relationship", foreign_keys='Relationship.user_id')
    # #necessary or desirable to have the inverse, when this user is "friend_id"??

    #get all active relationships
    active_relationships = db.relationship("Relationship",
                                           primaryjoin="and_(User.user_id==Relationship.user_id, "
                                           "Relationship.status=='act')")


class Status(db.Model):
    """Create statuses table.

    Used by Relationship and UsersInvites

    """

    __tablename__ = "statuses"

    status_id = db.Column(db.String(3), primary_key=True)
    status_description = db.Column(db.String(15), nullable=False)


class Relationship(db.Model):
    """Create friend relationships table.

    user_id is the user who initiated the request for friendship
    request_date is only populated for user who initiated the request
    friend_id is the user they asked to be friends
    statuses:  "pen" means friend has not answered
               "act" means friend said yes - this action will create a second
               row in this table with user_id/friend_id reversed and request_date
               will be null.
               "rej" means friend rejected (user will not be able to request again)
               "ina" means one of the friends terminated the relationship

    """

    __tablename__ = "relationships"

    relationship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    request_date = db.Column(db.DateTime)
    status = db.Column(db.String(3), db.ForeignKey('statuses.status_id'), nullable=False)

    def __repr__(self):
        return "<user_id=%s friend_id=%s>" % (self.user_id, self.friend_id)

    # get user info for this relationship
    usr = db.relationship("User", back_populates="all_relationships", foreign_keys='Relationship.user_id')

    #get friend info for this relationship
    friend = db.relationship("User", back_populates='all_relationships',
                             foreign_keys="Relationship.friend_id")


class Invitation(db.Model):
    """Create invitations table."""

    __tablename__ = "invitations"

    invite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    destination_lat = db.Column(db.String(12), nullable=False)
    destination_long = db.Column(db.String(12), nullable=False)
    rendezvous_date = db.Column(db.DateTime, nullable=False)

    #get all users who are on this invitation
    invite_users = db.relationship("User",
                                   secondary="users_invites",
                                   backref="invitations")

    def __repr__(self):
        return "<Invitation invite_id=%s destination_lat=%s\
                 destination_long=%s>" % (self.invite_id, self.destination_lat,
                                          self.destination_long)


class UserInvite(db.Model):
    """Relate users to invitations.

    You cannot tell from here who invited who - see Invitation to find the
    created_by_id:  that is the person who created the Invitation"""

    __tablename__ = "users_invites"

    ui_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    invite_id = db.Column(db.Integer, db.ForeignKey('invitations.invite_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status = db.Column(db.String(3), db.ForeignKey('statuses.status_id'))

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
    waypoint_lat = db.Column(db.String(12), nullable=False)
    waypoint_long = db.Column(db.String(12), nullable=False)

    def __repr__(self):
        return "<Waypoint waypoint_id=%s user_id=%s waypoint_lat=%s \
            waypoint_long=%s current_time=%s>" % (self.waypoint_id, self.user_id, self.waypoint_lat,
                                                  self.waypoint_long, self.current_time)

    #get user info for this waypoint
    waypoint_user = db.relationship('User')

    #get invititation info for this waypoint (includes destination)
    invites = db.relationship('Invitation',
                              backref='waypoints')


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
