
from django.conf import settings
from django.db import models

class GoogleCredential(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    credentials_json = models.TextField()  # we’ll encrypt later
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"GoogleCredential(user={self.user_id})"

class Rule(models.Model):
    ACTION_CHOICES = [
        ("archive", "Archive"),
        ("delete", "Delete"),
        ("label", "Apply Label"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    query = models.CharField(max_length=500)  # Gmail search query
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user})"
