# Generated by Django 4.2.2 on 2023-07-13 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_admin',
            new_name='is_account_staff',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_employee',
            field=models.BooleanField(default=False, verbose_name='Is employee'),
        ),
    ]