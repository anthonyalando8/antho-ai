from django.db import models
from django.contrib.auth.models import User

class InquiryMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inquiry_message", null=True)
    email = models.EmailField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=100,null=True, blank=True)
    user_name = models.CharField(max_length=50)
    message_body = models.TextField()
    message_reference_code = models.CharField(max_length=100)
    message_subject = models.CharField(max_length=100,null=True, blank=True)
    is_urgent = models.BooleanField(null=True, blank=True)
    is_responded = models.BooleanField(null=True, blank=True)
    date = models.DateTimeField()

    def __str__(self) -> str:
        return self.message_reference_code


class InquiryResponse(models.Model):
    message = models.ForeignKey(InquiryMessage, on_delete=models.CASCADE, related_name="inquiry_response", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inquiry_responded", null=True)
    response_reference_code = models.CharField(max_length=100)
    message_response = models.TextField(null=True, blank=True)
    read = models.BooleanField(null=True, blank=True, default=False)
    date = models.DateTimeField()

    def __str__(self) -> str:
        return self.response_reference_code