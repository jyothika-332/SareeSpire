# Generated by Django 4.2.1 on 2023-06-15 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_colorvariation_image'),
        ('wishlist', '0005_wishlist_product_delete_wishlistitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='image',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='product.colorvariation'),
            preserve_default=False,
        ),
    ]
