from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TODO


class TODOSerializer(serializers.ModelSerializer):
    class Meta:
        model = TODO
        fields = ['id', 'title', 'priority', 'status']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
