from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Income
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .serializers import IncomeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.mixins import LoginRequiredMixin

class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'category', 'date']
    ordering_fields = ['amount', 'date']
    search_fields = ['source', 'description', 'category__name']

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IncomeListView(ListView):
    model = Income
    template_name = 'incomes/list.html'
    context_object_name = 'incomes'


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    fields = ['amount', 'category', 'source', 'date', 'description']
    template_name = 'incomes/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('income_list')  # Replace with your URL for income list page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Income.INCOME_CATEGORIES  # Add income categories to the context
        return context

class IncomeDetailView(DetailView):
    model = Income
    template_name = 'incomes/detail.html'
    context_object_name = 'income'
