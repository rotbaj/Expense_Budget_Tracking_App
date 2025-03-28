# Generated by Django 5.1.7 on 2025-03-27 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='budget',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='budget',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='budget',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='category',
            field=models.CharField(choices=[('FOOD', 'Food'), ('TRANSPORT', 'Transport'), ('ENTERTAINMENT', 'Entertainment'), ('UTILITIES', 'Utilities'), ('OTHERS', 'Others')], default='Food', max_length=20),
        ),
        migrations.AlterField(
            model_name='budget',
            name='end_date',
            field=models.DateField(default='2025-12-31'),
        ),
        migrations.RemoveField(
            model_name='budget',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='period',
        ),
    ]
