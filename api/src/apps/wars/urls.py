from django.urls import path, include
from apps.wars import views

wars_urlpatterns = [
    path('', views.WarListAPIView.as_view(), name='index'),
    path('<int:pk>/', views.WarRetrieveAPIView.as_view(), name='details'),
]

memes_urlpatterns = [
    path('', views.MemeListCreateAPIView.as_view(), name='index'),
]

urlpatterns = [
    path('wars/', include((wars_urlpatterns, 'apps.wars'), namespace='wars')),
    path('memes/', include((memes_urlpatterns, 'apps.wars'), namespace='memes')),
]
