from django import forms

from finance.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('payment_method',)
