from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('events/', EventListCreateAPIView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailAPIView.as_view(), name='event-detail'),

    path('bookings/', BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail'),
    path('registeruser/', RegisterUsersBulk.as_view(), name='register-users-bulk'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/<int:event_id>/', UsersForEventView.as_view(), name='users-for-event'),
    path('qr-booking-form/', qr_booking_form_view, name='qr_booking_form'),

]

