# Generated by Django 5.1.7 on 2025-04-02 10:02

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(choices=[('FOOD', 'Food'), ('TRANSPORT', 'Transport'), ('ENTERTAINMENT', 'Entertainment'), ('UTILITIES', 'Utilities'), ('OTHERS', 'Others')], default='FOOD', max_length=20)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Budgets',
                'ordering': ['-start_date'],
            },
        ),
    ]
