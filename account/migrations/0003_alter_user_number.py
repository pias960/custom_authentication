# Generated by Django 5.1.4 on 2025-01-14 14:27

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='number',
            field=models.IntegerField(blank=True, validators=[account.models.maxnum]),
        ),
    ]
