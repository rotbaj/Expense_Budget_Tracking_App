"""
URL configuration for expense_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from rest_framework import permissions

# Swagger/OpenAPI configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Expense Tracker API",
        default_version='v1',
        description="API for personal finance tracking",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@expensetracker.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expenses/', include('expenses.urls')),
    path('incomes/', include('incomes.urls')), 
    path('budgets/', include('budgets.urls')), 
    path('accounts/', include('accounts.urls')), 

        # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Authentication
    path('api/auth/', include('accounts.urls')),
    
    # Apps
    path('api/accounts/', include('accounts.urls')),  # Authentication & User management
    path('api/budgets/', include('budgets.urls')),  # Budget management
    path('api/expenses/', include('expenses.urls')),  # Expense tracking
    path('api/incomes/', include('incomes.urls')),  # Income tracking
    path('api/reports/', include('reports.urls')),  # Reports & Analytics
    
    # Frontend
    path('', include('frontend.urls')),
]

# # Serve static files in development
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Custom error handlers
# handler400 = 'frontend.views.error_400'
# handler403 = 'frontend.views.error_403'
# handler404 = 'frontend.views.error_404'
# handler500 = 'frontend.views.error_500'