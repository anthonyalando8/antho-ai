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

genai = Model()


def index(request):
    first_chunk_dict = {'value': True}

    user = request.user
    if not user.is_authenticated:
        return redirect('auth0:login')
    

    def stream_response_generator(res, prompt, image):
        accumulatedResponse = ""
        concat_chunk = ''

        try:
            for chunk in res:
                accumulatedResponse += chunk.text
                if first_chunk_dict["value"]:
                    concat_chunk += f"<div class='border rounded m-2 p-1 bg-light'>{to_markdown_web(f'**{request.user.username}**{prompt}')}</div><div class='border rounded m-2 p-1 bg-light'>{to_markdown_web(f'**Gemini**{chunk.text}')}"
                    first_chunk_dict["value"] = False
                else:
                    concat_chunk += f"{to_markdown_web(chunk.text)}"

                html_chunk = render_to_string('main/partial.html', {'res': to_markdown_web(concat_chunk)})
                concat_chunk = ''
                yield html_chunk

            # Close the div after processing all chunks
            html_chunk = render_to_string('main/partial.html', {'res': '</div>'})
            first_chunk_dict['value'] = True

            yield html_chunk


            # Call the updateHistoryMessage function after processing all chunks
            updateHistoryMessage(request, accumulatedResponse, image, prompt)

        except Exception as e:
            # Handle any exceptions that occur during the loop
            print(f"An error occurred: {e}")
            # Close the div if an error occurs
            html_chunk = render_to_string('main/partial.html', {'res': '</div><div class"bg-warning text-white">Error occured!</div>'})
            first_chunk_dict['value'] = True
            yield html_chunk

    def to_markdown_web(text):
        text = text.replace('•', '  *')
        indented_text = textwrap.indent(text, '> ', predicate=lambda _: True)
        markdown_html = markdown.markdown(indented_text)
        return markdown_html
        
    def to_markdown_chat(chats):
        result = None
        results = []
        for message in chats:
            result = to_markdown_web(f'**{message.role}**\n\n {message.parts[0].text}')
            results.append(result)
        return results

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
                #chats = genai.image_model(form.cleaned_data['image'], message)
                image = form.cleaned_data['image']
                res = genai.image_model(image, message)
            else:
                res = genai.text_model(message)
                #chats = genai.text_model(message)
            #data = to_markdown_chat(chats)
            prompt = message
            #return JsonResponse({'html': render_to_string('main/partial.html', {'data': data})})
            return StreamingHttpResponse(stream_response_generator(res,prompt, image))
    else:
        form = CreateChatForm()
        
        # Generate the HTML for the partial template with default data
        #default_partial_html = render_to_string('main/partial.html', {'res': to_markdown_chat(genai.get_chats())})
        default_chat = ChatHistory.objects.filter(user=request.user).first()

        content = ""
        if has_chat_history(request.user):
            for chat in default_chat.messages_set.all():
                content += f"<div class='border rounded m-2 p-1 bg-light'>{to_markdown_web(f'**{request.user.username}**\n\n{chat.message}')}</div><div class='border rounded m-2 p-1 bg-light'>{to_markdown_web(f'**Gemini**\n\n{chat.response}')}</div>"
        return HttpResponse(render(request, 'main/chat.html',{"form": form, "default": content}))

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