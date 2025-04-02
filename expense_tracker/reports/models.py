from django.db import models
from django.conf import settings

class ReportPreset(models.Model):
    REPORT_TYPES = [
        ('SPENDING_BY_CATEGORY', 'Spending by Category'),
        ('INCOME_VS_EXPENSE', 'Income vs Expense'),
        ('BUDGET_PROGRESS', 'Budget Progress'),
        ('CUSTOM', 'Custom'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    parameters = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"