from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.meme_wars.views import WarViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'wars', WarViewSet, basename='wars')
router.register(r'votes', VoteViewSet, basename='votes')

urlpatterns = [
    path(r'', include(router.urls)),
]
