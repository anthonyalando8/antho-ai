from django.urls import path, include
from . import views

urlpatterns = [
    path("index/", views.index, name="index page"),
    path("", views.home, name="Home"),
    path('airtime/', views.airtime, name='airtime'),
    path('mpesa/', include('mpesa_api.urls')),
    path('chat/', include('chatbot.urls')),
]