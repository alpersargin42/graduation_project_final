# Generated by Django 4.2.6 on 2024-05-27 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_message'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]