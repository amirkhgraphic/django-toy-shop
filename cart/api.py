from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from rest_framework.generics import DestroyAPIView

from cart.serializers import CartProductDeleteSerializer
from cart.models import Cart, CartProduct


@login_required
def cart_product_api_view(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)

    try:
        cart_product = CartProduct.objects.get(product_id=product_id, cart=cart)
        cart_product.quantity = int(cart_product.quantity) + 1
        cart_product.save()

    except CartProduct.DoesNotExist:
        cart_product = CartProduct(product_id=product_id, cart=cart, quantity=1)
        cart_product.save()

    return redirect(reverse_lazy('cart:detail'))


@login_required
def cart_product_add_api_view(request, product_id):
    quantity = request.POST.get('quantity') or 1

    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)

    try:
        cart_product = CartProduct.objects.get(product_id=product_id, cart=cart)
        cart_product.quantity = int(cart_product.quantity) + int(quantity)
        cart_product.save()

    except CartProduct.DoesNotExist:
        cart_product = CartProduct(product_id=product_id, cart=cart, quantity=int(quantity))
        cart_product.save()

    return redirect(reverse_lazy('cart:detail'))


@method_decorator(login_required, name='dispatch')
class CartProductDeleteAPIView(DestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductDeleteSerializer
