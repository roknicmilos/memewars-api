from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from qwerty.views import IndexView
from apps.meme_wars.urls import urlpatterns as meme_wars_urlpatterns

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('meme-wars/', include((meme_wars_urlpatterns, 'apps.meme_wars'), namespace='meme_wars')),
]

urlpatterns += staticfiles_urlpatterns()
