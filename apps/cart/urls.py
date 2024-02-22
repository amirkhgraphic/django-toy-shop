from django.urls import path
from apps.cart.views import CartDetailView


urlpatterns = [
    path('', CartDetailView.as_view(), name='detail'),
    # path('update/<int:pk>', CartUpdateView.as_view(), name='update'),
    # path('delete/<int:pk>', CartDeleteView.as_view(), name='delete'),
]
