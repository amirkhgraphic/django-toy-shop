import uuid

from django.db import models

from apps.cart.models import Cart
from utils.abstracts import User, MyBaseModel


class Payment(MyBaseModel):
    PAYMENT_METHODS = (
        ('paypal', 'PayPal'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
    )

    STATUS = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )

    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, related_name='payments', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS, default='pending')
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHODS, default='paypal')
    transaction_id = models.CharField(max_length=63, blank=True, null=True)
    is_paid = models.BooleanField(default=False, blank=True)

    @property
    def amount(self):
        return self.cart.total_price or 0

    def __str__(self):
        return f'Payment #{self.id}'

    def save(self, *args, **kwargs):
        if self.is_paid:
            self.status = 'COMPLETED'
            self.cart.is_paid = True
            self.cart.save()
            self.transaction_id = uuid.uuid4().hex

        elif self.status == 'COMPLETED':
            self.is_paid = True
            self.cart.is_paid = True
            self.cart.save()
            self.transaction_id = uuid.uuid4().hex

        else:
            self.cart.is_paid = False
            self.cart.save()
            self.is_paid = False
            self.transaction_id = None

        super().save(*args, **kwargs)
