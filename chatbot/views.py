from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from .forms import CreateChatForm
from .gemini_model import Model
from main.generate_random_hashed_string import Generator
from django.template.loader import render_to_string
import markdown
from datetime import datetime
from . models import ChatHistory, Messages
import random
import string
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
import json

genai = Model()

current_chat_id = None

def index(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    session_id = str(request.session.session_key)
    print(session_id)
    
    user = request.user
    
    def stream_response_generator(res, prompt, image, message_id):
        accumulatedResponse = ""
        context = {
            "message_id":str(message_id),
            "prompt": prompt,
            "res": "",
            "is_first": True,
            "image": image
        }
        try:
            for chunk in res:
                new_chunk = chunk.text
                accumulatedResponse += new_chunk
                context['res'] = accumulatedResponse
                json_data = json.dumps(context).encode('utf-8')
                context['is_first'] = False
                context['is_on_progress'] = True

                yield json_data
                
            # Call the updateHistoryMessage function after processing all chunks
            if user.is_authenticated:
                updateHistoryMessage(request, accumulatedResponse, image, prompt, current_chat_id)
            #context = {"is_complete": True}
            
            # Done processing
            #yield json.dumps({}).encode('utf-8')

        except Exception as e:
            # Handle any exceptions that occur during the loop
            last_send, last_received  = genai.get_chat_model(user.email if user.is_authenticated else str(session_id)).rewind()
            print(f"An error occurred: {e}")
            context = {
                "is_error": True,
                "error_message": str(e)
                }
            yield json.dumps(context).encode('utf-8')

    prompt = ""
    image = None

    if request.method == "POST":
        if request.POST.get("send_prompt"):
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
                    res = genai.text_model(user.email if user.is_authenticated else session_id, message)
                prompt = message
                return StreamingHttpResponse(stream_response_generator(res,prompt, image, 
                                                                    Generator("request.user.email+request.user.username")),content_type="application/json")
        elif request.POST.get("get_ai_chats"):
            global current_chat_id
            if request.user.is_authenticated:
                request_chat_id = request.POST.get("get_ai_chats")
                if request_chat_id == "new_chat" or request_chat_id != str(get_user_cache(request.user, "previous_chat_id")):
                    current_chat_id = Generator(request.user.id)
                    print("New chart requested")
                    return JsonResponse({})
                elif request_chat_id == str(get_user_cache(request.user, "previous_chat_id")):
                    try:
                        print("Previous chart requested")

                        default_chat = ChatHistory.objects.get(user=request.user, history_id=request_chat_id)
                        current_history_value = default_chat.current_history
                        
                        genai.set_chat(user.email if user.is_authenticated else str(session_id),[] , True)

                        current_chat_id = request_chat_id
                        return JsonResponse(serialize('json', default_chat.messages_set.all()), safe=False)

                    except ChatHistory.DoesNotExist:
                        current_chat_id = None
                        cache.delete(f"{request.user.id}_previous_chat_id")
                        print("No such history existing")
                        return JsonResponse({})
                else:
                    return JsonResponse({})
            else:
                return JsonResponse({})
        else:
            return HttpResponse("Something not right!")
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
    print(request.session.session_key)
    context = {
        "user": request.user,
        "form": form,
        "default": {"chat_id": "new_chat"}
    }
    global current_chat_id
    current_chat_id = Generator(request.user.id)

    if cached_chat_id is not None:
        current_chat_id = cached_chat_id
        context["default"]["chat_id"] = cached_chat_id
               
    genai.set_chat(request.user.email if request.user.is_authenticated else str(request.session.session_key),[],True)
    return HttpResponse(render(request, 'main/chat.html', context))