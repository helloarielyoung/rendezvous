"""Rendezvous"""

from jinja2 import StrictUndefined, nodes
from jinja2.ext import Extension

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, render_template, redirect, request, flash, session, abort, json

#for time
import datetime
import pytz
import tzlocal

from helper_functions import *

from model import Status, User, Invitation, Waypoint, UserInvite, connect_to_db, db, hash_pass, compare_hash

#to convert unicode to literal string
import ast

import os

app = Flask(__name__)
map_api_key = os.environ["GOOGLE_JS_API_KEY"]
# session['google_key'] = map_api_key

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ["FLASK_APP_SECRET_KEY"]

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/login', methods=["GET"])
def login():
    """Display login form"""

    return render_template("login_form.html")


@app.route('/login', methods=["POST"])
def authenticate_login():
    """Authenticates user info and logs in if valid."""

    email = request.form.get("email")
    password = request.form.get("password")

    if User.query.filter_by(email=email).first() is not None:
        user = User.query.filter_by(email=email).first()

        if compare_hash(password, user.password):
            session['user_id'] = user.user_id
            session['user_name'] = user.name
            flash('You were successfully logged in')

            user_id = user.user_id
            return redirect('/users/' + str(user_id))
        else:
            flash('Bad password or user name')
            return redirect('/login')
    # we tried getting rid of what appears to be redundant else
    # but it did not work if it was valid email and bad password
    else:
        flash('Bad password or user name')
        return redirect('/login')


@app.route('/users/<user_id>')
def get_user(user_id):
    """Display user page if user data matches session data"""

    #check that user_id passed to route matches session data
    if session.get('user_id') == int(user_id):

        user = User.query.get(user_id)

        #in order to query for invites today or tomorrow
        #have not tested thoroughly, probably needs fine-tuning...
        ptz = pytz.timezone('US/Pacific')
        today = datetime.datetime.now(tz=ptz)
        tomorrow = today + + datetime.timedelta(days=1)
        today = "%s-%s-%s 00:00:00" % (today.year, today.month, today.day)

        #summary data of invites that:
        #   i created or was invited to
        #   that i accepted (status = 'act')
        #   that occur today or tomorrow
        imminent_invites_sum = db.session.query(UserInvite.status,
                                                UserInvite.invite_id,
                                                Invitation.rendezvous_name,
                                                Invitation.rendezvous_date,
                                                User.name,
                                                Invitation.rendezvous_location_name,
                                                Invitation.rendezvous_location_address,
                                                User.user_id)\
                                .join(Invitation, User)\
                                .filter(UserInvite.user_id == session['user_id'],
                                        UserInvite.status == 'act',
                                        Invitation.rendezvous_date >= today,
                                        Invitation.rendezvous_date <= tomorrow).all()

        #data of invites that:
        #   i created ("i" being the logged in user)
        #   only get user data for users who are not me
        #This gets ALL my invites - even ones i have cancelled (status = 'ina')
        stmt2 = db.text("SELECT i.invite_id,\
                                 i.rendezvous_name,\
                                 i.rendezvous_date,\
                                 i.rendezvous_location_name,\
                                 i.rendezvous_location_address,\
                                 i.created_by_id,\
                                 i.created_date,\
                                 ui.user_id,\
                                 ui.status,\
                                 statuses.status_description,\
                                 u.name,\
                                 u.email\
        FROM invitations i\
        JOIN users_invites ui on i.invite_id = ui.invite_id\
        JOIN statuses on ui.status = statuses.status_id\
        JOIN users u on u.user_id = ui.user_id and u.user_id != :user_id\
        WHERE i.created_by_id = :user_id\
        ORDER BY rendezvous_date, rendezvous_name, i.invite_id, statuses.status_description")

        stmt2 = stmt2.columns(Invitation.invite_id,
                              Invitation.rendezvous_name,
                              Invitation.rendezvous_date,
                              Invitation.rendezvous_location_name,
                              Invitation.rendezvous_location_address,
                              Invitation.created_by_id,
                              Invitation.created_date,
                              UserInvite.user_id,
                              UserInvite.status,
                              Status.status_description,
                              User.name,
                              User.email)
        all_my_invites = db.session.query(Invitation.invite_id,
            Invitation.rendezvous_name, Invitation.rendezvous_date,
            Invitation.rendezvous_location_name,
            Invitation.rendezvous_location_address, Invitation.created_by_id,
            Invitation.created_date, UserInvite.user_id, UserInvite.status,
            Status.status_description, User.name, User.email)\
            .from_statement(stmt2).params(user_id=session['user_id']).all()

        #summary data of invites that:
        #   i was invited to
        #   any status
        received_invites_sum = db.session.query(UserInvite.status,
                                                Status.status_description,
                                                UserInvite.invite_id,
                                                Invitation.rendezvous_name,
                                                Invitation.rendezvous_date,
                                                User.name,
                                                Invitation.rendezvous_location_name,
                                                Invitation.rendezvous_location_address,
                                                User.user_id)\
                                .join(Invitation, User, Status)\
                                .filter(UserInvite.user_id == session['user_id'],
                                        Invitation.created_by_id != session['user_id']).all()

        #Invitation Details Query
        #for invite_id, gather all the deets:
        #rendezvous_name, rendezvous_date, location_name, location_address,
        #created_by_id, created_by_name,
        #

        return render_template('user.html',
                               user=user,
                               imminent_invites_sum=imminent_invites_sum,
                               all_my_invites=all_my_invites,
                               received_invites_sum=received_invites_sum)

    else:
        flash('You must be logged in to access that page.')
        return redirect('/')


