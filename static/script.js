const form = document.getElementById("addhashtag");
const hashtags = document.getElementById("hashtags");
//const current_hashtags = document.getElementById("currentHashtags");

//subscribe to server events
var source = new EventSource("/stream");

form.onsubmit = addHashtag;

function updateHashtags(hashtags) {
  //send a post request with the new hashtag
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/hashtags", true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify({
      hashtags: hashtags
  }));
}

function addHashtag(event) {
  //get the new hashtag
  var formData = new FormData(event.target);
  var newHashtag = formData.get("hashtags");

  //get the current hashtag list
  const current_hashtags = document.getElementById("currentHashtags");
  var current_string = current_hashtags.innerText;


  // check if added hashtag has hash symbol, if not add it
  if(newHashtag[0] != "#") {
    newHashtag = "#"+newHashtag;
  }

  //add the new hashtag to the list
  current_string += (", " + newHashtag);
  current_hashtags.innerText = current_string;
  
  var current_hashtag_list = current_string.split(": ");
  current_hashtag_list = current_hashtag_list[1].split(", ");
  console.log(current_hashtag_list);

  //send a post request with the new hashtag
  updateHashtags(current_hashtag_list);

  //restart stream to start using the new hashtags
  source = new EventSource("/stream");

  //stop the form from opening a new window
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


//get the current hashtag list and send it to the server
const current_hashtags = document.getElementById("currentHashtags");
var current_string = current_hashtags.innerText;
var current_hashtag_list = current_string.split(": ");
current_hashtag_list = current_hashtag_list[1].split(", ");

updateHashtags(current_hashtag_list);



var iconSVG1 = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="16" height="16">' +
 '<circle r="8" cx="8" cy="8" style="fill:'
 
 var iconSVG2 = ';stroke:gray;stroke-width:0.1"/></svg>';


source.onmessage = function(event) {
    //var data = event.data;
    //var s = JSON.stringify(event.data);
    console.log(event.data);
    var a = JSON.parse(event.data);
    var coordList = a.coordinates.split(", ");
    var coords = {lat: coordList[1], lng: coordList[0]};

    var color = "red";
    if(a.label == 1.0) {
      color = "green";
    }
    else if(a.label == 0.0) {
      color = "blue";
    }
    else if(a.label == -1.0) {
      color = "red";
    }

    var icon = new H.map.Icon(iconSVG1 + color + iconSVG2);

    var marker = new H.map.Marker(coords, {icon: icon});

    map.addObject(marker);
}


