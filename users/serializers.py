from rest_framework import serializers
from .models import UserModel


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
