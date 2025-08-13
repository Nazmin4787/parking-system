from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import ParkingSlot, Booking
from .serializers import UserSerializer, ParkingSlotSerializer, BookingSerializer
from .permissions import IsAdminUser, IsCustomerUser

User = get_user_model()

# Registration view
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Allow role setting during registration (defaults to customer)
        data = request.data.copy()
        if 'role' not in data:
            data['role'] = 'customer'

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

# JWT Login view uses default TokenObtainPairView from SimpleJWT
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

# Admin-only: CRUD ParkingSlot views
class ParkingSlotListCreateView(generics.ListCreateAPIView):
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

class ParkingSlotRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

# Customer: List available parking slots (not occupied)
class AvailableParkingSlotsView(generics.ListAPIView):
    serializer_class = ParkingSlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ParkingSlot.objects.filter(is_occupied=False)

# Customer: Book a parking slot
class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerUser]

    def perform_create(self, serializer):
        # Mark slot as occupied when booking is made
        slot = serializer.validated_data['slot']
        if slot.is_occupied:
            raise serializers.ValidationError("Slot is already occupied.")
        slot.is_occupied = True
        slot.save()
        serializer.save(user=self.request.user)

# Customer: View own bookings
class UserBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerUser]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user, is_active=True)

# Customer: Cancel booking
from rest_framework.decorators import action
from rest_framework.views import APIView

class CancelBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCustomerUser]

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user, is_active=True)
        except Booking.DoesNotExist:
            return Response({"error": "Active booking not found."}, status=status.HTTP_404_NOT_FOUND)

        booking.is_active = False
        booking.end_time = timezone.now()
        booking.save()
        # Free the parking slot
        booking.slot.is_occupied = False
        booking.slot.save()
        return Response({"status": "Booking cancelled."}, status=status.HTTP_200_OK)



from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Car Parking System API")


