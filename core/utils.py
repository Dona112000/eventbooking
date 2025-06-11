# utils.py
import qrcode
import io
from django.core.files.base import ContentFile
from django.urls import reverse

def generate_qr_code_for_event(event_id):
    # Construct the URL that this QR code will encode
    qr_url = f"https://yourdomain.com/qr-booking/{event_id}/"  # Or use reverse if you pass request
    
    # Generate QR code image
    qr = qrcode.make(qr_url)

    # Save to BytesIO buffer
    buffer = io.BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Return ContentFile for saving in ImageField
    return ContentFile(buffer.read(), name=f'event_{event_id}_qr.png')

