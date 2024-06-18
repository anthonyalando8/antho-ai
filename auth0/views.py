from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
# Create your views here.
redirect_link = 'main:homepage'
def register(request):
    session_id = str(request.session._get_or_create_session_key())
    global redirect_link
    try:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                login(request, form.save())
                redirect_url = request.GET.get('redirect_url', redirect_link)
                return redirect(redirect_url)
        else:
            form = RegisterForm()
        return render(request, 'auth0/register.html',{'form':form, 'default': {'session_id':session_id}})
    except:
        return response_error_occured_refresh_page()

def login_view(request):
    session_id = str(request.session._get_or_create_session_key())
    global redirect_link
    try:
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                redirect_url = request.GET.get('redirect_url', redirect_link)

                return redirect(redirect_url)
        else:
            #redirect_link = request.META.get('HTTP_REFERER')
            form = AuthenticationForm()
        return render(request, 'auth0/login.html',{'form':form, 'default':{'session_id': session_id}})
    except:
        return response_error_occured_refresh_page()

from django.http import HttpResponse

def response_error_occured_refresh_page(request):
    html_content = """
    <html>
        <head>
            <meta http-equiv="refresh" content="3">
        </head>
        <body>
            Something went wrong! Refreshing page...
        </body>
    </html>
    """
    return HttpResponse(html_content)
