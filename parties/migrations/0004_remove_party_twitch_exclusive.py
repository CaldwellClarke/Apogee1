# Generated by Django 2.0.1 on 2018-10-17 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0003_party_twitch_exclusive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='party',
            name='twitch_exclusive',
        ),
    ]