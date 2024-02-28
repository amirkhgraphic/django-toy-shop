from django.urls import path

from shop.views import (ProductDetailView, ProductListView, MyProductsListView, ProductCreateView,
                        ProductDeleteView, ProductUpdateView, CategoryListView, CategoryDetailView,
                        BrandListView, BrandDetailView)


urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('myproducts/', MyProductsListView.as_view(), name='my-products'),
    path('product/create/', ProductCreateView.as_view(), name='create-product'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='update-product'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete-product'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('brand/<int:pk>/', BrandDetailView.as_view(), name='brand'),
    path('brands/', BrandListView.as_view(), name='brands'),
]
