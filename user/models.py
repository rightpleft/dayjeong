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

# 일정
class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=100)


# 일정 요청
class ScheduleRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_schedule')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_schedule')

    date = models.DateField()
    title = models.CharField(max_length=100)

    status = models.CharField(max_length=10, choices=[
        ('pending', '대기'),
        ('accepted', '수락'),
        ('rejected', '거절')
    ], default='pending')