# Generated by Django 5.1.11 on 2025-06-21 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='order_id',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='product_id',
            new_name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
