from django.db import models
from django.contrib.auth.models import User

# 친구
class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    blocked = models.BooleanField(default=False)

# 일정
class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=10)