from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from meme_wars.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
