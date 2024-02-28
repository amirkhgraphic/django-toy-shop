from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.finance.forms import PaymentForm
from apps.finance.models import Payment


class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'finance/checkout.html'
    success_url = reverse_lazy('finance:success')

    def get_context_data(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['cart'] = self.request.user.carts.get(is_active=True)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.cart_id = form.cleaned_data['cart_id']

        return super().form_valid(form)
