"use strict";

// Javascript for Rendezvous Map

//define the map and lines as global variables
var map;
var userLines = {};

// initialize the map
function initMap() {
    //initiates the map object
    map = new google.maps.Map(document.getElementById('map'), {
      center:  {'lat': center_lat, 'lng': center_lng },
      zoom: 14  ,
      mapTypeId: 'roadmap',
      mapTypeControl: false,
      streetViewControl: false,
      styles: [
    {
        "featureType": "administrative",
        "elementType": "labels.text.fill",
        "stylers": [{"color": "#444444"}]
    },
    {
        "featureType": "landscape",
        "elementType": "all",
        "stylers": [{"color": "#f2f2f2"}]
    },
    {
        "featureType": "landscape",
        "elementType": "geometry.fill",
        "stylers": [{"visibility": "on"}]
    },
    {
        "featureType": "landscape.man_made",
        "elementType": "geometry.fill",
        "stylers": [{"hue": "#ffd100"},
            {"saturation": "44"}]
    },
    {
        "featureType": "landscape.man_made",
        "elementType": "geometry.stroke",
        "stylers": [{"saturation": "-1"
            },
            {"hue": "#ff0000"}]
    },
    {
        "featureType": "landscape.natural",
        "elementType": "geometry",
        "stylers": [{"saturation": "-16"}]
    },
    {
        "featureType": "landscape.natural",
        "elementType": "geometry.fill",
        "stylers": [{"hue": "#ffd100"},
            {"saturation": "44"}]
    },
    {
        "featureType": "poi",
        "elementType": "all",
        "stylers": [{"visibility": "off"}]
    },
    {
        "featureType": "road",
        "elementType": "all",
        "stylers": [{"saturation": "-30"
            },
            {"lightness": "12"},
            {"hue": "#ff8e00"}]
    },
    {
        "featureType": "road.highway",
        "elementType": "all",
        "stylers": [{"visibility": "simplified"
            },
            {"saturation": "-26"}]
    },
    {
        "featureType": "road.arterial",
        "elementType": "labels.icon",
        "stylers": [{"visibility": "off"}]
    },
    {
        "featureType": "transit",
        "elementType": "all",
        "stylers": [{"visibility": "on"}]
    },
    {
        "featureType": "water",
        "elementType": "all",
        "stylers": [{"color": "#c0b78d"},
            {"visibility": "on"},
            {"saturation": "4"},
            {"lightness": "40"}]
    },
    {
        "featureType": "water",
        "elementType": "geometry",
        "stylers": [{"hue": "#ffe300"}]
    },
    {
        "featureType": "water",
        "elementType": "geometry.fill",
        "stylers": [{"hue": "#ffe300"},
            {"saturation": "-3"},
            {"lightness": "-10"}]
    },
    {
        "featureType": "water",
        "elementType": "labels",
        "stylers": [{"hue": "#ff0000"},
            {"saturation": "-100"},
            {"lightness": "-5"}]
    },
    {
        "featureType": "water",
        "elementType": "labels.text.fill",
        "stylers": [{"visibility": "off"}]
    },
    {
        "featureType": "water",
        "elementType": "labels.text.stroke",
        "stylers": [{"visibility": "off"}]
    }
]
    });

    // add marker for destination point
    var marker = new google.maps.Marker({
    position: {'lat': center_lat, 'lng': center_lng },
    map: map,
    title: 'Rendezvous Here'
    });

    //  make map dynamically resize when window is resized
    // google.maps.event.addDomListener(window, 'load', initialize);
    google.maps.event.addDomListener(window, "resize", function() {
     var center = map.getCenter();
     google.maps.event.trigger(map, "resize");
     map.setCenter(center); 
    });
}

// this waits until the page is loaded, queries the database for waypoint data
// for users on this invitation, then runs dataReceived
$(function() {
    $.get('/map-data.json', { invite_id }, dataReceived);
});

