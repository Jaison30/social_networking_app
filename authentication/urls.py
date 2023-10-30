# authentication/urls.py
from django.urls import path
from .views import UserCreateView, UserLoginView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('signup/', UserCreateView.as_view(), name='user-create'),
    path('logout/', LogoutView.as_view(), name='logout'),
]