from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from flight.models import *
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
    def setUp(self):
        # Create an Aeroplane instance
        self.aeroplane = Aeroplane.objects.create(
            aero_id="TEST_ID",
            aero_model="Test Model",
            tot_first_class=100,
            tot_economy=200
        )

    def test_departure_time_in_the_future(self):
        """
        Ensure that the save method raises a ValidationError if the departure_time is not in the future.
        """
        past_time = datetime.now() - timedelta(days=1)
        future_time = datetime.now() + timedelta(days=1)

        # Test past departure time
        flight_past = Flight(
            dest_airport="Test Destination",
            depart_airport="Test Departure",
            departure_time=past_time,
            duration=120,
            available_place=50,
            is_active=True,
            aero_id=self.aeroplane
        )

        with self.assertRaises(ValidationError):
            flight_past.save()

        # Test future departure time
        flight_future = Flight(
            dest_airport="Test Destination",
            depart_airport="Test Departure",
            departure_time=future_time,
            duration=120,
            available_place=50,
            is_active=True,
            aero_id=self.aeroplane
        )

        try:
            flight_future.save()
        except ValidationError:
            self.fail("save() raised ValidationError unexpectedly for a future departure_time")

class UserModelTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'user_id': 1,
            'username': 'validuser_123',
            'password': 'Validpassword1@',
            'first_name': 'Jeffery',
            'last_name': 'Wilson',
            'email': 'jeffery.wilson@example.com'
        }

    def test_valid_user(self):
        """
        Ensure a user with valid data does not raise a ValidationError.
        """
        user = User(**self.valid_data)
        try:
            user.full_clean()
        except ValidationError:
            self.fail("Valid user data raised ValidationError")

    def test_invalid_username(self):
        """
        Ensure invalid usernames raise a ValidationError.
        """
        invalid_usernames = ['ab', 'user@name', 'a' * 51]
        for username in invalid_usernames:
            with self.subTest(username=username):
                data = self.valid_data.copy()
                data['username'] = username
                user = User(**data)
                with self.assertRaises(ValidationError):
                    user.full_clean()

    def test_invalid_password(self):
        """
        Ensure invalid passwords raise a ValidationError.
        """
        invalid_passwords = ['password', 'PASSWORD', 'pass1234', 'Pass1234', 'P@ssw0rd', 'a' * 256]
        for password in invalid_passwords:
            with self.subTest(password=password):
                data = self.valid_data.copy()
                data['password'] = password
                user = User(**data)
                with self.assertRaises(ValidationError):
                    user.full_clean()

    def test_invalid_first_name(self):
        """
        Ensure invalid first names raise a ValidationError.
        """
        invalid_first_names = ['John1', 'J@hn', 'a' * 26]
        for first_name in invalid_first_names:
            with self.subTest(first_name=first_name):
                data = self.valid_data.copy()
                data['first_name'] = first_name
                user = User(**data)
                with self.assertRaises(ValidationError):
                    user.full_clean()

    def test_invalid_last_name(self):
        """
        Ensure invalid last names raise a ValidationError.
        """
        invalid_last_names = ['Doe1', 'D@e', 'a' * 26]
        for last_name in invalid_last_names:
            with self.subTest(last_name=last_name):
                data = self.valid_data.copy()
                data['last_name'] = last_name
                user = User(**data)
                with self.assertRaises(ValidationError):
                    user.full_clean()

    def test_invalid_email(self):
        """
        Ensure invalid emails raise a ValidationError.
        """
        invalid_emails = ['plainaddress', 'missingatsign.com', 'missingdomain@.com']
        for email in invalid_emails:
            with self.subTest(email=email):
                data = self.valid_data.copy()
                data['email'] = email
                user = User(**data)
                with self.assertRaises(ValidationError):
                    user.full_clean()