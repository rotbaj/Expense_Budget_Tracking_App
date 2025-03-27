from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReportPresetViewSet,
    ReportDashboardView,
    SpendingByCategoryReport,
    IncomeVsExpenseReport,
    BudgetProgressReport
)

router = DefaultRouter()
router.register(r'presets', ReportPresetViewSet, basename='reportpreset')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', ReportDashboardView.as_view(), name='report_dashboard'), 
    path('spending-by-category/', SpendingByCategoryReport.as_view(), name='spending-by-category'),
    path('income-vs-expense/', IncomeVsExpenseReport.as_view(), name='income-vs-expense'),
    path('budget-progress/', BudgetProgressReport.as_view(), name='budget-progress'),
]