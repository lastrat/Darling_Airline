from django.test import TestCase

from django.core.exceptions import ValidationError

from .models import * 

class FlightModelTest(TestCase):
    
    def test_available_place_less_than_0_raises_error(self):
        """
        check whether the save method raises a ValidationError when rhe palce available < 0
        """

        flight = Flight(f_id=2, dest_airport="Paris_france", depart_airport= "Yaounde - Cameroun", departure_time = "", duration = 120, available_place=-1, is_active=1, aero_id="dqh")

        self.assertRaises(ValidationError, flight.save)

        