from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.finance.forms import PaymentForm
from apps.finance.models import Payment


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

    def post(self, request, *args, **kwargs):
        user = self.request.user
        cart = self.request.user.carts.get(user=self.request.user, is_paid=False)
        # Payment.objects.create(user=user, cart=cart, is_paid=True, is_active=True)
        method = self.request.POST.get('payment_method')
        print(method)
        print('done'*100)

    def create(self, *args, **kwargs):
        print('hre')

    def form_valid(self, form):
        print(form.instance)
        form.instance.user = self.request.user
        form.instance.cart = self.request.user.carts.get(user=self.request.user, is_paid=False)
        form.instance.is_paid = True
        form.save(commit=False)

        return super().form_valid(form)
