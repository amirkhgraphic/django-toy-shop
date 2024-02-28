from django.urls import path
from django.views.generic import TemplateView

from apps.finance.views import PaymentCreateView

urlpatterns = [
    path('checkout/', PaymentCreateView.as_view(), name='check-out'),
    path('success/', TemplateView.as_view(template_name='finance/success.html'), name='success'),
    path('failed/', TemplateView.as_view(template_name='finance/failed.html'), name='failed'),
]
