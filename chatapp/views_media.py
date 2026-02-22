# chatapp/views_media.py
import os
import mimetypes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

from .models import ChatRoom, MediaFile


@csrf_exempt
def upload_media(request):
    """
    Handles media uploads from inputbar.html
    Saves image/video/audio/files to MEDIA/chat/
    Returns public URL for WebSocket broadcast.
    """

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    if "file" not in request.FILES:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    file = request.FILES["file"]
    room_name = request.POST.get("room")
    user = request.user if request.user.is_authenticated else None

    room, _ = ChatRoom.objects.get_or_create(name=room_name)

    # Detect file type
    mime, _ = mimetypes.guess_type(file.name)
    if mime is None:
        media_type = "file"
    elif mime.startswith("image"):
        media_type = "image"
    elif mime.startswith("video"):
        media_type = "video"
    elif mime.startswith("audio"):
        media_type = "audio"
    else:
        media_type = "file"

    # Save the file to MEDIA_ROOT
    from django.core.files.storage import default_storage
    from django.conf import settings
    import os

    # Generate a unique filename
    ext = os.path.splitext(file.name)[1]
    filename = f"{room_name}_{timezone.now().strftime('%Y%m%d_%H%M%S')}_{file.name}"
    file_path = os.path.join('media', filename)
    saved_path = default_storage.save(file_path, file)

    # Get the URL
    file_url = default_storage.url(saved_path)

    return JsonResponse({
        "success": True,
        "url": file_url,
        "media_type": media_type
    })
