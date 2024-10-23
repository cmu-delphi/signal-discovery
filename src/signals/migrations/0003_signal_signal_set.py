# Generated by Django 5.0.7 on 2024-10-11 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signal_sets', '0010_rename_available_geography_signalset_available_geographies_and_more'),
        ('signals', '0002_auto_20241002_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='signal',
            name='signal_set',
            field=models.ForeignKey(blank=True, help_text='Signal Set', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='signals', to='signal_sets.signalset'),
        ),
    ]
