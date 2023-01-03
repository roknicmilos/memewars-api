from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
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

urlpatterns += staticfiles_urlpatterns()
