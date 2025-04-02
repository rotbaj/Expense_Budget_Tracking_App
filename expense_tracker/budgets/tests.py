from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Budget
from expenses.models import Expense

User = get_user_model()

class BudgetModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.today = timezone.now().date()
        self.next_month = self.today + timedelta(days=30)
        
        self.budget_data = {
            'user': self.user,
            'amount': 1000.00,
            'category': 'FOOD',
            'start_date': self.today,
            'end_date': self.next_month,
            'description': 'Monthly food budget'
        }

    def test_create_budget(self):
        """Test budget creation with valid data"""
        budget = Budget.objects.create(**self.budget_data)
        self.assertEqual(budget.amount, 1000.00)
        self.assertEqual(budget.category, 'FOOD')
        self.assertEqual(budget.user, self.user)
        self.assertTrue(budget.is_active)
        self.assertEqual(str(budget), "Food Budget ($1000.00) for testuser")

    def test_budget_ordering(self):
        """Test budgets are ordered by start_date descending"""
        budget1 = Budget.objects.create(
            start_date=self.today - timedelta(days=10),
            end_date=self.next_month - timedelta(days=10),
            **self.budget_data
        )
        budget2 = Budget.objects.create(**self.budget_data)
        
        budgets = Budget.objects.all()
        self.assertEqual(budgets[0], budget2)
        self.assertEqual(budgets[1], budget1)

    def test_date_validation(self):
        """Test end date cannot be before start date"""
        with self.assertRaises(ValidationError):
            budget = Budget(
                start_date=self.today,
                end_date=self.today - timedelta(days=1),
                **self.budget_data
            )
            budget.full_clean()

    def test_category_choices(self):
        """Test all category choices are valid"""
        valid_choices = [choice[0] for choice in Budget.BUDGET_CATEGORIES]
        budget = Budget(**self.budget_data)
        self.assertIn(budget.category, valid_choices)

    def test_spent_amount_property(self):
        """Test spent_amount calculation"""
        budget = Budget.objects.create(**self.budget_data)
        
        # No expenses yet
        self.assertEqual(budget.spent_amount, 0)
        
        # Add expenses
        Expense.objects.create(
            user=self.user,
            amount=100.00,
            category='FOOD',
            budget=budget,
            date=self.today
        )
        Expense.objects.create(
            user=self.user,
            amount=200.00,
            category='FOOD',
            budget=budget,
            date=self.today
        )
        
        # Refresh from db and test
        budget.refresh_from_db()
        self.assertEqual(budget.spent_amount, 300.00)

    def test_remaining_amount_property(self):
        """Test remaining_amount calculation"""
        budget = Budget.objects.create(amount=500.00, **self.budget_data)
        
        # Initial remaining amount
        self.assertEqual(budget.remaining_amount, 500.00)
        
        # Add expense
        Expense.objects.create(
            user=self.user,
            amount=150.00,
            category='FOOD',
            budget=budget,
            date=self.today
        )
        
        # Test remaining amount
        budget.refresh_from_db()
        self.assertEqual(budget.remaining_amount, 350.00)

    def test_progress_percentage_property(self):
        """Test progress_percentage calculation"""
        budget = Budget.objects.create(amount=200.00, **self.budget_data)
        
        # 0% progress initially
        self.assertEqual(budget.progress_percentage, 0)
        
        # 50% progress
        Expense.objects.create(
            user=self.user,
            amount=100.00,
            category='FOOD',
            budget=budget,
            date=self.today
        )
        budget.refresh_from_db()
        self.assertEqual(budget.progress_percentage, 50)
        
        # 100% progress
        Expense.objects.create(
            user=self.user,
            amount=100.00,
            category='FOOD',
            budget=budget,
            date=self.today
        )
        budget.refresh_from_db()
        self.assertEqual(budget.progress_percentage, 100)
        
        # Test division by zero protection
        zero_budget = Budget.objects.create(amount=0, **self.budget_data)
        self.assertEqual(zero_budget.progress_percentage, 0)

    def test_update_spent_amount(self):
        """Test update_spent_amount property triggers save"""
        budget = Budget.objects.create(**self.budget_data)
        original_updated = budget.updated_at
        
        # Add expense and update
        Expense.objects.create(
            user=self.user,
            amount=50.00,
            category='FOOD',
            budget=budget,
            date=self.today
        )
        budget.update_spent_amount
        
        # Verify updated_at changed
        budget.refresh_from_db()
        self.assertNotEqual(budget.updated_at, original_updated)
        self.assertEqual(budget.spent_amount, 50.00)

    def test_active_budget_filtering(self):
        """Test is_active field works correctly"""
        active_budget = Budget.objects.create(**self.budget_data)
        inactive_budget = Budget.objects.create(
            is_active=False,
            **self.budget_data
        )
        
        active_budgets = Budget.objects.filter(is_active=True)
        self.assertIn(active_budget, active_budgets)
        self.assertNotIn(inactive_budget, active_budgets)

    def test_duplicate_category_handling(self):
        """Test handling of duplicate category entries"""
        # Note: 'RENT' appears twice in BUDGET_CATEGORIES
        budget = Budget.objects.create(
            category='RENT',
            **self.budget_data
        )
        self.assertEqual(budget.get_category_display(), 'Rent')