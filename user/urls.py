from django.urls import path
from .views import Home, UserLogin, UserRegister
urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login')
]