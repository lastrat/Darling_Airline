from django.shortcuts import render, redirect
<<<<<<< HEAD
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password

=======

from django.http import HttpResponse
>>>>>>> e56661bfad9060f07cd43f2132a26b24ca3ece4a

from django.db.models.functions import Now

from .models import *


def index(request):
    # Check if there is any session data
    if request.session.session_key:
        # Terminate the session
        auth_logout(request)
    return render(request, 'flight/index.html')

def home(request):
    if 'username' in request.session:
<<<<<<< HEAD
        current_user = request.session['username']
    else:
        current_user = None
    return render(request, 'flight/home.html', {'current_user': current_user})

def signup(request):
    if request.user.is_authenticated:
        return render(request, 'flight/profile.html')
    
    if request.method == 'POST':
         # Ensure CSRF token is checked
        if not request.POST.get('csrfmiddlewaretoken'):
            messages.error(request, 'CSRF verification failed. Please try again.')
            return render(request, 'flight/signup.html')
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        password = request.POST.get('password')

        if username and email and first_name and last_name and password:
            try:
                # Check if username or email already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists.')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists.')
                else:
                    # Create a new user instance
                    hashed_password = make_password(password) # Hash the password before saving the user
                    user = User(username=username, email=email, first_name=first_name, last_name=last_name, password=hashed_password)
                    user.save()
                    messages.success(request, 'Account created successfully! Please log in.')
                    return redirect('login')  # Redirect to login page after successful signup
            except IntegrityError as e:
                messages.error(request, 'An error occurred while creating the account.')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'flight/signup.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Fetch the user by username
            user = User.objects.get(username=username)
            # Check if the password matches
            if check_password(password, user.password):
                # Manually create a session
                request.session['user_id'] = user.user_id
                request.session['username'] = user.username
                messages.success(request, f'Welcome {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Wrong Username or Password!')
        except User.DoesNotExist:
            messages.error(request, 'Wrong Username or Password!')

    return render(request, 'flight/signin.html')
=======
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
>>>>>>> e56661bfad9060f07cd43f2132a26b24ca3ece4a

def profile(request):
    if 'username' in request.session:
        current_user = request.session['username']
        param = {'current_user': current_user}
        return render(request, 'flight/profile.html', param)
    else:
        return redirect('login')
    
def logout_view(request):
    # Log out the user and terminate the session
    auth_logout(request)
    # Message to confirm logout
    messages.success(request, "You have been logged out successfully.")
    # Redirect to the homepage
    return redirect('login')

def stops(request):
    if 'username' in request.session:
        uname2 = request.session['username']
        
        if request.method == 'GET':
            f_id = request.GET.get('f_id')
            if f_id is not None:
                data = Stop.objects.filter(flight_id=f_id)
                return render(request, 'flight/stops.html',{'current':uname2,'stop': data})
    return redirect('login')

def reservation(request):
    if 'username' in request.session:
        uname2 = request.session['username']
        print(f"test: {uname2}")

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
            no = int(request.POST.get('number'))
            ticket = str(request.POST.get('ticket'))
            print(f"ticket = {ticket} {no}")
            pr = Price.objects.get(class_type = ticket, flight_id=flight_id)
            request.session['f_id'] = flight_id
            request.session['no'] = no
            request.session['ticket'] = ticket
            price = pr.price
            total = price * no
            return render(request, 'flight/payment.html',{'current':uname2, 'total':total})
    else:
        return redirect('login')

def payment(request):
    if 'username' in request.session:
        uname2 = request.session['username']
        f_id = request.session['f_id']
        no = int(request.session['no'])
        ticket = request.session['ticket']
        user = User.objects.get(username=uname2)
        user_id = user.user_id
        
        flight = Flight.objects.get(f_id=f_id)
        if request.method == 'POST':
            total = int(request.POST.get('price'))
            
            # creating an instance of a reservation
            r = Reservation(ticket_categories= ticket, num_tickets = no,total_price=total,user_id=user, flight_id=flight, is_paid=1)
            r.save()
            
            # getting an instance of reservation
            reservation = Reservation.objects.get(num_tickets = no, user_id=user_id, flight_id=f_id, is_paid=1)
            
            # creating an instance of a payment
            pay = Payment(amount=total,payment_method = "Card CC", reservation_id=reservation)
            pay.save()
            f = Flight.objects.get(f_id=f_id)
            print(f"{f.depart_airport}")
            
            # reducing the available place
            f.buyplace(no)
            f.save()
            
            # creating the various tickets            
            for i in range(no):
                ticket1 = Ticket(
                    ticket_class = ticket,
                    price = int(total/no),
                    seat_number = int((100- (f.available_place + i))),
                    user_id = user,
                    flight_id = flight
                )
                ticket1.save()
            # Getting the various instance of a ticket bought by a particular user
            tickets = Ticket.objects.filter(user_id=user.user_id, flight_id = flight.f_id, ticket_class = ticket)

            return render(request, 'flight/ticket.html',{'tickets': tickets})
        return redirect('flights')
    return redirect('login')

def flights(request):
    data = Flight.objects.filter(departure_time__gt = Now(), available_place__gt=0)

    if 'username' in request.session:
        # if the user is logged in
        current_user = request.session['username']
        return render(request, 'flight/flights.html',{ 'current':current_user,
                       'flight': data}) 
    return render(request, 'flight/flights.html',{'flight': data})

def contact(request):
    if 'username' in request.session:
<<<<<<< HEAD
        user_id = request.session['user_id']
        try:
            current_user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            # Handle case where user does not exist
            return redirect('login')

=======
        current_user = request.session['username']
        param = {'current_user': current_user}
>>>>>>> e56661bfad9060f07cd43f2132a26b24ca3ece4a
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
        if request.method == 'POST':
            user_id = request.POST['user_id']
            f_id = request.POST['f_id']
            category = request.POST['category']
            # Getting the various instance of a ticket bought by a particular user
            tickets = Ticket.objects.filter(user_id=user_id, flight_id = f_id, ticket_class = category)

            return render(request, 'flight/ticket.html',{'tickets': tickets})
            
        uname2 = request.session['username']
        user = User.objects.get(username=uname2)
        user_id = user.user_id
        data = Reservation.objects.filter(is_paid =  1, user_id = user_id)
        if data is not None:
            return render(request,'flight/myreservations.html', {'current':uname2, 'reserved':data})
        else:
            return redirect('home')
    return redirect('login')

def ticket(request):
    if 'username' in request.session:
        pass
    else:
        return redirect('login')
        




