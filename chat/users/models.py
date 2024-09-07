from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    friends = models.ManyToManyField('self', blank=True, related_name='friends_user', symmetrical=False)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} -> {self.receiver}: {self.content[:30]}'