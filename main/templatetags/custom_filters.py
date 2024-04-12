# custom_filters.py
import markdown
import textwrap
from django import template

register = template.Library()

@register.filter(name='convert_to_markdown')
def convert_to_markdown(text):
    text = text.replace('•', '  *')
    text = text.replace('#', ' ###')
    indented_text = textwrap.indent(text, '> ', predicate=lambda _: True)
    markdown_html = markdown.markdown(indented_text)
    return markdown_html

@register.filter(name='prepend_gemini')
def prepend_gemini(value):
    return f"**SoftChat**\n\n {value}"

@register.filter(name='prepend_username')
def prepend_username(value, user):
    return f"**{user.username}**\n\n {value}"