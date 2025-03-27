from rest_framework import serializers
from .models import Expense, Category

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

    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'category', 'category_id',
            'description', 'date', 'created_at', 'updated_at'
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return value