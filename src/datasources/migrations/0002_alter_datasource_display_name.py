# Generated by Django 5.0.7 on 2024-10-15 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasource',
            name='display_name',
            field=models.CharField(blank=True, max_length=128, verbose_name='Display Name'),
        ),
    ]