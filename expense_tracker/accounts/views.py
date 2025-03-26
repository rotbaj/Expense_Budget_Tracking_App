from rest_framework import generics
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer