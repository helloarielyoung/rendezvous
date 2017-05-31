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
      zoom: 13  ,
      mapTypeId: 'roadmap'
        });

    // add marker for destination point
    var marker = new google.maps.Marker({
    position: {'lat': center_lat, 'lng': center_lng },
    map: map,
    title: 'Rendezvous Here'
        });

//doesn't work becuase userLines isn't populated when the map is rendered....
    //animate the symbols
    for (var i=0; i<userLines.length; i++) {
        var count = 30;
        setTimeout(animateSymbol(userLines[i], count), 4500);
        count = count + 10;
      }    
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
            // Define symbol for this user
            var lineSymbol = {
              path: google.maps.SymbolPath.CIRCLE,
              scale: 4,
              strokeColor: pickColor
              };
         
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

            //use the pathListByUser to draw that user's route on the map
                  var userLine = new google.maps.Polyline({
                    path: pathListByUser,
                    strokeColor: userLineColor,
                    icons: [{
                       icon: lineSymbol,
                       offset: '0%'
                        }],
                     map: map
                      });

            //save userId and userLine so I can update icon position in realitme later
            userLines[thisUserId] = userLine;

               
            //END loop for waypoints for this user
              } 
// debugger
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

//END of dataReceived function
}

//later will use this to update the the current location of the user along their route
    // var thisUser = userLines[user_id][icons][0][icon]  and ??MAYBE [strokeColor]




// // Use the DOM setInterval() function to change the offset of the symbol
// // at fixed intervals.
var id1
function animateSymbol(line, speed) {
    var count = 0;
    id1 = window.setInterval(function() {
      count = (count + 1);

      var icons = line.get('icons');
      icons[0].offset = (count / 2) + '%';
      line.set('icons', icons);
    // make animation to stop at destination
    if (line.get('icons')[0].offset == "99.5%") {
          icons[0].offset = '100%';
          line.set('icons', icons);
          window.clearInterval(id1);

  } }, speed);
}