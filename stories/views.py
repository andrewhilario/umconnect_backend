from django.shortcuts import render
from .serializers import StoriesSerializer, CreateStorySerializer
from .models import Stories
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import cloudinary.uploader
from operator import attrgetter
from itertools import groupby
from datetime import timedelta
from django.utils import timezone


class GetAllStoriesView(APIView):
    serializer_class = StoriesSerializer

    def get(self, request):
        stories = Stories.objects.all()
        stories = sorted(stories, key=lambda x: x.user.id)  # Sort stories by user's ID

        grouped_stories = {}
        for user_id, user_stories in groupby(stories, key=lambda x: x.user.id):
            grouped_stories[user_id] = list(user_stories)

        paginator = PageNumberPagination()
        paginator.page_size = 10

        # Convert grouped_stories.items() to a list of tuples before pagination
        grouped_stories_list = list(grouped_stories.items())
        result_page = paginator.paginate_queryset(grouped_stories_list, request)

        # Extract the stories from the result page
        flat_grouped_stories = [
            story for _, user_stories in result_page for story in user_stories
        ]

        serializer = self.serializer_class(flat_grouped_stories, many=True)
        return paginator.get_paginated_response(serializer.data)


class CreateStoryView(APIView):
    serializer_class = CreateStorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if "story" in request.FILES:
            file = request.FILES["story"]
            max_size_mb = 2

            if file.size > max_size_mb * 1024 * 1024:
                return Response(
                    {"error": "File size must be less than 5MB"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            upload_data = cloudinary.uploader.upload(file)
            url = upload_data["url"]
            request.data["story"] = url

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteStoriesAfter24Hours(APIView):
    def get(self, request):
        if Stories.objects.filter(
            created_at__lte=timezone.now() - timedelta(days=1)
        ).exist():
            Stories.objects.filter(
                created_at__lte=timezone.now() - timedelta(days=1)
            ).delete()
            return Response(
                {"message": "Stories older than 24 hours have been deleted."}
            )

        return Response({"message": "No stories to delete."})
