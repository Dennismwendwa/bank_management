# Generated by Django 4.2.1 on 2023-06-05 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='job',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
