from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path('', views.index, name='index'),

    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # Expense URLs
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/<int:pk>/edit/', views.edit_expense, name='edit_expense'),
    path('expenses/<int:pk>/delete/', views.delete_expense, name='delete_expense'),

    # Income URLs
    path('incomes/', views.income_list, name='income_list'),
    path('incomes/add/', views.add_income, name='add_income'),
    path('incomes/<int:pk>/edit/', views.edit_income, name='edit_income'),
    path('incomes/<int:pk>/delete/', views.delete_income, name='delete_income'),

    # Budget URLs
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.add_budget, name='add_budget'),
    path('budgets/<int:pk>/edit/', views.edit_budget, name='edit_budget'),
    path('budgets/<int:pk>/delete/', views.delete_budget, name='delete_budget'),
]