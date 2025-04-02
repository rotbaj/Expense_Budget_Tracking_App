from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import ReportPreset
import json

User = get_user_model()

class ReportPresetModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.report_data = {
            'user': self.user,
            'name': 'Monthly Spending Report',
            'report_type': 'SPENDING_BY_CATEGORY',
            'parameters': {
                'time_range': 'month',
                'categories': ['FOOD', 'TRANSPORTATION']
            }
        }

    def test_create_report_preset(self):
        """Test report preset creation with valid data"""
        report = ReportPreset.objects.create(**self.report_data)
        self.assertEqual(report.name, 'Monthly Spending Report')
        self.assertEqual(report.report_type, 'SPENDING_BY_CATEGORY')
        self.assertEqual(report.user, self.user)
        self.assertEqual(str(report), "testuser - Monthly Spending Report")
        self.assertEqual(report.parameters['time_range'], 'month')
        self.assertEqual(len(report.parameters['categories']), 2)

    def test_report_type_choices(self):
        """Test all report type choices are valid"""
        valid_choices = [choice[0] for choice in ReportPreset.REPORT_TYPES]
        report = ReportPreset(**self.report_data)
        self.assertIn(report.report_type, valid_choices)

    def test_invalid_report_type(self):
        """Test invalid report type raises error"""
        with self.assertRaises(ValidationError):
            report = ReportPreset(
                user=self.user,
                name='Invalid Report',
                report_type='INVALID_TYPE',
                parameters={}
            )
            report.full_clean()

    def test_parameters_json_field(self):
        """Test JSONField handles different parameter structures"""
        # Test with empty dict
        report1 = ReportPreset.objects.create(
            user=self.user,
            name='Empty Params',
            report_type='CUSTOM',
            parameters={}
        )
        self.assertEqual(report1.parameters, {})
        
        # Test with complex nested structure
        complex_params = {
            'filters': {
                'date_range': {
                    'start': '2023-01-01',
                    'end': '2023-12-31'
                },
                'categories': ['FOOD', 'ENTERTAINMENT'],
                'min_amount': 100
            },
            'group_by': 'month',
            'visualization': 'bar_chart'
        }
        
        report2 = ReportPreset.objects.create(
            user=self.user,
            name='Complex Params',
            report_type='CUSTOM',
            parameters=complex_params
        )
        self.assertEqual(report2.parameters['filters']['date_range']['start'], '2023-01-01')
        self.assertEqual(len(report2.parameters['filters']['categories']), 2)

    def test_ordering_meta(self):
        """Test reports are ordered by created_at descending"""
        report1 = ReportPreset.objects.create(
            name='Report 1',
            report_type='INCOME_VS_EXPENSE',
            user=self.user,
            parameters={}
        )
        
        report2 = ReportPreset.objects.create(
            name='Report 2',
            report_type='BUDGET_PROGRESS',
            user=self.user,
            parameters={}
        )
        
        reports = ReportPreset.objects.all()
        self.assertEqual(reports[0], report2)
        self.assertEqual(reports[1], report1)

    def test_user_relationship(self):
        """Test user foreign key relationship"""
        report = ReportPreset.objects.create(**self.report_data)
        self.assertEqual(report.user, self.user)
        
        # Test cascade delete
        user_id = self.user.id
        self.user.delete()
        with self.assertRaises(ReportPreset.DoesNotExist):
            ReportPreset.objects.get(id=report.id)

    def test_name_max_length(self):
        """Test name field max length constraint"""
        long_name = 'X' * 101
        with self.assertRaises(Exception):
            ReportPreset.objects.create(
                user=self.user,
                name=long_name,
                report_type='SPENDING_BY_CATEGORY',
                parameters={}
            )

    def test_default_parameters(self):
        """Test default parameters value"""
        report = ReportPreset.objects.create(
            user=self.user,
            name='Default Params',
            report_type='CUSTOM'
        )
        self.assertEqual(report.parameters, {})

    def test_updated_at_auto_update(self):
        """Test updated_at field auto-updates on save"""
        report = ReportPreset.objects.create(**self.report_data)
        original_updated = report.updated_at
        
        report.name = 'Updated Name'
        report.save()
        
        report.refresh_from_db()
        self.assertNotEqual(report.updated_at, original_updated)

    def test_string_representation(self):
        """Test string representation of model"""
        report = ReportPreset.objects.create(**self.report_data)
        self.assertEqual(str(report), f"{self.user.username} - {report.name}")