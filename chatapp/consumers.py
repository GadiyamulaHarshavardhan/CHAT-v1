# chatapp/consumers.py

import json
from collections import defaultdict
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message, MediaFile

User = get_user_model()

# NOTE: for production use Redis instead (this is per-process only)
ONLINE = defaultdict(set)


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = f"chat_{self.room_name}"

        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # presence
        ONLINE[self.room_name].add(user.username)

        # Send full list to this client
        await self.send_json({
            "type": "online_list",
            "users": list(ONLINE[self.room_name])
        })

        # broadcast join
        await self.channel_layer.group_send(self.group_name, {
            "type": "presence.event",
            "event": "user_join",
            "username": user.username
        })

    async def disconnect(self, close_code):
        user = self.scope["user"]

        if user and user.username in ONLINE.get(self.room_name, set()):
            ONLINE[self.room_name].discard(user.username)

            await self.channel_layer.group_send(self.group_name, {
                "type": "presence.event",
                "event": "user_leave",
                "username": user.username
            })

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """
        Handles 3 things:
        1. WebRTC signaling
        2. Normal messages
        3. Media messages (image / file / voice)
        """
        data = json.loads(text_data or "{}")
        user = self.scope["user"]
        sender = user.username

        # ------------------------------
        # 1️⃣ CALL SIGNALING
        # ------------------------------
        signal_types = {
            "call_request", "call_accept", "call_reject",
            "call_timeout", "offer", "answer", "ice", "call_end"
        }

        if data.get("type") in signal_types:
            payload = data.copy()
            payload["from"] = sender

            await self.channel_layer.group_send(self.group_name, {
                "type": "signal.event",
                "payload": payload
            })
            return

        # ------------------------------
        # TYPING INDICATOR
        # ------------------------------
        if data.get("type") == "typing":
            await self.channel_layer.group_send(self.group_name, {
                "type": "typing.event",
                "username": sender
            })
            return

        # ------------------------------
        # 2️⃣ MEDIA MESSAGE
        # ------------------------------
        if data.get("type") == "media":
            """
            JS sends:
            {
                "type": "media",
                "media_type": "image" | "file" | "voice",
                "media_url": "/media/uploads/.../file"
            }
            """
            attachments = [{
                "type": data.get("media_type"),
                "url": data.get("media_url"),
                "name": data.get("name", ""),
                "duration": data.get("duration", "")
            }]

            await self.channel_layer.group_send(self.group_name, {
                "type": "chat.message",
                "message": "",
                "username": sender,
                "attachments": attachments
            })

            await self._save_message(sender, self.room_name, "", attachments)
            return

        # ------------------------------
        # 3️⃣ NORMAL TEXT MESSAGE
        # ------------------------------
        message = data.get("message", "")
        attachments = data.get("attachments", [])

        if message or attachments:
            reply_to = data.get("reply_to", None)
            await self.channel_layer.group_send(self.group_name, {
                "type": "chat.message",
                "message": message,
                "username": sender,
                "attachments": attachments,
                "reply_to": reply_to
            })

            await self._save_message(sender, self.room_name, message, attachments)
            return

    # ---------------------------------------
    # PRESENCE EVENT
    # ---------------------------------------
    async def presence_event(self, event):
        await self.send_json({
            "type": event["event"],
            "username": event["username"]
        })

    # ---------------------------------------
    # TYPING EVENT
    # ---------------------------------------
    async def typing_event(self, event):
        # Don't send typing event back to the sender
        user = self.scope["user"]
        if user.username != event["username"]:
            await self.send_json({
                "type": "typing",
                "username": event["username"]
            })

    # ---------------------------------------
    # SIGNAL EVENT FOR CALLING
    # ---------------------------------------
    async def signal_event(self, event):
        await self.send_json(event["payload"])

    # ---------------------------------------
    # CHAT MESSAGE EVENT (MAIN)
    # ---------------------------------------
    async def chat_message(self, event):
        payload = {
            "message": event.get("message", ""),
            "username": event.get("username"),
            "attachments": event.get("attachments", [])
        }
        if event.get("reply_to"):
            payload["reply_to"] = event["reply_to"]
        await self.send_json(payload)

    # ---------------------------------------
    # SAVE TO DATABASE
    # ---------------------------------------
    @database_sync_to_async
    def _save_message(self, username, room_name, content, attachments):
        user = User.objects.filter(username=username).first()
        room, _ = ChatRoom.objects.get_or_create(name=room_name)

        msg = Message.objects.create(
            room=room,
            user=user,
            content=content or "",
            attachments_json=attachments or [],
        )

        # Save media separately
        for att in attachments or []:
            if att.get("url"):
                MediaFile.objects.create(
                    message=msg,
                    file_url=att["url"],
                    media_type=att.get("type", "file"),
                    duration=att.get("duration", ""),
                    name=att.get("name", "")
                )

        return msg

    # Utility
    async def send_json(self, obj):
        await self.send(text_data=json.dumps(obj))
