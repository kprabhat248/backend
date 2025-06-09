from django.db import models
from django.conf import settings

class Task(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50)
    points = models.PositiveIntegerField()
    icon = models.ImageField(upload_to='task_icons/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.name} ({self.points} points)"

class TaskSubmission(models.Model):
    STATUS_CHOICES = [('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')]
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='submissions/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    submitted_at = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ('task', 'user')