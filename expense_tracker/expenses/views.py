from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Expense, Category
from django.views.generic import ListView, CreateView
from .serializers import ExpenseSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse_lazy

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

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save()

class ExpenseCreateView(CreateView):
    model = Expense
    template_name = "expenses/form.html"
    fields = ['user', 'amount', 'category', 'description', 'date'] 
    success_url = reverse_lazy('expense_list') 