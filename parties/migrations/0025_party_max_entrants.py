# Generated by Django 2.0.1 on 2018-05-17 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0024_party_is_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='max_entrants',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
