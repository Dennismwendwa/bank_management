# Generated by Django 4.2.1 on 2023-06-12 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0004_saving_record'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saving_record',
            old_name='account_name',
            new_name='account_number',
        ),
    ]
