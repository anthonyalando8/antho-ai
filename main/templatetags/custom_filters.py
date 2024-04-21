import markdown
import textwrap
from django import template
import re

register = template.Library()

@register.filter(name='convert_to_markdown')
def convert_to_markdown(text):
    text = text.replace('•', ' * ')
    indented_text = textwrap.indent(text, '> ', predicate=lambda _: True)
    markdown_html = markdown.markdown(indented_text)
    # Regular expression pattern to match "```" followed by a word
    pattern_with_word = r'```(\w+)'

    # Regular expression pattern to match standalone "```"
    pattern_without_word = r'```(?!\w)'
    # Replace occurrences with the specified values
    markdown_html = re.sub(pattern_with_word, '<pre class="fs-6 bg-black card shadow-sm mw-100 d-inline-block text-info p-2" style="background-color:black; overflow-x: auto"><code>', markdown_html)
    markdown_html = re.sub(pattern_without_word, '</code></pre>', markdown_html)
    return markdown_html

@register.filter(name='prepend_gemini')
def prepend_gemini(value):
    return f"**SoftChatAI**\n\n {value}"

@register.filter(name='prepend_username')
def prepend_username(value, user):
    return f"**{user.username}**\n\n {value}"