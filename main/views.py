from django.shortcuts import render, redirect
from django.http import HttpResponse
import africastalking

# Create your views here.
def index(request):
    user = request.user
    # if not user.is_authenticated:
    #     return redirect('auth0:login')
    return render(request, "main/index.html", {'user':user})

def airtime(res):
    
    username = "softtronic"
    api_key = "c02c7227695535d6988dae4e1379bd0efd491f20d2a4987d6f14f04ccb9fd701"

    africastalking.initialize(username, api_key)

    airtime = africastalking.Airtime

    phone_number = "+254796211581"
    currency_code = "KES" #Change this to your country's code
    amount = 5

    try:
        response = airtime.send(phone_number=phone_number, amount=amount, currency_code=currency_code)
        return HttpResponse(response)
      
    except Exception as e:
        return HttpResponse(f"Encountered an error while sending airtime. More error details below.\n {e}")



