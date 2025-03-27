from django.urls import path, include
from .views import ReportDashboardView, ReportPresetViewSet, SpendingByCategoryReport, IncomeVsExpenseReport, BudgetProgressReport
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'presets', ReportPresetViewSet, basename='report-preset')

urlpatterns = [
    path('dashboard/', ReportDashboardView.as_view(), name='report_dashboard'),
    path('api/spending-by-category/', SpendingByCategoryReport.as_view(), name='spending-by-category'),
    path('api/income-vs-expense/', IncomeVsExpenseReport.as_view(), name='income-vs-expense'),
    path('api/budget-progress/', BudgetProgressReport.as_view(), name='budget-progress'),
    path('api/', include(router.urls)),
]