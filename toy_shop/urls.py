from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('users/', include(('apps.user.urls', 'apps.user'), namespace='user')),
    path('blog/', include(('apps.blog.urls', 'apps.blog'), namespace='blog')),
    path('shop/', include(('apps.shop.urls', 'apps.shop'), namespace='shop')),

    path('api/', include(('apis.urls', 'apis'), namespace='api')),

    path('', TemplateView.as_view(template_name='home/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='home/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='home/contact.html'), name='contact'),
    path('cart/', TemplateView.as_view(template_name='cart/cart.html'), name='cart'),
    path('checkout/', TemplateView.as_view(template_name='cart/checkout.html'), name='cart'),
    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
