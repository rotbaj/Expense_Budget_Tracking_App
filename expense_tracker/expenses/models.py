from django.db import models
from django.conf import settings
from budgets.models import Budget

class Category(models.Model):
    EXPENSE_CATEGORIES = [
        ('RENT', 'Rent'),
        ('GROCERIES', 'Groceries'),
        ('TRANSPORTATION', 'Transportation'),
        ('UTILITIES', 'Utilities'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('HEALTHCARE', 'Healthcare'),
        ('DEBT', 'Debt Repayment'),
        ('SAVINGS', 'Savings & Investments'),
        ('EDUCATION', 'Education'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True, choices=EXPENSE_CATEGORIES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=Category.EXPENSE_CATEGORIES)
    budget = models.ForeignKey( 
        Budget, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='expenses'
    )
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        budget_info = f" (Budget: {self.budget})" if self.budget else ""
        return f"{self.user.username} - {self.category}{budget_info} - ${self.amount}"

    def save(self, *args, **kwargs):
        # Auto-assign budget if category matches and date is within budget period
        if not self.budget and self.category:
            matching_budget = Budget.objects.filter(
                user=self.user,
                category=self.category,
                start_date__lte=self.date,
                end_date__gte=self.date
            ).first()
            if matching_budget:
                self.budget = matching_budget
        super().save(*args, **kwargs)