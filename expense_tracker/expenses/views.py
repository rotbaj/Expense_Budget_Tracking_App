from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Expense, Category
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .serializers import ExpenseSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ExpenseForm

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'date']
    ordering_fields = ['amount', 'date']
    search_fields = ['description', 'category__name']

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).select_related("category")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseListView(ListView):
    model = Expense
    template_name = 'expenses/list.html'
    context_object_name = 'expenses'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Example of passing the reverse URL for the detail view for each expense
        for expense in context['expenses']:
            expense.detail_url = reverse_lazy('expense_detail', kwargs={'pk': expense.pk})
        return context

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save()

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/form.html'
    
    # Automatically set the logged-in user for the expense
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('expense_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Add categories to the context
        return context

    def get_form_kwargs(self):
        # Ensure the user is passed to the form
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ExpenseEditView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    fields = ['amount', 'category', 'description', 'date']
    template_name = 'expenses/form.html'
    
    def form_valid(self, form):
        # Any additional logic can be added here
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('expense_detail', kwargs={'pk': self.object.pk})  
    
class ExpenseDetailView(DetailView):
    model = Expense
    template_name = 'expenses/detail.html'
    context_object_name = 'expense'