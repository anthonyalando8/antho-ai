from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="index page"),
    path("", views.home, name="Home"),
    path('airtime/', views.airtime, name='airtime')
]