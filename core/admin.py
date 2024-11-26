from django.contrib import admin


from core.models import UserSubscriberMapping, SubscriptionPlan, UserPortfolio, UserPayouts, ReferralPayouts


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_id','name','category','description')
    search_fields = ['plan_id','name','category','description']



@admin.register(UserSubscriberMapping)
class UserSubscriberMappingAdmin(admin.ModelAdmin):
    list_display = ('user','subscription_plan',)
    search_fields = ['paid','is_active','subscription_plan__plan_id','user__id']



@admin.register(UserPortfolio)
class UserSubscriberMappingAdmin(admin.ModelAdmin):
    list_display = ('user','subscription_plan','amount')
    search_fields = ['amount','subscription_plan__plan_id','user__id']

@admin.register(UserPayouts)
class UserPayoutsadmin(admin.ModelAdmin):
    list_display = ('user_subs_map_id','user_payouts_id','payout_amount',)


@admin.register(ReferralPayouts)
class ReferralPayoutsadmin(admin.ModelAdmin):
    list_display = ('referral_payout_id','user','referred_user','amount',)



