"""Utility file to seed rendezvous database"""

from sqlalchemy import func
from model import User, Invitation, Waypoint, UserInvite, RelationshipStatus

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
    user1 = User(user_id=1,
                 name='Test User 1',
                 email='user1@email.com',
                 password='Mypassword1')
    user2 = User(user_id=2,
                 name='Test User 2',
                 email='user2@email.com',
                 password='Mypassword1')
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
                         rendezvous_date='2017 05 09 09:00:00')
    db.session.add(invite1)

    db.session.commit()


def load_user_invites():
    """load relationship between users and invitations."""

    print "UserInvites"

    UserInvite.query.delete()

    ui1 = UserInvite(ui_id=1, invite_id=1, user_id=1)
    ui2 = UserInvite(ui_id=2, invite_id=1, user_id=2)
    db.session.add(ui1)
    db.session.add(ui2)

    db.session.commit()


def load_rel_status():
    """Load relationship status table with statuses."""

    print "Relationship Status"

    RelationshipStatus.query.delete()

    for status, descrip in [('pen', 'pending'),
                            ('rej', 'rejected'),
                            ('act', 'active'),
                            ('ina', 'inactive')]:
        rel = RelationshipStatus(rel_status_id=status, rel_status_description=descrip)
        db.session.add(rel)
    db.session.commit()


def load_waypoints():
    """Load test waypoints into database."""

    print "Waypoints"

    Waypoint.query.delete()

    route1 = [
        {'lat': 37.748915, 'lng': -122.4181515, 'time': '2017 05 09 8:30:00'},
        {'lat': 37.7482293, 'lng': -122.4182139, 'time': '2017 05 09 8:30:10'},
        {'lat': 37.7496136, 'lng': -122.4041771, 'time': '2017 05 09 8:30:15'},
        {'lat': 37.7505216, 'lng': -122.4036993, 'time': '2017 05 09 8:30:25'},
        {'lat': 37.7519918, 'lng': -122.4030731, 'time': '2017 05 09 8:30:30'},
        {'lat': 37.7703559, 'lng': -122.4097319, 'time': '2017 05 09 8:30:35'},
        {'lat': 37.7740446, 'lng': -122.4143887, 'time': '2017 05 09 8:30:45'},
        {'lat': 37.7762332, 'lng': -122.4116211, 'time': '2017 05 09 8:30:50'},
        {'lat': 37.7788903, 'lng': -122.4149656, 'time': '2017 05 09 8:31:00'},
        {'lat': 37.7881866, 'lng': -122.4168552, 'time': '2017 05 09 8:31:15'}
        ]

    for item in route1:
        waypoint_lat = item['lat']
        waypoint_long = item['lng']
        current_time = item['time']

        waypoint = Waypoint(invite_id=1, user_id=1,
                            current_time=current_time,
                            waypoint_lat=waypoint_lat,
                            waypoint_long=waypoint_long)
        db.session.add(waypoint)

    db.session.commit()

    route2 = [{'lat': 37.7786337, 'lng': -122.4470632, 'time': '2017 05 09 8:30:15'},
              {'lat': 37.7848573, 'lng': -122.4475605, 'time': '2017 05 09 8:30:25'},
              {'lat': 37.7852903, 'lng': -122.4467609, 'time': '2017 05 09 8:30:30'},
              {'lat': 37.7899599, 'lng': -122.4104554, 'time': '2017 05 09 8:30:35'},
              {'lat': 37.7890236, 'lng': -122.4102744, 'time': '2017 05 09 8:30:50'},
              {'lat': 37.7881866, 'lng': -122.4168552, 'time': '2017 05 09 8:31:20'}]

    for item in route2:
        waypoint_lat = item['lat']
        waypoint_long = item['lng']
        current_time = item['time']

        waypoint = Waypoint(invite_id=1, user_id=2,
                            current_time=current_time,
                            waypoint_lat=waypoint_lat,
                            waypoint_long=waypoint_long)
        db.session.add(waypoint)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_invitations():
    """Set value for the next invite_id after seeding database"""

    # Get the Max invite_id in the database
    result = db.session.query(func.max(Invitation.invite_id)).one()
    max_id = int(result[0])

    # Set the value for the next invite_id to be max_id + 1
    query = "SELECT setval('invitations_invite_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_user_invites():
    """Set value for the next user_invite after seeding database"""

    # Get the Max ui_id in the database
    result = db.session.query(func.max(UserInvite.ui_id)).one()
    max_id = int(result[0])

    # Set the value for the next users_invites ui_id to be max_id + 1
    query = "SELECT setval('users_invites_ui_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_waypoint_id():
    """Set value for the next waypoint_id after seeding database"""

    # Get the Max waypoint_id in the database
    result = db.session.query(func.max(Waypoint.waypoint_id)).one()
    max_id = int(result[0])

    # Set the value for the next waypoint_id to be max_id + 1
    query = "SELECT setval('waypoints_waypoint_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_invitations()
    load_waypoints()
    load_user_invites()
    set_val_user_id()
    set_val_invitations()
    set_val_user_invites()
    set_val_waypoint_id()
