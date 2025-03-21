from django.db import models
from django.contrib.auth.models import User 

# Expense Model
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
    class Meta:
        ordering = ['-date']

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
    class Meta:
        ordering = ['-date']

# # Budget Model
# class Budget(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     start_date = models.DateField()
#     end_date = models.DateField()

#     def __str__(self):
#         return f"{self.category} - {self.amount} (From {self.start_date} to {self.end_date})"