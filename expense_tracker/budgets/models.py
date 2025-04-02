from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum

class Budget(models.Model):
    BUDGET_CATEGORIES = [
        ('RENT', 'Rent'),
        ('FOOD', 'Food'),
        ('GROCERIES', 'Groceries'),
        ('TRANSPORTATION', 'Transportation'),
        ('UTILITIES', 'Utilities'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('HEALTHCARE', 'Healthcare'),
        ('DEBT', 'Debt Repayment'),
        ('SAVINGS', 'Savings & Investments'),
        ('EDUCATION', 'Education'),
        ('OTHER', 'Other'),
        ('RENT', 'Rent'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=BUDGET_CATEGORIES, default='FOOD')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = 'Budgets'
    
    def __str__(self):
        return f"{self.get_category_display()} Budget (${self.amount}) for {self.user.username}"
    
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs validation before saving
        super().save(*args, **kwargs)

    @property
    def spent_amount(self):
        return self.expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    @property
    def remaining_amount(self):
        return self.amount - self.spent_amount
    
    @property
    def progress_percentage(self):
        return (self.spent_amount / self.amount) * 100 if self.amount > 0 else 0