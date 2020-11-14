from django.shortcuts import render,redirect
from customer.models import Appointment,WorkerFeedback
from django.db.models import Sum
from worker.models import Skill,CustomerFeedback
from base.models import ContactSupport
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,"AdminDashboard.html")

def reports(request):
    nw=len(Appointment.objects.values('worker').distinct())
    nc=len(Appointment.objects.values('customer').distinct())
    ap = Appointment.objects.aggregate(Sum('amount'))
    wh = Appointment.objects.aggregate(Sum('working_hours'))
    return render(request,"adminReports.html",{'nw':nw,'nc':nc,'ap':ap['amount__sum'],'wh':wh['working_hours__sum']})

def catalogue(request):
    primary = Skill.objects.all().select_related()
    secondary = Skill.objects.filter(secondary_exist=True).select_related()
    additional = Skill.objects.filter(additional_exist=True).select_related()
    work_name = []
    work_name.extend([item['primary_skill'] for item in Skill.objects.values('primary_skill').distinct()])
    work_name.extend([item['secondary_skill'] for item in Skill.objects.values('secondary_skill').distinct()])
    work_name.extend([item['additional_skill'] for item in Skill.objects.values('additional_skill').distinct()])
    di = {'primary':primary,'secondary':secondary,'additional':additional,'work_name':work_name}
    return render(request,"adminCatalogue.html",di)

def filter(request):
    if request.method=="POST":
        skill_name = request.POST["skill_name"]
        wage = request.POST["wage"]
        wage=wage.split()
        low,high=0,0
        rating=request.POST["rating"]
        if len(wage)==2:
            low = int(wage[0])
            high = int(wage[1])
            primary = Skill.objects.filter(primary_skill=skill_name,primary_rate__range=(low-1,high+1),rating=rating)
            secondary = Skill.objects.filter(secondary_skill=skill_name,secondary_rate__range=(low-1,high+1),rating=rating)
            additional = Skill.objects.filter(additional_skill=skill_name,additional_rate__range=(low-1,high+1),rating=rating)
            work_name = []
            work_name.extend([item['primary_skill'] for item in Skill.objects.values('primary_skill').distinct()])
            work_name.extend([item['secondary_skill'] for item in Skill.objects.values('secondary_skill').distinct()])
            work_name.extend([item['additional_skill'] for item in Skill.objects.values('additional_skill').distinct()])
            di = {'primary':primary,'secondary':secondary,'additional':additional,'work_name':work_name}
            return render(request,"adminCatalogue.html",di)
        else:
            primary = Skill.objects.filter(primary_skill=skill_name,primary_rate__gte=300,rating=rating)
            secondary = Skill.objects.filter(secondary_skill=skill_name,secondary_rate__gte=300,rating=rating)
            additional = Skill.objects.filter(additional_skill=skill_name,additional_rate__gte=300,rating=rating)
            work_name = []
            work_name.extend([item['primary_skill'] for item in Skill.objects.values('primary_skill').distinct()])
            work_name.extend([item['secondary_skill'] for item in Skill.objects.values('secondary_skill').distinct()])
            work_name.extend([item['additional_skill'] for item in Skill.objects.values('additional_skill').distinct()])
            di = {'primary':primary,'secondary':secondary,'additional':additional,'work_name':work_name}
            return render(request,"adminCatalogue.html",di)
    else:
        return redirect('/administrator/catalogue')    

def feedback(request):
    customer = WorkerFeedback.objects.all()
    worker = CustomerFeedback.objects.all()
    return render(request,'adminFeedback.html',{'worker':worker,'customer':customer})

def block(request):    
    blocks = ContactSupport.objects.all()
    return render(request,'adminBlock.html',{'blocks':blocks})

def site(request):
    return redirect('/admin/base/siteannouncement')

def email(request):
    if request.method=="POST":
        body = request.POST["body"]
        message = request.POST["message"]
        to_email = request.POST["to_email"]
        send_mail(body,message,from_email='adityaintern11@gmail.com',recipient_list=[to_email])
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Email Sent')
        return redirect('/administrator/home')
    return render(request,'email.html')        
        