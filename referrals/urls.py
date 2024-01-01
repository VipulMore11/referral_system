# referrals/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', mainview, name='main-view'),
    path('<str:referral_code>', mainview, name='main-view'),
    path('signup/', signup, name='signup-view'),
    path('profile/', my_recommendation_view, name='recommendation-view'),
]
