from django import forms
from .models import Expense
from budgets.models import Budget

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'budget', 'description', 'date']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filter budgets to only show relevant ones for the user
            self.fields['budget'].queryset = Budget.objects.filter(user=user)
            
            # Set budget choices based on selected category
            if 'category' in self.data:
                try:
                    category = self.data.get('category')
                    self.fields['budget'].queryset = Budget.objects.filter(
                        user=user,
                        category=category
                    )
                except (ValueError, TypeError):
                    pass