from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Expense, Income, Budget
from .forms import ExpenseForm, IncomeForm, BudgetForm

# Home Page
def index(request):
    return render(request, 'core/index.html')

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

# Expense Views
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'core/expense_list.html', {'expenses': expenses})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'core/expense_form.html', {'form': form})

def edit_expense(request, pk):
    expense = get_object_or_404(Expense, id=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'core/expense_form.html', {'form': form})

def delete_expense(request, pk):
    expense = get_object_or_404(Expense, id=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'core/confirm_delete.html', {'object': expense})

# Income Views
def income_list(request):
    incomes = Income.objects.filter(user=request.user)
    return render(request, 'core/income_list.html', {'incomes': incomes})

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'core/income_form.html', {'form': form})

def edit_income(request, pk):
    income = get_object_or_404(Income, id=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'core/income_form.html', {'form': form})

def delete_income(request, pk):
    income = get_object_or_404(Income, id=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        return redirect('income_list')
    return render(request, 'core/confirm_delete.html', {'object': income})

# Budget Views
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'core/budget_list.html', {'budgets': budgets})

def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'core/budget_form.html', {'form': form})

def edit_budget(request, pk):
    budget = get_object_or_404(Budget, id=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'core/budget_form.html', {'form': form})

def delete_budget(request, pk):
    budget = get_object_or_404(Budget, id=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'core/confirm_delete.html', {'object': budget})