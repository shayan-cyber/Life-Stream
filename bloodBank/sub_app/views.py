from django.shortcuts import redirect, render, HttpResponse
from django.http import Http404, request
from .models import Bank,ChatRoom,Chat
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from datetime import datetime
from django.db.models import Max
from django.contrib.humanize.templatetags.humanize import naturaltime
from . import models
# Create your views here.
def home(request):
    updates = Bank.objects.filter(status = "Requested").union(Bank.objects.filter(status ="Active")).order_by("-time")
    req_updates = Bank.objects.filter(status="Requested")



    for i in req_updates:
        if timezone.now().year == i.req_time.year and timezone.now().month == i.req_time.month and timezone.now().day >= i.req_time.day + 7:
            print(str(i.name) + "delayed")
            i.status = "Donated"
            i.save()


    if request.method =="POST":
        blood_group = request.POST.get('blood_group', '')
        if blood_group !='All':
            updates= Bank.objects.filter(blood_group=blood_group, status="Requested").union(Bank.objects.filter(blood_group=blood_group,status ="Active")).order_by('-time')



    context = {
        'updates' : updates,

    }


    return render(request, "home.html", context)

def fullDetails(request, pk):
    if request.method =="POST":
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        name = request.POST.get('name','')
        print(email)
        print(phone)
        print(name)
        fulldet = Bank.objects.filter(pk=pk)[0]
        fulldet.status ="Requested"
        fulldet.req_time = timezone.now()

        fulldet.save()

        donor_mail = fulldet.email
        donor = fulldet.user.username
        donor_id =fulldet.user.pk
        #email to locator
        template_locator = render_to_string('Email_templates/email_to_donor.html',{'name':name, 'email':email, 'phone':phone, 'donor':donor, 'donor_id':donor_id})
        email_locator = EmailMessage(
            name + ' , Has Requested For Blood Donation',
            template_locator,
            settings.EMAIL_HOST_USER,
            [donor_mail],

            )
        email_locator.fail_silently = False
        email_locator.send()




        context={
            'fulldet':fulldet
        }
        return render(request,'fulldetails.html',context)
    else:
        return render(request,"error.html")
# @login_required(login_url='/')
def profile(request,pk):
    donor_user = User.objects.filter(pk = pk)[0]
    banks = Bank.objects.filter(user = donor_user, status="Requested").union(Bank.objects.filter(user = donor_user, status="Active")).order_by('-time')
    req_updates = Bank.objects.filter(status="Requested")



    for i in req_updates:
        if timezone.now().year == i.req_time.year and timezone.now().month == i.req_time.month and timezone.now().day >= i.req_time.day + 7:
            print(str(i.name) + "delayed")
            i.status = "Donated"
            i.save()
    chat_rooms = ChatRoom.objects.filter(owner__icontains=request.user.username).annotate(max_pub_date=Max('chat__time')).order_by('-max_pub_date')

    profs =[]
    print(chat_rooms)
    for i in chat_rooms:
        owner = i.chatter1
        #print(owner)
        chatname = str(owner).replace(request.user.username,'')

        profile1 = User.objects.filter(username=chatname)
        profs.append(profile1)

    print(profs)
    context ={
        "donor_user":donor_user,
        "updates":banks,
        "chatrooms":chat_rooms,
        "profs":profs,
    }


    return render(request,"profile.html", context)

@login_required(login_url='/')
def delupdt(request,pk):
    updt = Bank.objects.filter(pk=pk)[0]
    id = updt.user.pk
    updt.status = "Donated"
    updt.save()
    messages.success(request, "Your Data Has Been Deleted Successfully!!")

    return redirect('/profile/' + str(id))

def sign_up(request):
    if request.method =="POST":
        name = request.POST.get('name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        conf_pass = request.POST.get('conf_password','')
        userCheck = User.objects.filter(username =username)
        if len(username)> 20:
            messages.warning(request,"Too Long Username!!")
        elif password != conf_pass:
            messages.warning(request, "Passwords Don't Match!!")
        elif userCheck:
            messages.warning(request, "Username Already Exists , Kindly Change!!")
        else:
            user_obj = User.objects.create_user(first_name = name, password = password, email = email, username=username)

            user_obj.save()
            # prf =Profile(prof_user= user_obj)
            # prf.save()

            messages.success(request, "Account Created Successfully!!")
        return redirect("/")


    else:
        return render(request,"error.html")

def login_donor_home(request):
    if request.method =="POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        print(username + " " + password)
        user_obj = authenticate( username= username, password = password)
        print(user_obj)
        if user_obj is not None:
            login(request, user_obj)
            messages.success(request, "Logged In Successfully :^) ")
            return redirect('/')
        else:
            messages.warning(request, "Invalid Credentials : ( ")
            return redirect('/')
    else:
        return render(request, "home.html")

def login_donor_del(request):
    if request.method =="POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        prof = request.POST['profile']

        print(username + " " + password)
        user_obj = authenticate( username= username, password = password)
        print(user_obj)
        if user_obj is not None:
            login(request, user_obj)

            messages.success(request, "Logged In Successfully :^) ")
            return redirect('/profile/' + str(prof))
        else:
            messages.warning(request, "Invalid Credentials : ( ")
            return redirect('/profile/' + str(prof))
    else:
        return render(request, "error.html")


@login_required(login_url='/')
def add_updt(request):
    if request.method =="POST":
        name = request.POST.get('name', '')
        blood_group = request.POST.get('blood_group', '')
        email = request.POST.get('email', '')
        phone_no = request.POST.get('phone', '')
        decease = request.POST.get('decease', '')
        address = request.POST.get('address', '')
        bank = Bank(name=name, blood_group=blood_group, email=email, phone_no=phone_no, decease=decease, address=address,user = request.user)
        bank.save()
        messages.success(request, "Data Added Successfully !!")
        return redirect("/")
    else:
        return render(request, "error.html")
#chatroom
@login_required(login_url='/')
def talkmain(request,userchat):
    print(userchat)
    print(request.user)
    name_1 = userchat + request.user.username
    name_2 = request.user.username + userchat
    name = name_1 + name_2
    print(name)
    user = User.objects.filter(username=userchat)
    # profile = Profile.objects.get(user = user[0])
    #chatroom = ChatRoom.objects.get_or_create(
        #owner=name
    #)
    if ChatRoom.objects.filter(owner__icontains=name_1).union(ChatRoom.objects.filter(owner__icontains=name_2)):
        chatroom_created = ChatRoom.objects.filter(owner__icontains=name_1).union(ChatRoom.objects.filter(owner__icontains=name_2))[0]
    else:
        chatroom_save = ChatRoom(owner=name, chatter1=name_1)
        chatroom_save.save()
        chatroom_created = ChatRoom.objects.filter(owner__icontains=name_1).union(ChatRoom.objects.filter(owner__icontains=name_2))[0]




    msgs = Chat.objects.filter( room=chatroom_created.pk).order_by('-time')
    if request.method == 'POST':
        text = request.POST['messages1']
        #room = request.POST['room']
        chatter = request.POST['chatter']
        msg = Chat(text=text, room = chatroom_created, chatter=chatter)

        msg.save()


    return render(request, 'talk.html',{'userchat':userchat,'user':user[0], 'chatroom':chatroom_created,'msgs':msgs})

def donors_list(request):
    updts = Bank.objects.filter(status ="Donated").order_by("-req_time")
    context={
        "updts":updts
    }
    return render(request, "donors_list.html", context)
from django.contrib.auth import logout

def log_out(request):
    logout(request)
    return redirect("/")

