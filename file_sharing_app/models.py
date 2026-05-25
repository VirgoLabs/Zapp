from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

def default_expiry():
    return timezone.now() + timedelta(days=1)  # Default 24-hour expiry

# details of the file uploaded by user
class SharedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # NEW: We store the Cloudinary URL and Name instead of a physical file
    file_url = models.URLField(max_length=1000)
    file_name = models.CharField(max_length=255)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry)

    # Tracking downloads
    max_downloads = models.IntegerField(default=1)
    current_downloads = models.IntegerField(default=0)

    # checks if the uploaded file is expired or not
    def is_expired(self):
        return timezone.now() > self.expires_at

    # name of the file and its expiry time
    def __str__(self):
        return f"{self.file_name} (Expires: {self.expires_at})"