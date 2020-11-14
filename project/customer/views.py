from django.shortcuts import render,redirect
from django.contrib import messages,auth
from worker.models import Skill
from base.models import User, Room, Message
from django.http import HttpResponse
from .models import Appointment,WorkerFeedback
from django.core.mail import send_mail
from worker.models import CustomerFeedback
# Create your views here.
def dashboard(request):
    if request.user.is_authenticated and request.user.user_type=="Customer":
        return render(request,'CustomerDashboard.html')
    else:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Invalid Request. Login & Try again')
        return redirect('/')

def home(request):
    if request.user.is_authenticated and request.user.user_type=="Customer":
        return render(request,'dcHome.html')
    else:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Invalid Request. Login & Try again')
        return redirect('/')

def catalogue(request):
    primary = Skill.objects.all().select_related()
    secondary = Skill.objects.filter(secondary_exist=True).select_related()
    additional = Skill.objects.filter(additional_exist=True).select_related()
    work_name = []
    work_name.extend([item['primary_skill'] for item in Skill.objects.values('primary_skill').distinct()])
    work_name.extend([item['secondary_skill'] for item in Skill.objects.values('secondary_skill').distinct()])
    work_name.extend([item['additional_skill'] for item in Skill.objects.values('additional_skill').distinct()])
    di = {'primary':primary,'secondary':secondary,'additional':additional,'work_name':work_name}
    return render(request,"ccatalogue.html",di)

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
            return render(request,"ccatalogue.html",di)
        else:
            primary = Skill.objects.filter(primary_skill=skill_name,primary_rate__gte=300,rating=rating)
            secondary = Skill.objects.filter(secondary_skill=skill_name,secondary_rate__gte=300,rating=rating)
            additional = Skill.objects.filter(additional_skill=skill_name,additional_rate__gte=300,rating=rating)
            work_name = []
            work_name.extend([item['primary_skill'] for item in Skill.objects.values('primary_skill').distinct()])
            work_name.extend([item['secondary_skill'] for item in Skill.objects.values('secondary_skill').distinct()])
            work_name.extend([item['additional_skill'] for item in Skill.objects.values('additional_skill').distinct()])
            di = {'primary':primary,'secondary':secondary,'additional':additional,'work_name':work_name}
            return render(request,"ccatalogue.html",di)
    else:
        return redirect('/customer/catalogue')    
def startChat(request,customer_id,worker_id):
    obj = Room.objects.filter(customer=User.objects.get(id=customer_id),worker=User.objects.get(id=worker_id))
    if len(obj)==0:
        Room.objects.create(customer=User.objects.get(id=customer_id),worker=User.objects.get(id=worker_id),room_status="Opened")
        return redirect('/customer/displayChat')
    else:
        obj[0].room_status="Opened"
        obj[0].save()
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Room Reopened Again to chat.')    
        return redirect('/customer/displayChat')

def displayChat(request):
    obj = Room.objects.filter(customer=request.user)
    return render(request,"cdisplayChat.html",{'obj':obj})

def talk(request,rid):
    if request.method == 'POST':
        message = request.POST["message"]
        obj = Message.objects.create(message=message,sent_by=request.user)
        room_obj = Room.objects.get(id=rid)
        room_obj.chat.add(obj)
    room_obj = Room.objects.get(id=rid)
    messages=room_obj.chat.select_related()
    return render(request,"ctalk.html",{'rid':rid,'obj':messages})

def acceptWork(request,id):
    if request.method=="POST":
        appointment_date = request.POST["appointment_date"]
        appointment_time = request.POST["appointment_time"]
        amount = request.POST["amount"]
        working_hours = request.POST["working_hours"]
        work_name = request.POST["work_name"]
        obj = Room.objects.get(id=id)
        room_obj = Appointment.objects.create(work_name=work_name,worker=obj.worker,customer=obj.customer,working_hours=working_hours,appointment_date=appointment_date,appointment_time=appointment_time,amount=amount)
        msg = 'Mr. '+obj.worker.first_name+',\n\n\tCustomer '+obj.customer.first_name+' allows you to work. Check your Dashboard for more details\n\n'
        msg += 'Customer Name: '+obj.customer.first_name+'\nMobile Number: '+str(obj.customer.mobile)+'\nWorker Name: '+obj.worker.email+'\nWorker Mobile Number: '+str(obj.worker.mobile)+'\n\nThank you for choosing GoHelp Platform.'
        send_mail("GoHelp Platform",msg,from_email='adityaintern11@gmail.com',recipient_list=[obj.worker.email,obj.customer.email])    
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Appointment Created Successfully')
        return redirect('/customer/home')
    else:
        return redirect('/customer/displayChat')

def rejectWork(request,id):
    obj = Room.objects.get(id=id)
    obj.room_status="Closed"
    obj.save()
    msg = 'Mr. '+obj.worker.first_name+',\n\n\tCustomer '+obj.customer.first_name+' closed your application of work. More oppurtunities to come along'
    send_mail("GoHelp Platform",msg,from_email='adityaintern11@gmail.com',recipient_list=[obj.worker.email])    
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Work Rejected Successfully')    
    return redirect('/customer/home')

def workAllocated(request):
    obj = Appointment.objects.filter(customer=request.user)
    return render(request,"cworkAllocated.html",{'obj':obj})

import math
def feedback(request):
    if request.method=="POST":
        app_id = request.POST["appointment_id"]
        quality = request.POST["quality"]
        work_completed_in_time = request.POST["work_completed_in_time"]
        polite = request.POST["polite"]
        behaviour = request.POST["behaviour"]
        rating = request.POST['rating']
        obj = WorkerFeedback.objects.filter(appointment=Appointment.objects.get(id=app_id))
        if len(obj)>0:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Feedback Already Provided')
            return redirect('/customer/dashboard')
        else:
            appointment = Appointment.objects.get(id=app_id)
            obj = WorkerFeedback.objects.create(appointment=appointment,quality=quality,work_completed_in_time=work_completed_in_time,polite=polite,behaviour=behaviour,rating=rating)
            ratings_obj = WorkerFeedback.objects.filter(appointment__worker=appointment.worker).values('rating')
            ratings_obj = [item["rating"] for item in ratings_obj]
            new_rating = math.ceil(sum(ratings_obj)/len(ratings_obj))            
            skill_obj = Skill.objects.get(user=appointment.worker)
            skill_obj.rating = new_rating
            skill_obj.save()
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Feedback Provided Successfully')
            return redirect('/customer/dashboard')
    app_obj = Appointment.objects.filter(customer=request.user).values('id')
    feed_obj = WorkerFeedback.objects.filter(appointment__customer=request.user).values('appointment')
    feed_obj = {item['appointment'] for item in feed_obj}
    app_obj = {item['id'] for item in app_obj}
    required=list(app_obj.difference(feed_obj))
    app_obj = []
    for item in required:
        app_obj.append(Appointment.objects.get(id=item))
    if len(app_obj)==0:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'No Active Feedbacks')
        return redirect('/customer/home')
    return render(request,"customerFeedback.html",{'app_obj':app_obj})

def report(request):            
    feedbacks = CustomerFeedback.objects.filter(appointment__customer=request.user)
    appointments = Appointment.objects.filter(customer=request.user)
    amount, working_hours = [],[]
    for item in appointments:
        amount.append(item.amount)
        working_hours.append(item.working_hours)
    rating = []
    for item in feedbacks:
        rating.append(item.rating)
    di = {
        'app_len':len(appointments),
        'amount':sum(amount),
        'working_hours':sum(working_hours),
        'rating': sum(rating)/len(rating)
        }
    return render(request,"creport.html",di)
