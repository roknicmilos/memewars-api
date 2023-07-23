from django.urls import include, path

from apps.users.views import (
    GoogleAuthCallbackAPIView,
    GoogleAuthLoginURLAPIView,
    LogoutAPIView,
)

google_auth_urlpatterns = [
    path("login/", GoogleAuthLoginURLAPIView.as_view(), name="login"),
    path("callback/", GoogleAuthCallbackAPIView.as_view(), name="callback"),
]

users_urlpatterns = [
    path("google-auth/", include((google_auth_urlpatterns, "apps.users"), namespace="google_auth")),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]

urlpatterns = [path("", include((users_urlpatterns, "apps.users"), namespace="users"))]
