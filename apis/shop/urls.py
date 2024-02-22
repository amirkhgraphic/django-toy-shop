from django.urls import path

from apis.shop.views import (like_api_view, CategoryCreateAPIView, CategoryProductDeleteAPIView, GalleryCreateAPIView,
                             GalleryDeleteAPIView)

urlpatterns = [
    # Like
    path('like/<int:product_id>/<int:user_id>/', like_api_view, name='like'),

    # Category
    path('category/create/', CategoryCreateAPIView.as_view(), name='create-category'),
    path('category/delete/', CategoryProductDeleteAPIView.as_view(), name='delete-category'),

    # Gallery
    path('gallery/create/', GalleryCreateAPIView.as_view(), name='create-gallery'),
    path('gallery/delete/<int:pk>/', GalleryDeleteAPIView.as_view(), name='delete-gallery'),
]
