from django.shortcuts import render
from requests import delete
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import (
    ReelModelSerializer,
    CreateReelSerializers,
    CreateCommentSerializer,
)
import cloudinary.uploader
import os
import mimetypes


class GetAllReelsView(APIView):
    serializer_class = ReelModelSerializer

    def get(self, request):
        reels = ReelModel.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(reels, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CreateReelView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateReelSerializers

    def post(self, request):
        user = request.user

        if user.is_authenticated:
            if "reel_video" in request.data:
                file = request.data["reel_video"]
                max_size_mb = 5

                if file.size > max_size_mb * 1024 * 1024:
                    return Response(
                        {"error": "File size must be less than 5MB"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not self.is_video(file):
                    return Response(
                        {"error": "File must be a video"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                upload_data = cloudinary.uploader.upload(file, resource_type="video")
                url = upload_data["url"]
                request.data["reel_video"] = url

            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                serializer.save(user=user)
                return Response(
                    {"reel": serializer.data},
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def is_video(self, file):
        # Get the file extension
        _, extension = os.path.splitext(file.name)
        # Get the MIME type of the file
        mime_type, _ = mimetypes.guess_type(file.name)

        # Check if extension or MIME type indicates a video file
        if extension.lower() in [".mp4", ".avi", ".mov", ".mkv", ".flv"] or (
            mime_type is not None and mime_type.startswith("video")
        ):
            return True
        return False


class DeleteReelCronJob(APIView):
    def delete(self, request, pk=None):
        reel = get_object_or_404(ReelModel, pk=pk)
        reel.delete()
        return Response(
            {"message": "Reel deleted"},
            status=status.HTTP_200_OK,
        )


class ReelsLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk=None):
        user = request.user
        reel = get_object_or_404(ReelModel, pk=pk)

        if user.is_authenticated:
            if user in reel.likes.all():
                reel.likes.remove(user)
                return Response(
                    {"message": "Unliked"},
                    status=status.HTTP_200_OK,
                )
            else:
                reel.likes.add(user)
                return Response(
                    {"message": "Liked"},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"error": "User not authenticated"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CreateReelsCommentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCommentSerializer

    def post(self, request, pk=None):
        user = request.user
        reel = get_object_or_404(ReelModel, pk=pk)

        if user.is_authenticated:
            data = request.data
            data["user"] = user
            data["reel"] = reel

            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                comment = ReelCommentModel.objects.create(**data)
                serializer = self.serializer_class(comment)
                return Response(
                    {"comment": serializer.data},
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"error": "User not authenticated"},
            status=status.HTTP_400_BAD_REQUEST,
        )
