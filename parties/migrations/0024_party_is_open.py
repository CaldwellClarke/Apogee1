# Generated by Django 2.0.1 on 2018-05-16 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0023_auto_20180508_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
    ]
