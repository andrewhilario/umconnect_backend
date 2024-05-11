from enum import Enum
from .models import Notifications


class NotificationType(Enum):
    NEW_FRIEND_REQUEST = "NEW_FRIEND_REQUEST"
    FRIEND_REQUEST_ACCEPTED = "FRIEND_REQUEST_ACCEPTED"
    NEW_MESSAGE = "NEW_MESSAGE"
    NEW_POST = "NEW_POST"
    POST_LIKED = "POST_LIKED"
    POST_COMMENTED = "POST_COMMENTED"
    POST_SHARED = "POST_SHARED"


def create_notification(notification_type, sender, receiver):
    if notification_type == "NEW_FRIEND_REQUEST":
        title = "New Friend Request"
        message = f"{sender.username} sent you a friend request."
        notification = Notifications.objects.create(
            title=title,
            message=message,
            notification_type=NotificationType.NEW_FRIEND_REQUEST.value,
            user=receiver,
        )
        return notification

    if notification_type == NotificationType.FRIEND_REQUEST_ACCEPTED:
        title = "Friend Request Accepted"
        message = f"{sender.username} accepted your friend request."
        notification = Notifications.objects.create(
            title=title,
            message=message,
            notification_type=NotificationType.FRIEND_REQUEST_ACCEPTED.value,
            user=receiver,
        )
        return notification

    if notification_type == NotificationType.NEW_POST:
        title = "New Post"
        message = f"{sender.username} created a new post."
        notification = Notifications.objects.create(
            title=title,
            message=message,
            notification_type=NotificationType.NEW_POST.value,
            user=receiver,
        )
        return notification

    if notification_type == NotificationType.POST_LIKED:
        title = "Post Liked"
        message = f"{sender.username} liked your post."
        notification = Notifications.objects.create(
            title=title,
            message=message,
            notification_type=NotificationType.POST_LIKED.value,
            user=receiver,
        )
        return notification

    if notification_type == NotificationType.POST_COMMENTED:
        title = "Post Commented"
        message = f"{sender.username} commented on your post."
        notification = Notifications.objects.create(
            title=title,
            message=message,
            notification_type=NotificationType.POST_COMMENTED.value,
            user=receiver,
        )
        return notification

    if notification_type == NotificationType.POST_SHARED:
        title = "Post Shared"
        message = f"{sender.username} shared your post."
        notification = Notifications.objects.create(
            title=title,
            message=message,
            notification_type=NotificationType.POST_SHARED.value,
            user=receiver,
        )
        return notification

    return None
