from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pathlib
import textwrap
from .forms import CreateChatForm
from .gemini_model import Model
from django.template.loader import render_to_string
import markdown

genai = Model()
def index(response):
    def to_markdown_web(text):
        text = text.replace('•', '  *')
        indented_text = textwrap.indent(text, '> ', predicate=lambda _: True)
        markdown_html = markdown.markdown(indented_text)
        return markdown_html
    
    def to_markdown_chat(chats):
        result = None
        results = []
        for message in chats:
            result = to_markdown_web(f'**{message.role}**: {message.parts[0].text}')
            results.append(result)
        return results

    if response.method == "POST":
        form = CreateChatForm(response.POST, response.FILES)
        if form.is_valid():
            message = form.cleaned_data['message']
            print("Form.cleaned_data:", form.cleaned_data)
            chats = None
            if 'image' in form.cleaned_data and form.cleaned_data['image']:
                chats = genai.image_model(form.cleaned_data['image'], message)
            else:
                chats = genai.text_model(message)

            data = to_markdown_chat(chats)

            return JsonResponse({'html': render_to_string('main/partial.html', {'data': data})})
    else:
        #JsonResponse({'html': render_to_string('main/partial.html', {'data': to_markdown_chat(genai.get_chats())})})
        form = CreateChatForm()
        # Render the initial HTML with the form
        
        # Generate the HTML for the partial template with default data
        default_partial_html = render_to_string('main/partial.html', {'data': to_markdown_chat(genai.get_chats())})
    
    return HttpResponse(render(response, 'main/chat.html',{"form": form, "default": default_partial_html}))
    