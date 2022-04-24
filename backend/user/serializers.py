from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            password = make_password(validated_data['password']),
        )
