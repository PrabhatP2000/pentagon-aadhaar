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
        return HttpResponse('Error 404')


def handleLandlordCredentials(request):
    if request.method == 'POST':
        landlord_aadhaar_no = request.POST.get('llAadhaar')
        llMobile = request.POST.get('llMobile')
        if(landlord_aadhaar_no==resident_aadhaar_no):
            return HttpResponse("Resident Aadhaar and Landlord Aadhaar Cant be Same")
        else:
            landlord = Landlord(landlord_aadhaar=landlord_aadhaar_no, llMobile=llMobile)
            landlord.save()
            resident = Resident(resident_aadhaar=resident_aadhaar_no,landlord_aadhaar=landlord, resMobile=resident_mobile_no)
            resident.save()
            msg=f"Your Resident with Aadhaar no. {resident.resident_aadhaar} has requested to Borrow your address.Click the below link to give the Consent or you can visit our site xyz.com.  Link https://localhost:8000/landlord"
            # smsapi.sendSms(msg,landlord.llMobile)
            return HttpResponse('Success-Your Request has been Successfully Sent')
    else:
        return HttpResponse('Error 404')

def getLandlord(request):
    return render(request, 'landlord_login.html')

def handleLandlordLogin(request):
    if request.method == 'POST':
        landlord_aadhaar_no = request.POST['llAadhaar']
        isPresent=Landlord.objects.filter(landlord_aadhaar=landlord_aadhaar_no).first()
        if(isPresent is None):
            return HttpResponse("No One has requested to borrow your address")
        else:
            residents=Resident.objects.filter(landlord_aadhaar=landlord_aadhaar_no)
            return render(request, 'consent.html',{'data':residents,'landlord':landlord_aadhaar_no})
    else:
        return HttpResponse('Error 404')

def rejectedRequest(request):
    if request.method == 'POST':
        resident_aadhaar_no = request.POST['resident_aadhaar']
        landlord_aadhaar_no = request.POST['landlord_aadhaar']
        #Consent Status Update
        residents=Resident.objects.filter(resident_aadhaar=resident_aadhaar_no).first()
        if(residents.consent_status is None):
            residents.consent_status=False
            residents.save()
            return HttpResponse("Your Consent of Flase has been registered")
    else:
        return HttpResponse("Error 404")

def acceptedRequest(request):
    # Offline EKYC LOGIC HERE
    if request.method == "POST":
        resident_aadhaar_no = request.POST.get('resident_aadhaar')
        landlord_aadhaar_no = request.POST.get('landlord_aadhaar')
        context = {
            'llAadhaar': landlord_aadhaar_no,
            'llMobile': '8329253081',
            'resAadhaar': resident_aadhaar_no,
        }
        return render(request, 'ekyc.html', context)
    else:
        return HttpResponse("Error 404")

def ekycSuccess(request):

    if request.method == 'POST':
        resident_aadhaar_no = request.POST['resAadhaar']
        share_code=request.POST['shareCode']
        landlord_aadhaar_no = request.POST['llAadhaar']
        residents=Resident.objects.filter(resident_aadhaar=resident_aadhaar_no).first()
        landlords=Landlord.objects.filter(landlord_aadhaar=landlord_aadhaar_no).first()
        landlords.passcode=share_code
        residents.consent_status=True
        residents.save()
        landlords.save()
        msg=f"Your Landlord with Aadhaar no. {landlords.landlord_aadhaar} has successfully granted his consent for using his adress.Click the below link to Update your address or you can visit our site xyz.com.  Link https://localhost:8000/status"
        # smsapi.sendSms(msg,residents.resMobile)
        return HttpResponse('Success')
    else:
        return HttpResponse('Error 404')

def status(request):
    return render(request, 'status_site.html')

def handleStatus(request):
    if request.method == 'POST':
        resident_aadhaar_no = request.POST['resAadhaar']
        residents=Resident.objects.filter(resident_aadhaar=resident_aadhaar_no).first()
        print(residents.consent_status)
        return render(request, 'status_check.html',{'resident':residents})
    else:
        return HttpResponse("Error 404")

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
            return HttpResponse('Success')
        else:
            r.request_flag=False
            r.save()
            return HttpResponse('Invalid Address, Request Rejected')
    elif request.POST.get('submitCode', None):
        resAadhaar = request.POST.get('resident_aadhaar')
        shareCode = request.POST.get('shareCode')
        r = Resident.objects.filter(resident_aadhaar=int(resAadhaar)).first()
        llAadhaar = r.landlord_aadhaar.landlord_aadhaar
        print(llAadhaar)
        l = Landlord.objects.filter(landlord_aadhaar=llAadhaar).first()
        print(l.passcode)
        if int(shareCode) == l.passcode:
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
                'resAadhaar':resAadhaar
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
        return HttpResponse('error 404')




def saveZip(request):
    body = json.loads(request.body)
    print(body)
    filename = body['filename']
    filedata = body['filedata']
    shareCode = body['code']
    llAadhaar = body['llAadhaar']
    with open(f'main/ekyc/{filename}', "wb") as fh:
        fh.write(base64.decodebytes(bytes(filedata, 'utf-8')))

    archive = zipfile.ZipFile(f'main/ekyc/{filename}', 'r')
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
    x = Landlord.objects.filter(landlord_aadhaar=llAadhaar).first()
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
