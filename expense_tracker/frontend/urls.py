from django.urls import path
from .views import dashboard_view, budget_progress, dashboard, income_vs_expense, spending_by_category

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path("reports/budget-progress/", budget_progress, name="budget_progress"),
    path("reports/dashboard/", dashboard, name="dashboard"),
    path("reports/income-vs-expense/", income_vs_expense, name="income_vs_expense"),
    path("reports/spending-by-category/", spending_by_category, name="spending_by_category"),
]