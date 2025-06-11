from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from .utils import generate_qr_code_for_event  # import the QR generator


class EventSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if obj.qr_code:
            return request.build_absolute_uri(obj.qr_code.url) if request else obj.qr_code.url
        return None

    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        event.qr_code.save(f"event_{event.id}_qr.png", generate_qr_code_for_event(event.id))
        return event
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user']  # Tell DRF not to expect this in the request
        


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn’t match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user