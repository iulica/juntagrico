from django.contrib.admin import register
from juntagrico.admins.base_admin import BaseAdmin
from juntagrico.config import Config
from juntagrico.entity.subtypes import SubscriptionSize, SubscriptionType


@register(SubscriptionType)
class SubscriptionTypeAdmin(BaseAdmin):
    list_display = ['__str__', 'price', 'required_assignments',
                    'required_core_assignments', 'visible', 'trial']

    def get_exclude(self, request, obj=None):
        if not Config.enable_shares():
            return ['shares'] if self.exclude is None else self.exclude.append('shares')
        return self.exclude


if Config.enable_shares():
    SubscriptionTypeAdmin.list_display.insert(2, 'shares')


@register(SubscriptionSize)
class SubscriptionSizeAdmin(BaseAdmin):
    list_display = ['__str__', 'units', 'product', 'visible', 'depot_list']
