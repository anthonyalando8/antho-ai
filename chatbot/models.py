from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Chat(models.Model):
    message = models.CharField(max_length=12000)
    image = models.ImageField(upload_to="images/")

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chathistory", null=True)
    history_id = models.CharField(max_length=30, null=True, blank=True)
    date = models.DateField()

    def __str__(self) -> str:
        return str(self.date)

class Messages(models.Model):
    chatHistory = models.ForeignKey(ChatHistory, on_delete=models.CASCADE)
    message = models.CharField(max_length=30000, null=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    response = models.CharField(max_length=5000)
    date = models.DateTimeField()

    def __str__(self) -> str:
        return f""" message: 
        {self.message},
        response: {self.response}
        """