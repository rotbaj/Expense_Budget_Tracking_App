from rest_framework import serializers
from .models import Income
from expenses.serializers import CategorySerializer

class IncomeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Income
        fields = [
            'id', 'amount', 'income_type', 'category', 'category_id',
            'source', 'date', 'description', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'amount': {'min_value': 0.01}
        }

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return data