# Generated by Django 4.2.1 on 2023-06-17 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordered_product',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='ordered_product',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Ordered_Product',
        ),
    ]