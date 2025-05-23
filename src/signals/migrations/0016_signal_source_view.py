# Generated by Django 5.0.7 on 2025-01-28 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0015_severitypyramidrung_used_in_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE view signals_signal_source_view AS (
                SELECT
                ss.id,
                ss.name as "signal",
                dd.name as "source",
                ss.signal_set_id as "signal_set"
                FROM signals_signal ss
                LEFT JOIN datasources_datasource dd
                ON ss.source_id = dd.id
            )
            """
        )
    ]
