from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ReportPreset
from .serializers import ReportPresetSerializer
from expenses.models import Expense
from incomes.models import Income
from budgets.models import Budget
from django.db.models import Sum, Q
from datetime import date, timedelta
from django.views import View
from django.utils import timezone

class ReportPresetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows report presets to be viewed or edited.
    """
    queryset = ReportPreset.objects.all()
    serializer_class = ReportPresetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

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
        ).values('category').annotate(total=Sum('amount')).order_by('-total')
        
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
                'category': budget.get_category_display(),
                'budget_amount': budget.amount,
                'spent_amount': expenses,
                'remaining_amount': budget.amount - expenses,
                'progress_percentage': round(progress, 2),
                'period': budget.period,
                'start_date': budget.start_date,
                'end_date': end_date
            })
        
        return Response(results)

class ReportDashboardView(View):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Get default report data
        today = timezone.now().date()
        
        # 1. Spending by Category (last 30 days)
        category_spending = Expense.objects.filter(
            user=request.user,
            date__gte=today - timedelta(days=30)
        ).values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')[:5]
        
        # 2. Income vs Expense (current month)
        current_month_start = today.replace(day=1)
        income_expense_data = {
            'income': Income.objects.filter(
                user=request.user,
                date__gte=current_month_start
            ).aggregate(total=Sum('amount'))['total'] or 0,
            'expense': Expense.objects.filter(
                user=request.user,
                date__gte=current_month_start
            ).aggregate(total=Sum('amount'))['total'] or 0,
        }
        
        # 3. Budget Progress (active budgets)
        active_budgets = Budget.objects.filter(
            Q(user=request.user) &
            Q(start_date__lte=today) &
            (Q(end_date__gte=today) | Q(end_date__isnull=True))
        )
        
        budget_progress = []
        for budget in active_budgets:
            spent = Expense.objects.filter(
                user=request.user,
                category=budget.category,
                date__gte=budget.start_date,
                date__lte=budget.end_date if budget.end_date else today
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            progress = (spent / budget.amount) * 100 if budget.amount > 0 else 0
            
            budget_progress.append({
                'category': budget.get_category_display(),
                'budget': budget.amount,
                'spent': spent,
                'remaining': budget.amount - spent,
                'progress': round(progress, 1),
                'is_over': spent > budget.amount
            })
        
        # 4. Recent reports
        recent_reports = ReportPreset.objects.filter(
            user=request.user
        ).order_by('-updated_at')[:3]
        
        context = {
            'category_spending': category_spending,
            'income_expense': income_expense_data,
            'budget_progress': budget_progress,
            'recent_reports': recent_reports,
            'current_month': current_month_start.strftime('%B %Y'),
            'last_30_days': (today - timedelta(days=30)).strftime('%b %d') + " - " + today.strftime('%b %d')
        }
        
        return render(request, 'reports/dashboard.html', context)