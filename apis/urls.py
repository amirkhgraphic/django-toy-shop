from django.urls import path, include


urlpatterns = [
    path('user/', include(('apis.user.urls', 'apis.user'), namespace='user')),
    path('blog/', include(('apis.blog.urls', 'apis.blog'), namespace='blog')),
    path('shop/', include(('apis.shop.urls', 'apis.shop'), namespace='shop')),
    # path('cart/', include(('apis.cart.urls', 'apis.cart'), namespace='cart')),
    # path('finance/', include(('apis.finance.urls', 'apis.finance'), namespace='finance')),
]
