# Generated by Django 3.0.8 on 2020-12-10 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_attachment_attachmentonly'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='attachmentOnly',
        ),
    ]