//this is the callback function after json data is received.
function dataReceived(results) {
    var allWaypoints = results['data'];

    var symbolColors = ['blue', 'purple', 'red', 'yellow'];
    var symbolColorCount = 0;  //for symbol color
    var userLineColor;  //for route polyline
    var iconColorCount = 0;  //for legend icon color
    //iterate through waypoints_by_user to get users
    for (var user in allWaypoints) {
        //Save this user id for later
        var thisUserId = allWaypoints[user]['id'];
        if (thisUserId == user_id) { //this is the logged in user
            var pickColor = 'white'; //white
        } else {
            pickColor = symbolColors[symbolColorCount];
            symbolColorCount++;
        }
     
        // variable to hold the waypoints for this user
        var pathListByUser = [];
        //iterate through waypoints to get path for this user
        for (var i=0; i<allWaypoints[user]['waypoints'].length; i++) {
            pathListByUser.push({'lat': parseFloat(allWaypoints[user]['waypoints'][i][0]),
                                 'lng': parseFloat(allWaypoints[user]['waypoints'][i][1])});

            //assign line color for logged in user
            if (thisUserId == user_id) {
                userLineColor = '#000000'; //black
            } else {userLineColor = '#999999';} //gray
      
        //END loop for waypoints for this user
        } 

    //Add line for this user to the map
    var userLine = new google.maps.Polyline({
        path: pathListByUser,
        strokeColor: userLineColor,
        icons: [{
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 4,
                strokeColor: pickColor
                },
            offset: '0%'
        }],
        map: map
    });
    //save user data so I can update icon position/legend in realitme later
    //format: {user_id: {'line': googlemap line object, 'name': user name,
    //    'eta_text': eta_text, 'eta_value': eta_value, 'symbolColor': color}} 
    userLines[thisUserId]= {
        'line': userLine, 'name': allWaypoints[user]['name'],
        'starting_eta_text': allWaypoints[user]['starting_eta_text'],
        'starting_eta_value': allWaypoints[user]['starting_eta_value'],
        'symbolColor': pickColor
    }

    //legend
    var iconBase = 'https://maps.google.com/mapfiles/kml/paddle/';
    var icons = {
        thisUserId: {
            name: userLines[thisUserId]['name'] + " - " + etaTime(userLines[thisUserId]['starting_eta_value']),
            icon: iconBase + changeColorName(userLines[thisUserId]['symbolColor']) +'-circle-lv.png'
        }
    };
    var legend = document.getElementById('legend');
    for (var key in icons) {
        var type = icons[key];
        var name = type.name;
        var icon = type.icon;
        var div = document.createElement('div');
        div.innerHTML = '<img src="' + icon + '"> ' + name;
        legend.appendChild(div);
    }
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(legend);

    //END loop for users in allWaypoints
    }

    //animate the symbols on the lines
    var lineSpeed = 40;
    for(var user in userLines){
        animateSymbol(userLines[user]['line'], lineSpeed, userLines[user]['name']);
        lineSpeed = lineSpeed + 40;
    }
//END of dataReceived function
}

// Animate the symbol. Offset 0=the begining of the polyline, 100=the end.
function animateSymbol(inputLine, inputSpeed, userName) {
    var id1;
    var count1 = 0;
    var line = inputLine;
    var speed = inputSpeed;

    id1 = setInterval(function() {
        count1 = (count1 + 1);
        var icons = line.get('icons');
        icons[0].offset = (count1 / 2) + '%';
        line.set('icons', icons);

        // make traffic alert for user3
        if ((userName == "Test User 3") && (count1 == 101)) {
            trafficAlert(userName);
        }
        // make animation to stop at destination
        if (parseInt(line.get('icons')[0].offset) > 99.5) {     
            icons[0].offset = '100%';  
            clearInterval(id1);
            // remove polyline from map when arrive
            line.setMap(null);          
            alert(userName + 'arrived!')
            // make a list of "active users" and delete from that list
            // when this happens and then call function that re-renders
            // legend based on users that are in the list?
        }
    }, speed);
// END animateSymbol
}

function trafficAlert (userName) {
    name = userName;
    alert (name + " has encountered traffic. 4 minute delay.");
}

function changeColorName (color) {
    var colors = {
        'white': 'wht',
        'blue': 'blu',
        'purple': 'purple',
        'red': 'red',
        'yellow': 'ylw',
        'default': 'blu'
    };
    return (colors[color] || colors['default']);
}

function timeNow() {
    var d = new Date(new Date().getTime()).toLocaleTimeString();//,
    return d;
}

function etaTime(etaValue) {
    var seconds = etaValue;
    var d = new Date(new Date().getTime() + seconds*1000).toLocaleTimeString();//,
    return d;
}