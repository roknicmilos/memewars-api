from django.http import JsonResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.wars.views import WarViewSet, VoteViewSet
from apps.users.urls import urlpatterns as auth_urlpatterns

router = DefaultRouter()
router.register(r'wars', WarViewSet, basename='wars')
router.register(r'votes', VoteViewSet, basename='votes')

wars_urlpatterns = [
    path(r'', include(router.urls)),
]

api_urlpatterns = [
    path('', lambda r: JsonResponse(data={'message': "This is not a path you're looking for"})),
    *auth_urlpatterns,
    *wars_urlpatterns,
]

urlpatterns = [
    path('api/v1/', include((api_urlpatterns, 'apps.wars'), namespace='api'))
]
