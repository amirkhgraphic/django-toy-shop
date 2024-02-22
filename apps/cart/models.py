from django.db import models
from django.db.models import F, OuterRef, Subquery, Sum
from django.utils import timezone

from apps.shop.models import Product, Price
from utils.abstracts import MyBaseModel, User


class Cart(MyBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f'cart #{self.id}'

    @property
    def total_price(self):
        # total_price = 0
        # for cart_product in self.cart_products.all():
        #     total_price += cart_product.product.latest_price * cart_product.quantity
        # return total_price
        latest_prices_subquery = Price.objects.filter(
            product=OuterRef('product')
        ).order_by('-created_at').values('price')[:1]

        return self.cart_products.annotate(
            latest_price=Subquery(latest_prices_subquery)
        ).aggregate(
            total_price=Sum(F('latest_price') * F('quantity'))
        )['total_price'] or 0

    def update_signal(self):
        self.updated_at = timezone.now()
        self.save(update_fields=['updated_at'])


class CartProduct(MyBaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.product.latest_price} x {self.quantity}'

    @property
    def total_price(self):
        return self.product.latest_price * self.quantity

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_signal()

    class Meta:
        unique_together = ('cart', 'product')
