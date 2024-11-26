

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from oauth2_provider.models import RefreshToken, Application, AccessToken
from django.utils import timezone
from oauthlib import common

from core.models import UserSubscriberMapping, UserPortfolio
from core.serializers.subscription_serializer import SubscriptionSerializer
from core.serializers.user_detail_serializer import UserDetailsSerializer
from simple_crm.models import User
from simple_crm.users.user_serializers.user_serializer import CreateUserSerializer, UpdateUserSerializer
from utility.common_utils import custom_response_obj
from utility.crud_helper import CrudHelper
from core.serializers.user_portfolio_mapping_serializer import UserPortfolioMappingDetailsSerializer
from datetime import timedelta



class UserService:

    __user_crud_helper=CrudHelper(CreateUserSerializer)

    """
        creates an obj in user field
    """
    def create_user(self, data):
        try:
            user = User.objects.get(phone=data.get('phone'))
            return custom_response_obj(data=CreateUserSerializer(user).data,code=400,message='User with this phone number already exists')
        except ObjectDoesNotExist:
            referral_code=data.get('referral_code', None)
            if referral_code is not None:
                user=User.objects.get(referral_code=referral_code)
                data['referred_by']=user.id

            user=self.__user_crud_helper.add_obj(data)
            return user


    """
        get data by id , Id will always be primary key
        if id is not provided then return all data
    """
    def get_data(self, data, request=None, pagination=None):
        if data is not None:
            return self.__user_crud_helper.get_all_data(request=request, paginate=pagination, exclude={'email':request.user.email})
        else:
            return self.__user_crud_helper.get_data_by_id(id=data.get('id'))
    """
        updates table obj using update data and primary key of the obj 
        that is currently being updated
    """
    def update_data(self, data, instance_primary_key):
        return CrudHelper(UpdateUserSerializer).update_obj(data, update_key_value=instance_primary_key)

    """
        Deletes data against the primary key
    """
    def delete_data(self, instance_primary_key):
        return self.__user_crud_helper.delete_obj(instance_primary_key)


    """
        Authenticate user and generate access token
    """
    def login_user(self, data):
        username = get_user_model().objects.get(phone=data.get('phone'))
        correct_password = username.check_password(data.get('password'))
        if correct_password:
            return self.__generate_token(username, data=data)
        else:
            return custom_response_obj(data=None, message='Invalid credentials, Please check your username/password',
                                       code=401)

    def __generate_token(self, user, data):
        application = Application.objects.all().first()

        remember_me = data.get('remember_me')
        if not remember_me:
            expires = timezone.now() + timedelta(seconds=18600)
        else:
            expires = timezone.now() + timedelta(days=30)
        current_token = common.generate_token()
        refresh_token = common.generate_token()
        access_token = AccessToken(
            user=user,
            scope='',
            expires=expires,
            token=current_token,
            application=application
        )
        access_token.save()
        refresh_token_data = RefreshToken(
            user=user,
            token=refresh_token,
            application=application,
            access_token=access_token
        )
        refresh_token_data.save()
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return custom_response_obj(data={
            'access_token': current_token,
            'refresh_token': refresh_token,
            'expiry': expires,
            'user': user.username,
            'email':user.email,
            'subscription_done':user.subscription_done,
            },

            code=200)
    """
        Refresh access token
    """
    def refresh_token(self, data):
        refresh_token = self.__validate_refresh_token(refresh_token=data['refresh_token'])
        if refresh_token is not None:
            user = refresh_token.user
            refresh_token.revoked = timezone.now()
            refresh_token.save()
            return self.__generate_token(user=user, data=data)
        else:
            return custom_response_obj(data=None,
                                       message='Invalid refresh token, please login to generate new access token',
                                       )

    def __validate_refresh_token(self, refresh_token):
        try:
            refresh_token=RefreshToken.objects.get(token=refresh_token,revoked__isnull=True)
            return refresh_token
        except ObjectDoesNotExist:
            return None


    def list_all_users(self, options):
        filter_options=["username","phone","email"]
        filters={}
        for i in filter_options:
            value=options.get(i, None)
            if value:
                filters[i]=value


        users=self.__user_crud_helper.get_all_data(filters)
        return users



    def get_user_details(self, user_id):
        try:
            user=User.objects.get(id=user_id)
            print(user, user.id)
            subscriptions_taken=UserSubscriberMapping.objects.filter(user__id=user.id)
            portfolio=UserPortfolio.objects.filter(user__id=user.id)

            response={
                'user':UserDetailsSerializer(user).data,
                'subscriptions_taken':SubscriptionSerializer([x.subscription_plan for x in subscriptions_taken], many=True).data,
                'portfolio':UserPortfolioMappingDetailsSerializer(portfolio, many=True).data
            }
            return custom_response_obj(response, code=200)
        except ObjectDoesNotExist:
            return custom_response_obj(message=f'User details not found with id {user_id}',code=404)
