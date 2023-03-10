from django.urls import path
from qrng import views

urlpatterns = [
    path('',  views.home, name='home'),
    path('random/', views.random)]