from django.urls import path

from core.views.referral_payouts import ReferralPayoutsView
from core.views.user_payouts import UserPayoutsView
from core.views.user_portfolio_view import UserPortfolioServiceView
from core.views.subscription_service import SubscriptionServiceView
from core.views.user_subscripe_plan import UserSubscriptionView
from core.views.user_withdrawals import UserWithdrawalView

urlpatterns = [
    path('subscription', SubscriptionServiceView.as_view()),
    path('subscription-mapping',  UserSubscriptionView.as_view()),
    path('user-portfolio',  UserPortfolioServiceView.as_view()),
    path('user-withdrawal',UserWithdrawalView.as_view()),
    path('user-payouts',UserPayoutsView.as_view()),
    path('referral-payouts', ReferralPayoutsView.as_view())
]