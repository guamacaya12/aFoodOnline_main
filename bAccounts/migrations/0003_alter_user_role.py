# Generated by Django 4.2 on 2023-07-11 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bAccounts', '0002_rename_phone_numner_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'vendor'), (2, 'Customer')], null=True),
        ),
    ]
