from django.db import models
from django.contrib.auth.models import User
from expenses.models import Category
from django.core.exceptions import ValidationError

class Budget(models.Model):
    PERIOD_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('YEARLY', 'Yearly'),
        ('CUSTOM', 'Custom'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='MONTHLY')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        unique_together = ['user', 'category', 'period', 'start_date']

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - ${self.amount}/{self.period.lower()}"

    def clean(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date")