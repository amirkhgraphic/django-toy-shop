from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .local_settings import ADMIN_URL


urlpatterns = [
    path(f'{ADMIN_URL}', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('users/', include(('user.urls', 'user'), namespace='user')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('shop/', include(('shop.urls', 'shop'), namespace='shop')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('finance/', include(('finance.urls', 'finance'), namespace='finance')),

    path('api/user/', include(('user.api_urls', 'user'), namespace='api_user')),
    path('api/blog/', include(('blog.api_urls', 'blog'), namespace='api_blog')),
    path('api/shop/', include(('shop.api_urls', 'shop'), namespace='api_shop')),
    path('api/cart/', include(('cart.api_urls', 'cart'), namespace='api_cart')),

    path('', TemplateView.as_view(template_name='home/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='home/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='home/contact.html'), name='contact'),
    path('cart/', TemplateView.as_view(template_name='cart/cart.html'), name='cart'),
    path('checkout/', TemplateView.as_view(template_name='finance/checkout.html'), name='cart'),
    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
