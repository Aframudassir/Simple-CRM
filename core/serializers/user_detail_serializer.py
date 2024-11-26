from rest_framework import serializers

from core.models import ReferralPayouts
from simple_crm.models import User


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['id','email','phone','username','referral_code']



class ReferralPayoutSerializer(serializers.ModelSerializer):
    user=UserDetailsSerializer(many=False)
    referred_user=UserDetailsSerializer(many=False)
    class Meta:
        model=ReferralPayouts
        fields='__all__'
