"use strict";

// Javascript for Rendezvous Map

//define the map and lines as global variables
var map;
var userLines = {};
var newUserLines = {};

// initialize the map
function initMap() {
    //initiates the map object
    map = new google.maps.Map(document.getElementById('map'), {
      center:  {'lat': center_lat, 'lng': center_lng },
      zoom: 13  ,
      mapTypeId: 'roadmap',
      mapTypeControl: false,
      streetViewControl: false
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
            //save userId and userLine so I can update icon position in realitme later
// current format:  {user_id: googlemap line object}
            userLines[thisUserId] = userLine;

            newUserLines[thisUserId]= {'line': userLine, 'name': allWaypoints[user]['name'],
           'eta_text': allWaypoints[user]['starting_eta_text'],
           'eta_value': allWaypoints[user]['starting_eta_value'],
           'symbolColor': pickColor}
            // newuserLines[thisUserId]['line'] = userLine;
            // newuserLines[thisUserId]['name'] = allWaypoints[user]['name'];
            // newuserLines[thisUserId][''] = userLine;
//change to: {user_id: {'line': googlemap line object, 'name': name,
        //    'eta_text': eta_text, 'eta_value': eta_value, 'symbolColor': color}}  
        //get name:    allWaypoints[user]['name']
        //get name:  pickColor

  //added allWaypoints[user]['starting_eta_text'] and allWaypoints[user]['starting_eta_value']
  // so should be able to push one (or both) of those into userLines along with 
  // the user name so both name and ETA can be updated on the Legend
            // can i change this to include the user name and their ETA without
             // breaking everything?
            // userLines[thisUserId] = [userLine, allWaypoints[user]['name', 'ETA']]
            // yes, this makes the user line:  userLines[<userID>][0]
            // and the name:  userLines[<userID>][1]
            // why did i want the user name in here?  so I can modify the legend, I think?
            // and use the name in an alert when that user arrives at destination

        //legend
            var iconColors = ['blu', 'purple', 'red', 'ylw'];
            if (thisUserId == user_id) {  //this is the logged in user
              var iconColor = 'wht';
            } else  { iconColor = iconColors[iconColorCount];
              iconColorCount +=1;
            }
            var iconBase = 'https://maps.google.com/mapfiles/kml/paddle/';
    // debugger       
            var icons = {
              thisUserId: {
                name: allWaypoints[user]['name'],
                icon: iconBase + iconColor +'-circle-lv.png'
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

//animate
var lineSpeed = 40;
for(var user in newUserLines)
{ 
animateSymbol(newUserLines[user]['line'], lineSpeed);
lineSpeed = lineSpeed + 50;
}

//END of dataReceived function
}

//later will use this to update the the current location of the user along their route
    // var thisUser = userLines[user_id][icons][0][icon]  and ??MAYBE [strokeColor]


// // Use the DOM setInterval() function to change the offset of the symbol
// // at fixed intervals.  offset 0=the begining of the polyline, 100=the end

function animateSymbol(inputLine, inputSpeed) {
    
    var id1;
    var count1 = 0;
    var line = inputLine;
    var speed = inputSpeed;

    id1 = setInterval(function() {
      count1 = (count1 + 1);
      var icons = line.get('icons');
      icons[0].offset = (count1 / 2) + '%';
      line.set('icons', icons);

    // make animation to stop at destination
      if (parseInt(line.get('icons')[0].offset) > 99.5) {     
            icons[0].offset = '100%';  
            clearInterval(id1);
            // remove polyline from map when arrive
            line.setMap(null);
    }
     }, speed);
    
}