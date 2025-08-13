from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model with roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('security', 'Security'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

# Parking slot model
class ParkingSlot(models.Model):
    slot_number = models.CharField(max_length=20, unique=True)
    floor = models.CharField(max_length=5)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Slot {self.slot_number} (Floor {self.floor})"

# Booking model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Booking by {self.user.username} on slot {self.slot.slot_number}"
# Add any additional models here as needed

