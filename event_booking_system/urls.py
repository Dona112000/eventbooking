from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # For login page

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core app URLs (your API and frontend QR views)
    path('', include('core.urls')),

    # Authentication with Djoser
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # Simple JWT Token Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Django default login view for @login_required
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]

# Media file handling (for QR code images etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
