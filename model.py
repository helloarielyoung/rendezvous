"""Models and database functions for Ariel's project - db Rendezvous."""

from flask_sqlalchemy import SQLAlchemy
# from helper_functions import *
import bcrypt

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
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    origin_lat = db.Column(db.String(12))
    origin_long = db.Column(db.String(12))

    #get all invitations for this user
    invites = db.relationship("Invitation",
                              secondary="users_invites",
                              backref="users")

    #pending invitations
    pending_invites = db.relationship("Invitation",
                                      secondary="users_invites",
                                      secondaryjoin="and_(User.user_id==UserInvite.user_id, "
                                      "UserInvite.status=='pen')",
                                      backref="pending_invite_users")

    active_invites = db.relationship("Invitation",
                                     secondary="users_invites",
                                     secondaryjoin="and_(User.user_id==UserInvite.user_id, "
                                     "UserInvite.status=='act')",
                                     backref="active_invite_users")

    rejected_invites = db.relationship("Invitation",
                                       secondary="users_invites",
                                       secondaryjoin="and_(User.user_id==UserInvite.user_id, "
                                       "UserInvite.status=='rej')",
                                       backref="rejected_invite_users")

    #get all relationships
    all_relationships = db.relationship("Relationship", foreign_keys='Relationship.user_id')
    # #necessary or desirable to have the inverse, when this user is "friend_id"??

    #get all active relationshps
    act_relationships = db.relationship("Relationship",
                                        primaryjoin="and_(User.user_id==Relationship.user_id, "
                                        "Relationship.status=='act')")

    #get friends data for active relationships
    active_friends = db.relationship("User",
                                     primaryjoin="and_(User.user_id==Relationship.user_id, "
                                     "Relationship.status=='act')",
                                     secondary="relationships", secondaryjoin="User.user_id==Relationship.friend_id")

    #get friends data for pending relationships
    pending_friends = db.relationship("User",
                                      primaryjoin="and_(User.user_id==Relationship.user_id, "
                                      "Relationship.status=='pen')",
                                      secondary="relationships", secondaryjoin="User.user_id==Relationship.friend_id")

    #get friends data for rejected relationships
    rejected_friends = db.relationship("User",
                                       primaryjoin="and_(User.user_id==Relationship.user_id, "
                                       "Relationship.status=='rej')",
                                       secondary="relationships", secondaryjoin="User.user_id==Relationship.friend_id")

    def __repr__(self):
        return "<User user_id=%s name=%s>" % (self.user_id, self.name)


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

    # get user info for this relationship
    usr = db.relationship("User", back_populates="all_relationships", foreign_keys='Relationship.user_id')

    #get friend info for this relationship
    friend = db.relationship("User", back_populates='all_relationships',
                             foreign_keys="Relationship.friend_id")

    def __repr__(self):
        return "<user_id=%s friend_id=%s>" % (self.user_id, self.friend_id)


class Invitation(db.Model):
    """Create invitations table."""

    __tablename__ = "invitations"

    invite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    destination_lat = db.Column(db.String(30), nullable=False)
    destination_lng = db.Column(db.String(30), nullable=False)
    rendezvous_date = db.Column(db.DateTime, nullable=False)
    rendezvous_name = db.Column(db.String(100), nullable=False)

    #get all users who are on this invitation
    invite_users = db.relationship("User",
                                   secondary="users_invites",
                                   backref="invitations")

    def __repr__(self):
        return "<Invitation invite_id=%s destination_lat=%s\
                 destination_lng=%s>" % (self.invite_id, self.destination_lat,
                                          self.destination_lng)


