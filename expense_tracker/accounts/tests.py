from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_create_user(self):
        """Test user creation with valid data"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), 'testuser')

    def test_create_superuser(self):
        """Test superuser creation"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_email_required(self):
        """Test that email is required"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='noemail',
                email='',
                password='testpass123'
            )

    def test_email_unique(self):
        """Test email uniqueness"""
        User.objects.create_user(**self.user_data)
        with self.assertRaises(Exception):  # IntegrityError
            User.objects.create_user(
                username='testuser2',
                email='test@example.com',
                password='testpass123'
            )

    def test_username_required(self):
        """Test that username is required"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='',
                email='test2@example.com',
                password='testpass123'
            )


class UserProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile
        
        # Sample image for testing
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'simple image content',
            content_type='image/jpeg'
        )

    def test_profile_creation_via_signal(self):
        """Test profile is automatically created via signal"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(str(self.profile), "testuser's Profile")

    def test_default_profile_values(self):
        """Test default profile values"""
        self.assertEqual(self.profile.currency, 'USD')
        self.assertEqual(self.profile.monthly_budget, 0)
        self.assertIsNone(self.profile.profile_picture)

    def test_currency_choices(self):
        """Test valid currency choices"""
        valid_currencies = [choice[0] for choice in UserProfile.CURRENCY_CHOICES]
        self.assertIn(self.profile.currency, valid_currencies)

        # Test invalid currency
        with self.assertRaises(ValidationError):
            self.profile.currency = 'XYZ'
            self.profile.full_clean()

    def test_monthly_budget_validation(self):
        """Test monthly budget validation"""
        # Test negative budget
        with self.assertRaises(ValidationError):
            self.profile.monthly_budget = -100
            self.profile.full_clean()

        # Test valid budget
        self.profile.monthly_budget = 1000.50
        self.profile.full_clean()
        self.assertEqual(self.profile.monthly_budget, 1000.50)

    def test_profile_picture_upload(self):
        """Test profile picture upload"""
        self.profile.profile_picture = self.test_image
        self.profile.save()
        
        self.assertTrue(self.profile.profile_picture)
        self.assertIn('test_image', self.profile.profile_picture.name)

    def test_profile_update_via_signal(self):
        """Test profile is updated when user is saved"""
        new_username = 'updateduser'
        self.user.username = new_username
        self.user.save()
        
        self.profile.refresh_from_db()
        self.assertEqual(str(self.profile), f"{new_username}'s Profile")

    def test_one_to_one_relationship(self):
        """Test one-to-one relationship between User and UserProfile"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.user.profile, self.profile)

        # Test you can't create another profile for the same user
        with self.assertRaises(Exception):  # IntegrityError
            UserProfile.objects.create(user=self.user)


class UserProfileSignalTests(TestCase):
    def test_profile_creation_signal(self):
        """Test profile is created when new user is created"""
        user_count = User.objects.count()
        profile_count = UserProfile.objects.count()
        
        new_user = User.objects.create_user(
            username='signaluser',
            email='signal@example.com',
            password='testpass123'
        )
        
        # Verify counts increased and profile exists
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertEqual(UserProfile.objects.count(), profile_count + 1)
        self.assertTrue(hasattr(new_user, 'profile'))

    def test_profile_update_signal(self):
        """Test profile is saved when user is updated"""
        user = User.objects.create_user(
            username='originuser',
            email='original@example.com',
            password='testpass123'
        )
        
        # Change username and save
        original_profile_updated = user.profile.updated_at
        user.username = 'updateduser'
        user.save()
        
        # Verify profile was updated
        user.profile.refresh_from_db()
        self.assertNotEqual(user.profile.updated_at, original_profile_updated)