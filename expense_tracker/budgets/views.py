from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Budget
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .serializers import BudgetSerializer
from django_filters.rest_framework import DjangoFilterBackend

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'period', 'is_active']
    ordering_fields = ['amount', 'start_date']
    search_fields = ['category__name']

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetListView(ListView):
    model = Budget
    template_name = 'budgets/list.html' 
    context_object_name = 'budgets'

class BudgetCreateView(CreateView):
    model = Budget
    template_name = "budgets/form.html"
    fields = ['user', 'amount', 'category', 'period', 'start_date', 'end_date'] 
    success_url = reverse_lazy('budget_list') 

class BudgetUpdateView(UpdateView):
    model = Budget
    fields = ['category', 'amount', 'period', 'start_date', 'end_date']
    template_name = "budgets/budget_form.html"
    success_url = reverse_lazy("budget_list")

class BudgetDeleteView(DeleteView):
    model = Budget
    template_name = "budgets/budget_confirm_delete.html"
    success_url = reverse_lazy("budget_list")

class BudgetDetailView(DetailView):
    model = Budget
    template_name = "budgets/budget_detail.html"