from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import base64
import zipfile
from .models import Resident,Landlord
from .files import smsapi
from xml.dom import minidom
import xml.etree.ElementTree as et
from lxml import etree
import datetime

# Create your views here.


resident_aadhaar_no=""
resident_mobile_no=""

def index(request):
    return render(request, 'index.html')

def getResident(request):
    return render(request, 'resident.html')

def handleResident(request):
    global resident_aadhaar_no
    global resident_mobile_no
    if request.method == 'POST':
        resident_aadhaar_no = request.POST.get('resAadhaar')
        resident_mobile_no = request.POST.get('resMobile')
        return render(request, 'landlord.html')
    else:
        return render(request, '404.html')


def handleLandlordCredentials(request):
    if request.method == 'POST':
        # landlord_aadhaar_no = request.POST.get('llAadhaar')
        llMobile = request.POST.get('llMobile')
        if(llMobile==resident_mobile_no):
            return render(request, 'unsuccess.html',{'data':"The Resident Mobile Number can't be same as Landlord's Mobile Number"})
        else:
            landlord = Landlord(llMobile=llMobile)
            landlord.save()
            print(resident_mobile_no,type(resident_mobile_no))
            resident = Resident(resident_aadhaar=resident_aadhaar_no, llMobile=landlord, resMobile=resident_mobile_no)
            resident.save()
            msg=f"Your Resident with Aadhaar no. {resident.resident_aadhaar} has requested to Borrow your address.Click the below link to give the Consent or you can visit our site xyz.com.  Link https://localhost:8000/landlord"
            # smsapi.sendSms(msg,landlord.llMobile)
        return render(request, 'success.html',{'data':'Success-Your Request has been Successfully Sent'})
    else:
        return render(request, '404.html')

def getLandlord(request):
    return render(request, 'landlord_login.html')

def handleLandlordLogin(request):
    if request.method == 'POST':
        llMobile = request.POST['llMobile']
        print(llMobile)
        llAadhaar = request.POST['llAadhaar']
        isPresent=Landlord.objects.filter(llMobile=llMobile).first()
        if(isPresent is None):
            return render(request, 'unsuccess.html',{'data':"No One has requested to borrow your address"})
        else:
            residents=Resident.objects.filter(llMobile=llMobile)
            return render(request, 'consent.html',{'data':residents,'llMobile': llMobile, 'llAadhaar': llAadhaar})
    else:
        return render(request, '404.html')

def rejectedRequest(request):
    if request.method == 'POST':
        resident_aadhaar_no = request.POST['resident_aadhaar']
        # landlord_aadhaar_no = request.POST['llMobile']
        #Consent Status Update
        residents=Resident.objects.filter(resident_aadhaar=resident_aadhaar_no).first()
        if(residents.consent_status is None):
            residents.consent_status=False
            residents.save()
            return render(request, 'success.html',{'data':"Your Consent of Flase has been registered"})
    else:
        return render(request, '404.html')

def acceptedRequest(request):
    # Offline EKYC LOGIC HERE
    if request.method == "POST":
        resident_aadhaar_no = request.POST.get('resident_aadhaar')
        llMobile = request.POST.get('llMobile')
        print(llMobile, 'shree')
        llAadhaar = request.POST.get('llAadhaar')
        context = {
            'llMobile': llMobile,
            'resAadhaar': resident_aadhaar_no,
            'llAadhaar': llAadhaar
        }
        return render(request, 'ekyc.html', context)
    else:
        return render(request, '404.html')

def ekycSuccess(request):
    if request.method == 'POST':
        resident_aadhaar_no = request.POST['resAadhaar']
        share_code=request.POST['shareCode']
        residents=Resident.objects.filter(resident_aadhaar=resident_aadhaar_no).first()
        residents.consent_status=True
        residents.save()
        msg=f"Your Landlord has successfully granted his consent for using his adress.Click the below link to Update your address or you can visit our site xyz.com.  Link https://localhost:8000/status"
        # smsapi.sendSms(msg,residents.resMobile)
        return render(request, 'success.html',{'data':"Offline eKYC Successful"})
    else:
        return render(request, '404.html')

def status(request):
    return render(request, 'status_site.html')

def handleStatus(request):
    if request.method == 'POST':
        resident_aadhaar_no = request.POST['resAadhaar']
        residents=Resident.objects.filter(resident_aadhaar=resident_aadhaar_no).first()
        print(residents.consent_status)
        return render(request, 'status_check.html',{'resident':residents})
    else:
        return render(request, '404.html')

