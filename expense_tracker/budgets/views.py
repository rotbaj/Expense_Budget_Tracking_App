from rest_framework import viewsets
from .models import Budget
from .serializers import BudgetSerializer
from rest_framework.permissions import IsAuthenticated

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)