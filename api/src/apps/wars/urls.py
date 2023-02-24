from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.wars.views import WarViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'wars', WarViewSet, basename='wars')
router.register(r'votes', VoteViewSet, basename='votes')

urlpatterns = [
    path('', include((router.urls, 'apps.wars'), namespace='wars'))
]
