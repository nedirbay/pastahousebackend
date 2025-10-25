from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    username = serializers.CharField(required=False)
    tokens = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password', 'username', 'is_staff', 'created_at', 'tokens')
        read_only_fields = ('id', 'is_staff', 'created_at', 'tokens')

    def get_tokens(self, user):
        """Get token pairs for the user."""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def generate_unique_username(self, email):
        """Generate unique username from email."""
        # берём часть до @ и добавляем случайный суффикс
        base = email.split('@')[0]
        username = base
        while User.objects.filter(username=username).exists():
            # если занят, добавляем 8 случайных символов
            random_suffix = str(uuid.uuid4())[:8]
            username = f"{base}_{random_suffix}"
        return username

    def create(self, validated_data):
        password = validated_data.pop('password')
        # если username не предоставлен, генерируем из email
        if 'username' not in validated_data:
            validated_data['username'] = self.generate_unique_username(validated_data['email'])
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        # не позволяем менять username через update
        validated_data.pop('username', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
