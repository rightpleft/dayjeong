from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')

    status = models.CharField(max_length=10, choices=[
        ('pending', '대기'),
        ('accepted', '친구'),
        ('blocked', '차단')
    ], default='pending')