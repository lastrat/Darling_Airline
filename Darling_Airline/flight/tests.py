from django.test import TestCase
from django.core.exceptions import ValidationError
#from django.utils import timezone

from .models import *


class FlightModelTest(TestCase):

    def test_available_place_less_than_0_raises_error(self):
        """
        Check whether the save method raises a ValidationError when the available_place is less than 0.
        """

        #create an instance of user
        user = User(user_id=1, username="Darling", first_name="Sim Sim", last_name = "Rochinel", password="1234", email = "simo@gmail.com")
        
        # Create an Aeroplane instance
        aeroplane = Aeroplane.objects.create(
            aero_id="TEST_ID",
            aero_model="Test Model",
            tot_first_class=100,
            tot_economy=200
        )

        flight = Flight(
            f_id=5,
            dest_airport="Paris_france",
            depart_airport="Yaounde - Cameroun",
            departure_time="2024-06-01 12:00:00",
            duration=120,
            available_place=100,
            is_active=1,
            aero_id=aeroplane  # Assign the Aeroplane instance
        )
        
        #self.assertRaises( ValidationError, flight.save )
       # with self.assertRaises(ValidationError) as context:
        #    flight.save()
            
        #ticket = Ticket(ticket_id= 1, ticket_class= "first",  price=-100 , seat_number=25 , user_id=user, flight_id=flight)
        #self.assertRaises( ValidationError, ticket.save )

        reservation = Reservation(ticket_categories = "first", num_tickets=5 , total_price= 100,user_id= user, flight_id= flight, is_paid=0)
        #self.assertRaises( ValidationError, reservation.save )
        
        """price = Price(
             id = "First price",
            class_type = "Economy",
            valid_from = "2024-06-01 12:00:00",
            valid_to = "2024-07-01 12:00:00",
            price = -200,
            flight_id = flight
        )
        
        self.assertRaises( ValidationError, price.save )"""
        
        
        payment = Payment(
            amount = -500,
            payment_method = "cc card",
            reservation_id = reservation
        )
        
        self.assertRaises( ValidationError, payment.save )