# Generated by Django 4.2.6 on 2024-03-03 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='added_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.customer'),
        ),
    ]
