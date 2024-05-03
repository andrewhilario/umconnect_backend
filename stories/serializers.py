from rest_framework import serializers
from .models import Stories
from users.serializers import UserModelSerializer


class StoriesSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = Stories
        fields = [
            "id",
            "user",
            "story",
            "created_at",
        ]


class CreateStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = [
            "story",
        ]
