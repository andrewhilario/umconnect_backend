from django.urls import path
from . import views

urlpatterns = [
    path("", views.GetAllNotificationByUser.as_view(), name="get_all_notifications"),
    path(
        "<int:pk>/",
        views.UpdateNotificationToRead.as_view(),
        name="update_notification",
    ),
    path(
        "all/",
        views.UpdateAllNotificationsToRead.as_view(),
        name="update_all_notifications",
    ),
]
