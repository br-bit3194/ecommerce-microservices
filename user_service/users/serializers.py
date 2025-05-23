# user_service/serializers.py
from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name', 'email']
