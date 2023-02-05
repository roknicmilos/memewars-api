from django.urls import path

from apps.users.views import LoginAPIView

urlpatterns = [
    path('token/', LoginAPIView.as_view(), name='auth_token'),
]
