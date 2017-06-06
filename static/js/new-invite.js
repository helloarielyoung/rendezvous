 $(document).ready(function() { 
    $('#newInvitationSubmit').click( function(evt){
        evt.preventDefault();
        var friendList = [];

        for ( var i=0; i< $('.rendezvousFriends').length; i++) {
            friendList.push($('.rendezvousFriends')[i].value);
        }
        var data = {rendezvousName: $('#rendezvousName').val(),
                rendezvousDateTime: $('#rendezvousDateTime').val(),
                rendezvousLocationAddress: $('#rendezvousLocationAddress').text(),
                rendezvousLocationName: $('#rendezvousLocationName').text(),
                rendezvousFriends: JSON.stringify(friendList),
                destinationLat: destination_lat,
                destinationLng: destination_lng
                };
        $.post("/invitation-save.json", data, function(msg) {
                $("#inviteModal").modal('hide');
                $('#inviteSuccessModal').modal();
            });
      });

      // add a search box to a map

$('#inviteModal').on('hidden.bs.modal', function(){
    $(this).find('form')[0].reset();
    $("#pac-input").val("")
});

//when the New Invitation form opens, find the autofocus field
$('#inviteModal').on('shown.bs.modal', function () {
  $('#rendezvousName').focus();
});

}); //END of on document ready

//variable to hold place information outside of map
var placeInfo
//save the rendezvous location to store in waypoints
var destination_lat
var destination_lng

//launches the New Invitation modal form
function launchModal2() {
     $('#inviteModal').modal();
}


       function initMap() {
        //set a default center
        var curLatlng1 = new google.maps.LatLng(37.087654, -122.087545);

        var mapOptions = {
          center: curLatlng1,
          zoom: 13,
          mapTypeId: 'roadmap',
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
        };

        var map = new google.maps.Map(document.getElementById('map'), mapOptions);

        //if user's geolaction can be obtained, set that as center
        if (navigator.geolocation) {
        
            navigator.geolocation.getCurrentPosition(function (position) {
                    initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                    map.setCenter(initialLocation);
                    });
                }
        else (console.log("navigator geolocation not working"))

        // Create the search box and link it to the UI element.
        var input = document.getElementById('pac-input');
        var searchBox = new google.maps.places.SearchBox(input);
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        // Bias the SearchBox results towards current map's viewport.
        map.addListener('bounds_changed', function() {
          searchBox.setBounds(map.getBounds());
        });

        var markers = [];
        // Listen for the event fired when the user selects a prediction and retrieve
        // more details for that place.
        searchBox.addListener('places_changed', function() {
          var places = searchBox.getPlaces();

          if (places.length == 0) {
            return;
          }

          // Clear out the old markers.
          markers.forEach(function(marker) {
            marker.setMap(null);
          });
          markers = [];

          // For each place, get the icon, name and location.
          var bounds = new google.maps.LatLngBounds();
          places.forEach(function(place) {
            if (!place.geometry) {
              console.log("Returned place contains no geometry");
              return;
            }
            var icon = {
              url: place.icon,
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
            };

            // Create a marker for each place.
            markers.push(new google.maps.Marker({
              map: map,
              icon: icon,
              title: place.name,
              position: place.geometry.location
            }));

            if (place.geometry.viewport) {
              // Only geocodes have viewport.
              bounds.union(place.geometry.viewport);
            } else {
              bounds.extend(place.geometry.location);
            }

          });
          map.fitBounds(bounds);
            //add onclick event to markers to pass geometry of that place to invitation
            markers.forEach(function(marker) {
                marker.addListener('click', function() {
                    console.log(marker.getPosition().lat(), marker.getPosition().lng());
                    destination_lat = marker.getPosition().lat();
                    destination_lng = marker.getPosition().lng();
                    // show it on the modal form
                      $("#rendezvousLocationName").html(places[0].name);
                      $('#rendezvousLocationAddress').html(places[0].formatted_address);
                    launchModal2();
                });
            });
            // add another listener on HOOVER to get place info.  start from this,
            // but will have to look through markers as above:
            // google.maps.event.addListener(marker, 'click', function() {
            //   infowindow.setContent('<div><strong>' + place.name + '</strong><br>' +
            //     place.formatted_address + '</div>');
            //   infowindow.open(map, this);
            // });
        });

      }