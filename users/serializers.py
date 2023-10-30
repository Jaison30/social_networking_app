from rest_framework import serializers
from authentication.models import CustomUser 
from .models import Friendship


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')


class UserSearchSerializer(serializers.Serializer):
    search = serializers.CharField(max_length=100, required=False)


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('sender', 'receiver')


class FriendRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='receiver.username')
    email = serializers.EmailField(source='receiver.email')
    class Meta:
        model = Friendship
        fields = ('id', 'username', 'email')


class FriendRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('status', )