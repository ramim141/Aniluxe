# Generated by Django 5.0.4 on 2024-09-10 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='popularity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
