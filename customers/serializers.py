from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomerProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff"]


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ["user", "city", "age", "phone_number", "is_active"]
