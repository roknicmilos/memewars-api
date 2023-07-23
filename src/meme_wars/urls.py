from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.users.urls import urlpatterns as users_urlpatterns
from apps.wars.urls import urlpatterns as wars_urlpatterns
from meme_wars.views import APIIndexView, IndexView

schema_urlpatterns = [
    path("download/", SpectacularAPIView.as_view(), name="download"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="api:schema:download"), name="swagger"),
    path("redoc/", SpectacularRedocView.as_view(url_name="api:schema:download"), name="redoc"),
]

api_urlpatterns = [
    path("", APIIndexView.as_view(), name="index"),
    *users_urlpatterns,
    *wars_urlpatterns,
    path("schema/", include((schema_urlpatterns, "meme_wars"), namespace="schema")),
]

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    path("api/", include((api_urlpatterns, "meme_wars"), namespace="api")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
