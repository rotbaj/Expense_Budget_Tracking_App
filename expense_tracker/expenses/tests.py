from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from budgets.models import Budget
from .models import Category, Expense

User = get_user_model()

class CategoryModelTests(TestCase):
    def setUp(self):
        self.category_data = {
            'name': 'FOOD',
            'description': 'All food-related expenses'
        }

    def test_create_category(self):
        """Test category creation with valid data"""
        category = Category.objects.create(**self.category_data)
        self.assertEqual(category.name, 'FOOD')
        self.assertEqual(category.get_name_display(), 'Food')
        self.assertEqual(str(category), 'Food')

    def test_category_unique_name(self):
        """Test that category names must be unique"""
        Category.objects.create(**self.category_data)
        with self.assertRaises(Exception):
            Category.objects.create(**self.category_data)

    def test_invalid_category_name(self):
        """Test invalid category name raises error"""
        with self.assertRaises(ValidationError):
            category = Category(name='INVALID', description='Invalid category')
            category.full_clean()

    def test_category_choices(self):
        """Test all category choices are valid"""
        valid_choices = [choice[0] for choice in Category.EXPENSE_CATEGORIES]
        category = Category(name='RENT')
        self.assertIn(category.name, valid_choices)


class ExpenseModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.budget = Budget.objects.create(
            user=self.user,
            amount=1000.00,
            category='FOOD',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30)
        )
        
        self.expense_data = {
            'user': self.user,
            'amount': 100.00,
            'category': 'FOOD',
            'description': 'Weekly groceries',
            'date': timezone.now().date()
        }

    def test_create_expense(self):
        """Test expense creation with valid data"""
        expense = Expense.objects.create(**self.expense_data)
        self.assertEqual(expense.amount, 100.00)
        self.assertEqual(expense.category, 'FOOD')
        self.assertEqual(expense.user, self.user)
        self.assertEqual(str(expense), f"{self.user.username} - FOOD - $100.00")

    def test_expense_with_budget(self):
        """Test expense with budget association"""
        expense = Expense.objects.create(budget=self.budget, **self.expense_data)
        self.assertEqual(expense.budget, self.budget)
        self.assertEqual(str(expense), f"{self.user.username} - FOOD (Budget: {self.budget}) - $100.00")

    def test_expense_ordering(self):
        """Test expenses are ordered by date descending"""
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        expense1 = Expense.objects.create(date=today, **self.expense_data)
        expense2 = Expense.objects.create(date=yesterday, **self.expense_data)
        
        expenses = Expense.objects.all()
        self.assertEqual(expenses[0], expense1)
        self.assertEqual(expenses[1], expense2)

    def test_auto_budget_assignment(self):
        """Test budget is auto-assigned when matching category and date"""
        expense = Expense.objects.create(**self.expense_data)
        expense.save()  # Trigger auto-assignment
        
        # Refresh from db
        expense.refresh_from_db()
        self.assertEqual(expense.budget, self.budget)

    def test_no_auto_budget_when_outside_date_range(self):
        """Test budget not assigned when expense date is outside budget period"""
        future_date = timezone.now().date() + timedelta(days=31)
        expense = Expense.objects.create(date=future_date, **self.expense_data)
        expense.save()
        
        expense.refresh_from_db()
        self.assertIsNone(expense.budget)

    def test_no_auto_budget_when_category_mismatch(self):
        """Test budget not assigned when category doesn't match"""
        expense_data = self.expense_data.copy()
        expense_data['category'] = 'RENT'
        expense = Expense.objects.create(**expense_data)
        expense.save()
        
        expense.refresh_from_db()
        self.assertIsNone(expense.budget)

    def test_budget_update_on_expense_save(self):
        """Test budget's spent amount updates when expense is saved"""
        # Initial budget should have 0 spent
        self.assertEqual(self.budget.spent_amount, 0)
        
        # Create expense that matches budget
        expense = Expense.objects.create(**self.expense_data)
        expense.save()
        
        # Refresh budget from db
        self.budget.refresh_from_db()
        self.assertEqual(self.budget.spent_amount, 100.00)

    def test_expense_amount_validation(self):
        """Test expense amount must be positive"""
        with self.assertRaises(ValidationError):
            expense = Expense(amount=-100.00, **self.expense_data)
            expense.full_clean()

    def test_expense_date_not_in_future(self):
        """Test expense date cannot be in the future"""
        future_date = timezone.now().date() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            expense = Expense(date=future_date, **self.expense_data)
            expense.full_clean()