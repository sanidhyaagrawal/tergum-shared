# Generated by Django 3.0.8 on 2020-12-16 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_attachment_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
