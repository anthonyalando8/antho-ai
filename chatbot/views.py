from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import CreateChatForm
from . models import ChatHistory
import random
import string
from django.core.cache import cache
from django.core.serializers import serialize

def index(request):

    user_agent = request.META.get('HTTP_USER_AGENT', '')
    user = request.user

    if request.method == "POST":
        if request.POST.get("get_ai_chats"):
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
        "default": {
            "chat_id": "new_chat",
            "session_id": session_id
        }
    }
    
    if cached_chat_id is not None:
        context["default"]["chat_id"] = cached_chat_id
               
    return HttpResponse(render(request, 'main/chat.html', context))