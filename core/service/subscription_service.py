from core.serializers.subscription_serializer import SubscriptionSerializer
from utility.crud_helper import CrudHelper


class SubscriptionPlan:
    __subscription_crud_helper=CrudHelper(SubscriptionSerializer)

    def create(self, data):
        return self.__subscription_crud_helper.add_obj(data)

    def update(self,data):
        return self.__subscription_crud_helper.update_obj(data,update_key_value=data.get("plan_id"))

    def list(self):
        return self.__subscription_crud_helper.get_all_data()

    def retrieve(self, subscription_id):
        return self.__subscription_crud_helper.get_data_by_id(subscription_id)

    def delete(self, subscription_id):
        return self.__subscription_crud_helper.delete_obj(subscription_id)