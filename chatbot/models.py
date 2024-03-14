from django.db import models

# Create your models here.
class Chat(models.Model):
    message = models.CharField(max_length=10000)
    image = models.ImageField(upload_to="images/")
