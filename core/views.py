from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404

# List all events / Create event
class EventListCreateAPIView(APIView):
    # Returns a list of all events (public).

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
#Allows creating a new event (no auth required).
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, delete a specific event
class EventDetailAPIView(APIView):

#get: Fetches a specific event by its pk.

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

#put: Updates a specific event.
    def put(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   #delete: Deletes a specific event.
    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# List and create bookings (auth required)
class BookingListCreateAPIView(APIView):
#Only logged-in (authenticated) users are allowed to access this API view.
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, delete a specific booking
class BookingDetailAPIView(APIView):
#All actions (get, put, delete) work only on bookings that belong to the logged-in user.
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

#This view allows a logged-in user to update a specific booking if that booking belongs to them.


    def put(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterUsersBulk(APIView):
    def post(self, request):
        users_data = request.data.get('users')
        if not users_data or not isinstance(users_data, list):
            return Response({"error": "Provide a list of users"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate input data first
        for user_data in users_data:
            name = user_data.get('name')
            email = user_data.get('email')
            if not name or not email:
                return Response({"error": "Each user must have name and email"}, status=status.HTTP_400_BAD_REQUEST)
        
        emails = [user['email'] for user in users_data]
        
        # Check if any of the emails already exist
        existing_users = User.objects.filter(email__in=emails).values_list('email', flat=True)
        existing_emails = list(existing_users)
        
        if existing_emails:
            return Response(
                {"error": "Some users already registered", "emails": existing_emails},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prepare users to create
        users_to_create = [User(name=user['name'], email=user['email']) for user in users_data]
        
        # Bulk create
        User.objects.bulk_create(users_to_create)
        
        return Response({"message": f"{len(users_to_create)} users registered successfully."})

    
class UsersForEventView(APIView):
    def get(self, request, event_id):
        bookings = Booking.objects.filter(event_id=event_id)
        user_ids = bookings.values_list('user_id', flat=True).distinct()
        
        users = User.objects.filter(id__in=user_ids)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)