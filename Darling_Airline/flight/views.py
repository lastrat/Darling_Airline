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
        




