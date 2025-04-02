from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render
from django.views import View
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from .models import User


class RegisterUserView(generics.CreateAPIView):
    """
    View for user registration.
    Creates a new user and associated profile.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            {"detail": "User created successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token obtain view that includes user details in the response
    """
    serializer_class = CustomTokenObtainPairSerializer


class ProfileView(View):
    """
    View for displaying user profile (template-based)
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/profile.html')