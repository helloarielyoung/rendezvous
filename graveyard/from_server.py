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

    return render_template("google_maps_animation.html")