from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="chatbot"),
    #path('submit/', views.submit, name='Submit')
]