
let lat = document.getElementById('lat')
let long = document.getElementById('long')


var options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
};

function success(pos) {
  var crd = pos.coords;

  latitude = crd.latitude
  longitude = crd.longitude
  accuracy = crd.accuracy
  lat.value = latitude
  long.value = longitude
}

function error(err) {
  console.warn(`ERROR(${err.code}): ${err.message}`);
}

navigator.geolocation.getCurrentPosition(success, error, options);