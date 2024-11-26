from rest_framework.views import APIView

from simple_crm.users.service.user_porfolio import UserPortfolioService
from utility.api_framework import ApiFramework


class UserHomeView(APIView, ApiFramework):
    serializer =None


    def process(self):
        return UserPortfolioService().portfolio_details(self.data)

    def get(self, request):
        self.data=request.user.id
        return self.main()