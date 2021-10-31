
let lat = document.getElementById('lat')
let long = document.getElementById('long')
let shareCode = document.getElementById('shareCode')

shareCode.addEventListener('click', function() {
  llAadhaar.disabled = false
  llMobile.disabled = false
})

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
