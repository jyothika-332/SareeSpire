# Generated by Django 4.2.1 on 2023-07-06 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discount',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='minimum_purchase',
            field=models.BigIntegerField(null=True),
        ),
    ]
