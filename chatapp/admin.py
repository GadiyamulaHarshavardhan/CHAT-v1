from django.contrib import admin
from .models import ChatRoom, Message, MediaFile, CallRecording

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "user", "timestamp")
    list_filter = ("room", "timestamp")

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "file_url", "media_type", "name", "uploaded_at")
    list_filter = ("media_type", "uploaded_at")

@admin.register(CallRecording)
class CallRecordingAdmin(admin.ModelAdmin):
    list_display = ("id", "caller", "receiver", "room_name", "file_url", "duration", "started_at", "ended_at")
    list_filter = ("started_at", "ended_at", "caller", "receiver")
    search_fields = ("caller", "receiver", "room_name")
