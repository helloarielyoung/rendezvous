"""Utility file to seed rendezvous database"""

from sqlalchemy import func
from model import User, Invitation, Waypoint, UserInvite

from model import connect_to_db, db
from server import app
import datetime


def load_users():
    """Load users into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Here's some test users
    user1 = User(user_id=1, name='Test User 1')
    user2 = User(user_id=2, name='Test User 2')
    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()


def load_invitations():
    """Load test invitation into database."""

    print "Invitations"

    Invitation.query.delete()

    invite1 = Invitation(invite_id=1, destination_lat=37.37901,
                         destination_long=-122.4070,
                         #do I need datetime.datetime('2017 05 09')??
                         rendezvous_date='2017 05 09')
    db.session.add(invite1)

    db.session.commit()


def load_waypoints():
    """Load test waypoints into database."""

    print "Waypoints"

    Waypoint.query.delete()

    #sample if doing manually:
    #waypoint1 = Waypoint(waypoint_id=1,
    #                     invite_id=1, user_id=1,
    #                     current_date = now,
    #                     waypoint+lat=some number, waypoint_long=some number)

    # probably going to want to do this from a file even
    # for my tiny sample data

    # for row in open("seed_data/u.data"):
    #     row = row.rstrip()
    #     user_id, movie_id, score, timestamp = row.split("\t")

    #     rating = Rating(user_id=user_id, movie_id=movie_id, score=score)

    #     db.session.add(rating)

    # db.session.commit()


def load_user_invites():
    """load relationship between users and invitations"""

    print "UserInvites"

    UserInvite.query.delete()

    ui1 = UserInvite(ui_id=1, invite_id=1, user_id=1)
    ui2 = UserInvite(ui_id=2, invite_id=1, user_id=2)
    db.session.add(ui1)
    db.session.add(ui2)

    db.session.commit()

# Need this?? Why was it only needed for User and not the other tables??

# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_invitations()
    load_waypoints()
    load_user_invites()
    # set_val_user_id()
