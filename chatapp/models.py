from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="messages", on_delete=models.SET_NULL, null=True)
    content = models.TextField(blank=True)
    attachments_json = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.user}: {self.content[:50]}"


class MediaFile(models.Model):
    """
    FIXED MODEL — fully compatible with your JS + backend
    """
    message = models.ForeignKey(Message, related_name="media_files", on_delete=models.CASCADE)

    # Stored file path (matches your JS "url")
    file_url = models.TextField()  # Accepts any URL (local or external)

    # image, video, audio, file, voice
    media_type = models.CharField(max_length=20)

    # optional fields for voice & file info
    name = models.CharField(max_length=255, blank=True)
    duration = models.CharField(max_length=20, blank=True)  # "00:10"

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type}: {self.file_url}"

class CallRecording(models.Model):
    caller = models.CharField(max_length=150)
    receiver = models.CharField(max_length=150)

    room_name = models.CharField(max_length=150, null=True, blank=True)

    # store file as URL, not path. JS needs URL.
    file_url = models.TextField()  

    duration = models.IntegerField(null=True, blank=True)

    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.caller} → {self.receiver} ({self.created_at})"
