from rest_framework import serializers

from apps.shop.models import Like, Category, Gallery


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('product', 'user')


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'thumbnail')


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('id', 'file', 'product_id', 'format', 'type', 'created_at', 'updated_at')
