from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

from core.models import SubscriptionPlan, UserSubscriberMapping
from core.serializers.subscription_mapping_serializer import UserSubscriptionMappingSerializer, UserDetailsSubscriptionMappingSerializer as DetailsSerializer
from core.service.user_payouts import UserPayoutsDetails
from simple_crm.models import User
from utility.common_utils import custom_response_obj
from utility.crud_helper import CrudHelper


class UserSubscriptionService:

    __crud_helper=CrudHelper(UserSubscriptionMappingSerializer)

    def create_mapping(self, data):
        try:
            user=User.objects.get(id=data.get('user'))
            plan_details=SubscriptionPlan.objects.get(plan_id=data.get('subscription_plan'))
            user.subscription_done=True
            user.save()
            if user.referred_by is not None:
                UserPayoutsDetails().create_payout_per_user(user=user.referred_by, referred_user=user, amount=plan_details.price * 0.10)
            if plan_details.re_payment_type=="MONTHLY":
                data['next_payment_on']=datetime.now().date()+timedelta(days=30)
            elif plan_details.re_payment_type=='END_OF_TERM':
                data['next_payment_on'] = datetime.now().date() + timedelta(days=365)

            return self.__crud_helper.add_obj(data)
        except ObjectDoesNotExist:
            return custom_response_obj(message='data not found', code=404)

    def get_users_based_on_subscription(self, subscription_plan_id, pagination, request):
        data=CrudHelper(DetailsSerializer).get_all_data({'subscription_plan__plan_id':subscription_plan_id},paginate=pagination, request=request)
        data['data']=[x['user'] for x in data['data']]
        return data

    def plans_by_user(self, user):
        data=UserSubscriberMapping.objects.filter(user__id=user).values('user_subscriber_id','paid','is_active').annotate(
            name=F('subscription_plan__name'),
            description=F('subscription_plan__description'),
            price=F('subscription_plan__price'),
            term=F('subscription_plan__term'),
            expected_return=F('subscription_plan__expected_return'),
            payment_done_on=F('subscription_plan__updated_at'),
            re_payment_type=F('subscription_plan__re_payment_type')
        )

        return custom_response_obj(data=data, message='request processed successfully',code=200)