@app.route('/register', methods=["GET"])
def registration_form():
    """Display form to register new user."""

    return render_template("registration_form.html")


@app.route('/register', methods=["POST"])
def register_process():
    """Create new user from registration form."""

    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    # check if email exists, and if not add to DB
    if User.query.filter_by(email=email).first() is not None:
        flash("You already have an account!")

    else:
        # hash password before storing
        password = hash_pass(password)
        user = User(email=email,
                    name=name,
                    password=password)
        db.session.add(user)
        db.session.commit()
        flash("You are now registered! Please login below.")

    return redirect("/login")


@app.route('/logout')
def logout():
    """logs out user"""

    del session['user_id']
    del session['user_name']

    flash("You have logged out")

    return redirect('/')


@app.route('/rendezvous-map')
def googlemap2():
    """This is a demo map - Google map with animated routes populated from database.

    """

    if session.get('user_id') is None:
        return redirect('/')

    else:
        user_id = session['user_id']
        # this is for the demo map (rendezvous_map.html)
        selfquery = db.session.query(Waypoint.waypoint_lat,
                                     Waypoint.waypoint_long).filter(Waypoint.user_id == user_id,
                                                                    Waypoint.invite_id == 1).all()
        # This will have to be changed to accept the user id and the invtation
        # from session
        if user_id == 1:
            other = 2
        else:
            other = 1

        otherquery = db.session.query(Waypoint.waypoint_lat,
                                      Waypoint.waypoint_long).filter(Waypoint.user_id == other,
                                                                     Waypoint.invite_id == 1).all()
        center = db.session.query(Invitation.destination_lat,
                                  Invitation.destination_lng).filter(Invitation.invite_id == 1).first()
        user_id = session['user_id']
        # to draw the polyline of route:
        # user1path = needs to be formated as: [{'lat': 37.748915, 'lng': -122.4181515},
             # {'lat': 37.7482293, 'lng': -122.4182139}]
        return render_template("rendezvous_map.html",
                               selfquery=selfquery,
                               otherquery=otherquery,
                               center=center,
                               user_id=user_id,
                               map_api_key=map_api_key)


@app.route('/map-data.json', methods=["GET"])
def map_data():
    """returns waypoint data by user_id for this invite_id in json

    data is grouped by user_id and sorted by current_time

    format of returned data is:

    {'data': [{'id': #, 'waypoints': [[lat, lng],[lat,lng]], 'name':name}, .....]}
        (note:  jsonify turns the tuples into arrays in javaScript)

    """

    invite_id = request.args.get("invite_id")

    # dictionary to hold the waypoints for all users
    all_waypoints = {'data': []}

    #list of ALL users on this invite
    users_list = db.session.query(Waypoint.user_id).filter(Waypoint.invite_id == invite_id).distinct().all()
    #is this step necessary?  think the id will be a tuple if not done
    users_list = [i[0] for i in users_list]

    for user in users_list:
        user_dict = {'id': 0, 'name': '', 'waypoints': []}
        user_dict['id'] = user
        user_dict['name'] = User.query.get(user).name
        user_dict['starting_eta_text'] = db.session.query(Waypoint.starting_eta_text).filter(Waypoint.invite_id == invite_id, Waypoint.user_id == user).first()
        user_dict['starting_eta_value'] = db.session.query(Waypoint.starting_eta_value).filter(Waypoint.invite_id == invite_id, Waypoint.user_id == user).first()
        user_dict['waypoints'] = db.session.query(Waypoint.waypoint_lat, Waypoint.waypoint_long).filter(Waypoint.invite_id == invite_id, Waypoint.user_id == user).order_by(Waypoint.waypoint_id).all()
        #append all the users dictionaries to all_waypoints
        all_waypoints['data'].append(user_dict)

    return jsonify(all_waypoints)


