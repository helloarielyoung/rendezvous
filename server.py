"""Rendezvous"""

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, render_template, redirect, request, flash, session, abort, json
import datetime
from model import User, Invitation, Waypoint, UserInvite, connect_to_db, db, hash_pass, compare_hash

import os

app = Flask(__name__)
map_api_key = os.environ["GOOGLE_JS_API_KEY"]

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

        return render_template('user.html', user=user)

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
    """Google map with animated routes populated from database.

    Only display to a logged in user
    """

    if session.get('user_id') is None:
        return redirect('/')

    else:
        user_id = session['user_id']

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

    {{'user_id': 'self', 'waypoints': [('lat', 'lng'), ('lat', 'lng')...]
      },
        {'userdata': {2: [('lat', 'lng'), ('lat', 'lng'),...],
                      3: [('lat', 'lng'), ('lat', 'lng'),...]
                      }
         }
     }
        (note:  jsonify turns the tuples into arrays in javaScript)

    """

    invite_id = request.args.get("invite_id")
    user_id = session['user_id']

    #query for logged in user's waypoints
    self_waypoints = db.session.query(Waypoint.waypoint_lat, Waypoint.waypoint_long).filter(Waypoint.invite_id == invite_id, Waypoint.user_id == user_id).order_by(Waypoint.waypoint_id).all()

    #populate dictionary for logged in user
    waypoints_for_self = {'user_id': 'self'}
    waypoints_for_self['waypoints'] = self_waypoints

    #populate dictoinary for all other users on this invitation
    # Get list of users for this invitation
    user_list = db.session.query(Waypoint.user_id).filter(Waypoint.invite_id == invite_id, Waypoint.user_id != user_id).distinct().all()
    user_list = [r[0] for r in user_list]
    # make dictionary with those keys/values and waypoints for that user
    waypoints_by_user = {'userdata': {}}

    # loop through list of users and query for waypoints with this invite id
    for user in user_list:
        waypoints_by_user['userdata'].setdefault(user, []).extend(db.session.query(Waypoint.waypoint_lat, Waypoint.waypoint_long).filter(Waypoint.invite_id == invite_id, Waypoint.user_id == user).order_by(Waypoint.waypoint_id).all())

    return jsonify(waypoints_for_self, waypoints_by_user)


@app.route('/rendezvous-map-v3', methods=['POST'])
def googlemapv2():
    """Google map with animated routes populated from database.

    Only display to a logged in user
    Receives user_id and invite_id and displays routes accordingly
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

    Use google maps autofill to select destination (capture that waypoint)
        (perhaps this is a link to a subsequent page then come back to invitation?)
    Select date & time for rendezvous_map
    Select Friends to invite

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
        user_friends = user.act_friends

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
        print "invitation saved"

        rendezvous_name = request.form.get("rendezvousName")
        rendezvous_date = request.form.get("rendezvousDateTime")
        rendezvous_friends = request.form.get("rendezvousFriends")
        user_id = session['user_id']
        destination_lat = str(request.form.get("destinationLat"))
        destination_lng = str(request.form.get("destinationLng"))

        # print json.loads(rendezvous_friends)
        # print rendezvous_name
        # print rendezvous_date

        #make an instance ov Invitation with that data...
        invite1 = Invitation(created_by_id=user_id,
                             created_date=datetime.datetime.now(),
                             destination_lat=destination_lat,
                             destination_lng=-destination_lng,
                             rendezvous_date=rendezvous_date,
                             rendezvous_name=rendezvous_name)

        db.session.add(invite1)
        db.session.flush()
        print invite1.invite_id

#         #add the user who created this invite to the ui table
        ui1 = UserInvite(invite_id=invite1.invite_id, user_id=user_id, status='act')
        db.session.add(ui1)

#         #add the other users
        for user in rendezvous_friends:
            ui = UserInvite(invite_id=invite1.invite_id, user_id=user, status='pen')
            db.session.add(ui)

#         #don't commit until they are all added without error
        db.session.commit()

        success = {'status': 'successful'}
        return jsonify(success)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')
