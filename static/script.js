const form = document.getElementById("addhashtag");
const hashtags = document.getElementById("hashtags");
//const current_hashtags = document.getElementById("currentHashtags");

form.onsubmit = addHashtag;

function addHashtag(event) {
  var formData = new FormData(event.target);
  var hashtags = formData.get("hashtags");
  const current_hashtags = document.getElementById("currentHashtags");
  var current_string = current_hashtags.innerText;
  //current_string += hashtags;
  console.log(current_string);
  event.preventDefault();
}





// Create a Platform object (one per application):
var platform = new H.service.Platform({
    'apikey': apikey
  });

// Obtain the default map types from the platform object:
var defaultLayers = platform.createDefaultLayers();


// Instantiate (and display) a map object:
var map = new H.Map(
    document.getElementById('mapContainer'),
    defaultLayers.vector.normal.map,
    {
      zoom: 4,
      center: { lat: 52.5, lng: 13.4 },
      pixelRatio: window.devicePixelRatio || 1
    });

// add a resize listener to make sure that the map occupies the whole container
window.addEventListener('resize', () => map.getViewPort().resize());

//Step 3: make the map interactive
// MapEvents enables the event system
// Behavior implements default interactions for pan/zoom (also on mobile touch environments)
var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

// Create the default UI:
var ui = H.ui.UI.createDefault(map, defaultLayers);



//subscribe to server events
//var source = new EventSource("/stream");

var iconSVG = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="16" height="16">' +
 '<circle r="8" cx="8" cy="8" style="fill:red;stroke:gray;stroke-width:0.1" />' +
'</svg>';

/*
source.onmessage = function(event) {
    var data = event.data.substring(2, event.data.length-1);
    //var s = JSON.stringify(event.data);
    console.log(data);
    var a = JSON.parse(data);
    var coords = {lat: a.loc.coordinates[1], lng: a.loc.coordinates[0]};

    var icon = new H.map.Icon(iconSVG);

    var marker = new H.map.Marker(coords, {icon: icon});

    map.addObject(marker);
}
*/

