from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            login(request, form.save())

            redirect_url = request.GET.get('redirect_url', 'main:homepage')
            return redirect(redirect_url)
    else:
        form = RegisterForm()
    return render(request, 'auth0/register.html',{'form':form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            redirect_url = request.GET.get('redirect_url', 'main:homepage')

            return redirect(redirect_url)
    else:
        form = AuthenticationForm()
    return render(request, 'auth0/login.html',{'form':form})