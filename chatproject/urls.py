from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


@login_required
def smart_login_redirect(request):
    """Redirect staff users to admin dashboard, regular users to chat."""
    if request.user.is_staff:
        return redirect("/panel/create-user/")
    return redirect("/chat/general/")


urlpatterns = [
    path("admin/", admin.site.urls),

    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("login-redirect/", smart_login_redirect, name="login_redirect"),

    path("", include("chatapp.urls")),
]

# ENABLE MEDIA SERVING
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ENABLE STATIC SERVING (for development with Daphne)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

