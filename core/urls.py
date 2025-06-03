from django.urls import path
from .views import *

urlpatterns = [
    path('events/', EventListCreateAPIView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailAPIView.as_view(), name='event-detail'),

    path('bookings/', BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail'),
    path('registeruser/', RegisterUsersBulk.as_view(), name='register-users-bulk'),
    path('users/<int:event_id>/', UsersForEventView.as_view(), name='users-for-event'),

]
