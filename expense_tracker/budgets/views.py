from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Budget
from .serializers import BudgetSerializer


# DRF ViewSet for API
class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'start_date']
    ordering_fields = ['amount', 'start_date']
    search_fields = ['category']
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# API List View
class BudgetListAPIView(generics.ListAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Budget.objects.filter(user=self.request.user)
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset


# Django Class-based Views for Templates
class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'budgets/list.html' 
    context_object_name = 'budgets'
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    fields = ['amount', 'category', 'start_date', 'end_date', 'description']
    template_name = 'budgets/form.html'
    success_url = reverse_lazy('budget_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Budget created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = dict(Budget.BUDGET_CATEGORIES)
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget.attrs.update({'class': 'datepicker'})
        form.fields['end_date'].widget.attrs.update({'class': 'datepicker'})
        return form

class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    fields = ['amount', 'category', 'start_date', 'end_date', 'description']
    template_name = "budgets/form.html"
    success_url = reverse_lazy("budget_list")
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Budget updated successfully!')
        return super().form_valid(form)


class BudgetDetailView(LoginRequiredMixin, DetailView):
    model = Budget
    template_name = 'budgets/detail.html'
    context_object_name = 'budget'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budget = self.get_object()
        budget.update_spent_amount() 
        context['expenses'] = self.object.expenses.all()
        context['spent_amount'] = budget.spent_amount()
        context['remaining_amount'] = budget.remaining_amount()
        context['progress_percentage'] = budget.progress_percentage()
        return context

@login_required
def toggle_budget_status(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    budget.is_active = not budget.is_active
    budget.save()
    messages.success(request, f"Budget '{budget.category}' is now {'Active' if budget.is_active else 'Inactive'}.")
    return redirect('budget_list')  