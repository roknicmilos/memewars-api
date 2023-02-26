from django.urls import path, include
from apps.wars.views import WarListAPIView, MemeListAPIView

wars_urlpatterns = [
    path('', WarListAPIView.as_view(), name='list'),
]

memes_urlpatterns = [
    path('', MemeListAPIView.as_view(), name='list'),
]

urlpatterns = [
    path('wars/', include((wars_urlpatterns, 'apps.wars'), namespace='wars')),
    path('memes/', include((memes_urlpatterns, 'apps.wars'), namespace='memes')),
]
