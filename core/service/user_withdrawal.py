from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from core.models import UserSubscriberMapping
from core.serializers.subscription_mapping_serializer import UserDetailsSubscriptionMappingSerializer
from utility.common_utils import custom_response_obj


class RaiseWithdrawalRequest:

    def raise_withdrawal(self, data):
        try:
            user_sub_mapping=UserSubscriberMapping.objects.get(user_subscriber_id=data['user_subscriber_id'],
                                                               withdraw_request_accepted=False,
                                                               is_active=True)

            user_sub_mapping.withdraw_request_raised=True
            user_sub_mapping.withdraw_request_raised_on=datetime.now().date()
            user_sub_mapping.save()

            return custom_response_obj(data={'response':'withdrawal request saved'}, code=200)
        except ObjectDoesNotExist:
            return custom_response_obj(message='requested details not found', code=404)

    def close_withdrawal_request(self, data):
        try:
            user_sub_mapping = UserSubscriberMapping.objects.get(user_subscriber_id=data['user_subscriber_id'],
                                                                 withdraw_request_raised=True,
                                                                 is_active=True)

            user_sub_mapping.withdraw_request_accepted = True
            user_sub_mapping.withdraw_request_raised_accepted_on = datetime.now().date()
            user_sub_mapping.paid=True
            user_sub_mapping.paid_on=datetime.now().date()
            user_sub_mapping.is_active=False
            user_sub_mapping.save()

            return custom_response_obj(data={'response': 'withdrawal request saved'}, code=200)
        except ObjectDoesNotExist:
            return custom_response_obj(message='requested details not found', code=404)


    def get_withdrawal_request(self):
        user_sub_mapping = UserSubscriberMapping.objects.filter(withdraw_request_raised=True)
        return custom_response_obj(data=UserDetailsSubscriptionMappingSerializer(user_sub_mapping, many=True).data)

