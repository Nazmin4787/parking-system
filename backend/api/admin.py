from django.contrib import admin
from .models import User, ParkingSlot, Booking

admin.site.register(User)
admin.site.register(ParkingSlot)
admin.site.register(Booking)
