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
    post_image = serializers.ImageField(required=False)
    user = UserModelSerializer(read_only=True)
    is_shared = serializers.BooleanField(required=False)

    class Meta:
        model = PostModel
        fields = [
            "content",
            "user",
            "created_at",
            "updated_at",
            "post_image",
            "is_shared",
        ]


class UpdatePostSerializer(serializers.ModelSerializer):
    post_image = serializers.ImageField(required=False)

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
    class Meta:
        model = ShareCommentModel
        fields = "__all__"


class ShareLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareLikeModel
        fields = "__all__"


class SharePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostModel
        fields = [
            "content",
            "is_shared",
            "user",
            "created_at",
            "updated_at",
            "post_image",
        ]


class ShareSerializer(serializers.ModelSerializer):
    user = UserSerializerForShareAndComments(read_only=True)
    share_content = serializers.CharField(required=False, allow_blank=True)
    post = SharePostSerializer(read_only=True)
    likes = ShareLikeSerializer(many=True, source="sharelikemodel_set", read_only=True)
    comments = ShareCommentSerializer(
        many=True, source="sharecommentmodel_set", read_only=True
    )

    class Meta:
        model = ShareModel
        fields = [
            "user",
            "share_content",
            "created_at",
            "updated_at",
            "post",
            "likes",
            "comments",
        ]


class UserSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
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
            "content",
            "is_shared",
            "user",
            "created_at",
            "updated_at",
            "post_image",
            "comments",
            "likes",
            "shares",
        ]
