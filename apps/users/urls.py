from django.urls import path
from apps.users.views import get_auth_toke

urlpatterns = [
    path('token/', get_auth_toke),
]
