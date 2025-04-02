from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('currency', 'monthly_budget', 'profile_picture')


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_staff', 
        'get_currency',
        'get_monthly_budget'
    )
    list_select_related = ('profile',)

    def get_currency(self, instance):
        return instance.profile.currency
    get_currency.short_description = 'Currency'

    def get_monthly_budget(self, instance):
        return instance.profile.monthly_budget
    get_monthly_budget.short_description = 'Monthly Budget'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'monthly_budget')
    search_fields = ('user__username', 'user__email')
    raw_id_fields = ('user',)
    list_per_page = 20

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Preferences', {
            'fields': ('currency', 'monthly_budget')
        }),
        ('Profile', {
            'fields': ('profile_picture',),
            'classes': ('collapse',)
        }),
    )


# Register the custom User model
admin.site.register(User, CustomUserAdmin)