from django.urls import path
from users.views import get_auth_toke

urlpatterns = [
    path('token/', get_auth_toke),
]
