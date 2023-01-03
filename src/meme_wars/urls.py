from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from meme_wars.views import IndexView
from apps.meme_wars.urls import urlpatterns as meme_wars_urlpatterns

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
