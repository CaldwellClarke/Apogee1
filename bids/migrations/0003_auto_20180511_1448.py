# Generated by Django 2.0.1 on 2018-05-11 18:48

import bids.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0002_bid_party'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_amount',
            field=models.IntegerField(default=0, validators=[bids.models.validate_bid_amount]),
        ),
    ]