from django.db import models
from django.contrib.auth.models import AbstractUser
from django_clamd.validators import validate_file_infection
from django_cryptography.fields import encrypt

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.BigIntegerField()
    message = models.CharField(max_length=2048)

class Profile(models.Model):
    age = models.IntegerField()
    dob = models.DateField()
    photo = models.FileField(upload_to='profile_pics/')
    address_lane_1 = models.CharField(max_length=200)
    address_lane_2 = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))
    state = models.CharField(max_length=50,choices=state_choices)
    pincode = models.IntegerField()
    alternate_phone = models.BigIntegerField()
    proof_of_residence = models.FileField(upload_to='residence_proof/')
class User(AbstractUser):
    mobile = models.BigIntegerField(null=True)
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    user_profile = models.ForeignKey(Profile,on_delete=models.DO_NOTHING,null=True)
    choices = (('Worker','Worker'),('Customer','Customer'))
    user_type = models.CharField(max_length=10,choices=choices,null=True)

class SiteAnnouncement(models.Model):
    message=models.CharField(max_length=2048)
    link_exist = models.BooleanField()
    link = models.CharField(max_length=2048,blank=True,null=True)

class Message(models.Model):
    message = models.CharField(max_length=2048)
    sent_by = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True,null=True,blank=True)
class Room(models.Model):
    worker = models.ForeignKey(User,on_delete=models.CASCADE,related_name='worker')
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='customer')
    room_status = models.CharField(max_length=10,choices=(('Opened','Opened'),('Closed','Closed')))
    chat = models.ManyToManyField(Message,related_name='messages')

class ContactSupport(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reported_on')
    reported_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reported_by',blank=True,null=True)
    issue = models.CharField(max_length=200)
    description = models.CharField(max_length=2048)
    proof = models.FileField(upload_to='proofs',blank=True,null=True)