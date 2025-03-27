from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import ReportPreset
from .serializers import ReportPresetSerializer
from expenses.models import Expense
from incomes.models import Income
from budgets.models import Budget
from django.db.models import Sum
from datetime import date, timedelta
from django.views import View


class ReportDashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/dashboard.html') 

class ReportPresetViewSet(viewsets.ModelViewSet):
    serializer_class = ReportPresetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReportPreset.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SpendingByCategoryReport(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        time_range = request.query_params.get('range', 'month')
        today = date.today()
        
        if time_range == 'week':
            start_date = today - timedelta(days=7)
        elif time_range == 'month':
            start_date = today.replace(day=1)
        elif time_range == 'year':
            start_date = today.replace(month=1, day=1)
        else:
            start_date = today - timedelta(days=30)
        
        expenses = Expense.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lte=today
        ).values('category__name').annotate(total=Sum('amount')).order_by('-total')
        
        return Response({
            'start_date': start_date,
            'end_date': today,
            'results': list(expenses)
        })

class IncomeVsExpenseReport(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        today = date.today()
        start_date = today.replace(day=1)  # Current month
        
        expenses = Expense.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lte=today
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        incomes = Income.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lte=today
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            'start_date': start_date,
            'end_date': today,
            'income': incomes,
            'expense': expenses,
            'balance': incomes - expenses
        })

class BudgetProgressReport(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        today = date.today()
        budgets = Budget.objects.filter(
            user=request.user,
            is_active=True,
            start_date__lte=today,
        )
        
        results = []
        for budget in budgets:
            end_date = budget.end_date if budget.end_date else today
            expenses = Expense.objects.filter(
                user=request.user,
                category=budget.category,
                date__gte=budget.start_date,
                date__lte=end_date
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            progress = (expenses / budget.amount) * 100 if budget.amount > 0 else 0
            
            results.append({
                'budget_id': budget.id,
                'category': budget.category.name,
                'budget_amount': budget.amount,
                'spent_amount': expenses,
                'remaining_amount': budget.amount - expenses,
                'progress_percentage': round(progress, 2),
                'period': budget.period,
                'start_date': budget.start_date,
                'end_date': end_date
            })
        
        return Response(results)