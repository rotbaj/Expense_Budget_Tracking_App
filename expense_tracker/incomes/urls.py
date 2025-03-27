from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncomeViewSet, IncomeListView, IncomeCreateView, IncomeDetailView

router = DefaultRouter()
router.register(r'incomes', IncomeViewSet, basename='income')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', IncomeListView.as_view(), name='income_list'),
    path('create/', IncomeCreateView.as_view(), name='income_create'),
    path('incomes/detail/<int:pk>/', IncomeDetailView.as_view(), name='income_detail'),
]