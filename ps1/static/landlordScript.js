//get

let inputBox = document.getElementById("inputBox")
let submitLlDetails = document.getElementById('submitLlDetails')

var invalidChars = [
  "-",
  "+",
  "e",
]

//call


submitLlDetails.disabled = true

//function

inputBox.addEventListener("input", function () {
  this.value = this.value.replace(/[^0-9]/g, "")
})

inputBox.addEventListener("keyup", function (e) {
  if (invalidChars.includes(e.key)) {
    e.preventDefault()
  }
  if (this.value.length == 10){
    submitLlDetails.disabled = false
    submitLlDetails.type = 'submit'
  }
  else{
    submitLlDetails.disabled = true
  }
})
