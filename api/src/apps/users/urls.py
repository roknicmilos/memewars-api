from django.urls import path, include

from apps.users.views import GoogleAuthLoginUrlAPIView, GoogleAuthCallbackAPIView

google_auth_urlpatterns = [
    path('login-url/', GoogleAuthLoginUrlAPIView.as_view(), name='login_url'),
    path('callback/', GoogleAuthCallbackAPIView.as_view(), name='callback'),
]

urlpatterns = [
    path('google-auth/', include((google_auth_urlpatterns, 'apps.users'), namespace='google_auth')),
]
