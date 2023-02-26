from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.wars.views import WarViewSet, MemeViewSet

router = DefaultRouter()
router.register(r'wars', WarViewSet, basename='wars')
router.register(r'memes', MemeViewSet, basename='memes')

urlpatterns = [
    path('', include((router.urls, 'apps.wars'), namespace='wars'))
]
