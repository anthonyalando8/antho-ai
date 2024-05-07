from django.urls import path, include
from . import views

app_name = "main"

urlpatterns = [
    path("",views.index, name="homepage"),
    path('airtime/', views.airtime, name='airtime'),
    path('about/', views.about, name='about'),
    path('manage/admin/', views.admin_dashboard, name='admin'),
    path('manage/admin/dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('manage/admin/messages', views.admin_get_messages, name='admin_messages'),
]