# Generated by Django 5.2.3 on 2025-07-25 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_master_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='master',
            name='reviews',
        ),
    ]
