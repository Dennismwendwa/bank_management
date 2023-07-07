# Generated by Django 4.2.2 on 2023-07-06 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0019_account_total_paybil'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('id_number', models.CharField(max_length=50, unique=True)),
                ('contact_number', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('agent_number', models.CharField(blank=True, max_length=50, null=True)),
                ('registed_on', models.DateField(auto_now_add=True)),
            ],
        ),
    ]