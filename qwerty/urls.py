from django.contrib import admin
from django.urls import path

from qwerty.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
]
