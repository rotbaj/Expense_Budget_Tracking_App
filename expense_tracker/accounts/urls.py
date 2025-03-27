from django.urls import path
from .views import RegisterUserView, CustomTokenObtainPairView, ProfileView
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'), 
    path('logout/', LogoutView.as_view(), name='logout'), 
]