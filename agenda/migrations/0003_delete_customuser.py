# Generated by Django 5.2.1 on 2025-05-19 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0002_visit_created_at_visit_updated_at_customuser_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
