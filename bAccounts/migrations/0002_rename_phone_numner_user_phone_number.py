# Generated by Django 4.2 on 2023-06-01 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bAccounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phone_numner',
            new_name='phone_number',
        ),
    ]
