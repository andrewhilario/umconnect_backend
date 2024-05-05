from rest_framework import serializers
from .models import Friends, UserModel, FriendRequests


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "date_of_birth",
            "phone_number",
            "bio",
            "profile_picture",
            "created_at",
            "updated_at",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_verified",
            "cover_photo",
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "date_of_birth",
            "phone_number",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # The UserManager is automatically used by the ModelSerializer
        return UserModel.objects.create_user(**validated_data)


class FriendSerializer(serializers.ModelSerializer):
    friend = UserModelSerializer(read_only=True)

    class Meta:
        model = Friends
        fields = ["friend", "added_at"]


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserModelSerializer(read_only=True)
    receiver = UserModelSerializer(read_only=True)

    class Meta:
        model = FriendRequests
        fields = ["id", "sender", "receiver", "sent_at", "is_accepted"]


class UserSerializer(serializers.ModelSerializer):
    friends = FriendSerializer(many=True, read_only=True)
    friend_requests = FriendRequestSerializer(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "date_of_birth",
            "phone_number",
            "bio",
            "profile_picture",
            "created_at",
            "updated_at",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_verified",
            "cover_photo",
            "friends",
            "friend_requests",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["friends"] = FriendSerializer(
            instance.user.all(), many=True
        ).data
        representation["friend_requests"] = FriendRequestSerializer(
            instance.receiver.all(), many=True
        ).data
        return representation
