# Generated by Django 4.2.2 on 2023-07-12 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0026_company_approved_alter_company_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='admin_review',
            field=models.BooleanField(default=False),
        ),
    ]
