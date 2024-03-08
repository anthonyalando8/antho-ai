from django.shortcuts import render
from django.http import HttpResponse

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
from .forms import CreateChatForm
import markdown

def index(response):
    def to_markdown(text):
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
    
    def to_markdown_web(text):
        text = text.replace('•', '  *')
        indented_text = textwrap.indent(text, '> ', predicate=lambda _: True)
        markdown_html = markdown.markdown(indented_text)
        return markdown_html

    genai.configure(api_key="AIzaSyCOeQQMrsEc6mB1GQK3lJHV85dAd7U3Who")

    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
            
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    #response_text = model.generate_content("Online jobs in kenya?", stream=True)

    if response.method == "POST":
        form = CreateChatForm(response.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            model_response = chat.send_message(message)
    else:
        form = CreateChatForm()
    
    def to_markdown_chat(chats = chat.history):
        result = None
        results = []
        for message in chats:
            result = to_markdown_web(f'**{message.role}**: {message.parts[0].text}')
            results.append(result)
        return results
    
    #markdown_text = to_markdown(model_response.text).data
    
    return render(response, 'main/chat.html',{"chats": to_markdown_chat(), "form": form})

# def submit(response):
#     #form = None
#     if response.method == "POST":
#         form = CreateChatForm(response.POST)
#         if form.is_valid():
#             message = form.cleaned_data['Message']
#     else:
#         form = CreateChatForm()
#     return form
    