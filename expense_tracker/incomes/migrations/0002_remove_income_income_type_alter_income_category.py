# Generated by Django 5.1.7 on 2025-03-27 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incomes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='income',
            name='income_type',
        ),
        migrations.AlterField(
            model_name='income',
            name='category',
            field=models.CharField(choices=[('SALARY', 'Salary'), ('FREELANCE', 'Freelance'), ('INVESTMENT', 'Investment'), ('GIFT', 'Gift'), ('OTHER', 'Other')], default='SALARY', max_length=20),
        ),
    ]
