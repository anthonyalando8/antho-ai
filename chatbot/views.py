from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from .forms import CreateChatForm
from .gemini_model import Model
from main.generate_random_hashed_string import Generator
from datetime import datetime
from . models import ChatHistory
import random
import string
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
import json
from PIL import Image
import base64
import io

genai = Model()


def index(request):

    user_agent = request.META.get('HTTP_USER_AGENT', '')
    user = request.user
    def stream_response_generator(res, prompt, image, message_id, request_session_id, request_chat_id):
        accumulatedResponse = ""
        try:
            img_data = image.read()
            # Encode the byte array as base64
            base64_image = base64.b64encode(img_data).decode("utf-8")
            print("base64: ", base64_image)
        except Exception as e:
            print(e)
            base64_image = None
        context = {
            "message_id":str(message_id),
            "prompt": prompt,
            "res": "",
            "is_first": True,
            "image": base64_image
        }
        try:
            for chunk in res:
                new_chunk = chunk.text
                accumulatedResponse += new_chunk
                context['res'] = accumulatedResponse
                json_data = json.dumps(context).encode('utf-8')
                context['is_first'] = False
                context['is_on_progress'] = True
                json_data += b'\n'
                yield json_data
                
                
            # Call the updateHistoryMessage function after processing all chunks
            if user.is_authenticated:
                updateHistoryMessage(request, accumulatedResponse, image, prompt, request_chat_id)

        except Exception as e:
            # Handle any exceptions that occur during the loop
            if image == None:
                last_send, last_received  = genai.get_chat_model(user.email if user.is_authenticated else request_session_id).rewind()
            print(f"An error occurred: {e}")
            context = {
                "is_error": True,
                "error_message": "Generate error! Trying reloading"
                }
            yield json.dumps(context).encode('utf-8')

    prompt = ""
    image = None

    if request.method == "POST":
        if request.POST.get("send_prompt"):
            request_session_id = request.POST.get("session_id")
            request_chat_id = request.POST.get("request_chat_id")
            genai.set_chat(user.email if user.is_authenticated else request_session_id,[] , False)

            form = CreateChatForm(request.POST, request.FILES)
            if form.is_valid():
                message = form.cleaned_data['message']
                res = None
                if 'image' in form.cleaned_data and form.cleaned_data['image']:
                    image = form.cleaned_data['image']
                    
                    res = genai.image_model(user.email if user.is_authenticated else request_session_id, image , message)
                    
                else:
                    try:
                        res = genai.text_model(user.email if user.is_authenticated else request_session_id, message)
                    except KeyError as e:
                        context = {
                                "is_error": True,
                                "error_message": "Requested engine does not exist!"
                        }
                        return JsonResponse(context)
                prompt = message
                return StreamingHttpResponse(stream_response_generator(res,prompt, image, 
                                                                    Generator("request.user.email+request.user.username"),
                                                                    request_session_id, request_chat_id),content_type="application/json")
        elif request.POST.get("get_ai_chats"):
            if request.user.is_authenticated:
                request_chat_id = request.POST.get("get_ai_chats")
                if request_chat_id == "new_chat" or request_chat_id != str(get_user_cache(request.user, "previous_chat_id")):
                    
                    print("New chart requested")
                    return JsonResponse({})
                elif request_chat_id == str(get_user_cache(request.user, "previous_chat_id")):
                    try:
                        print("Previous chart requested")

                        default_chat = ChatHistory.objects.get(user=request.user, history_id=request_chat_id)
                        current_history_value = default_chat.current_history
                        
                        #genai.set_chat(user.email if user.is_authenticated else str(session_id),[] , True)

                        return JsonResponse(serialize('json', default_chat.messages_set.all()), safe=False)

                    except ChatHistory.DoesNotExist:
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
        if history_id == "new_chat":
            history_id = Generator(request.user.email)
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
    session_id = str(request.session._get_or_create_session_key())
    context = {
        "user": request.user,
        "form": form,
        "default": {"chat_id": "new_chat",
                    "session_id": session_id}
    }
    
    if cached_chat_id is not None:
        context["default"]["chat_id"] = cached_chat_id
               
    genai.set_chat(request.user.email if request.user.is_authenticated else session_id,[],True)
    return HttpResponse(render(request, 'main/chat.html', context))