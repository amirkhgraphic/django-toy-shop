from django.urls import path

from apis.user.views import Signup, Login, TestToken

urlpatterns = [
    path('signup/', Signup.as_view(), name='sign-up'),
    path('login/', Login.as_view(), name='log-in'),
    path('testtoken/', TestToken.as_view(), name='test-token'),
]
