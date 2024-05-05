from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.urls import reverse
import pathlib
import textwrap
from .forms import CreateChatForm
from .gemini_model import Model
from main.generate_random_hashed_string import Generator
from django.template.loader import render_to_string
import markdown
from datetime import datetime
from . models import ChatHistory, Messages
import random
import string
import json
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

genai = Model()

current_chat_id = None

def index(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    print(user_agent)
    session_id = request.session.session_key
    
    user = request.user
    # if not user.is_authenticated:
    #     # Construct the login URL with the redirect URL parameter
    #     current_url = request.build_absolute_uri()
    #     login_url = reverse('auth0:login') + f'?redirect_url={current_url}'
    #     return redirect(login_url)
    
    
    def stream_response_generator(res, prompt, image, message_id):
        accumulatedResponse = ""
        context = {
            "message_id":message_id,
            "prompt": prompt,
            "res": "",
            "isFirst": True,
            "isLast": False,
            "isError": False,
            "user": user,
            "onProgress":True,
            "image": image
        }
        try:
            for chunk in res:
               
                new_chunk = chunk.text
                accumulatedResponse += new_chunk
                context['res'] = accumulatedResponse
                html_chunk = render_to_string('main/partial.html', context)
                context['isFirst'] = False
                yield html_chunk
                
            
            # Call the updateHistoryMessage function after processing all chunks
            if user.is_authenticated:
                updateHistoryMessage(request, accumulatedResponse, image, prompt, current_chat_id)
            
            context['isLast'] = True
            context['isFirst'] = False
            context["onProgress"] = False
            context['res'] = ""
            
            # Done processing
            html_chunk = render_to_string('main/partial.html', context)
            yield html_chunk

            

        except Exception as e:
            # Handle any exceptions that occur during the loop
            last_send, last_received  = genai.get_chat_model(user.email if user.is_authenticated else session_id).rewind()
            print(f"An error occurred: {e}")
            # Close the div if an error occurs
            context['isError'] = True
            html_chunk = render_to_string('main/partial.html', context)
            yield html_chunk

    prompt = ""
    image = None

    if request.method == "POST":
        form = CreateChatForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.cleaned_data['message']
            print("Form.cleaned_data:", form.cleaned_data)
            #chats = None
            res = None
            if 'image' in form.cleaned_data and form.cleaned_data['image']:
                image = form.cleaned_data['image']
                res = genai.image_model(user.email if user.is_authenticated else session_id, image , message)
            else:
                res = genai.text_model(user.email if user.is_authenticated else session_id,message)
            prompt = message
            return StreamingHttpResponse(stream_response_generator(res,prompt, image, 
                                                                   Generator("request.user.email+request.user.username")))
    else:
        chat_id = request.GET.get('c', None)
        global current_chat_id

        if chat_id:
            context = {
                "user": request.user,
                "form": CreateChatForm(),
                "default": []
            }
            try:
                default_chat = ChatHistory.objects.get(user=request.user, history_id=chat_id)
                context["default"] = default_chat.messages_set.all()
                current_history_value = default_chat.current_history
                # try:
                #     data = json.loads(current_history_value)
                #     print(data)
                # except json.JSONDecodeError:
                #     print("Invalid JSON format")
                genai.set_chat(user.email if user.is_authenticated else session_id,[] , True)

                current_chat_id = chat_id
                return HttpResponse(render(request, 'main/chat.html', context))

            except ChatHistory.DoesNotExist:
                    context["default"] = []
                    cache.delete(f"{request.user.id}_previous_chat_id")
                    return redirect('chatbot:chat')
        else:
            return redirect_page(request)

def updateHistoryMessage(request, modelResponse, image, prompt, history_id):
        date = datetime.now().date()
        date_time = datetime.now() 
        current_history = genai.get_chat_model(request.user.email).history

        if not user_has_chat_history(request.user):
            history_id= Generator(request.user.email)
            history = ChatHistory(date=date, history_id=history_id, 
                                  current_history=current_history)
            history.save()
            request.user.chathistory.add(history)
        
        cache.set(f"{request.user.id}_previous_chat_id", history_id, timeout=86400)

        try:
            user_chat_history = ChatHistory.objects.get(user=request.user, history_id=history_id)
            # Record exists, you can access it here
        except ObjectDoesNotExist:
            history = ChatHistory(date=date, history_id=history_id, current_history=current_history)
            history.save()
            request.user.chathistory.add(history)
        user_chat_history = ChatHistory.objects.get(user=request.user, history_id=history_id)
        user_chat_history.current_history = current_history

# Save the object to persist the changes
        user_chat_history.save()
        user_chat_history.messages_set.create(message=prompt, response=modelResponse, date=date_time, 
                                              image=image, request_id=Generator(request.user.username))

        
def user_has_chat_history(user):
    user_chat_history_count = ChatHistory.objects.filter(user=user).count()
    return user_chat_history_count > 0

def generate_id(length=25):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_user_cache(user, key):
    return cache.get(f"{user.id}_{key}")

def redirect_page(request):
    form = CreateChatForm()

    cached_chat_id = get_user_cache(request.user, "previous_chat_id")
    context = {
        "user": request.user,
        "form": form,
        "default": []
    }
    global current_chat_id

    if cached_chat_id is not None:
        redirect_url = reverse('chatbot:chat') + f'?c={cached_chat_id}'
        return redirect(redirect_url)
               
    else:
        current_chat_id = Generator(request.user.id)
        genai.set_chat(request.user.email if request.user.is_authenticated else request.session.session_key,[],True)
        return HttpResponse(render(request, 'main/chat.html', context))