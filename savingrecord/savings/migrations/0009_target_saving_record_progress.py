# Generated by Django 4.2.1 on 2023-06-13 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0008_target_saving_record_balence_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='target_saving_record',
            name='progress',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
