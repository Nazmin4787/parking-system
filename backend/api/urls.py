from django.urls import path
from . import views
from .views import (
    RegisterUserView, LoginView,
    ParkingSlotListCreateView, ParkingSlotRetrieveUpdateDestroyView,
    AvailableParkingSlotsView, BookingCreateView, UserBookingListView, CancelBookingView
)

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),

    path('slots/', ParkingSlotListCreateView.as_view(), name='slot-list-create'),
    path('slots/<int:pk>/', ParkingSlotRetrieveUpdateDestroyView.as_view(), name='slot-detail'),

    path('slots/available/', AvailableParkingSlotsView.as_view(), name='available-slots'),

    path('bookings/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/user/', UserBookingListView.as_view(), name='user-bookings'),
    path('bookings/<int:pk>/cancel/', CancelBookingView.as_view(), name='booking-cancel'),

    path('', views.home, name='home'),
]
