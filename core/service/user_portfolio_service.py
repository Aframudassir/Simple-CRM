from core.models import UserSubscriberMapping
from core.serializers.user_portfolio_mapping_serializer import UserPortfolioMappingSerializer, UserPortfolioMappingDetailsSerializer as DetailsSerializer
from utility.common_utils import custom_response_obj
from utility.crud_helper import CrudHelper

class PortfolioService:

    def add_portfolio(self, data):
        user=data.get('user', None)
        if user is None:
            users=UserSubscriberMapping.objects.filter(subscription_plan__plan_id=data.get('plan_id'),
                                                       ).values_list('user__id', flat=True)

            if len(users)==0:
                return custom_response_obj(message=f'Selected plan with id {data.get("plan_id")} has no active paid users, please select other plan', code=400)
            add_data=[]
            for i in users:
                add_data.append({'user':i,
                                 'amount':data['amount'],
                                 'subscription_plan':data['plan_id'],
                                 'amount_added_on':data['amount_added_on']
                                 })
            return CrudHelper(UserPortfolioMappingSerializer).add_obj(add_data, many=True)
        else:
            return CrudHelper(UserPortfolioMappingSerializer).add_obj({'user':user,
                                 'amount':data['amount'],
                                 'subscription_plan':data['plan_id'],
                                 'amount_added_on':data['amount_added_on']
                                                                    })

    def update_portfolio(self, data):
        return CrudHelper(UserPortfolioMappingSerializer).update_obj(data=data,
                                                                     update_key_value=data['portfolio_mapping_id']
                                                                    )

    def delete_portfolio(self, data):
        return CrudHelper(UserPortfolioMappingSerializer).delete_obj(id=data)

    def get_portfolio(self, query, paginate, request):
        filter_options = ["user__username", "amount__gte","amount__lte", "subscription_plan__name",
                          "subscription_plan__category",]
        filters = {}
        for i in filter_options:
            value = query.get(i, None)
            if value:
                filters[i] = value
        return CrudHelper(DetailsSerializer).get_all_data(query=filters, paginate=paginate, request=request)

