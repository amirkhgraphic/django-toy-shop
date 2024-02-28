from django.contrib.auth import views as auth_views
from django.urls import path

from user.views import SignupView, LoginView, ProfileUpdateView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='sign-up'),
    path('login/', LoginView.as_view(), name='log-in'),
    path('logout/', auth_views.LogoutView.as_view(), name='log-out'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
]
