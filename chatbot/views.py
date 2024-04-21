from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
import pathlib
import textwrap
from .forms import CreateChatForm
from .gemini_model import Model
from django.template.loader import render_to_string
import markdown
from datetime import datetime
from . models import ChatHistory, Messages
import random
import string
import pprint

genai = Model()


def index(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    print(user_agent)
    
    user = request.user
    if not user.is_authenticated:
        return redirect('auth0:login')
    
    def stream_response_generator(res, prompt, image, message_id):
        print(message_id)
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
                #try:
                new_chunk = chunk.text
                accumulatedResponse += new_chunk
                context['res'] = accumulatedResponse
                html_chunk = render_to_string('main/partial.html', context)
                context['isFirst'] = False
                yield html_chunk
                #except Exception as e:
                    #print(f'{type(e).__name__}: {e}')
            
            # Call the updateHistoryMessage function after processing all chunks
            updateHistoryMessage(request, accumulatedResponse, image, prompt)
            
            context['isLast'] = True
            context['isFirst'] = False
            context["onProgress"] = False
            context['res'] = ""
            
            # Done processing
            html_chunk = render_to_string('main/partial.html', context)
            yield html_chunk

            

        except Exception as e:
            # Handle any exceptions that occur during the loop
            last_send, last_received  = genai.get_chat_model(user).rewind()
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
                res = genai.image_model(request, image , message)
            else:
                res = genai.text_model(request,message)
            prompt = message
            message_id = generate_id(20)
            return StreamingHttpResponse(stream_response_generator(res,prompt, image, message_id))
    else:
        genai.set_chat(request.user)
        form = CreateChatForm()
        default_chat = ChatHistory.objects.filter(user=request.user).first()

        context = {
            "user": request.user,
            "form": form,
            "default": []
        }
        
        if has_chat_history(request.user):
            context["default"] = default_chat.messages_set.all()
            pprint.pprint(context["default"].reverse())
        return HttpResponse(render(request, 'main/chat.html',context))

def updateHistoryMessage(request, modelResponse, image, prompt):
        date = datetime.now().date()
        date_time = datetime.now()

        new_id = generate_id(25)

        if not has_chat_history(request.user):
            history = ChatHistory(date=date, history_id=new_id)
            history.save()
            request.user.chathistory.add(history)
        
        user_chat_history = ChatHistory.objects.filter(user=request.user).first()
        user_chat_history.messages_set.create(message=prompt, response=modelResponse, date=date_time, image=image)

        
def has_chat_history(user):
    # Filter ChatHistory records based on the current user's ID
    user_chat_history_count = ChatHistory.objects.filter(user=user).count()
    return user_chat_history_count > 0

def generate_id(length=25):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))