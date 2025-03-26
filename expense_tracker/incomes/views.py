from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Income
from .serializers import IncomeSerializer
from django_filters.rest_framework import DjangoFilterBackend

class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['income_type', 'category', 'date']
    ordering_fields = ['amount', 'date']
    search_fields = ['source', 'description', 'category__name']

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)