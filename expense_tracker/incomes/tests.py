from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Income

User = get_user_model()

class IncomeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.today = timezone.now().date()
        self.income_data = {
            'user': self.user,
            'amount': 1000.00,
            'category': 'SALARY',
            'source': 'Acme Corp',
            'date': self.today,
            'description': 'Monthly salary'
        }

    def test_create_income(self):
        """Test income creation with valid data"""
        income = Income.objects.create(**self.income_data)
        self.assertEqual(income.amount, 1000.00)
        self.assertEqual(income.category, 'SALARY')
        self.assertEqual(income.source, 'Acme Corp')
        self.assertEqual(income.user, self.user)
        self.assertEqual(str(income), "testuser - $1000.00")
        self.assertEqual(income.description, 'Monthly salary')

    def test_income_ordering(self):
        """Test incomes are ordered by date descending"""
        yesterday = self.today - timedelta(days=1)
        
        income1 = Income.objects.create(
            date=yesterday,
            **self.income_data
        )
        income2 = Income.objects.create(
            date=self.today,
            **self.income_data
        )
        
        incomes = Income.objects.all()
        self.assertEqual(incomes[0], income2)
        self.assertEqual(incomes[1], income1)

    def test_category_choices(self):
        """Test all category choices are valid"""
        valid_choices = [choice[0] for choice in Income.INCOME_CATEGORIES]
        income = Income(**self.income_data)
        self.assertIn(income.category, valid_choices)

    def test_invalid_category(self):
        """Test invalid category raises error"""
        with self.assertRaises(ValidationError):
            income = Income(
                category='INVALID',
                **{k: v for k, v in self.income_data.items() if k != 'category'}
            )
            income.full_clean()

    def test_amount_validation(self):
        """Test amount must be positive"""
        with self.assertRaises(ValidationError):
            income = Income(
                amount=-100.00,
                **{k: v for k, v in self.income_data.items() if k != 'amount'}
            )
            income.full_clean()

    def test_source_required(self):
        """Test source field is required"""
        with self.assertRaises(Exception):
            Income.objects.create(
                source='',
                **{k: v for k, v in self.income_data.items() if k != 'source'}
            )

    def test_date_validation(self):
        """Test date cannot be in the future"""
        future_date = self.today + timedelta(days=1)
        with self.assertRaises(ValidationError):
            income = Income(
                date=future_date,
                **{k: v for k, v in self.income_data.items() if k != 'date'}
            )
            income.full_clean()

    def test_user_relationship(self):
        """Test user foreign key relationship"""
        income = Income.objects.create(**self.income_data)
        self.assertEqual(income.user, self.user)
        
        # Test cascade delete
        user_id = self.user.id
        self.user.delete()
        with self.assertRaises(Income.DoesNotExist):
            Income.objects.get(id=income.id)

    def test_optional_description(self):
        """Test description can be blank"""
        income = Income.objects.create(
            description='',
            **{k: v for k, v in self.income_data.items() if k != 'description'}
        )
        self.assertEqual(income.description, '')

    def test_created_updated_timestamps(self):
        """Test auto-created timestamps"""
        income = Income.objects.create(**self.income_data)
        self.assertIsNotNone(income.created_at)
        self.assertIsNotNone(income.updated_at)
        
        # Test updated_at changes on save
        original_updated = income.updated_at
        income.source = 'New Source'
        income.save()
        self.assertNotEqual(income.updated_at, original_updated)

    def test_verbose_name_plural(self):
        """Test correct plural name"""
        self.assertEqual(Income._meta.verbose_name_plural, 'Incomes')

    def test_max_digits_validation(self):
        """Test amount doesn't exceed max digits"""
        with self.assertRaises(Exception):
            Income.objects.create(
                amount=10000000000.00,  # Exceeds max_digits=10
                **{k: v for k, v in self.income_data.items() if k != 'amount'}
            )

    def test_decimal_places_validation(self):
        """Test decimal places are limited to 2"""
        income = Income.objects.create(
            amount=1000.123,
            **{k: v for k, v in self.income_data.items() if k != 'amount'}
        )
        self.assertEqual(income.amount, 1000.12)  # Should be rounded to 2 decimal places