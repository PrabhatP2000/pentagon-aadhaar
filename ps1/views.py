from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

# Function to accept the Landlord's credentials from the user
def getLandlordCredentials(request):
        if request.method == 'POST':
            landLordcredetial=request.POST['aadhaarCredentials']
            # We have to save this to the databases
            return render(request, 'success.html')
        else:
            return render(request, '404.html')
    