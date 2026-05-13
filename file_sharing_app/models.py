from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

def default_expiry():
    return timezone.now() + timedelta(days=1)  # Default 24-hour expiry

# details of the file uploaded by user
class SharedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # the file which user uploads is stored here 
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry)

# checks if the uploaded file is expired or n0t
    def is_expired(self):
        return timezone.now() > self.expires_at

# name of the file and it expiry time
    def __str__(self):
        return f"{self.file.name} (Expires: {self.expires_at})"


