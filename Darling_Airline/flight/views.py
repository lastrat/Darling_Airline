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
    return redirect('index')
def flights(request):
    data = Flight.objects.filter(departure_time__gt = Now())

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

def book(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            flight = request.POST.get('flight')
            #flightdate = request.POST.get('flightDate')
            #flightclass = request.POST.get('flightClass')

            countrycode = request.POST['countryCode']
            mobile = request.POST['mobile']
            email = request.POST['email']

            flight = Flight.objects.get(id=flight)

            userscount = request.POST['usersCount']
            users = []
            for i in range(1, int(userscount) + 1):
                fname = request.POST[f'user{i}first_name']
                lname = request.POST[f'user{i}last_name']
                #gender = request.POST[f'user{i}Gender']
                users.append(
                    user.objects.create(
                        first_name=fname,
                        last_name=lname,
                        #gender=gender.lower()
                    )
                )

            coupon = request.POST.get('coupon')

            try:
                ticket1 = createticket(request.user, users, userscount,
                                       flight
                        , flightdate, flightclass, coupon,
                                       countrycode, email, mobile)
                fare = calculate_fare(flightclass, userscount, flight
)
                return render(request, "flight/payment.html", {
                    'fare': fare + FEE,
                    'ticket': ticket1.id
                })
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")

def ticket_data(request, ref):
    ticket = Ticket.objects.get(ref_no=ref)
    return JsonResponse({
        'ref': ticket.ref_no,
        'from': ticket.flight.origin.code,
        'to': ticket.flight.destination.code,
        'flight_date': ticket.flight_ddate,
        'status': ticket.status
    })

@csrf_exempt
def get_ticket(request):
    ref = request.GET.get("ref")
    ticket1 = Ticket.objects.get(ref_no=ref)
    data = {
        'ticket1':ticket1,
        'current_year': datetime.now().year
    }
    pdf = render_to_pdf('flight/ticket.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
