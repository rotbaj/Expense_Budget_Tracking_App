from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from budgets.models import Budget
from expenses.models import Expense
from incomes.models import Income

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def budget_progress(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, "reports/budget_progress.html", {"budgets": budgets})

@login_required
def dashboard(request):
    total_income = Income.objects.filter(user=request.user).aggregate(total=models.Sum("amount"))["total"] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total=models.Sum("amount"))["total"] or 0
    recent_expenses = Expense.objects.filter(user=request.user).order_by("-date")[:5]
    return render(request, "reports/dashboard.html", {"total_income": total_income, "total_expenses": total_expenses, "recent_expenses": recent_expenses})

@login_required
def income_vs_expense(request):
    total_income = Income.objects.filter(user=request.user).aggregate(total=models.Sum("amount"))["total"] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total=models.Sum("amount"))["total"] or 0
    return render(request, "reports/income_vs_expense.html", {"total_income": total_income, "total_expenses": total_expenses})

@login_required
def spending_by_category(request):
    categories = Expense.objects.filter(user=request.user).values("category__name").annotate(total_spent=models.Sum("amount"))
    return render(request, "reports/spending_by_category.html", {"categories": categories})
