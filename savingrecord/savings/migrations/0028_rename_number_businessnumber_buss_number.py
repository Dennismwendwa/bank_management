# Generated by Django 4.2.2 on 2023-07-12 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0027_company_admin_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='businessnumber',
            old_name='number',
            new_name='buss_number',
        ),
    ]