class UserInvite(db.Model):
    """Relate users to invitations.

    You cannot tell from here who invited who - see Invitation to find the
    created_by_id:  that is the person who created the Invitation"""

    __tablename__ = "users_invites"

    ui_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    invite_id = db.Column(db.Integer, db.ForeignKey('invitations.invite_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status = db.Column(db.String(3), db.ForeignKey('statuses.status_id'))
    created_date = db.Column(db.DateTime, nullable=False)

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
    # current_time = db.Column(db.DateTime, nullable=False)
    waypoint_lat = db.Column(db.String(17), nullable=False)
    waypoint_long = db.Column(db.String(17), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Waypoint waypoint_id=%s user_id=%s waypoint_lat=%s \
            waypoint_long=%s current_time=%s>" % (self.waypoint_id, self.user_id, self.waypoint_lat,
                                                  self.waypoint_long)

    #get user info for this waypoint
    waypoint_user = db.relationship('User')

    #get invititation info for this waypoint (includes destination)
    invites = db.relationship('Invitation',
                              backref='waypoints')

##############################################################################
# Helper functions


def example_data():
    """create some sample data for testing"""

    Invitation.query.delete()
    UserInvite.query.delete()
    Status.query.delete()
    User.query.delete()

    #populate statuses
    for status, descrip in [('pen', 'pending'),
                            ('rej', 'rejected'),
                            ('act', 'active'),
                            ('ina', 'inactive')]:
        rel = Status(status_id=status, status_description=descrip)
        db.session.add(rel)
    db.session.commit()

    #populate users
    u1 = User(user_id=1,
              name='Test User 1',
              email='user1@email.com',
              password=hash_pass('pass'))
    u2 = User(user_id=2,
              name='Test User 2',
              email='user2@email.com',
              password=hash_pass('pass'))
    u3 = User(user_id=3,
              name='Test User 3',
              email='user3@email.com',
              password=hash_pass('pass'))

    #create invitations
    invite1 = Invitation(invite_id=1,
                         created_by_id=1,
                         created_date='2017 05 09 9:00:00',
                         destination_lat=37.7888568,
                         destination_lng=-122.4115372,
                         #do I need datetime.datetime('2017 05 09')??
                         rendezvous_date='2017 05 12 09:00:00',
                         rendezvous_name='Outing with friends')

    invite2 = Invitation(invite_id=2,
                         created_by_id=1,
                         created_date='2017 05 09 9:00:00',
                         destination_lat=37.7888568,
                         destination_lng=-122.4115372,
                         #do I need datetime.datetime('2017 05 09')??
                         rendezvous_date='2017 05 19 11:00:00',
                         rendezvous_name="Starbucks with Joe")

    #add users to invitations with statuses
    ui1 = UserInvite(ui_id=1, invite_id=1, user_id=1, status='act', created_date='01/01/2017')
    ui2 = UserInvite(ui_id=2, invite_id=1, user_id=2, status='act', created_date='01/01/2017')
    ui3 = UserInvite(ui_id=3, invite_id=1, user_id=3, status='act', created_date='01/01/2017')

    db.session.add_all([u1, u2, u3])
    db.session.commit()

    db.session.add_all([invite1, invite2])
    db.session.commit()

    db.session.add_all([ui1, ui2, ui3])
    db.session.commit()


def connect_to_db(app, db_uri='postgresql:///rendezvous'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


#these are here instead of in server.py or helper_functions.py because of issues
#with needing to use them in multiple places and struggling to avoid problems
#run into when trying to import from server into model while importing from model
#into server.  This seemed the best solution.
def hash_pass(password):
    """Hashes passwords

    Note: this will only work right with passwords up to 72char.  Would have to
    add code to handle larger ones (see bcrypt documentation)
    """

    pswd = password.encode('utf-8')
    pw_hash = bcrypt.hashpw(pswd, bcrypt.gensalt())

    return pw_hash


def compare_hash(password_submitted, db_password):
    """Compare submitted password to hashed password in db and return T or F"""

    #how Agne did it (where password1 is submitted, and password2 is in db:
    # return bcrypt.hashpw(password1.encode('utf-8'), password2.encode('utf-8').decode() == password2)
    pswd = password_submitted.encode('utf-8')

    return bcrypt.checkpw(pswd, db_password.encode('utf-8'))


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
