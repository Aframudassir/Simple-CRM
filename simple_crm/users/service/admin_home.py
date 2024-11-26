import datetime

from django.db.models import Sum, F

from core.models import UserSubscriberMapping, UserPayouts, UserPortfolio
from utility.common_utils import custom_response_obj


class AdminHome:


    def get_admin_home(self):
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=30)
        users_details=UserSubscriberMapping.objects.all()
        active_users=len(users_details.filter(is_active=True))
        users_joined_last_30_days=len(users_details.filter(paid_on__gte=start_date, paid_on__lte=end_date,is_active=True))

        payouts_done_last_30_days=UserPayouts.objects.filter(created_at__gte=start_date, created_at__lte=end_date).aggregate(payouts_done=Sum(F('payout_amount')))

        portfolio=list(UserPortfolio.objects.values().filter(amount_added_on__gte=start_date, amount_added_on__lte=end_date).order_by('-amount_added_on'))[:10]

        results={'active_users':active_users, 'user_joined_30_days':users_joined_last_30_days,
                 'recent_portfolio':portfolio, 'payouts_done_last_30_days':payouts_done_last_30_days}

        return custom_response_obj(data=results)