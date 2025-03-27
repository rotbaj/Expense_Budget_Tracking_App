from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BudgetViewSet, BudgetListView, BudgetCreateView, BudgetUpdateView, BudgetDeleteView, BudgetDetailView

router = DefaultRouter()
router.register(r'budgets', BudgetViewSet, basename='budget')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', BudgetListView.as_view(), name='budget_list'),
    path('create/', BudgetCreateView.as_view(), name='budget_create'),\
    path("<int:pk>/edit/", BudgetUpdateView.as_view(), name="budget_edit"),
    path("<int:pk>/delete/", BudgetDeleteView.as_view(), name="budget_delete"),
    path("<int:pk>/", BudgetDetailView.as_view(), name="budget_detail"),
]