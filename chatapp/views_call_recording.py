# chatapp/views_call_recording.py
import os
import uuid
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import CallRecording

logger = logging.getLogger(__name__)


@csrf_exempt
def save_call_recording(request):
    """
    Accepts audio blob from JS and stores file + DB record
    """
    if request.method != "POST":
        logger.warning("save_call_recording called with non-POST method")
        return JsonResponse({"error": "POST required"}, status=400)

    caller = request.POST.get("caller")
    receiver = request.POST.get("receiver")
    room_name = request.POST.get("room_name", "")
    duration = request.POST.get("duration", 0)

    logger.info(f"Attempting to save call recording: caller={caller}, receiver={receiver}, room_name={room_name}, duration={duration}")

    audio_file = request.FILES.get("recording")
    if not audio_file:
        logger.error("No recording file provided in request")
        return JsonResponse({"error": "No file"}, status=400)

    try:
        # Generate file name
        filename = f"recordings/{uuid.uuid4()}.webm"
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Ensure recordings directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save file manually
        with open(file_path, "wb+") as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        file_url = settings.MEDIA_URL + filename

        # Save to DB
        rec = CallRecording.objects.create(
            caller=caller,
            receiver=receiver,
            room_name=room_name,
            file_url=file_url,
            duration=duration
        )

        logger.info(f"Successfully saved call recording id={rec.id}, file_url={file_url}")

        return JsonResponse({
            "success": True,
            "recording_url": file_url,
            "id": rec.id
        })
    except Exception as e:
        logger.error(f"Error saving call recording: {e}")
        return JsonResponse({"error": "Internal server error"}, status=500)
