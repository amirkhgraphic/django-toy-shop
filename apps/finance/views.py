from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.finance.models import Payment


class PaymentCreateView(CreateView):
    model = Payment
    fields = ('payment_method',)
    template_name = 'finance/checkout.html'
    success_url = reverse_lazy('')
