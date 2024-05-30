from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
import africastalking
from .models import InquiryMessage, InquiryResponse
from datetime import datetime, timedelta
from main . generate_random_hashed_string import Generator
from django.contrib.auth.models import User
from django.core.serializers import serialize
# Create your views here.
def index(request):
    try:
        user = request.user
        if user.is_authenticated:
            user_groups = user.groups.all()
        
        if request.method == 'POST':
            if request.POST.get("send_message"):
                user_email = request.POST.get("user_email")
                user_name = request.POST.get("user_name")
                urgent = request.POST.get("is_urgent")
                message_body = request.POST.get("message_body")
                form_is_valid = True
                is_urgent = True if urgent else False

                context_response ={
                    'status_code': 'ok', 
                    'message': {'status_ok':'Message sent successfully!'}
                }

                if len(message_body) > 300:
                    context_response['status_code'] = 'error'
                    context_response["message"].pop("status_ok")
                    context_response["message"] = {'status_error_message_body': "Message too long!"}
                    form_is_valid = False
                if len(user_name) > 50:
                    context_response["message"].pop("status_ok")
                    if context_response['status_code'] != 'error':
                        context_response['status_code'] = 'error'
                    context_response["message"]["status_error_user_name"] = "username too long"
                    form_is_valid = False

                if form_is_valid:
                    context_response = send_message_inquiry(request.user,user_email,user_name, is_urgent, message_body, context_response)

                return JsonResponse(context_response)
            
        return render(request, "main/index.html", {'user':user})
    except Exception as e:
        print(e)
        return HttpResponse(str("Something went wrong!!!..."))
    


def admin_dashboard(request):
    user = request.user
    if user.is_authenticated:
        if is_user_admin(user):
            if request.method == 'GET':
                inquiries = InquiryMessage.objects.filter(is_responded=False)
                context = {
                    "messages": inquiries
                }
                return render(request, 'main/admin-dashboard.html', {})
            else:
                if request.POST.get("load_seven_range"):
                    date_range = [datetime.now() - timedelta(days=i) for i in range(7)]
                    user_counts_per_day = {}
                    print(request.GET)
                    for day in date_range:
                        # Calculate the start and end of the day
                        day_start = datetime(day.year, day.month, day.day, 0, 0, 0)
                        day_end = datetime(day.year, day.month, day.day, 23, 59, 59)
                        
                        # Count the number of users who joined on the current day
                        user_count = User.objects.filter(date_joined__range=(day_start, day_end)).count()
                        
                        # Store the count in the dictionary
                        user_counts_per_day[day.strftime('%Y-%m-%d')] = user_count
                    return JsonResponse(user_counts_per_day)
        
        return HttpResponse(not_authorized())
    else:
        return redirect("auth0:login")

def admin_get_messages(request):
    user = request.user
    if user.is_authenticated:
        if is_user_admin(user):
            if request.method == 'GET':
                
                return render(request, 'main/admin-messages.html', {}) 
            else:
                if request.POST.get("get_messages"):
                    inquiries = InquiryMessage.objects.filter(is_responded=False)

                    return JsonResponse(serialize('json', inquiries), safe=False)
                elif request.POST.get("send_reply"):
                    context_response ={
                        'status_code': 'ok', 
                        'message': {'status_ok':'Reply sent successfully!'}
                    }
                    context_response = send_reply(request, context_response)
                    return JsonResponse(context_response)
        else:
            return HttpResponse(not_authorized())
    else:
        return redirect('auth0:login')
def is_user_admin(user):
    is_admin = False
    for group in user.groups.all():
        if group.name == "Admin":
            is_admin = True
            break
    return is_admin

def not_authorized():
    return """
        <html>
        <head>
            <meta http-equiv="refresh" content="2; url='/'">
        </head>
        <body>
            <p>Not authorised to view this page! Redirecting...</p>
        </body>
        </html>
        """
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

def about(request):
    return render(request, 'main/about.html',{})

def send_message_inquiry(user, user_email, user_name, is_urgent,message_body , context_response):
    date = datetime.now()
    phone = ""
    message_reference_code = Generator(user_email)
    message_subject = "General"
    is_responded = False

    try:
        # Attempt to create and save the InquiryMessage object
        inquiry = InquiryMessage(
            message_reference_code=message_reference_code,
            user=user,
            email=user_email,
            date=date,
            phone=phone,
            message_body=message_body,
            message_subject=message_subject,
            is_urgent=is_urgent,
            is_responded=is_responded,
            user_name=user_name
        )
        inquiry.save()
        user.inquiry_message.add(inquiry)
        context_response['status_code'] = 'ok'
        context_response["message"]["status_ok"] = "Message sent successfully!"
    except Exception as e:
        context_response["message"].pop("status_ok")
        context_response['status_code'] = 'error'
        context_response["message"]["status_error_save"] = "Something went wrong!"
        print("An error occurred:", str(e))
    return context_response

def send_reply(request, context_response):
    message_reference_code = request.POST.get("message_reference_code")
    message_reply = request.POST.get("message_reply")
    try:
        message = InquiryMessage.objects.get(message_reference_code=message_reference_code)
        reply_inquiry(request.user, message, message_reply)

    except Exception as e:
        context_response["message"].pop("status_ok")
        context_response['status_code'] = 'error'
        context_response["message"]["status_error_save"] = "Something went wrong!"
    return context_response

def reply_inquiry(user, message, message_response):
    date = datetime.now()
    response_reference_code = Generator(user.email)
    
    inquiry_reply = InquiryResponse(
        user=user,
        message=message,
        response_reference_code=response_reference_code,
        message_response=message_response,
        date=date
    )
    inquiry_reply.save()
    message.is_responded = True
    message.save()
    message.inquiry_response.add(inquiry_reply)