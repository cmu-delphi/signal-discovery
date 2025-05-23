# Generated by Django 5.0.7 on 2024-10-08 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signal_sets', '0003_alter_signalset_data_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signalset',
            name='data_source',
            field=models.CharField(blank=True, max_length=255, verbose_name='Data Source'),
        ),
        migrations.AlterField(
            model_name='signalset',
            name='data_type',
            field=models.CharField(blank=True, max_length=255, verbose_name='Data Type'),
        ),
        migrations.AlterField(
            model_name='signalset',
            name='language',
            field=models.CharField(blank=True, max_length=255, verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='signalset',
            name='maintainer_email',
            field=models.CharField(blank=True, max_length=255, verbose_name='Maintainer Email'),
        ),
        migrations.AlterField(
            model_name='signalset',
            name='maintainer_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Maintainer Name'),
        ),
        migrations.AlterField(
            model_name='signalset',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='255'),
        ),
        migrations.AlterField(
            model_name='signalset',
            name='organization',
            field=models.CharField(blank=True, max_length=255, verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='signalset',
            name='origin_datasource',
            field=models.CharField(blank=True, max_length=255, verbose_name='Origin Data Source'),
        ),
        migrations.AlterField(
            model_name='signalset',
            name='preprocessing_description',
            field=models.CharField(blank=True, max_length=255, verbose_name='Preprocessing Description'),
        ),
        migrations.AlterField(
            model_name='signalset',
            name='version_number',
            field=models.CharField(blank=True, max_length=255, verbose_name='Version Number'),
        ),
    ]
