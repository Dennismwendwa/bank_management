# Generated by Django 4.2.2 on 2023-07-06 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0020_agents'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agents',
            old_name='registed_on',
            new_name='registered_on',
        ),
    ]
