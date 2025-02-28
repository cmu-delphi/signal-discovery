# Generated by Django 5.0.7 on 2024-10-07 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signal_sets', '0001_initial'),
        ('signals', '0002_auto_20241002_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signalset',
            name='severity_pyramid_rungs',
            field=models.ManyToManyField(blank=True, help_text='Severity pyramid rungs of the signal set.', related_name='signal_sets', to='signals.severitypyramidrung'),
        ),
    ]
