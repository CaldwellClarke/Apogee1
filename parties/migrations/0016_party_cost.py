# Generated by Django 2.0.1 on 2018-03-08 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0015_auto_20180301_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]