# Generated by Django 5.1.11 on 2025-06-22 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
