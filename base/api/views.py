from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

from users.models import UserModel
from users.serializers import UserModelSerializer
from django.contrib.auth import get_user_model


class get_routes(APIView):
    def get(self, request):
        routes = {
            "users": "/users/",
            "posts": "/posts/",
            "token": "/token/",
            "token/refresh": "/token/refresh/",
            "token/verify": "/token/verify/",
        }
        return Response(routes)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["role"] = user.role
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
