// Weekly earthquake data from USGS
var url =
  'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson';

// Send the data.features object to the createFeatures function
d3.json(url, function (data) {
  createFeatures(data.features);
  console.log(data.features);
});

function createFeatures(earthquakeData) {

  // Define a function we want to run once for each feature in the features array
  // Add popup with magnitude, place, and date/time
  function onEachFeature(feature, layer) {
    layer.bindPopup(
      '<h2>' + 'Magnitude: ' + feature.properties.mag +
      '</h2><hr><b><h3>' + feature.properties.place +
      '</h3><h3>' + new Date(feature.properties.time) + '</h3>'
    );
  }

  function getColor(magnitude) {
    return magnitude > 5 ? 'Red' :
      magnitude > 4 ? 'Orange' :
      magnitude > 3 ? 'Yellow' :
      magnitude > 2 ? 'Green' :
      magnitude > 1 ? 'Blue' :
      'White';
  }

  // Create a GeoJSON layer containing the features array on the earthquakeData object
  // Run the onEachFeature function once for each piece of data in the array
  var earthquakes = L.geoJSON(earthquakeData, {
    onEachFeature: onEachFeature,
    pointToLayer: function (feature, layer) {

      return L.circleMarker(layer, {
        radius: feature.properties.mag * 2.7,
        fillColor: getColor(feature.properties.mag),
        color: "black",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.75
      });
    }
  });

  // Sending our earthquakes layer to the createMap function
  createMap(earthquakes);
}

function createMap(earthquakes) {

  // Define variables for our tile layers
  var lightmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    minZoom: 2,
    id: "mapbox.light",
    accessToken: API_KEY,
    noWrap: true
  });

  var outdoorsmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 22,
    minZoom: 1,
    id: "mapbox.outdoors",
    accessToken: API_KEY,
    noWrap: true
  });

  var satellitemap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 22,
    minZoom: 1,
    id: "mapbox.satellite",
    accessToken: API_KEY,
    noWrap: true
  });

  // Only one base layer can be shown at a time
  var baseMaps = {
    Outdoors: outdoorsmap,
    Light: lightmap,
    Satellite: satellitemap
  };

  // Create overlay object to hold our overlay layer
  var overlayMaps = {
    Earthquakes: earthquakes
  };

  // Create our map with layers to display on load
  var myMap = L.map('map', {
    center: [37.09, 0],
    zoom: 3,
    layers: [outdoorsmap, earthquakes]
  });

  // Create layer control
  L.control
    .layers(baseMaps, overlayMaps, {
      collapsed: false
    })
    .addTo(myMap);

  // Create legend for the mag colors

////////////THIS DOESNT WORK//////////////
  var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 1, 2, 3, 4, 5]
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

// legend.addTo(map);
}