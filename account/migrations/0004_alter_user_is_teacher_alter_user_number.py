# Generated by Django 5.1.4 on 2025-01-14 14:45

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='number',
            field=models.CharField(blank=True, max_length=11, validators=[account.models.maxnum]),
        ),
    ]
