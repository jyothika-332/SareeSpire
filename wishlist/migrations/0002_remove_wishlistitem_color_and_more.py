# Generated by Django 4.2.1 on 2023-06-13 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlistitem',
            name='color',
        ),
        migrations.RemoveField(
            model_name='wishlistitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='wishlistitem',
            name='wishlist',
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
        migrations.DeleteModel(
            name='WishlistItem',
        ),
    ]
