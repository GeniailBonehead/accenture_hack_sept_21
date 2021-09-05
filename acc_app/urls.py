from django.urls import path, include
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('accenture', acc_index),
    path('accenture/portfolio', portfolio),
    path('accenture/stock/<int:data_id>&<str:name>&<str:link>', acc_stock),
    path('accenture/post', acc_post),
    path('accenture/send_message', send_mess),
    path('accenture/last_buy_online', acc_last_buy_online),
    path('accenture/last_buy_nice', last_buy_nice),
    path('accenture/charts/<int:data_id>', charts),
    path('accenture/stats/equities/<str:link>', stats),
]
