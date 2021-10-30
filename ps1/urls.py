from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('resident/', views.getResident,name='resident'),
    path('handle_resident', views.handleResident, name="handleResident"),
    path('handle_landlord',views.handleLandlordCredentials,name='handleLandLord'),
    path('landlord/',views.getLandlord,name="landlord"),
    path('handle_landlord_login',views.handleLandlordLogin,name="handleLandLordLogin"),
    path('request_rejected/',views.rejectedRequest,name="requestRejected"),
    path('request_accepted/',views.acceptedRequest,name="requestAccepted"),
    path('ekyc_success/', views.ekycSuccess, name="ekycSuccess"),
    path('status',views.status,name="st"),
    path('handle_status',views.handleStatus,name="handleStatus"),
    path('address_update',views.updateAddress,name="addressUpdate"),
    path('api/<path:apiLink>', views.getapi),  # for AJAX purpose
    path('saveZip/', views.saveZip),
]
