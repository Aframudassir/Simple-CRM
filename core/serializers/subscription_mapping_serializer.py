from rest_framework import serializers

from core.models import UserSubscriberMapping
from simple_crm.models import User


class UserSubscriptionMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserSubscriberMapping
        fields='__all__'


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username','phone','email']


class UserDetailsSubscriptionMappingSerializer(serializers.ModelSerializer):

    user=UserDetailsSerializer()
    class Meta:
        model=UserSubscriberMapping
        fields='__all__'