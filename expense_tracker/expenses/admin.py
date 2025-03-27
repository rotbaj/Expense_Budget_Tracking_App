from django.contrib import admin
from .models import Expense, Category
from django.db.models import Count

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'expense_count')
    search_fields = ('name', 'description')
    list_per_page = 20
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(expense_count=Count("expense"))

    def expense_count(self, obj):
        return obj.expense_set.count()
    expense_count.short_description = '# Expenses'

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'date', 'short_description')
    list_filter = ('category', 'date', 'user')
    search_fields = ('description', 'category__name', 'user__username')
    date_hierarchy = 'date'
    list_select_related = ('user', 'category')
    list_per_page = 50
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'category', 'amount')
        }),
        ('Details', {
            'fields': ('date', 'description'),
            'classes': ('collapse',)
        }),
    )
    
    def short_description(self, obj):
        return obj.description[:50] + '...' if obj.description else ''
    short_description.short_description = 'Description'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)