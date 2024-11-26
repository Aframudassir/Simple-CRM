import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=100, unique=True)
    username=models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    user_consent = models.BooleanField(default=False)
    subscription_done = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=100, default=uuid.uuid4)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='customer_referral', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username", "email"]

    def __str__(self):
        return str(self.username)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['phone', 'email'], name='unique_user')
        ]
