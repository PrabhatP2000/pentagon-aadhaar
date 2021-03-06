//get
let llAadhaar = document.getElementById('llAadhaar')
let textCaptcha = document.getElementById('textCaptcha')
let imgcaptcha = document.getElementById('imgcaptcha')
let reloadCaptcha = document.getElementById('reloadCaptcha')
let sendOTP = document.getElementById('sendOTP')
let textOTP = document.getElementById('textOTP')
let shareCode = document.getElementById('shareCode')
let validateOTP = document.getElementById('validateOTP')
let authResidentForm = document.getElementById('authResidentForm')
let nextPage = document.getElementById('nextPage')
let msgLabel = document.getElementById('msgLabel')
let llMobile = document.getElementById('llMobile')
let steponeresponse
let steptworesponse
let stepthreeresponse
let uuid

llAadhaar.disabled = true
llMobile.disabled = true

console.log(window.location.pathname)

//call
reloadCaptcha.addEventListener('click', stepOne)

sendOTP.addEventListener('click', stepTwo)

validateOTP.addEventListener('click', stepThree)

nextPage.addEventListener('click', function() {
  llAadhaar.disabled = false
  llMobile.disabled = false
})

//Function
function stepOne(){
  msgLabel.innerText = ""
  let xhr = new XMLHttpRequest()

  xhr.open('POST', '/api/https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/get/captcha', true)
  xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"))
  xhr.setRequestHeader("Content-Type", "application/json")
  xhr.onload = function(){
    if (this.status == 200){
      x = JSON.parse(this.responseText)
      steponeresponse = x
      imgcaptcha.src = `data:image/png;base64,${x.captchaBase64String}`
      console.log(imgcaptcha.src)
    }
  }
  data = {
    "langCode": "en",
    "captchaLength": "3",
    "captchaType": "2",
  }
  xhr.send(JSON.stringify(data))

}

function stepTwo(){


  msgLabel.innerText = ""
  let xhr = new XMLHttpRequest()

  xhr.open('POST', '/api/https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/generate/aadhaar/otp', true)
  xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"))
  xhr.setRequestHeader("Content-Type", "application/json")
  xhr.setRequestHeader("appid","MYAADHAAR")
  xhr.setRequestHeader("Accept-Language", "en_in")
  uuid = uuidv4().toString()
  xhr.setRequestHeader("x-request-id", uuid)
  xhr.onload = function(){
    if (this.status == 200){
      x = JSON.parse(this.responseText)
      steptworesponse = x
      console.log(steptworesponse)
      console.log(steptworesponse.status)
      if (steptworesponse.status === 'Success'){
        textOTP.type = "text"
        validateOTP.type = "button"
        shareCode.type = "text"
        llAadhaar.disabled = true
        llMobile.disabled = true
        maintainLogs("Requesting for Ekyc")
      }
      else{
        msgLabel.innerText = "Invalid Captcha"
        msgLabel.style.color = "red"
      }
    }
  }

  data = {
    "uidNumber": llAadhaar.value,
    "captchaTxnId": steponeresponse.captchaTxnId,
    "captchaValue": textCaptcha.value,
    "transactionId": `MYAADHAAR:${uuid}`
  }
  console.log(data)
  xhr.send(JSON.stringify(data))



}

function stepThree(){
  msgLabel.innerText = ""
  let xhr = new XMLHttpRequest()
  msgLabel.innerText = "Validating ..."
  xhr.open('POST', '/api/https://stage1.uidai.gov.in/eAadhaarService/api/downloadOfflineEkyc', true)
  xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"))
  xhr.setRequestHeader("Content-Type", "application/json")
  xhr.onload = function(){
    if (this.status == 200){
      x = JSON.parse(this.responseText)
      stepthreeresponse = x
      console.log(stepthreeresponse)
      if (stepthreeresponse.status == "Success"){
        nextPage.type = "submit"
        msgLabel.innerText = "OTP validated Successfully, Click Next to Continue"
        msgLabel.style.color = "green"
        saveZip()
        maintainLogs("Offline Ekyc Request Success")
      }
      else{
        msgLabel.innerText = "Invalid OTP"
        maintainLogs("Offline Ekyc Request Failed")
      }
    }
  }

  data = {

    "txnNumber": steptworesponse.txnId,
    "otp": textOTP.value,
    "shareCode" : shareCode.value,
    "uid": llAadhaar.value,

  }

  console.log(data)
  xhr.send(JSON.stringify(data))

}


stepOne()

function maintainLogs(message){

  let xhr = new XMLHttpRequest()

  xhr.open('POST', '/logs/', true)

  xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"))
  xhr.setRequestHeader("Content-Type", "application/json")

  xhr.onload = function(){
    if (this.status == 200){
      console.log(this.response)
    }
  }

  data = {
    "transactionId" : steptworesponse.txnId ,
    "message" : message
  }
  console.log(data)

  xhr.send(JSON.stringify(data))

}

function saveZip(){

  let xhr = new XMLHttpRequest()

  xhr.open('POST', '/saveZip/', true)

  xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"))
  xhr.setRequestHeader("Content-Type", "application/json")

  xhr.onload = function(){
    if (this.status == 200){
      console.log(this.response)
    }
  }

  data = {
    "filedata" : stepthreeresponse.eKycXML,
    "filename" : stepthreeresponse.fileName,
    "code" : shareCode.value,
    "llMobile": llMobile.value
  }
  console.log(data)

  xhr.send(JSON.stringify(data))

}



function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}

function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}
