from django.shortcuts import render,redirect
from django.contrib import messages,auth
from .models import Skill,CustomerFeedback
from base.models import Room, Message
from customer.models import Appointment,WorkerFeedback
# Create your views here.
def dashboard(request):
    if request.user.is_authenticated and request.user.user_type=="Worker":
        return render(request,'workerDashboard.html')
    else:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Invalid Request. Login & Try again')
        return redirect('/')

def home(request):
    if request.user.is_authenticated and request.user.user_type=="Worker":
        return render(request,'dwHome.html')
    else:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Invalid Request. Login & Try again')
        return redirect('/')

def addSkill(request):
    if request.method=="POST":
        primary_skill = request.POST["primary_skill"]
        primary_exp = request.POST["primary_exp"]
        primary_rate = request.POST["primary_rate"]
        secondary_skill = request.POST["secondary_skill"]
        secondary_exist = True
        if secondary_skill=="":
            secondary_exist = False
        secondary_exp = request.POST["secondary_exp"]
        secondary_rate = request.POST["secondary_rate"]
        additional_skill = request.POST["additional_skill"]
        additional_exp = request.POST["additional_exp"]
        additional_rate = request.POST["additional_rate"]
        additional_exist = True
        if secondary_skill=="":
            additional_exist = False
        if len(Skill.objects.filter(user=request.user))>0:
            Skill.objects.filter(user=request.user).update(secondary_exist=secondary_exist,additional_exist=additional_exist,user=request.user,primary_exp=primary_exp,secondary_exp=secondary_exp,additional_exp=additional_exp,primary_rate=primary_rate,secondary_rate=secondary_rate,additional_rate=additional_rate,primary_skill=primary_skill,secondary_skill=secondary_skill,additional_skill=additional_skill)
        else:
            Skill.objects.create(secondary_exist=secondary_exist,additional_exist=additional_exist,user=request.user,primary_exp=primary_exp,secondary_exp=secondary_exp,additional_exp=additional_exp,primary_rate=primary_rate,secondary_rate=secondary_rate,additional_rate=additional_rate,primary_skill=primary_skill,secondary_skill=secondary_skill,additional_skill=additional_skill)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Skill Added Successfully')
        return redirect('/worker/dashboard')
    obj = Skill.objects.filter(user=request.user)
    if len(obj)>0:
        return render(request,"addSkill.html",{'obj':obj[0]})    
    else:
        return render(request,"addSkill.html")    

def catalogue(request):
    primary = Skill.objects.all().select_related()
    secondary = Skill.objects.filter(secondary_exist=True).select_related()
    additional = Skill.objects.filter(additional_exist=True).select_related()
    work_name = []
    work_name.extend([item['primary_skill'] for item in Skill.objects.values('primary_skill').distinct()])
    work_name.extend([item['secondary_skill'] for item in Skill.objects.values('secondary_skill').distinct()])
    work_name.extend([item['additional_skill'] for item in Skill.objects.values('additional_skill').distinct()])
    di = {'primary':primary,'secondary':secondary,'additional':additional,'work_name':work_name}
    return render(request,"wcatalogue.html",di)

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
            return render(request,"wcatalogue.html",di)
        else:
            primary = Skill.objects.filter(primary_skill=skill_name,primary_rate__gte=300,rating=rating)
            secondary = Skill.objects.filter(secondary_skill=skill_name,secondary_rate__gte=300,rating=rating)
            additional = Skill.objects.filter(additional_skill=skill_name,additional_rate__gte=300,rating=rating)
            work_name = []
            work_name.extend([item['primary_skill'] for item in Skill.objects.values('primary_skill').distinct()])
            work_name.extend([item['secondary_skill'] for item in Skill.objects.values('secondary_skill').distinct()])
            work_name.extend([item['additional_skill'] for item in Skill.objects.values('additional_skill').distinct()])
            di = {'primary':primary,'secondary':secondary,'additional':additional,'work_name':work_name}
            return render(request,"wcatalogue.html",di)
    else:
        return redirect('/worker/catalogue')    

def displayChat(request):
    obj = Room.objects.filter(worker=request.user)
    return render(request,"wdisplayChat.html",{'obj':obj})

def talk(request,rid):
    if request.method == 'POST':
        message = request.POST["message"]
        obj = Message.objects.create(message=message,sent_by=request.user)
        room_obj = Room.objects.get(id=rid)
        room_obj.chat.add(obj)
    room_obj = Room.objects.get(id=rid)
    messages=room_obj.chat.select_related()
    return render(request,"wtalk.html",{'rid':rid,'obj':messages})

def workAllocated(request):
    obj = Appointment.objects.filter(worker=request.user)
    return render(request,'wworkAllocated.html',{'obj':obj})

def feedback(request):
    if request.method=="POST":
        app_id = request.POST["appointment_id"]
        response = request.POST["response"]
        support = request.POST["support"]
        behaviour = request.POST["behaviour"]
        rating = request.POST['rating']
        obj = CustomerFeedback.objects.filter(appointment=Appointment.objects.get(id=app_id))
        if len(obj)>0:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Feedback Already Provided')
            return redirect('/worker/dashboard')
        else:
            appointment = Appointment.objects.get(id=app_id)
            obj = CustomerFeedback.objects.create(appointment=appointment,response=response,support=support,behaviour=behaviour,rating=rating)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Feedback Provided Successfully')
            return redirect('/worker/dashboard')
    app_obj = Appointment.objects.filter(worker=request.user).values('id')
    feed_obj = CustomerFeedback.objects.filter(appointment__worker=request.user).values('appointment')
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
        return redirect('/worker/home')
    return render(request,"workerFeedback.html",{'app_obj':app_obj})

def report(request):
    appointments = Appointment.objects.filter(worker=request.user)
    amount, working_hours = [],[]
    skill = Skill.objects.get(user=request.user)
    for item in appointments:
        amount.append(item.amount)
        working_hours.append(item.working_hours)
    di = {
        'app_len':len(appointments),
        'amount':sum(amount),
        'working_hours':sum(working_hours),
        'rating': skill.rating
        }
    return render(request,"wreport.html",di)
