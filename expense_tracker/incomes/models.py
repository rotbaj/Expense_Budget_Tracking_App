from django.db import models
from django.contrib.auth.models import User
from expenses.models import Category 

class Income(models.Model):
    INCOME_TYPES = [
        ('SALARY', 'Salary'),
        ('FREELANCE', 'Freelance'),
        ('INVESTMENT', 'Investment'),
        ('GIFT', 'Gift'),
        ('OTHER', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    income_type = models.CharField(max_length=20, choices=INCOME_TYPES)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    source = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Incomes'

    def __str__(self):
        return f"{self.user.username} - {self.income_type} - ${self.amount}"