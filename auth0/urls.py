from django.urls import path, include
from . import views as view_auth
from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    logout(request)
    return redirect('auth0:login')

app_name = "auth0"

urlpatterns =[
    path('register/', view_auth.register, name="register"),
    path('', view_auth.login_view, name="auth"),
    path('login/', view_auth.login_view, name="login"),
    path('logout/', logout_view, name="logout")
]