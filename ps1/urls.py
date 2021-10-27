from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('landlordform',views.landlordform,name='landlordform'),
    path('status_of_requests',views.status_of_requests,name='status_of_requests'),
    path('residentlogin',views.residentlogin,name='residentlogin'),
    path('landlordlogin',views.landlordlogin,name='landlordlogin'),
    path('resident_address',views.resident_address,name='resident_address'),

]