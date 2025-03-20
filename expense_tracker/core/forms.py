# core/forms.py
from django import forms
from .models import Expense, Income, Budget

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'date']

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'category', 'description', 'date']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount', 'category', 'description', 'start_date', 'end_date']