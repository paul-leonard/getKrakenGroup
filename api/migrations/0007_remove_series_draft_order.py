# Generated by Django 3.1.5 on 2021-01-21 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_merge_20210121_0522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='series',
            name='draft_order',
        ),
    ]
