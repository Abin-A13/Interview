from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    )

    owner = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    result = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

