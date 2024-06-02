from django.contrib import admin

from .models import *


admin.site.register(User)

admin.site.register(Flight)

admin.site.register(Aeroplane)

admin.site.register(Stop)

admin.site.register(Price)

admin.site.register(Reservation)

admin.site.register(Payment)

admin.site.register(Contact)

admin.site.register(Ticket)