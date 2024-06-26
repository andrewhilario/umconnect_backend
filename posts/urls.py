from django.urls import path
from . import views


urlpatterns = [
    path("", views.GetAllPostsView.as_view(), name="list_posts"),
    path("user/", views.GetPostByUserView.as_view(), name="list_posts_by_user"),
    path(
        "user/<int:pk>/",
        views.GetPostByUserIdView.as_view(),
        name="list_posts_by_user_id",
    ),
    path(
        "user/shared-posts/",
        views.GetSharedPostByUser.as_view(),
        name="list_shared_posts_by_user",
    ),
    path("create/", views.CreatePostView.as_view(), name="create_post"),
    path(
        "<int:pk>/",
        views.UpdateAndGetPostByIdView.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
            }
        ),
        name="update_get_post_by_id",
    ),
    path("<int:pk>/like/", views.LikePostView.as_view(), name="like_post"),
    path("<int:pk>/unlike/", views.UnlikePostView.as_view(), name="unlike_post"),
    path(
        "<int:pk>/comment/",
        views.CommentPostView.as_view(),
        name="create_comment",
    ),
    path("share-posts/", views.AllSharedPostsView.as_view(), name="share_post"),
    path(
        "<int:pk>/share/",
        views.SharePostView.as_view(),
        name="share_post",
    ),
    path(
        "<int:pk>/share/like/",
        views.LikeSharedPostView.as_view(),
        name="like_shared_post",
    ),
    path(
        "<int:pk>/share/comment/",
        views.CommentSharedPostView.as_view(),
        name="comment_shared_post",
    ),
    path(
        "delete/<int:pk>/",
        views.DeletePostByIdView.as_view(),
        name="delete_post_by_id",
    ),
]
