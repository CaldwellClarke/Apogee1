# Generated by Django 2.0.1 on 2018-06-07 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userstatistics', '0004_statisticsinfo_max_profit_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statisticsinfo',
            name='max_profit_event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parties.Party'),
        ),
    ]
