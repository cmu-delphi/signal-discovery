# Generated by Django 5.0.7 on 2025-01-16 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0011_geographicscope_used_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geographicscope',
            name='name',
            field=models.CharField(help_text='Name of the geographic scope.', max_length=255, verbose_name='name'),
        ),
    ]
