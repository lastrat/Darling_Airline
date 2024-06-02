from django.db import models
from django.core.exceptions import ValidationError

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length= 25)
    email = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user_id}:{self.username}"

class Aeroplane(models.Model):
    aero_id = models.CharField(max_length=20, primary_key=True)
    aero_model = models.CharField(max_length=30)
    tot_first_class = models.IntegerField()
    tot_economy = models.IntegerField()
    
    def __str__(self):
        return f"{self.aero_id}: {self.aero_model}"

class Flight(models.Model):
    f_id = models.AutoField(primary_key=True)
    dest_airport = models.CharField(max_length=50)
    depart_airport = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    duration = models.IntegerField()
    available_place = models.IntegerField()
    is_active = models.BooleanField()
    aero_id = models.ForeignKey(Aeroplane, on_delete=models.CASCADE)
    
    def buyplace(self, num):
        self.available_place = self.available_place - num 

    def clean(self)-> None:
        if self.available_place < 0:
            raise ValidationError("The Available place can not be less than zero")
        return super().clean()
    
    def save(self,*args, **kwargs)-> None:
        self.clean()
        return super().save(*args,**kwargs)
    def __str__(self):
        return f"{str(self.f_id)}: {self.depart_airport} ==> {self.dest_airport}"


class Contact(models.Model):
    #creating an automatic field using a function called build_id
    num = models.AutoField(primary_key=True, auto_created=True)
    mail = models.EmailField()
    phone = models.CharField(max_length=15)
    msg = models.CharField(max_length=150)
    client = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.num} : {self.mail}"


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_class = models.CharField(max_length=20)
    price = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    seat_number = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.ticket_id} : ({self.ticket_class}: {self.price}) => ({self.user_id.first_name} {self.user_id.last_name}, {self.seat_number}, {self.flight_id.depart_airport} to {self.flight_id.dest_airport}) => {self.purchase_date}"

    def clean(self)-> None:
        if self.price < 0:
            raise ValidationError("The place of a ticket can not be less than zero")
        return super().clean()
    
    def save(self,*args, **kwargs)-> None:
        self.clean()
        return super().save(*args,**kwargs)

    
class Stop(models.Model):
    stop_id = models.IntegerField(primary_key=True, auto_created=True)
    airport_name = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{int(self.stop_id)} : {self.airport_name} ==> {self.arrival_time}"


class Reservation(models.Model):
    reservationId= models.AutoField(primary_key=True)
    ticket_categories = models.CharField(max_length=25)
    num_tickets = models.IntegerField()
    total_price = models.FloatField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=0)
    
    def __str__(self):
        return f"{int(self.reservationId)} : {self.user_id.first_name} ==> {self.flight_id.depart_airport}"
    

    def clean(self)-> None:
        if self.num_tickets < 0:
            raise ValidationError("The Number of ticket can not be less than zero")
        if self.total_price < 0:
            raise ValidationError("The total price can not be less than zero")
        return super().clean()
    
    def save(self,*args, **kwargs)-> None:
        self.clean()
        return super().save(*args,**kwargs)



class Price(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    class_type = models.CharField(max_length=30)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    price = models.IntegerField(default=200)
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} : {self.class_type} ==> {self.price} || {self.flight_id.depart_airport} ==> {self.flight_id.dest_airport}"
    def clean(self)-> None:
        if self.price < 0:
            raise ValidationError("The price can not be less than zero")
        return super().clean()
    
    def save(self,*args, **kwargs)-> None:
        self.clean()
        return super().save(*args,**kwargs)
    

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    payment_method =models.CharField(max_length=50)
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{int(self.payment_id)} : {self.reservation_id.user_id.first_name}({self.reservation_id.user_id.user_id}) ==> {self.amount} ==> {self.reservation_id.flight_id.depart_airport}"



    def clean(self)-> None:
        if self.amount < 0:
            raise ValidationError("The amount of a payment can not be less than zero")
    
    def save(self,*args, **kwargs)-> None:
        self.clean()
        return super().save(*args,**kwargs)


