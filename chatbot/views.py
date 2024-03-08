from django.shortcuts import render
from django.http import HttpResponse

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
import markdown
#from google.colab import userdata

def index(request):
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
    response = chat.send_message("Online jobs in kenya?")

    markdown_text = to_markdown(response.text).data

    return render(request, 'main/chat.html',{"chat":to_markdown_web(response.text)})
    