# Generated by Django 5.1.7 on 2025-03-27 14:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0002_alter_budget_options_alter_budget_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='budget',
            options={'ordering': ['-start_date'], 'verbose_name_plural': 'Budgets'},
        ),
        migrations.AlterField(
            model_name='budget',
            name='category',
            field=models.CharField(choices=[('FOOD', 'Food'), ('TRANSPORT', 'Transport'), ('ENTERTAINMENT', 'Entertainment'), ('UTILITIES', 'Utilities'), ('OTHERS', 'Others')], default='FOOD', max_length=20),
        ),
        migrations.AlterField(
            model_name='budget',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='budget',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
