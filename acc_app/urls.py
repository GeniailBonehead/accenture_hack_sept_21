from django.urls import path, include
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('accenture/last_buy_online', acc_last_buy_online),
    path('accenture/last_buy_nice', last_buy_nice),
    path('accenture/charts/<int:data_id>', charts),
    path('accenture/stats/equities/<str:link>', stats),
]
