from django.contrib import admin
from .models import InquiryMessage, InquiryResponse

# Register your models here.
admin.site.register(InquiryResponse)
admin.site.register(InquiryMessage)
