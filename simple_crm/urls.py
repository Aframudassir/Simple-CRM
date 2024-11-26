from django.urls import path

from simple_crm.users.views.admin_home import AdminHomeView
from simple_crm.users.views.login import LoginUserView
from simple_crm.users.views.registration import UserView
from simple_crm.users.views.user_details import UserDetailsView
from simple_crm.users.views.user_home import UserHomeView
from simple_crm.users.views.users_plans import UsersPlansView


urlpatterns = [
    path('', UserView.as_view()),
    path('login', LoginUserView.as_view()),
    path('plans', UsersPlansView.as_view()),
    path('details', UserDetailsView.as_view()),
    path('home',UserHomeView.as_view()),
    path('admin-home', AdminHomeView.as_view())
]