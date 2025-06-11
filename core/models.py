
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import qrcode
from io import BytesIO
from django.core.files import File


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    available_seats = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qr_code = models.ImageField(upload_to='event_qrcodes/', blank=True, null=True)


    def __str__(self):
        return self.title


    def generate_qr_code(self):
        qr_data = f"http://127.0.0.1:8000/qr-booking/{self.id}/"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        filename = f"{self.title}_qr.png"
        self.qr_code.save(filename, File(buffer), save=False)
        buffer.close()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr_code()
            super().save(*args, **kwargs)
            
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    num_tickets = models.PositiveIntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"




