# Generated by Django 3.0.8 on 2021-01-31 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
        ('services', '0026_auto_20210131_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='submissions',
            field=models.ManyToManyField(related_name='contract_submissions', to='employee.Submissions'),
        ),
    ]
