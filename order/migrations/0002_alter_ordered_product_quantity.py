# Generated by Django 4.2.1 on 2023-07-06 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordered_product',
            name='quantity',
            field=models.BigIntegerField(null=True),
        ),
    ]
