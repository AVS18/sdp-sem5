from django.db import models
from base.models import User
from customer.models import Appointment
# Create your models here.
class Skill(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    primary_skill = models.CharField(max_length=200)
    secondary_skill = models.CharField(max_length=200,blank=True,null=True)
    additional_skill = models.CharField(max_length=200,blank=True,null=True)
    primary_exp = models.IntegerField()
    secondary_exp = models.IntegerField(blank=True,null=True)
    additional_exp = models.IntegerField(blank=True,null=True)
    primary_rate = models.IntegerField()
    secondary_rate = models.IntegerField(blank=True,null=True)
    additional_rate = models.IntegerField(blank=True,null=True)
    secondary_exist = models.BooleanField(default=True)
    additional_exist = models.BooleanField(default=True)
    rating = models.IntegerField(default=5)

class CustomerFeedback(models.Model):
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True)
    behaviour = models.CharField(max_length=10,choices=(("Good","Good"),("Bad","Bad"),("Average","Average")))
    support = models.CharField(max_length=10,choices=(("Good","Good"),("Bad","Bad"),("Average","Average")))
    response = models.CharField(max_length=10,choices=(("Good","Good"),("Bad","Bad"),("Average","Average")))
    rating = models.IntegerField()
    