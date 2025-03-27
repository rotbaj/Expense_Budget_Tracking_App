from django.db import models
from django.contrib.auth.models import User

class Income(models.Model):
    INCOME_CATEGORIES = [
        ('SALARY', 'Salary'),
        ('FREELANCE', 'Freelance'),
        ('INVESTMENT', 'Investment'),
        ('GIFT', 'Gift'),
        ('OTHER', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=INCOME_CATEGORIES, default='SALARY') 
    source = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Incomes'

    def __str__(self):
        return f"{self.user.username} - ${self.amount}"