from django.test import TestCase
from django.core.exceptions import ValidationError
#from django.utils import timezone

from .models import Flight, Aeroplane, Flight


class FlightModelTest(TestCase):

    def test_available_place_less_than_0_raises_error(self):
        """
        Check whether the save method raises a ValidationError when the available_place is less than 0.
        """

        # Create an Aeroplane instance
        aeroplane = Aeroplane.objects.create(
            aero_id="TEST_ID",
            aero_model="Test Model",
            tot_first_class=100,
            tot_economy=200
        )

        flight = Flight(
            f_id=2,
            dest_airport="Paris_france",
            depart_airport="Yaounde - Cameroun",
            departure_time="2024-06-01 12:00:00",
            duration=120,
            available_place=-1,
            is_active=1,
            aero_id=aeroplane  # Assign the Aeroplane instance
        )

        with self.assertRaises(ValidationError) as context:
            flight.save()

        self.assertIn("The Available place can not be less than zero", str(context.exception))  # Updated assertion
