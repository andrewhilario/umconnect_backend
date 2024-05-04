from django.shortcuts import render

# REST Framework
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
import cloudinary.uploader


# Serializers
from .serializers import (
    CreateUserSerializer,
    UserModelSerializer,
    FriendSerializer,
    UserSerializer,
    FriendRequestSerializer,
)

# Models
from .models import UserModel, Friends, FriendRequests


class SignUpView(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = UserModel.objects.create_user(**serializer.validated_data)
            user.save()

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UpdateUserView(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = UserModel.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def partial_update(self, request, pk=None):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)

        if "profile_picture" in request.FILES:
            file = request.FILES["profile_picture"]
            max_size_mb = 2
            if file.size > max_size_mb * 1024 * 1024:
                return Response(
                    {"error": f"File size should not exceed {max_size_mb}MB"},
                    status=400,
                )

            upload_data = cloudinary.uploader.upload(file)
            user.profile_picture = upload_data["url"]

        if "cover_photo" in request.FILES:
            file = request.FILES["cover_photo"]
            max_size_mb = 2
            if file.size > max_size_mb * 1024 * 1024:
                return Response(
                    {"error": f"File size should not exceed {max_size_mb}MB"},
                    status=400,
                )

            upload_data = cloudinary.uploader.upload(file)
            user.cover_photo = upload_data["url"]

        if "bio" in request.data:
            if len(request.data["bio"]) > 200:
                return Response(
                    {"error": "Bio should not exceed 200 characters"}, status=400
                )
            user.bio = request.data["bio"]

        # Handle first_name and last_name update
        if "first_name" in request.data:
            user.first_name = request.data["first_name"]

        if "last_name" in request.data:
            user.last_name = request.data["last_name"]

        # Save user object

        user.save()
        return Response(
            {
                "message": "User updated successfully",
                "user": UserModelSerializer(user).data,
            },
            status=200,
        )


class GetAllUsersView(APIView):

    def get(self, request):
        users = UserModel.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(users, request)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)


class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


class ViewUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(UserModel, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


class ViewUserByUsernameView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(UserModel, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


class AddandRemoveFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        friend = get_object_or_404(UserModel, pk=pk)

        if user == friend:
            return Response(
                {"error": "You cannot add yourself as a friend"}, status=400
            )

        if Friends.objects.filter(user=user, friend=friend).exists():
            return Response({"error": "Friend already exists"}, status=400)

        add_friend = Friends.objects.create(user=user, friend=friend)
        add_friend.save()

        return Response(
            {
                "message": "Friend added successfully",
                "friend_id": FriendSerializer(add_friend).data,
            },
            status=201,
        )

    def delete(self, request, pk):
        user = get_object_or_404(UserModel, pk=pk)
        friend = get_object_or_404(UserModel, pk=request.data["friend_id"])
        user.friends.remove(friend)
        return Response({"message": "Friend removed successfully"}, status=200)


class FriendRequestsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        friend_requests = FriendRequests.objects.filter(receiver=user)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(friend_requests, request)
        if page is not None:
            serializer = FriendRequestSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=200)


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        friend = get_object_or_404(UserModel, pk=pk)

        if user == friend:
            return Response(
                {"error": "You cannot send a friend request to yourself"}, status=400
            )

        if FriendRequests.objects.filter(sender=user, receiver=friend).exists():
            return Response({"error": "Friend request already exists"}, status=400)

        add_friend_request = FriendRequests.objects.create(sender=user, receiver=friend)
        add_friend_request.save()

        return Response(
            {
                "message": "Friend request sent successfully",
                "friend_request_id": FriendRequestSerializer(add_friend_request).data,
            },
            status=201,
        )


class RemoveFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        friend_request = get_object_or_404(
            FriendRequests, pk=request.data["friend_request_id"]
        )
        friend_request.delete()
        return Response({"message": "Friend request removed successfully"}, status=200)


class FriendsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        friends = Friends.objects.filter(user=user)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(friends, request)
        if page is not None:
            serializer = FriendSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data, status=200)
