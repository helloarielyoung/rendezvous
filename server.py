"""Rendezvous"""

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, render_template, redirect, request, flash, session

from model import User, Invitation, Waypoint, UserInvite, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "supersecretsecretkey2W00T"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/map-animate')
def map():
    """Homepage."""

    return render_template("map_animate_new_points.html")

@app.route('/map-directions')
def map_directions():
    """Homepage."""

    return render_template("mapbox-gl-directions.html")


@app.route('/map-steps')
def map_steps():
    """Homepage."""

    return render_template("request_directions_with_steps.html")


@app.route('/googlemap')
def googlemap():
    """Google map with animated route. Hardcoded version"""

    return render_template("google_maps_animation2.html")

@app.route('/googlemap2')
def googlemap2():
    """Google map with animated route. Database version"""

    user1data = db.session.query(Waypoint.waypoint_lat,
                               Waypoint.waypoint_long,
                               Waypoint.current_time).filter(Waypoint.user_id == 1,
                                                             Waypoint.invite_id == 1).all()

    user2data = db.session.query(Waypoint.waypoint_lat,
                                 Waypoint.waypoint_long,
                                 Waypoint.current_time).filter(Waypoint.user_id == 2,
                                 Waypoint.invite_id == 1).all()

    return render_template("google_maps_animation2.html", user1data=user1data, user2data=user2data)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    
    app.run(port=5000, host='0.0.0.0')
