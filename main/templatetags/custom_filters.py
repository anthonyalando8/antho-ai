import markdown
import textwrap
from django import template
import re

register = template.Library()

@register.filter(name='prepend_gemini')
def prepend_gemini(value):
    return f"**SoftChatAI**\n\n{value}"

@register.filter(name='prepend_username')
def prepend_username(value, user):
    return f"**{user.username if user.is_authenticated else 'You'}**\n\n {value}"