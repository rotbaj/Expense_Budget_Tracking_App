from rest_framework import serializers
from .models import ReportPreset

class ReportPresetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportPreset
        fields = ['id', 'name', 'report_type', 'parameters', 'created_at', 'updated_at']

    def validate_parameters(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Parameters must be a JSON object")
        return value