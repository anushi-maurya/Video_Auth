from django.db import models
from django.contrib.auth.models import User

# Function that defines where uploaded videos will be stored
# Example path: media/videos/filename.mp4
def video_upload_path(instance, filename):
    return 'videos/' + filename

class Video(models.Model):
    # Optional video title (can be empty)
    title = models.CharField(max_length=255, blank=True)

    # Optional description for the video
    description = models.TextField(blank=True)

    # The actual uploaded video file
    # Stored inside MEDIA_ROOT/videos/
    file = models.FileField(upload_to='videos/')

    # The user who uploaded the video (linked to Django User model)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')

    # Timestamp automatically set when video is uploaded
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Unique SHA-256 hash of the video file (used to detect duplicates)
    file_hash = models.CharField(max_length=64, unique=True)

    # File size stored in bytes
    size = models.PositiveBigIntegerField(null=True, blank=True)

    def __str__(self):
        # Display video name and uploader in admin panel or shell
        return f"{self.title or self.file.name} ({self.uploaded_by})"

