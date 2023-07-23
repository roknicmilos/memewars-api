from django.urls import include, path

from apps.wars import views

wars_urlpatterns = [
    path("", views.WarListAPIView.as_view(), name="index"),
    path("<int:pk>/", views.WarRetrieveAPIView.as_view(), name="details"),
]

memes_urlpatterns = [
    path("", views.MemeListCreateAPIView.as_view(), name="index"),
    path("<int:pk>/", views.MemeDestroyAPIView.as_view(), name="details"),
]

votes_urlpatterns = [
    path("", views.VoteListCreateAPIView.as_view(), name="index"),
    path("<int:pk>/", views.VotePatchAPIView.as_view(), name="details"),
]

urlpatterns = [
    path("wars/", include((wars_urlpatterns, "apps.wars"), namespace="wars")),
    path("memes/", include((memes_urlpatterns, "apps.wars"), namespace="memes")),
    path("votes/", include((votes_urlpatterns, "apps.wars"), namespace="votes")),
]
