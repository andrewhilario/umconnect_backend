import json
from django.shortcuts import render

# REST Framework
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics

# Serializers
from .serializers import (
    CreatePostSerializer,
    PostSerializer,
    ShareCommentSerializer,
    UpdatePostSerializer,
    CommentSerializer,
    ShareSerializer,
    ShareLikeSerializer,
    CreateShareCommentSerializer,
)

# Models
from .models import (
    PostModel,
    LikeModel,
    CommentModel,
    ShareModel,
    ShareLikeModel,
    ShareCommentModel,
)
from posts import serializers
import cloudinary.uploader


# Create your views here.
class CreatePostView(APIView):
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.is_authenticated:

            if "post_image" in request.FILES:

                files = request.FILES.getlist("post_image")
                max_size_mb = 2
                for file in files:
                    if file.size > max_size_mb * 1024 * 1024:
                        return Response(
                            {"error": f"File size should not exceed {max_size_mb}MB"},
                            status=400,
                        )

                image_urls = []
                for file in files:
                    upload_data = cloudinary.uploader.upload(file)
                    url = upload_data["url"]
                    image_urls.append(url)
                print("image_urls", image_urls)

                image_urls_json = json.dumps(image_urls)
                request.data["post_image"] = image_urls_json

            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                serializer.save(user=user)

                return Response(
                    {"post": serializer.data},
                    status=201,
                )

            return Response(serializer.errors, status=400)

        else:
            print("User not authenticated")
        return Response({"error": "No image files provided"}, status=400)


class UpdateAndGetPostByIdView(ModelViewSet):
    serializer_class = UpdatePostSerializer
    queryset = PostModel.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class DeletePostByIdView(APIView):
    queryset = PostModel.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        post.delete()
        return Response(status=204)


class GetAllPostsView(APIView):
    serializer_class = PostSerializer
    queryset = PostModel.objects.all().order_by("-created_at")

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 5
        posts = paginator.paginate_queryset(self.queryset, request)
        serializer = self.serializer_class(posts, many=True)
        return paginator.get_paginated_response(serializer.data)


class GetPostByUserView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return (
            PostModel.objects.filter(user=user)
            .prefetch_related("likes")
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class GetPostByUserIdView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        return (
            PostModel.objects.filter(user=user_id)
            .prefetch_related("likes")
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class LikePostView(APIView):
    queryset = PostModel.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            return Response(status=204)
        post.likes.add(user)
        return Response(status=204)


class UnlikePostView(APIView):
    queryset = PostModel.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            return Response(status=204)
        return Response(status=204)


class CommentPostView(APIView):
    queryset = PostModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CommentSerializer

    def patch(self, request, pk=None):
        post = get_object_or_404(PostModel.objects.all(), pk=pk)
        user = request.user

        serializer = self.serializer_class(data=request.data)

        if "comment_image" in request.FILES:
            file = request.FILES["comment_image"]
            max_size_mb = 2
            if file.size > max_size_mb * 1024 * 1024:
                return Response(
                    {"error": f"File size should not exceed {max_size_mb}MB"},
                    status=400,
                )

        if serializer.is_valid():
            comments = CommentModel.objects.create(
                user=user,
                post=post,
                comment=serializer.validated_data["comment"],
            )
            comments.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AllSharedPostsView(APIView):
    serializer_class = serializers.ShareSerializer
    queryset = ShareModel.objects.all().order_by("-created_at")

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 5
        posts = paginator.paginate_queryset(self.queryset, request)
        serializer = self.serializer_class(posts, many=True)
        return paginator.get_paginated_response(serializer.data)


class SharePostView(APIView):
    queryset = PostModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ShareSerializer

    def patch(self, request, pk=None):
        post = get_object_or_404(PostModel.objects.all(), pk=pk)
        user = request.user

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            post = get_object_or_404(PostModel.objects.all(), pk=pk)
            post.is_shared = True
            post.save()
            if serializer.validated_data["share_content"] is not None:
                shares = ShareModel.objects.create(
                    user=user,
                    post=post,
                    share_content=serializer.validated_data["share_content"],
                )
                shares.save()
            else:
                shares = ShareModel.objects.create(user=user, post=post)
                shares.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LikeSharedPostView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ShareLikeSerializer

    def patch(self, request, pk=None):
        post = get_object_or_404(ShareModel.objects.all(), pk=pk)
        user = request.user

        if ShareLikeModel.objects.filter(user=user, share=post).exists():
            liked = ShareLikeModel.objects.get(user=user, share=post)
            liked.delete()
            return Response({"message": "Shared Post unliked"}, status=200)

        likes = ShareLikeModel.objects.create(user=user, share=post)
        likes.save()
        return Response({"message": "Shared Post liked"}, status=201)


class CommentSharedPostView(APIView):
    queryset = ShareModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CreateShareCommentSerializer

    def patch(self, request, pk=None):
        post = get_object_or_404(ShareModel.objects.all(), pk=pk)
        user = request.user

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            comments = ShareCommentModel.objects.create(
                user=user,
                share=post,
                share_comment=serializer.validated_data["share_comment"],
            )
            comments.save()
            return Response(ShareCommentSerializer(comments).data, status=201)

        return Response(serializer.errors, status=400)


class GetSharedPostByUser(generics.ListAPIView):
    serializer_class = serializers.ShareSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return ShareModel.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)
