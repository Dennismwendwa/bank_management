# Generated by Django 4.2.2 on 2023-06-20 07:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('savings', '0011_statements_amount_statements_transaction_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saving_account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=50, unique=True)),
                ('deposit', models.DecimalField(decimal_places=4, max_digits=12)),
                ('account_balance', models.DecimalField(decimal_places=4, max_digits=12)),
                ('account_type', models.CharField(max_length=100)),
                ('transaction_count', models.CharField(default=0, max_length=100)),
                ('opening_date', models.DateTimeField()),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Saving_account_statements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=12)),
                ('transaction_date', models.DateTimeField()),
                ('account_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings.saving_account')),
            ],
        ),
    ]