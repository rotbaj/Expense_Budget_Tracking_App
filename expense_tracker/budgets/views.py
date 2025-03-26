from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Budget
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