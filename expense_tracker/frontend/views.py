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
    # Calculate totals
    total_income = Income.objects.filter(user=request.user).aggregate(total=models.Sum("amount"))["total"] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total=models.Sum("amount"))["total"] or 0
    
    # Get recent transactions
    recent_expenses = Expense.objects.filter(user=request.user).order_by("-date")[:5]
    recent_incomes = Income.objects.filter(user=request.user).order_by("-date")[:5]
    
    # Calculate spending by category
    categories = Expense.objects.filter(user=request.user).values(
        'category'
    ).annotate(
        total_spent=models.Sum('amount')
    ).order_by('-total_spent')[:5]
    
    # Prepare context
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'recent_expenses': recent_expenses,
        'recent_incomes': recent_incomes,
        'categories': categories,
        'balance': total_income - total_expenses,
        'income_expense': { 
            'income': total_income,
            'expense': total_expenses,
            'balance': total_income - total_expenses
        }
    }
    
    return render(request, "reports/dashboard.html", context)

@login_required
def income_vs_expense(request):
    total_income = Income.objects.filter(user=request.user).aggregate(total=models.Sum("amount"))["total"] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total=models.Sum("amount"))["total"] or 0
    return render(request, "reports/income_vs_expense.html", {"total_income": total_income, "total_expenses": total_expenses})

@login_required
def spending_by_category(request):
    categories = Expense.objects.filter(user=request.user).values("category__name").annotate(total_spent=models.Sum("amount"))
    return render(request, "reports/spending_by_category.html", {"categories": categories})
