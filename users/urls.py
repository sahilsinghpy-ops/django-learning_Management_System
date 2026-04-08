from django.urls import path
from .views import RegisterView, CookieLoginView, LogoutView, UserListView,register_page,login_page

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', CookieLoginView.as_view(), name='api_login'),
    path('all/', UserListView.as_view(), name='api_alllogin'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('register-page/', register_page, name='register-page'),
    path('login-page/', login_page,name='login-page')
]