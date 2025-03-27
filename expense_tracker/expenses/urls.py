from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, CategoryViewSet, ExpenseListView, ExpenseCreateView, ExpenseDetailView, ExpenseEditView  

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', ExpenseListView.as_view(), name='expense_list'),
    path('create/', ExpenseCreateView.as_view(), name='expense_create'),
    path('<int:pk>/', ExpenseDetailView.as_view(), name='expense_detail'),
    path('expenses/<int:pk>/edit/', ExpenseEditView.as_view(), name='expense_edit'),
]