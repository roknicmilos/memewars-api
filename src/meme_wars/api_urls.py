from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from apps.users.urls import urlpatterns as users_urlpatterns
from apps.wars.urls import urlpatterns as wars_urlpatterns
from meme_wars.views import APIIndexView

v1_api_urlpatterns = [
    *users_urlpatterns,
    *wars_urlpatterns,
]

schema_urlpatterns = [
    path('download/', SpectacularAPIView.as_view(), name='download'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema:download'), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema:download'), name='redoc'),
]

urlpatterns = [
    path('', APIIndexView.as_view(), name='index'),
    path('v1/', include((v1_api_urlpatterns, 'meme_wars'), namespace='v1')),
    path('schema/', include((schema_urlpatterns, 'meme_wars'), namespace='schema')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
