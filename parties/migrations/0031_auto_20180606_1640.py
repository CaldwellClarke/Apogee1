# Generated by Django 2.0.1 on 2018-06-06 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0030_auto_20180525_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='max_entrants',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(None, 'Unlimited'), (3, 3), (10, 10), (25, 25), (50, 50), (100, 100), (500, 500), (1000, 1000)], null=True),
        ),
    ]
