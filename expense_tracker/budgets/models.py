from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Budget(models.Model):
    BUDGET_CATEGORIES = [
        ('FOOD', 'Food'),
        ('TRANSPORT', 'Transport'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('UTILITIES', 'Utilities'),
        ('OTHERS', 'Others'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=BUDGET_CATEGORIES, default='FOOD')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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