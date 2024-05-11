from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Notifications
from .serializers import NotificationSerializer


# Create your views here.
class GetAllNotificationByUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        notifications = Notifications.objects.filter(user=user_id)

        pagination_class = PageNumberPagination()
        pagination_class.page_size = 10
        page = pagination_class.paginate_queryset(notifications, request)

        if page is not None:
            serializer = NotificationSerializer(page, many=True)
            return pagination_class.get_paginated_response(serializer.data)

        return Response(
            {"message": "No notifications found for this user."},
            status=status.HTTP_404_NOT_FOUND,
        )


class UpdateNotificationToRead(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        notification = Notifications.objects.get(pk=pk)
        notification.is_read = True
        notification.save()
        return Response(
            {"message": "Notification updated successfully."}, status=status.HTTP_200_OK
        )


class UpdateAllNotificationsToRead(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_id = request.user.id
        notifications = Notifications.objects.filter(user=user_id)
        for notification in notifications:
            notification.is_read = True
            notification.save()

        return Response(
            {"message": "All notifications updated successfully."},
            status=status.HTTP_200_OK,
        )
