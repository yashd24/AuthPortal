from rest_framework import serializers
from .models import UserModel,ForgotPasswordMapping
from datetime import datetime,timedelta
from django.utils import timezone
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = UserModel
        fields = ('userID', 'username', 'email', 'password', 'password2', 'date_joined', 'last_updated', 'is_staff', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):

        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        
        del validated_data['password2']
        user = UserModel.objects.create_user(**validated_data)
        return user
    


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForgotPasswordMapping
        fields = ('email', 'token', 'date_created', 'is_active')
        extra_kwargs = {'token': {'read_only': True}, 'date_created': {'read_only': True}, 'is_active': {'read_only': True}}


    