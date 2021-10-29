from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('landlorddetails',views.landlorddetails,name='landlorddetails'),
    path('status_of_requests',views.status_of_requests,name='status_of_requests'),
    path('residentlogin',views.residentlogin,name='residentlogin'),
    path('landlordlogin',views.landlordlogin,name='landlordlogin'),
    path('resident_address',views.resident_address,name='resident_address'),
    path('enterpasscode',views.enterpasscode,name='enterpasscode'),
    path('request_status',views.request_status,name='request_status'),
    path('check_status_login',views.check_status_login,name='check_status_login'),

]