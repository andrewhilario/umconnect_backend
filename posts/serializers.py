from dataclasses import fields
from rest_framework import serializers

from .models import (
    CommentModel,
    PostModel,
    ShareModel,
    ShareCommentModel,
    ShareLikeModel,
)
from users.serializers import UserModelSerializer
from users.models import UserModel

# Serializers


class CreatePostSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    is_shared = serializers.BooleanField(required=False)

    class Meta:
        model = PostModel
        fields = [
            "content",
            "user",
            "created_at",
            "updated_at",
            "is_shared",
            "post_type",
            "post_image",
        ]


class UpdatePostSerializer(serializers.ModelSerializer):

    user = UserModelSerializer(read_only=True)

    class Meta:
        model = PostModel
        fields = [
            "content",
            "user",
            "created_at",
            "updated_at",
            "post_image",
        ]


class UserSerializerForShareAndComments(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "profile_picture",
        ]


class CommentSerializer(serializers.ModelSerializer):
    comment_image = serializers.ImageField(required=False)
    user = UserSerializerForShareAndComments(read_only=True)

    class Meta:
        model = CommentModel
        fields = [
            "comment",
            "user",
            "created_at",
            "updated_at",
            "comment_image",
        ]


class ShareCommentSerializer(serializers.ModelSerializer):
    user = UserSerializerForShareAndComments(read_only=True)

    class Meta:
        model = ShareCommentModel
        fields = [
            "id",
            "user",
            "share_comment",
            "created_at",
        ]


class CreateShareCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareCommentModel
        fields = [
            "share_comment",
        ]


class ShareLikeSerializer(serializers.ModelSerializer):
    user = UserSerializerForShareAndComments(read_only=True)

    class Meta:
        model = ShareLikeModel
        fields = [
            "user",
            "created_at",
            "updated_at",
        ]


class SharePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = [
            "content",
            "is_shared",
            "user",
            "created_at",
            "updated_at",
        ]


class IsSharedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = [
            "id",
        ]


class ShareSerializer(serializers.ModelSerializer):
    post = IsSharedPostSerializer(read_only=True)
    user = UserSerializerForShareAndComments(read_only=True)
    share_content = serializers.CharField(required=False, allow_blank=True)
    likes = ShareLikeSerializer(many=True, source="sharelikemodel_set", read_only=True)
    comments = ShareCommentSerializer(
        many=True, source="sharecommentmodel_set", read_only=True
    )

    class Meta:
        model = ShareModel
        fields = [
            "id",
            "user",
            "share_content",
            "created_at",
            "updated_at",
            "likes",
            "comments",
            "post",
        ]


class UserSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "profile_picture",
        ]


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializerForPost(read_only=True)
    comments = CommentSerializer(many=True, source="commentmodel_set", read_only=True)
    likes = UserSerializerForPost(many=True, read_only=True)
    shares = ShareSerializer(many=True, source="sharemodel_set", read_only=True)

    class Meta:
        model = PostModel
        fields = [
            "id",
            "content",
            "post_type",
            "is_shared",
            "user",
            "created_at",
            "updated_at",
            "comments",
            "likes",
            "shares",
            "post_image",
        ]
