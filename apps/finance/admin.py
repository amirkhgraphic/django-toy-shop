from django.contrib import admin

from apps.finance.models import Payment
from utils.admin.mixins import DateListFilterMixin, LinkifyMixin, ActionsMixin


@admin.register(Payment)
class PaymentAdmin(DateListFilterMixin, LinkifyMixin, ActionsMixin, admin.ModelAdmin):
    list_display = ('__str__', 'cart_link', 'user_link', 'amount', 'status', 'is_paid', 'transaction_id',
                    'payment_method', 'created_at', 'updated_at', 'is_active')
    list_filter = ('user', 'is_paid', 'status', 'payment_method') + DateListFilterMixin.list_filter
    fields = ('cart', 'user', 'payment_method', 'status', 'is_paid', 'is_active', 'transaction_id', 'created_at',
              'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at', '-updated_at')
