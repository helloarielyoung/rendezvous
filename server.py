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
        if user.password == password:
            session['login'] = user.user_id
            session['user_name'] = user.name
            print session
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
    """Display user page"""

    user = User.query.get(user_id)

    return render_template('user.html', user=user)


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
        user = User(email=email,
                    name=name,
                    password=password)
        db.session.add(user)
        db.session.commit()
        flash("You are registered! Please login below.")

    return redirect("/login")


@app.route('/logout')
def logout():
    """logs out user"""

    del session['login']
    del session['user_name']

    flash("You are logged out")

    return redirect('/')


@app.route('/rendezvous-map')
def googlemap2():
    """Google map with animated routes populated from database.

    Only display to a logged in user
    """

    if session.get('login') is None:
        return redirect('/')

    else:
        login = session['login']

        selfquery = db.session.query(Waypoint.waypoint_lat,
                                      Waypoint.waypoint_long).filter(Waypoint.user_id == login,
                                                                     Waypoint.invite_id == 1).all()
        # This will have to be changed to accept the user id and the invtation
        # from session
        if login == 1:
            other = 2
        else:
            other = 1

        otherquery = db.session.query(Waypoint.waypoint_lat,
                                      Waypoint.waypoint_long).filter(Waypoint.user_id == other,
                                                                     Waypoint.invite_id == 1).all()

        center = db.session.query(Invitation.destination_lat,
                                  Invitation.destination_long).filter(Invitation.invite_id == 1).first()

        login = session['login']
        # to draw the polyline of route:
        # user1path = needs to be formated as: [{'lat': 37.748915, 'lng': -122.4181515},
             # {'lat': 37.7482293, 'lng': -122.4182139}]

        return render_template("rendezvous_map.html",
                               selfquery=selfquery,
                               otherquery=otherquery,
                               center=center,
                               login=login)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    
    app.run(port=5000, host='0.0.0.0')
