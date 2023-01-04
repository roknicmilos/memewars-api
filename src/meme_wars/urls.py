from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from apps.users.urls import urlpatterns as users_urlpatterns
from apps.wars.urls import urlpatterns as wars_urlpatterns

api_urlpatterns = [
    *users_urlpatterns,
    *wars_urlpatterns,
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((api_urlpatterns, 'meme_wars'), namespace='api')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
