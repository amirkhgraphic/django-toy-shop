from django.views.generic import DetailView

from cart.models import Cart


class CartDetailView(DetailView):
    model = Cart
    template_name = 'cart/cart.html'
    context_object_name = 'cart'

    def get_object(self, queryset=None):
        user_id = self.request.user.id
        latest_cart = Cart.objects.filter(user_id=user_id, is_paid=False).order_by('-created_at').first()

        if latest_cart is None:
            latest_cart = Cart.objects.create(user_id=user_id, is_paid=False)

        return latest_cart
