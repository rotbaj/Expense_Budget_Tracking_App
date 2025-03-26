from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BudgetViewSet

router = DefaultRouter()
router.register(r'budgets', BudgetViewSet, basename='budget')

urlpatterns = [
    path('', include(router.urls)),
]