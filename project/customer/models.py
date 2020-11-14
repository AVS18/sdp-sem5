from django.db import models
from base.models import User
# Create your models here.
class Appointment(models.Model):
    worker = models.ForeignKey(User,on_delete=models.CASCADE,related_name='my_worker')
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='my_customer')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    amount = models.IntegerField()
    working_hours = models.IntegerField()
    work_name = models.CharField(max_length=2048,null=True,blank=True)

class WorkerFeedback(models.Model):
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True)
    quality = models.IntegerField()
    work_completed_in_time = models.CharField(max_length=10,choices=(("Yes","Yes"),("No","No")))
    polite=models.CharField(max_length=10,choices=(("Yes","Yes"),("No","No")))
    behaviour=models.CharField(max_length=10,choices=(("Good","Good"),("Bad","Bad"),("Average","Average")))
    rating = models.IntegerField()