from rest_framework import serializers
from .models import ReelModel, ReelCommentModel, ReelLikeModel, ReelShareModel
from users.serializers import UserModelSerializer
from users.models import UserModel


class ReelCommentModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = ReelCommentModel
        fields = [
            "user",
            "reel",
            "comment",
            "created_at",
        ]


class ReelShareModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReelShareModel
        fields = [
            "user",
            "reel",
            "share_content",
            "created_at",
        ]


class UserSerializerForReels(serializers.ModelSerializer):
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


class ReelModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    comments = ReelCommentModelSerializer(
        many=True, read_only=True
    )  # Update source parameter
    likes = UserSerializerForReels(many=True, read_only=True)
    shares = ReelShareModelSerializer(many=True, read_only=True)

    class Meta:
        model = ReelModel
        fields = [
            "user",
            "reel_video",
            "reel_caption",
            "created_at",
            "likes",
            "comments",
            "shares",
        ]


class CreateReelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReelModel
        fields = [
            "reel_video",
            "reel_caption",
        ]


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReelCommentModel
        fields = [
            "comment",
        ]
