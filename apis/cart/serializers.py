from rest_framework import serializers

from cart import CartProduct, Cart


class CartProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ('id', 'product', 'cart', 'quantity')


class CartProductDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ('id',)


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user')


class CartDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user')
