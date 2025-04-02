from rest_framework import serializers
from .models import Expense, Category
from budgets.models import Budget 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Auto-assigns the logged-in user
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    budget = serializers.PrimaryKeyRelatedField(  # Add this field
        queryset=Budget.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'category', 'category_id',
            'budget', 'description', 'date', 'created_at', 'updated_at'
        ]

    def validate(self, data):
        # Validate that budget category matches expense category if budget is set
        if data.get('budget') and data['budget'].category != data['category']:
            raise serializers.ValidationError(
                "Expense category must match budget category"
            )
        return data