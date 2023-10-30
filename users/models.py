from django.db import models
from authentication.models import CustomUser 

# Create your models here.


class Friendship(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=10, default='pending')  # 'pending', 'accepted', or 'rejected'

