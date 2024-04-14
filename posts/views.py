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
from .serializers import CreatePostSerializer, PostSerializer, UpdatePostSerializer

# Models
from .models import PostModel, LikeModel, CommentModel, ShareModel
from posts import serializers


# Create your views here.
class CreatePostView(APIView):
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = self.serializer_class(data=request.data)

            if "post_image" in request.FILES:
                file = request.FILES["post_image"]
                max_size_mb = 2
                if file.size > max_size_mb * 1024 * 1024:
                    return Response(
                        {"error": f"File size should not exceed {max_size_mb}MB"},
                        status=400,
                    )

            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)


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
    queryset = PostModel.objects.all()

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
        return PostModel.objects.filter(user=user).prefetch_related("likes")

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
