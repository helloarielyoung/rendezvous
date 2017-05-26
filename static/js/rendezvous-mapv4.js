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

// this will change to results['data'][0] when I am no longer sending the self & other waypoints lists
      var allWaypoints = results[2]['data'];
      var allWaypointsLength = Object.keys(allWaypoints).length;
debugger

//frome here to end of here will be removed when allWaypoints works
      // logged in user:
      // var waypointsForSelf = results[0]['waypoints'];
      // var waypointsForSelfLength = waypointsForSelf.length;

      // all other users on this invite:
      // var waypointsByUser = results[1]['userdata'];
      // var waypointsByUserLength = Object.keys(waypointsByUser).length;

      // Define symbol for logged in user
      // var selfLineSymbol = {
      //   path: google.maps.SymbolPath.CIRCLE,
      //   scale: 4,
      //   // logged in user has a black dot
      //   strokeColor: 'black'
      //     };

      // var selfPathList = []
      // for (var i = 0; i < waypointsForSelfLength; i++) {
      //   selfPathList.push({'lat': parseFloat(waypointsForSelf[i][0]),
      //                     'lng': parseFloat(waypointsForSelf[i][1])});
      //     }

      // Create the polyline for logged in user
      // selfLine = new google.maps.Polyline({
      // path: selfPathList,
      //   //logged in user has a black line
      //   strokeColor: '#000000',
      //   icons: [{
      //     icon: selfLineSymbol,
      //     offset: '0%'
      //     }],
      //   map: map
      //   });
//end of section that will be removed when allWaypoints works

      // get logged in userid from  $('#map').data('user_id') instead of session
      // can't use Jinja in js script!

// all_wyapoints looks like this:
// {'data': [{'id': #, 'name': name, 'waypoints': [[lat, lng],[lat,lng]]}, .....]}
// allWaypoints should be [{'id': #, , 'name': name, 'waypoints': [[lat, lng],[lat,lng]]}, .....]

//will get rid of this, and add all users to userLines at end of this section
      // userLines[ user_id ] = selfLine;
//end of get rid of this

      // colors for the not-the-logged-in-users' symbols
      symbolColors = ['blue', 'purple', 'red', 'yellow'];
          var colorCount = 0;
          //iterate through waypoints_by_user to get users
          for (var user in allWaypoints) {
              //Save this user id for later
              //how to get userid from allWaypoints:  allWaypoints[0]['id']
              var thisUserId = allWaypoints[user]['id'];
              if (thisUserId = user_id) { //this is the logged in user
                  var pickColor = 'black'
              else
                  pickColor = symbolColors[colorCount];
                  colorCount++;
              }
///here is where i got to Friday morning!  else is apparently not right for javaScript

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

                  var userLine = new google.maps.Polyline({
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


//NEED THE USER NAME FOR THIS - 
//restructuring server.py to change waypoints_by_user to include the name
//and have the data in a much more accessible format... then can modify this to work
            // legend
            //for loop here appending to dictionary an icon for each user in this format:
                // { 2: {
                //     name: 'User2',
                //     icon: iconBase + 'blu-circle-lv.png'
                //     }
//           var iconBase = 'https://maps.google.com/mapfiles/kml/paddle/';
//           var icons = {};
//           var colorCount = 0;
//           var iconSymbolNames = ['blu', 'purple', 'red', 'ylw'];

//           for (var user in waypointsByUser) {   
//               var inside = {}
//               thisUserId = user;
//               inside['name'] = thisUserId;
//               inside['icon'] = iconBase +iconSymbolNames[colorCount]+'-circle-lv.png';
// // symbolColors[colorCount]
//               icons[thisUserId] = inside
//               colorCount++;
//           }
//             var legend = document.getElementById('legend');
//             for (var key in icons) {
//                 var type = icons[key];
//                 var name = type.name;
//                 var icon = type.icon;
//                 var div = document.createElement('div');
//                 div.innerHTML = '<img src="' + icon + '"> ' + name;
//                 legend.appendChild(div);
//               }

//         map.controls[google.maps.ControlPosition.TOP_RIGHT].push(legend);

      //END function dataReceived
        }

// console.log(userLines)
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