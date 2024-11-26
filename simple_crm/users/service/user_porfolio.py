from django.db.models import F, Sum
from dateutil import parser as parser
from datetime import  datetime, timedelta
from core.models import UserSubscriberMapping, UserPortfolio
from utility.common_utils import custom_response_obj


class UserPortfolioService:

    def portfolio_details(self, user_id):

        user=UserSubscriberMapping.objects.filter(user__id=user_id,
                                                  is_active=True).values('last_payout_done').annotate(subscription_plan=F('subscription_plan__plan_id'),
                        ).order_by('-last_payout_done')

        plans={x['subscription_plan']:x['last_payout_done'] for x in user}
        portfolio_details = UserPortfolio.objects.filter(user__id=user_id,
                                                         subscription_plan__in=list(plans.keys()))

        total_invested=0

        trades_performed=0
        earnings=0

        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        portfolio_data = UserPortfolio.objects.filter(
            user__id=user_id,
            amount_added_on__gte=start_date,
            amount_added_on__lte=end_date
        ).values('amount_added_on','amount').order_by('amount_added_on')

        data = [
            {
                'date': entry['amount_added_on'].strftime('%Y-%m-%d'),
                'amount': entry['amount']
            }
            for entry in portfolio_data
        ]

        for i in portfolio_details:

            total_invested+=i.subscription_plan.price
            if plans[i.subscription_plan.plan_id] is None or (parser.parse(str(plans[i.subscription_plan.plan_id])).date()>= parser.parse(str(i.amount_added_on)).date()):
                earnings+=i.amount
            trades_performed+=1



        results={'portfolio':total_invested+earnings,
                 'earnings':earnings,
                 'trades_performed':trades_performed,
                 'graph':data
                 }
        return custom_response_obj(data=results,code=200)


