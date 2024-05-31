from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length= 25)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Aeroplane(models.Model):
    aero_id = models.CharField(max_length=20, primary_key=True)
    aero_model = models.CharField(max_length=30)
    tot_first_class = models.IntegerField()
    tot_economy = models.IntegerField()
    
    def __str__(self):
        return self.aero_id

class Flight(models.Model):
    f_id = models.AutoField(primary_key=True)
    dest_airport = models.CharField(max_length=50)
    depart_airport = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    duration = models.IntegerField()
    available_place = models.IntegerField()
    is_active = models.BooleanField()
    aero_id = models.ForeignKey(Aeroplane, on_delete=models.CASCADE)


class Contact(models.Model):
    #creating an automatic field using a function called build_id
    num = models.AutoField(primary_key=True, auto_created=True)
    mail = models.EmailField()
    phone = models.CharField(max_length=15)
    msg = models.CharField(max_length=150)
    client = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        return self.mail


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_class = models.CharField(max_length=20)
    price = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    seat_number = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)

    
class Stop(models.Model):
    stop_id = models.IntegerField(primary_key=True, auto_created=True)
    airport_name = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)


class Reservation(models.Model):
    reservationId= models.AutoField(primary_key=True)
    ticket_categories = models.CharField(max_length=25)
    num_tickets = models.IntegerField()
    total_price = models.FloatField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)

class Price(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    class_type = models.CharField(max_length=30)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.id

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    payment_method =models.CharField(max_length=50)
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE)


