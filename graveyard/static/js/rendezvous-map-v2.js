"use strict";

// Javascript for Rendezvous Map v3

document.addEventListener('DOMContentLoaded', function () {
  if (document.querySelectorAll('#map').length > 0)
  {
    if (document.querySelector('html').lang)
      lang = document.querySelector('html').lang;
    else
      lang = 'en';

    var js_file = document.createElement('script');
    js_file.type = 'text/javascript';
    js_file.src = 'https://maps.googleapis.com/maps/api/js?callback=initMap&key=AIzaSyAQebJTWGOQmOsuTYscQ5bjCVjBenHOgC0&language=' + lang;
    document.getElementsByTagName('head')[0].appendChild(js_file);
  }
});

//define the map and lines as global variables
var map;
var selfLine;
var userLines = {};
var symbolColors;

// this waits until the page is loaded, queries the database for waypoint data
// for users on this invitation, then runs dataReceived
$(function() {
    $.get('/map-data.json', { invite_id: {{ invite_id }} }, dataReceived);
    });

//this is the callback function after json data is received.
//   it divies up the json into a separate object for self and
//   for others.  Draws the initial routes for all users on invite
//   and puts different colored icons on their starting points
function dataReceived(results) {
      // logged in user:
      waypointsForSelf = results[0]['waypoints'];
      var waypointsForSelfLength = waypointsForSelf.length;

      // all other users on this invite:
      waypointsByUser = results[1]['userdata'];
      var waypointsByUserLength = Object.keys(waypointsByUser).length;

      // Define symbol for logged in user
      var selfLineSymbol = {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 4,
        // logged in user has a green dot
        strokeColor: '#393'
          };

      var selfPathList = []
      for (var i = 0; i < waypointsForSelfLength; i++) {
        selfPathList.push({'lat': parseFloat(waypointsForSelf[i][0]),
                          'lng': parseFloat(waypointsForSelf[i][1])});
          }

      // Create the polyline for logged in user
      selfLine = new google.maps.Polyline({
      path: selfPathList,
        //logged in user has a black line
        strokeColor: '#000000',
        icons: [{
          icon: selfLineSymbol,
          offset: '0%'
          }],
        map: map
        });
      userLines[ {{ session.login }} ] = selfLine;

      // colors for the not-the-logged-in-users' symbols
      //                   purple, orange, tomato, darkturquoise
      symbolColors = ['#a862ea', '#ff944d', '#ff6347', '#00CED1'];
          var colorCount = 0;
          //iterate through waypoints_by_user to get users
          for (var user in waypointsByUser) {
              //Save this user id for later
              var thisUserId = user;
              var pickColor = symbolColors[colorCount];
              colorCount++;
              // Define symbol for this user
              var userLineSymbol = {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 4,
                strokeColor: pickColor
                };
           
              // variable to hold the waypoints
              var pathListByUser = [];

              //iterate through waypoints to get path for this user
              for (var i=0; i<waypointsByUser[user].length; i++) {
                  pathListByUser.push({'lat': parseFloat(waypointsByUser[user][i][0]),
                                     'lng': parseFloat(waypointsByUser[user][i][1])});

                  userLine = new google.maps.Polyline({
                    path: pathListByUser,
                    strokeColor: '#999999',
                    icons: [{
                       icon: userLineSymbol,
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
      //END function dataReceived
        }

//later will use this to update the the current location of the user along their route
    // var thisUser = userLines[user_id][icons][0][icon]  ??MAYBE [strokeColor]

// initialize the map
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
      center:  {'lat': {{ center[0] }}, 'lng': {{ center[1] }} },
      zoom: 14  ,
      mapTypeId: 'roadmap'
        });

    // add marker for destination point
    var marker = new google.maps.Marker({
    position: {'lat': {{ center[0] }}, 'lng': {{ center[1] }} },
    map: map,
    title: 'Rendezvous Here'
        });

    //animates the movement of the Symbols
    // setTimeout(animateSymbol(userLine, 45), 4500)
    // animateSymbol(selfLine, 40);
       }

// Use the DOM setInterval() function to change the offset of the symbol
// at fixed intervals.
// var id1
// function animateSymbol(line, speed) {
//     var count = 0;
//     id1 = window.setInterval(function() {
//       count = (count + 1);

//       var icons = line.get('icons');
//       icons[0].offset = (count / 2) + '%';
//       line.set('icons', icons);
    //make animation to stop at destination
    // if (line.get('icons')[0].offset == "99.5%") {
//           icons[0].offset = '100%';
//           line.set('icons', icons);
//           window.clearInterval(id1);

//   } }, speed);
// }