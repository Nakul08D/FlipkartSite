# Generated by Django 5.0 on 2023-12-22 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_product_category_seller_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller_product',
            name='img',
            field=models.ImageField(default=1, upload_to='media/'),
            preserve_default=False,
        ),
    ]
