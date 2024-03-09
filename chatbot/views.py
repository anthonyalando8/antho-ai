from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
from .forms import CreateChatForm
from django.template.loader import render_to_string

import markdown

def index(response):
    genai.configure(api_key="AIzaSyCOeQQMrsEc6mB1GQK3lJHV85dAd7U3Who")

    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
    
    if 'chat_history' not in response.session:
        response.session['chat_history'] = []

    #del response.session['chat_history']

    chat_history = response.session.get('chat_history', [])
    #print(chat_history)

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    def to_markdown(text):
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
    
    def to_markdown_web(text):
        text = text.replace('•', '  *')
        indented_text = textwrap.indent(text, '> ', predicate=lambda _: True)
        markdown_html = markdown.markdown(indented_text)
        return markdown_html
    
    def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    
    #response_text = model.generate_content("Online jobs in kenya?", stream=True)
    def to_markdown_chat(chats = chat.history):
        result = None
        results = []
        print(str(chat_history))
        for message in chats:
            result = to_markdown_web(f'**{message.role}**: {message.parts[0].text}')
            results.append(result)
        return results
    

    if response.method == "POST":
        form = CreateChatForm(response.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            #if is_ajax(response):
            model_response = chat.send_message(message)
            new_message = f""" 
            parts{{
                text: "{message}"
            }}
            role: "user",
            parts{{
                text: {model_response.text}
            }}
            role: "model", """
            #chat_history.append(new_message)
            data = to_markdown_chat(chat.history)
            #response.session['chat_history'] = chat.history

            return JsonResponse({'html': render_to_string('main/partial.html', {'data': data})})
    else:
        form = CreateChatForm()

    
    #markdown_text = to_markdown(model_response.text).data
    
    return HttpResponse(render(response, 'main/chat.html',{"form": form}))

# def submit(response):
#     #form = None
#     if response.method == "POST":
#         form = CreateChatForm(response.POST)
#         if form.is_valid():
#             message = form.cleaned_data['Message']
#     else:
#         form = CreateChatForm()
#     return form
    