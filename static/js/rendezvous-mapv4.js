"use strict";

// Javascript for Rendezvous Map v3

//define the map and lines as global variables
var map;
var selfLine;
var userLines = {};
var symbolColors;

// this waits until the page is loaded, queries the database for waypoint data
// for users on this invitation, then runs dataReceived

$(function() {
    $.get('/map-data.json', { invite_id }, dataReceived);
    });

//this is the callback function after json data is received.
function dataReceived(results) {
    console.log("inside js v4")
// this will change to results['data'][0] when I am no longer sending the self & other waypoints lists
    var allWaypoints = results[2]['data'];

        symbolColors = ['blue', 'purple', 'red', 'yellow'];
        var colorCount = 0;
        var userLineColor;
        //iterate through waypoints_by_user to get users
        for (var user in allWaypoints) {
            //Save this user id for later
            var thisUserId = allWaypoints[user]['id'];
            if (thisUserId == user_id) { //this is the logged in user
                var pickColor = '#000000'; //black
            } else {
                pickColor = symbolColors[colorCount];
                colorCount++;
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
                  pathListByUser.push({'lat': parseFloat(allWaypoints[user]['waypoints'][0]),
                                     'lng': parseFloat(allWaypoints[user]['waypoints'][1])});

                  //assign line color for logged in user
                  if (thisUserId == user_id) {
                      userLineColor = '#000000'; //black
                  } else {userLineColor = '#999999';} //gray

            //use th pathListByUser to draw that user's route on the map
            var userLine = new google.maps.Polyline({
              path: pathListByUser,
              strokeColor: userLineColor,
              icons: [{
                 icon: lineSymbol,
                 offset: '0%'
                  }],
               map: map
                });

            //save userId and userLine in an object so I can update position
            //of the icon later
            userLines[thisUserId] = userLine;                     
            //END loop for waypoints for this user
              } 
        //END loop for users in waypointsByUser
          }
          console.log("end of return function");
}

//later will use this to update the the current location of the user along their route
    // var thisUser = userLines[user_id][icons][0][icon]  ??MAYBE [strokeColor]

// initialize the map
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {

      // change this to get the center point from the ajax call that's getting
      // the waypoints stuff

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
      }
 
// debugger
// why is userLines empty here when it is populated outside this function?
// is it because dataReceived actually runs after this because it's waiting
// for whole page to load?!!

//     animateSymbol(selfLine, count);
//     //animates the movement of the Symbols
//     for (var i in userLines) {
//       alert(i);
//       var count = 30;
//       setTimeout(animateSymbol(userLines[i], count), 4500);
//       count = count + 10;
//       } 
//     }

// // Use the DOM setInterval() function to change the offset of the symbol
// // at fixed intervals.
// var id1
// function animateSymbol(line, speed) {
//     var count = 0;
//     id1 = window.setInterval(function() {
//       count = (count + 1);

//       var icons = line.get('icons');
//       icons[0].offset = (count / 2) + '%';
//       line.set('icons', icons);
//     // make animation to stop at destination
//     if (line.get('icons')[0].offset == "99.5%") {
//           icons[0].offset = '100%';
//           line.set('icons', icons);
//           window.clearInterval(id1);

//   } }, speed);
// }