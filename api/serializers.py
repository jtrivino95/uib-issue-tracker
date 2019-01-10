from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Ticket, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
