from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Chat(models.Model):
    message = models.CharField(max_length=12000)
    image = models.ImageField(upload_to="images/")

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chathistory", null=True)
    history_id = models.CharField(max_length=100, primary_key=True)
    current_history = models.TextField()
    date = models.DateField()

    def __str__(self) -> str:
        return str(self.history_id)

class Messages(models.Model):
    chatHistory = models.ForeignKey(ChatHistory, on_delete=models.CASCADE)
    request_id = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=30000, null=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    response = models.CharField(max_length=5000)
    date = models.DateTimeField()

    def __str__(self) -> str:
        return str(self.request_id)