def updateAddress(request):
    print(request.POST)
    # resAadhaar = '999996438044'
    if request.POST.get('updateAddress', None):
        resAadhaar = request.POST.get('resident_aadhaar')
        r = Resident.objects.filter(resident_aadhaar=int(resAadhaar)).first()
        r.careof = request.POST.get('careof')
        r.country = request.POST.get('country')
        r.dist = request.POST.get('dist')
        r.house = request.POST.get('house')
        r.landmark = request.POST.get('landmark')
        r.loc= request.POST.get('loc')
        r.pc = request.POST.get('pc')
        r.po = request.POST.get('po')
        r.state = request.POST.get('state')
        r.street = request.POST.get('street')
        r.subdist= request.POST.get('subdist')
        r.vtc= request.POST.get('vtc')
        lat = float(request.POST.get('lat'))
        long = float(request.POST.get('long'))
        if validateLocation(r.country, r.state, lat, long):
            r.request_flag=True
            r.save()
            return render(request, 'success.html',{'data':"Congratulations,Your Address has been updated successfully"})
        else:
            r.request_flag=False
            r.save()
            return render(request, 'unsuccess.html',{'data':"Invalid Address, Request Rejected"})
    elif request.POST.get('submitCode', None):
        resAadhaar = request.POST.get('resident_aadhaar')
        shareCode = request.POST.get('shareCode')
        r = Resident.objects.filter(resident_aadhaar=int(resAadhaar)).first()
        llMobile = r.llMobile.llMobile
        print(llMobile)
        l = Landlord.objects.filter(llMobile=llMobile).first()
        print(l.passcode)
        if shareCode and int(shareCode) == l.passcode:
            flag = True
            context = {
                'auth': flag,
                'l': l,
                'resAadhaar':resAadhaar
            }
        else:
            flag = False
            context = {
                "auth": flag,
                'resAadhaar':resAadhaar,
                'msg': 'Please Enter correct share code'
            }
        return render(request, 'updateResidentAddress.html', context)
    elif request.method == 'POST':
        print('in post')
        resAadhaar = request.POST.get('resident_aadhaar')
        context = {
            'resAadhaar': resAadhaar
        }
        return render(request, 'updateResidentAddress.html', context)
    else:
        return render(request, '404.html')


def maintainLogs(request):
    body = json.loads(request.body)
    transactionId = body['transactionId']
    message = body['message']
    file = open('ps1/logs/audit.log', 'a')
    now = datetime.datetime.now()
    now = str(now)[:-7]
    file.write(f"{now} - {transactionId}: {message} \n")
    file.close()
    return HttpResponse(json.dumps({'status': 'success'}))

def saveZip(request):
    body = json.loads(request.body)
    print(body)
    filename = body['filename']
    filedata = body['filedata']
    shareCode = body['code']
    llMobile = body['llMobile']
    with open(f'ps1/ekyc/{filename}', "wb") as fh:
        fh.write(base64.decodebytes(bytes(filedata, 'utf-8')))

    archive = zipfile.ZipFile(f'ps1/ekyc/{filename}', 'r')
    name = filename.split('.')[0]
    file = archive.open(f'{name}.xml', pwd=bytes(f'{shareCode}', 'utf-8'))
    xmldata = file.read()
    data = xmldata.decode()
    root = et.fromstring(data)
    uid = root.find('UidData')
    poa = uid.find('Poa')
    careof = poa.attrib['careof']
    country = poa.attrib['country']
    dist = poa.attrib['dist']
    house = poa.attrib['house']
    landmark = poa.attrib['landmark']
    loc= poa.attrib['loc']
    pc = poa.attrib['pc']
    po = poa.attrib['po']
    state = poa.attrib['state']
    street = poa.attrib['street']
    subdist= poa.attrib['subdist']
    vtc= poa.attrib['vtc']
    print(state, street, dist, subdist)
    x = Landlord.objects.filter(llMobile=llMobile).first()
    x.careof = careof
    x.country = country
    x.dist = dist
    x.house = house
    x.landmark = landmark
    x.loc = loc
    x.pc = pc
    x.po = po
    x.state = state
    x.street = street
    x.subdist = subdist
    x.vtc = vtc
    x.passcode = int(shareCode)
    x.save()
    return HttpResponse(json.dumps({'status': 'success'}))


def validateLocation(country, state, lat, long):
    header = {
            "Content-Type": "application/json"
        }
    link = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={long}&zoom=18&addressdetails=1'
    response = requests.get(link, headers=header)
    loc = json.loads(response.text)
    address = loc['address']
    if country == address['country'] and state == address['state']:
        return True
    return False

# for AJAX
def getapi(request, apiLink):

    ct = request.content_type

    header = {
        "Content-Type": ct
    }
    if request.method == 'POST':
        body = request.body
        print(apiLink)
        print(header)
        print(body)

        response = requests.post(apiLink, headers=header, data=body)
        print(response)
        return HttpResponse(response)
    else:
        response = requests.get(apiLink, headers=header)
        print(response)
        return HttpResponse(response)


    #Deletion code for the landlord and resident
    # residents=Resident.objects.filter(landlord_aadhaar=landlord_aadhaar_no).count()
        # if(residents==1):
        #     Landlord.objects.filter(landlord_aadhaar=landlord_aadhaar_no).delete()
        #     return HttpResponse("Done")
        # else:
        #     Resident.objects.filter(resident_aadhaar=resident_aadhaar_no).delete()
        #     return HttpResponse("Done")
