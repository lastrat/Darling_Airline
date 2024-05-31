from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.db.models.functions import Now

from .models import *

def index(request):
    return render(request, 'flight/index.html')

def home(request):
    return render(request, 'flight/index.html')

def save(request):
    if 'username' in request.session:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST['username']
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pwd = request.POST['password']
        user = User(username = username, first_name = f_name, last_name = l_name, email = email, password = pwd )
        user.save()
        return redirect('login')
    return render(request, template_name='flight/signup.html')
def signin(request):
    if 'username' in request.session:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['password']
        check_user = User.objects.filter(username = username, password = pwd)
        if check_user:
            # start a session for the current user
            request.session['username'] = username
            return redirect('profile')
        else:
            msg = "Wrong Username or password!"
            return render(request, 'flight/signin.html', {'msg': msg})
    return render(request, template_name='flight/signin.html')

def profile(request):
    if 'username' in request.session:
        actual_user = request.session['username']
        param = {'current_user': actual_user}
        return render(request, 'flight/profile.html', param)
    else:
        return redirect('login')
    
def logout(request):
    try:
        del request.session['username']
    except:
        return redirect('login')
    return redirect('login')

def stops(request):
    if 'username' in request.session:
        uname2 = request.session['username']
        
        if request.method == 'GET':
            f_id = request.GET.get('f_id')
            if f_id is not None:
                data = Stop.objects.filter(flight_id=f_id)
                return render(request, 'flight/stops.html',{'current':uname2,'stop': data})
    return redirect('index')

def reservation(request):
    if 'username' in request.session:
        uname2 = request.session['username']

        if request.method == 'GET':
            voyid = request.GET.get('voyid')
            if voyid is not None:
                v = Flight.objects.filter(f_id = voyid)
                if v is not None:
                    return render(request, 'flight/reservation.html',{'flight': v, 'current':uname2})
                else:
                    return ('flight')
        if request.method == 'POST':
            uname2 = request.session['username']
            flight_id = request.POST['id']
            no = request.POST['number']
            ticket = request.POST.get('ticket')
            #return render(request, 'flight/reservation1.html',)
            # Continuation here

    return redirect('index')
def flights(request):
    data = Flight.objects.filter(departure_time__gt = Now(), available_place__gt=0)

    if 'username' in request.session:
        # if the user is logged in
        current = request.session['username']
        return render(request, 'flight/flights.html',{ 'current':current, 'flight': data})
    return render(request, 'flight/flights.html',{'flight': data})

def contact(request):
    if 'username' in request.session:
        current_user = request.session['username']
        param = {'current_user': current_user}
        if request.method == 'POST':
            email1 = request.POST['contemail']
            #num1 = Contact.objects.get(email = email1)
            cli = User.objects.get(email = email1)
            phonecont = request.POST['contphone']
            message1 = request.POST['message']
            cont = Contact(mail = email1, phone = phonecont, msg = message1, client = cli)
            cont.save()
            return HttpResponse('form sent!')
        return render(request, 'flight/contact.html', param)

    else:
        return redirect('login')
    
def myreservations(request):
    if 'username' in request.session:
        uname2 = request.session['username']
        data = Reservation.objects.filter()


