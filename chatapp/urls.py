from django.urls import path
from .views_call_recording import save_call_recording
from .views_media import upload_media
from . import views

urlpatterns = [
    # Default landing — redirect to login
    path("", views.redirect_to_login, name="home"),

    # Chat room
    path("chat/<str:room_name>/", views.chat_room, name="chat_room"),

    # Admin panel create user
    path("panel/create-user/", views.admin_create_user, name="admin_create_user"),

    # Call recording upload endpoint
    path("call/record/", save_call_recording, name="save_call_recording"),
    #media upload
    path("media/upload/", upload_media, name="upload_media"),

]
