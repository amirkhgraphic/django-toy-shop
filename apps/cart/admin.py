from django.contrib import admin

from apps.cart.models import Cart, CartProduct
from utils.admin.mixins import InlineMixin, DateListFilterMixin, ActionsMixin, LinkifyMixin


class CartProductInline(InlineMixin, admin.TabularInline):
    model = CartProduct

    readonly_fields = ('price', 'total_price') + InlineMixin.readonly_fields

    def price(self, obj: CartProduct):
        return obj.product.latest_price

    def total_price(self, obj: CartProduct):
        return obj.product.latest_price * obj.quantity

    price.short_description = 'Price'
    total_price.short_description = 'Total Price'


@admin.register(Cart)
class CartAdmin(ActionsMixin, LinkifyMixin, DateListFilterMixin, admin.ModelAdmin):
    list_display = ('__str__', 'user_link', 'is_paid', 'total_price', 'created_at', 'updated_at', 'is_active')
    list_filter = ('user', 'is_paid',) + DateListFilterMixin.list_filter
    fields = ('user', 'is_paid', 'created_at', 'updated_at', 'is_active')
    inlines = [CartProductInline]
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    ordering = ('-created_at', '-updated_at')
