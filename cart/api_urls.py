from django.urls import path

from cart.api import cart_product_add_api_view, cart_product_api_view, CartProductDeleteAPIView

urlpatterns = [
    path('cartproduct/<int:product_id>/', cart_product_api_view, name='cart-product'),
    path('cartproduct/add/<int:product_id>/', cart_product_add_api_view, name='cart-product-add'),
    path('cartproduct/delete/<int:pk>', CartProductDeleteAPIView.as_view(), name='cart-product-delete'),
]
