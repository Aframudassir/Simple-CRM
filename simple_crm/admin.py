from django.contrib import admin


from django.contrib.auth.admin import UserAdmin
from simple_crm.models import User



@admin.register(User)
class UserAdmin(UserAdmin):

    list_display = ('username','phone',)
    search_fields = ['username','phone',]

    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('phone','user_consent','subscription_done','referral_code', 'referred_by')
        }),

    )



