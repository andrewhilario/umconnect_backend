from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.SignUpView.as_view(), name="signup"),
    path(
        "update/",
        views.UpdateUserView.as_view(
            {
                "patch": "partial_update",
            }
        ),
        name="update",
    ),
    path("me/", views.GetUserView.as_view(), name="me"),
    path("user/<int:pk>/", views.ViewUserView.as_view(), name="user"),
    path(
        "friends/",
        views.FriendsListView.as_view(),
        name="friends-list",
    ),
    path(
        "add-friend/<int:pk>/",
        views.AddandRemoveFriendView.as_view(),
        name="add-friend",
    ),
    path(
        "remove-friend/<int:pk>/",
        views.AddandRemoveFriendView.as_view(),
        name="add-friend",
    ),
]
