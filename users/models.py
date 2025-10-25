from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Use email as unique identifier
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
