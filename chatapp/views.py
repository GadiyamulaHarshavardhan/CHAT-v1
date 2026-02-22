from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q
from django.utils import timezone

from .models import ChatRoom, MediaFile, CallRecording


# -----------------------------------------
# DEFAULT REDIRECTION
# -----------------------------------------
def redirect_to_login(request):
    return redirect("login")


# -----------------------------------------
# CHAT ROOM VIEW
# -----------------------------------------
@login_required
def chat_room(request, room_name):
    room, _ = ChatRoom.objects.get_or_create(name=room_name)
    messages = (
        room.messages
        .select_related("user")
        .all()
        .order_by("-timestamp")[:50][::-1]
    )

    return render(request, "chat_room.html", {
        "room_name": room_name,
        "messages": messages
    })


# -----------------------------------------
# ADMIN CHECK
# -----------------------------------------
def is_admin(user):
    return user.is_staff


# -----------------------------------------
# ADMIN DASHBOARD — USERS, MEDIA, CALL RECORDS
# -----------------------------------------
@user_passes_test(is_admin)
def admin_create_user(request):

    # ----------------------------------------------------
    # FORM FOR CREATING USERS
    # ----------------------------------------------------
    class CreateUserForm(forms.Form):
        username = forms.CharField(max_length=150)
        password = forms.CharField(widget=forms.PasswordInput)
        is_staff = forms.BooleanField(required=False)
        is_superuser = forms.BooleanField(required=False)

    # --- Handle Form Submit ---
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            user = User.objects.create_user(
                username=data["username"],
                password=data["password"]
            )
            user.is_staff = data["is_staff"]
            user.is_superuser = data["is_superuser"]
            user.save()

            return redirect("admin_create_user")
    else:
        form = CreateUserForm()

    # ----------------------------------------------------
    # USERS LIST
    # ----------------------------------------------------
    users = User.objects.all().order_by("-id")[:50]

    # ----------------------------------------------------
    # MEDIA FILES: IMAGES + VIDEOS
    # ----------------------------------------------------
    media = MediaFile.objects.order_by("-uploaded_at")[:100]

    # ----------------------------------------------------
    # CALL RECORDINGS LIST
    # ----------------------------------------------------
    call_records = CallRecording.objects.order_by("-created_at")[:100]

    # ----------------------------------------------------
    # RENDER DASHBOARD TEMPLATE
    # ----------------------------------------------------
    return render(request, "admin_create_user.html", {
        "form": form,
        "users": users,
        "media": media,
        "call_records": call_records,
    })
