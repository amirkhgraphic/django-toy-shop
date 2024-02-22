from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.generics import CreateAPIView, DestroyAPIView

from apis.cart.serializers import (CartProductCreateSerializer, CartProductDeleteSerializer, CartCreateSerializer,
                                   CartDeleteSerializer)
from apps.cart.models import Cart, CartProduct


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


class CartProductDeleteAPIView(DestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductDeleteSerializer


class CartCreateAPIView(CreateAPIView):
    serializer_class = CartCreateSerializer


class CartDeleteAPIView(DestroyAPIView):
    serializer_class = CartDeleteSerializer
