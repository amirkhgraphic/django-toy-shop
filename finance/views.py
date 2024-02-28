from django.urls import reverse_lazy
from django.views.generic import CreateView

from finance.forms import PaymentForm
from finance.models import Payment


class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'finance/checkout.html'
    success_url = reverse_lazy('finance:success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['cart'] = self.request.user.carts.get(user=self.request.user, is_paid=False)
        return context

    def form_valid(self, form):
        payment = form.save(commit=False)

        payment.user = self.request.user
        payment.cart = self.request.user.carts.get(user=self.request.user, is_paid=False)
        payment.is_paid = True

        payment.save()
        return super().form_valid(form)
