from django.urls import path
from . import views

app_name = 'main_app_cart'

urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
]
