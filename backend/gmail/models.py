
from django.conf import settings
from django.db import models

class GoogleCredential(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    credentials_json = models.TextField()  # we’ll encrypt later
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"GoogleCredential(user={self.user_id})"
