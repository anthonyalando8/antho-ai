from django.contrib import admin
from .models import ChatHistory, Messages

# Register your models here.
admin.site.register(ChatHistory)
admin.site.register(Messages)