@app.route('/rendezvous-map-v3', methods=['POST'])
def googlemapv2():
    """Google map with animated routes.

    Only display to a logged in user
    Receives user_id and invite_id and passes back the center point of that invite.
    The route data is acquired by the page using an AJAX request to '/map-data.json'
    """

    #make sure you cannot get here if not logged in:
    if session.get('user_id') is None:
        return redirect('/')

    else:
        # this may be bad form:  got "user_id" from session in user.html...
        user_id = request.form.get("user_id")
        invite_id = request.form.get("invite_id")

        center = db.session.query(Invitation.destination_lat,
                                  Invitation.destination_lng).filter(Invitation.invite_id == invite_id).first()

                  # Invitation.query.get(invite_id).waypoints  # ?? will this be a query of all the invitation objects?
                    #and then iterate through it in HTML picking out each
                    #user's route and assigning colors based on whether waypoint.user_id
                    # equals user_id or not?

        return render_template("rendezvous_map_v3.html",
                               center=center,
                               invite_id=invite_id,
                               user_id=user_id,
                               map_api_key=map_api_key)


@app.route('/invitation-new')
def invitation_new():
    """Page to create a new invitation.

    """

    #only get here if you are logged in
    if session.get('user_id') is None:
        flash("You must be logged in to access this page")
        return redirect('/')

    else:
        user_id = session['user_id']
        user = User.query.get(user_id)
        #returns a list of User objects that are the user's active friends
        # user.act_friends[0].name gets the name of first friend in list of active friends
        user_friends = user.active_friends

        return render_template("invitation_new.html",
                               map_api_key=map_api_key,
                               user_friends=user_friends)


@app.route('/invitation-save.json', methods=['POST'])
def invitation_save():
    """Save invitation data to the database"""

# need to add test (and manuall test this!)
    if session.get('user_id') is None:
        # flash('You must be logged in to access that page')
        return abort(400)

    else:
        # print "invitation saved"
        rendezvous_name = request.form.get("rendezvousName")
        rendezvous_date = request.form.get("rendezvousDateTime")
        rendezvous_friends = request.form.get("rendezvousFriends")
        destination_lat = request.form.get("destinationLat")
        destination_lng = request.form.get("destinationLng")
        rendezvous_location_name = request.form.get("rendezvousLocationName")
        rendezvous_location_address = request.form.get("rendezvousLocationAddress")

        user_id = session['user_id']
        created_date = datetime.datetime.now()

        #make an instance of Invitation with that data...
        invite1 = Invitation(created_by_id=user_id,
                             created_date=created_date,
                             destination_lat=destination_lat,
                             destination_lng=destination_lng,
                             rendezvous_date=rendezvous_date,
                             rendezvous_name=rendezvous_name,
                             rendezvous_location_name=rendezvous_location_name,
                             rendezvous_location_address=rendezvous_location_address)

        db.session.add(invite1)
        db.session.flush()
        # print invite1.invite_id

        #add the user who created this invite to the ui table
        ui1 = UserInvite(invite_id=invite1.invite_id, user_id=user_id, status='act', created_date=created_date)
        db.session.add(ui1)

        #add the other users
        rendezvous_friends = ast.literal_eval(rendezvous_friends)

        # print type(rendezvous_friends)
        for user in rendezvous_friends:
            user_id = user
            print user_id
            ui = UserInvite(invite_id=invite1.invite_id, user_id=user_id, status='pen', created_date=created_date)
            db.session.add(ui)

#         #don't commit until they are all added without error
        db.session.commit()

        success = {'status': 'successful'}
        return jsonify(success)

# don't need this I don't think = just putting deets & accept/decline buttons
# on the users page
# @app.route('/invitation-pending-manage')
# def invitation_manage_pending():
#     """Accept or reject pending invitations"""

#     if session.get('user_id') is None:
#         return redirect('/')

#     else:
#         user_id = session["user_id"]
#         invite_id = request.form.get("invite_id")

#         return render_template("invitation_manage_pending.html",
#                                 user_id=user_id,
#                                 invite_id=invite_id)


@app.route('/invitation-change-status.json', methods=['POST'])
def invitation_update():
    """Update invitation as accepted or rejected"""

# need to add test (and manuall test this!)
    if session.get('user_id') is None:
        # flash('You must be logged in to access that page')
        return abort(400)

    else:
        invite_id = int(request.form.get("invite_id"))
        user_id = session['user_id']
        status = request.form.get("invite_submit_button")

        if status == "Pending":
            status_id = "pen"
        elif status == "Accept":
            status_id = "act"
        elif status == "Cancel":
            status_id = "ina"
        elif status == "Decline":
            status_id = 'rej'

        if status == 'ina':
            #user who created this invite is cancelling it, need to update
            #status for all users on the invitation
            db.session.query(UserInvite).filter(UserInvite.invite_id == invite_id).update({UserInvite.status: status_id}, synchronize_session=False)
        else:
            invite_to_update =\
                UserInvite.query.filter(UserInvite.user_id == user_id,
                                        UserInvite.invite_id == invite_id).one()

            invite_to_update.status = status_id

        db.session.commit()

        #to send confirmation message back
        invite_name = db.session.query(Invitation.rendezvous_name).filter(Invitation.invite_id == invite_id).first()
        flash("Invitation \'" + invite_name[0] + "\'' status changed to " + status)

        return redirect(redirect_url())


# Helper Functions
def redirect_url(default='index'):
    """redirect user back to page they came from"""
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')
