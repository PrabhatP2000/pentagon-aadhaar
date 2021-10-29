from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def landlorddetails(request):
    return render(request, 'landlorddetails.html')    

def status_of_requests(request):
    return render(request, 'status_of_requests.html')   

def residentlogin(request):
    return render(request, 'residentlogin.html')  

def landlordlogin(request):
    return render(request, 'landlordlogin.html')  

def resident_address(request):
    return render(request, 'resident_address.html')

def enterpasscode(request):
    return render(request, 'enterpasscode.html')

def request_status(request):
    return render(request, 'request_status.html')    

def check_status_login(request):
    return render(request, 'check_status_login.html')  

# Function to accept the Landlord's credentials from the user
def getLandlordCredentials(request):
        if request.method == 'POST':
            landLordcredetial=request.POST['aadhaarCredentials']
            # We have to save this to the databases
            return render(request, 'success.html')
        else:
            return render(request, '404.html')
    