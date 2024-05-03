from django.urls import path
from . import views


urlpatterns = [
    path("", views.GetAllReelsView.as_view(), name="list_reels"),
    path("create/", views.CreateReelView.as_view(), name="create_reel"),
    path(
        "<int:pk>/like/",
        views.ReelsLikeView.as_view(),
        name="like_reel",
    ),
    path(
        "<int:pk>/comment/",
        views.CreateReelsCommentView.as_view(),
        name="create_comment",
    ),
    path(
        "<int:pk>/delete/",
        views.DeleteReelCronJob.as_view(),
        name="delete_reel",
    ),
]
