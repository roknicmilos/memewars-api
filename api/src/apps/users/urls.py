from django.urls import path, include

from apps.users.views import GoogleAuthLoginUrlAPIView, GoogleAuthCallbackAPIView

google_auth_urlpatterns = [
    path('login/', GoogleAuthLoginUrlAPIView.as_view(), name='login'),
    path('callback/', GoogleAuthCallbackAPIView.as_view(), name='callback'),
]

urlpatterns = [
    path('google-auth/', include((google_auth_urlpatterns, 'apps.users'), namespace='google_auth')),
]
