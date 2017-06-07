"""Utility file to seed rendezvous database"""

from sqlalchemy import func
from model import *

from server import app
from server import hash_pass

from helper_functions import *


def load_users():
    """Load users into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Here's some test users

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
    u4 = User(user_id=4,
              name='Test User 4',
              email='user4@email.com',
              password=hash_pass('pass'))

    u5 = User(user_id=5,
              name='Test User 5',
              email='user5@email.com',
              password=hash_pass('pass'))

    u6 = User(user_id=6,
              name='Test User 6',
              email='user6@email.com',
              password=hash_pass('pass'))

    u7 = User(user_id=7,
              name='Test User 7',
              email='user7@email.com',
              password=hash_pass('pass'))

    db.session.add_all([u1, u2, u3, u4, u5, u6, u7])

    db.session.commit()


def load_invitations():
    """Load test invitation into database."""

    print "Invitations"

    Invitation.query.delete()

    invite1 = Invitation(invite_id=1,
                         created_by_id=1,
                         created_date='2017 05 09 9:00:00',
                         destination_lat=37.7888754,
                         destination_lng=-122.411542,
                         #do I need datetime.datetime('2017 05 09')??
                         rendezvous_date='2017 06 07 09:00:00',
                         rendezvous_name='Girls Coffee Date',
                         rendezvous_location_name='Starbucks',
                         rendezvous_location_address='123 Street')

    invite2 = Invitation(invite_id=2,
                         created_by_id=1,
                         created_date='2017 05 15 9:00:00',
                         destination_lat=37.7888754,
                         destination_lng=-122.411542,
                         rendezvous_date='2017 06 07 18:00:00',
                         rendezvous_name='Dinner with Joe',
                         rendezvous_location_name='Test location 2',
                         rendezvous_location_address='345 Street')

    invite3 = Invitation(invite_id=3,
                         created_by_id=2,
                         created_date='2017 05 20 9:00:00',
                         destination_lat=37.7888754,
                         destination_lng=-122.411542,
                         rendezvous_date='2017 06 08 13:00:00',
                         rendezvous_name='Sue\'s Birthday',
                         rendezvous_location_name='Test location',
                         rendezvous_location_address='678 Street')

    invite4 = Invitation(invite_id=4,
                         created_by_id=3,
                         created_date='2017 05 20 9:00:00',
                         destination_lat=37.7888754,
                         destination_lng=-122.411542,
                         rendezvous_date='2017 06 08 15:00:00',
                         rendezvous_name='Drinks with Allison',
                         rendezvous_location_name='A Bar',
                         rendezvous_location_address='8910 Some Ave')

    invite5 = Invitation(invite_id=5,
                         created_by_id=3,
                         created_date='2017 05 20 9:00:00',
                         destination_lat=37.7888754,
                         destination_lng=-122.411542,
                         rendezvous_date='2017 06 09 15:00:00',
                         rendezvous_name='Out on the town',
                         rendezvous_location_name='A Hot Bar',
                         rendezvous_location_address='1010 Street')
    db.session.add_all([invite1, invite2, invite3, invite4, invite5])

    db.session.commit()


def load_user_invites():
    """load test relationships between users and invitations."""

    print "UserInvites"

    UserInvite.query.delete()

    # created by 1:
    ui1 = UserInvite(ui_id=1, invite_id=1, user_id=1, status='act', created_date='01/01/2017')
    ui2 = UserInvite(ui_id=2, invite_id=1, user_id=2, status='act', created_date='01/01/2017')
    ui3 = UserInvite(ui_id=3, invite_id=1, user_id=3, status='act', created_date='01/01/2017')

    #created by 1:
    ui4 = UserInvite(ui_id=4, invite_id=2, user_id=1, status='act', created_date='01/01/2017')
    ui5 = UserInvite(ui_id=5, invite_id=2, user_id=3, status='act', created_date='01/01/2017')
    ui6 = UserInvite(ui_id=6, invite_id=2, user_id=4, status='act', created_date='01/01/2017')
    ui7 = UserInvite(ui_id=7, invite_id=2, user_id=5, status='pen', created_date='01/01/2017')
    ui8 = UserInvite(ui_id=8, invite_id=2, user_id=2, status='rej', created_date='01/01/2017')
    #created by 2:
    ui9 = UserInvite(ui_id=9, invite_id=3, user_id=2, status='act', created_date='01/01/2017')
    ui10 = UserInvite(ui_id=10, invite_id=3, user_id=1, status='pen', created_date='01/01/2017')
    ui11 = UserInvite(ui_id=11, invite_id=3, user_id=3, status='rej', created_date='01/01/2017')
    ui12 = UserInvite(ui_id=12, invite_id=3, user_id=4, status='act', created_date='01/01/2017')
    ui13 = UserInvite(ui_id=13, invite_id=3, user_id=5, status='act', created_date='01/01/2017')

    # created by 3:
    ui14 = UserInvite(ui_id=14, invite_id=4, user_id=3, status='act', created_date='01/01/2017')
    ui15 = UserInvite(ui_id=15, invite_id=4, user_id=1, status='act', created_date='01/01/2017')
    ui16 = UserInvite(ui_id=16, invite_id=4, user_id=2, status='pen', created_date='01/01/2017')

   # created by 3:
    ui17 = UserInvite(ui_id=17, invite_id=5, user_id=3, status='act', created_date='01/01/2017')
    ui18 = UserInvite(ui_id=18, invite_id=5, user_id=1, status='rej', created_date='01/01/2017')
    ui19 = UserInvite(ui_id=19, invite_id=5, user_id=2, status='act', created_date='01/01/2017')

    db.session.add_all([ui1, ui2, ui3, ui4, ui5, ui6, ui7, ui8, ui9, ui10, ui11,
                        ui12, ui13, ui14, ui15, ui15, ui16, ui17, ui18, ui19])

    db.session.commit()


def load_status():
    """Load status table with statuses."""

    print "Statuses"

    Status.query.delete()

    for status, descrip in [('pen', 'pending'),  # has not been accepted/rejected
                            ('rej', 'declined'),  # declined
                            ('act', 'accepted'),  # accepted (or if self, sent out)
                            ('ina', 'cancelled')]:  # cancelled or finished
        rel = Status(status_id=status, status_description=descrip)
        db.session.add(rel)
    db.session.commit()


def load_relationships():
    """Load test relationships into database.

    Null request date means this record was created when user_id
    accepted friend request initiated by friend_id"""

    print "Relationshps"

    Relationship.query.delete()

    # active relationship
    rel1 = Relationship(user_id=1, friend_id=2, status='act', request_date='2017 05 09 09:00:00')
    rel2 = Relationship(user_id=1, friend_id=3, status='act', request_date='2017 05 09 09:00:00')
    rel3 = Relationship(user_id=2, friend_id=1, status='act')
    rel4 = Relationship(user_id=3, friend_id=1, status='act')
    rel7 = Relationship(user_id=3, friend_id=2, status='act', request_date='2017 05 09 09:00:00')
    rel8 = Relationship(user_id=2, friend_id=3, status='act')
    rel9 = Relationship(user_id=1, friend_id=6, status='act', request_date='2017 05 09 09:00:00')
    rel10 = Relationship(user_id=6, friend_id=1, status='act')
    # pending relationship
    rel5 = Relationship(user_id=1, friend_id=4, status='pen', request_date='2017 05 09 09:00:00')
    # rejected relationship
    rel6 = Relationship(user_id=1, friend_id=5, status='rej', request_date='2017 05 09 09:00:00')

    db.session.add_all([rel1, rel2, rel3, rel4, rel5, rel6, rel7, rel8, rel9, rel10])

    db.session.commit()


def load_waypoints():
    """Load test waypoints into database."""

# test addresses:
# '683 Sutter St San Francisco'
# '2340 Turk St San Francisco'
# '221 4th St San Francisco'
# '955 Howard St San Francisco'
# '299 Octavia St San Francisco'
# '2166 Chestnut St San Francisco'

    print "Waypoints"

    Waypoint.query.delete()

#need to add starting ETA to these
#starting_eta_text
#starting_eta_value

# 55 Francisco St San Francisco
    route1 = [{'lat': 37.8056759, 'lng': -122.4056522}, {'lat': 37.8056888, 'lng': -122.4054091}, {'lat': 37.8038687, 'lng': -122.4049994}, {'lat': 37.80419, 'lng': -122.4022693}, {'lat': 37.8039573, 'lng': -122.4020258}, {'lat': 37.7922635, 'lng': -122.3997971}, {'lat': 37.7908979, 'lng': -122.4106552}, {'lat': 37.7890236, 'lng': -122.4102744}, {'lat': 37.7888568, 'lng': -122.4115372}]

    for item in route1:
        waypoint_lat = item['lat']
        waypoint_long = item['lng']
        # current_time = item['time']

        waypoint = Waypoint(invite_id=1, user_id=1,
                            # current_time=current_time,
                            waypoint_lat=waypoint_lat,
                            waypoint_long=waypoint_long,
                            created_date='01/01/2017',
                            starting_eta_value=765,
                            starting_eta_text='13 mins')
        db.session.add(waypoint)

    db.session.commit()

#helper_functions.get_route_data('299 Octavia St San Francisco','683 Sutter st San Francisco')

    route2 = [{'lat': 37.7746434, 'lng': -122.4242785},
              {'lat': 37.7738748, 'lng': -122.4241174},
              {'lat': 37.7736814, 'lng': -122.42573},
              {'lat': 37.7746043, 'lng': -122.4259057},
              {'lat': 37.7752318, 'lng': -122.420976},
              {'lat': 37.7882861, 'lng': -122.423617},
              {'lat': 37.7899599, 'lng': -122.4104554},
              {'lat': 37.7890236, 'lng': -122.4102744},
              {'lat': 37.7888568, 'lng': -122.4115372}]


    for item in route2:
        waypoint_lat = item['lat']
        waypoint_long = item['lng']
        # current_time = item['time']

        waypoint = Waypoint(invite_id=1, user_id=2,
                            # current_time=current_time,
                            waypoint_lat=waypoint_lat,
                            waypoint_long=waypoint_long,
                            created_date='01/01/2017',
                            starting_eta_value=814,
                            starting_eta_text='14 mins')
        db.session.add(waypoint)

    db.session.commit()

# https://maps.googleapis.com/maps/api/directions/json?origin=221+4th+St+San+Francisco&destination=683+Sutter+St+San+Francisco&mode=driving&key=AIzaSyAQebJTWGOQmOsuTYscQ5bjCVjBenHOgC0get_route_data('221 4th St San Francisco','683 Sutter St San Francisco')
# '221 4th St San Francisco'
    route3 = [{'lat': 37.7831001, 'lng': -122.4025164},
              {'lat': 37.7820395, 'lng': -122.4011837},
              {'lat': 37.78380380000001, 'lng': -122.3989875},
              {'lat': 37.7879767, 'lng': -122.4035082},
              {'lat': 37.78982740000001, 'lng': -122.4038894},
              {'lat': 37.7888568, 'lng': -122.4115372}]

    for item in route3:
        waypoint_lat = item['lat']
        waypoint_long = item['lng']
        # current_time = item['time']

        waypoint = Waypoint(invite_id=1, user_id=3,
                            # current_time=current_time,
                            waypoint_lat=waypoint_lat,
                            waypoint_long=waypoint_long,
                            created_date='01/01/2017',
                            starting_eta_value=517,
                            starting_eta_text='9 mins')
        db.session.add(waypoint)

#helper_functions.get_route_data('299 Octavia St San Francisco','683 Sutter st San Francisco')

    route4 = [{'lat': 37.7746434, 'lng': -122.4242785},
              {'lat': 37.7738748, 'lng': -122.4241174},
              {'lat': 37.7736814, 'lng': -122.42573},
              {'lat': 37.7746043, 'lng': -122.4259057},
              {'lat': 37.7752318, 'lng': -122.420976},
              {'lat': 37.7882861, 'lng': -122.423617},
              {'lat': 37.7899599, 'lng': -122.4104554},
              {'lat': 37.7890236, 'lng': -122.4102744},
              {'lat': 37.7888568, 'lng': -122.4115372}]

    for item in route4:
        waypoint_lat = item['lat']
        waypoint_long = item['lng']
        # current_time = item['time']

        waypoint = Waypoint(invite_id=2, user_id=1,
                            # current_time=current_time,
                            waypoint_lat=waypoint_lat,
                            waypoint_long=waypoint_long,
                            created_date='01/01/2017',
                            starting_eta_value=814,
                            starting_eta_text='14 mins')
        db.session.add(waypoint)

    db.session.commit()

# https://maps.googleapis.com/maps/api/directions/json?origin=221+4th+St+San+Francisco&destination=683+Sutter+St+San+Francisco&mode=driving&key=AIzaSyAQebJTWGOQmOsuTYscQ5bjCVjBenHOgC0get_route_data('221 4th St San Francisco','683 Sutter St San Francisco')
#  get_route_data('221 4th St San Francisco','683 Sutter St San Francisco')
    route5 = [{'lat': 37.7831001, 'lng': -122.4025164},
              {'lat': 37.7820395, 'lng': -122.4011837},
              {'lat': 37.78380380000001, 'lng': -122.3989875},
              {'lat': 37.7879767, 'lng': -122.4035082},
              {'lat': 37.78982740000001, 'lng': -122.4038894},
              {'lat': 37.7888568, 'lng': -122.4115372}]

    for item in route5:
        waypoint_lat = item['lat']
        waypoint_long = item['lng']
        # current_time = item['time']

        waypoint = Waypoint(invite_id=2, user_id=3,
                            # current_time=current_time,
                            waypoint_lat=waypoint_lat,
                            waypoint_long=waypoint_long,
                            created_date='01/01/2017',
                            starting_eta_value=517,
                            starting_eta_text='9 mins')
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
    load_status()
    load_relationships()
    load_invitations()
    load_waypoints()
    load_user_invites()
    set_val_user_id()
    set_val_invitations()
    set_val_user_invites()
    set_val_waypoint_id()
