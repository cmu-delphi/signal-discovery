# Generated by Django 5.0.7 on 2024-10-13 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signal_sets', '0010_rename_available_geography_signalset_available_geographies_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='signalset',
            old_name='geographic_granulalarity',
            new_name='geographic_granularity',
        ),
    ]
