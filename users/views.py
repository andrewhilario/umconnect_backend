from django.shortcuts import render

# REST Framework
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Serializers
from .serializers import CreateUserSerializer, UserModelSerializer

# Models
from .models import UserModel


class SignUpView(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = UserModel.objects.create_user(**serializer.validated_data)
            user.save()

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UpdateUserView(ModelViewSet):
    serializer_class = CreateUserSerializer
    queryset = UserModel.objects.all()

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
