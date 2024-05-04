from django.urls import path, include
from . import views

app_name = "main"

urlpatterns = [
    path("",views.index, name="homepage"),
    path('airtime/', views.airtime, name='airtime'),
    path('about/', views.about, name='about'),
]