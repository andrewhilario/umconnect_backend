from django.urls import path
from . import views


urlpatterns = [
    path("", views.GetAllUsersView.as_view(), name="get_all_users"),
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
        "user/<str:username>/",
        views.ViewUserByUsernameView.as_view(),
        name="user_by_username",
    ),
    path(
        "friends/",
        views.FriendsListView.as_view(),
        name="friends-list",
    ),
    path(
        "friend-requests/",
        views.FriendRequestsListView.as_view(),
        name="friend-requests",
    ),
    path(
        "send-friend-request/<int:pk>/",
        views.SendFriendRequestView.as_view(),
        name="send-friend-request",
    ),
    path(
        "remove-friend-request/<int:pk>/",
        views.RemoveFriendRequestView.as_view(),
        name="remove-friend-request",
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
