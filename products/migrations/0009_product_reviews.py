# Generated by Django 5.0.4 on 2024-09-12 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_review_body_alter_review_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reviews',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.review'),
        ),
    ]
