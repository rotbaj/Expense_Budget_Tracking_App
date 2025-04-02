from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """Custom user model that extends Django's AbstractUser"""
    email = models.EmailField(unique=True, blank=False, null=False)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('NGN', 'Nigerian Naira'),
    ]

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='USD'
    )
    monthly_budget = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)]
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Signals to automatically create/update UserProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile automatically when a new user is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the profile whenever the user is saved"""
    instance.profile.save()