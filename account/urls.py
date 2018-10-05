from django.urls import path
from .views import get_phone_number, check_otp, get_password, user_login, user_logout



urlpatterns = [
    path('get-phone-number/', get_phone_number, name='get-phone-number'),
    path('check-otp/', check_otp, name='check-otp'),
    path('get-password/', get_password, name='get-password'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
