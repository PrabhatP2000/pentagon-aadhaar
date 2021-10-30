from django.db import models

# Create your models here.

class Landlord(models.Model):
    llMobile = models.IntegerField(primary_key=True)
    passcode=models.IntegerField(default=1111)
    careof = models.CharField(max_length=50,blank=True)
    country = models.CharField(max_length=50,blank=True)
    dist = models.CharField(max_length=50,blank=True)
    house = models.CharField(max_length=50,blank=True)
    landmark = models.CharField(max_length=50,blank=True)
    loc= models.CharField(max_length=50,blank=True)
    pc = models.CharField(max_length=50,blank=True)
    po = models.CharField(max_length=50,blank=True)
    state = models.CharField(max_length=50,blank=True)
    street = models.CharField(max_length=50,blank=True)
    subdist= models.CharField(max_length=50,blank=True)
    vtc= models.CharField(max_length=50,blank=True)

    def __str__(self):
        return str(self.llMobile)

class Resident(models.Model):
    resident_aadhaar = models.IntegerField(primary_key=True)
    consent_status = models.BooleanField(null=True)
    llMobile = models.ForeignKey(Landlord,on_delete=models.CASCADE)
    resMobile = models.IntegerField(default=9999999999)
    careof = models.CharField(max_length=50,blank=True)
    country = models.CharField(max_length=50,blank=True)
    dist = models.CharField(max_length=50,blank=True)
    house = models.CharField(max_length=50,blank=True)
    landmark = models.CharField(max_length=50,blank=True)
    loc= models.CharField(max_length=50,blank=True)
    pc = models.CharField(max_length=50,blank=True)
    po = models.CharField(max_length=50,blank=True)
    state = models.CharField(max_length=50,blank=True)
    street = models.CharField(max_length=50,blank=True)
    subdist= models.CharField(max_length=50,blank=True)
    vtc= models.CharField(max_length=50,blank=True)

    def __str__(self):
        return str(self.resident_aadhaar)
