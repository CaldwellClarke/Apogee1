# Generated by Django 2.0.1 on 2018-07-31 20:21

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_profit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('lottery_num_events', models.IntegerField(default=0)),
                ('lottery_total_earnings', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('lottery_total_participants', models.IntegerField(default=0)),
                ('lottery_star_event_time', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], null=True, size=48)),
                ('lottery_star_time', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], null=True, size=48)),
                ('lottery_join_event_time', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], null=True, size=48)),
                ('lottery_join_time', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], null=True, size=48)),
                ('bid_num_events', models.IntegerField(default=0)),
                ('bid_total_earnings', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('bid_star_event_time', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], null=True, size=48)),
                ('bid_star_time', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], null=True, size=48)),
                ('bid_join_event_time', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], null=True, size=48)),
                ('bid_join_time', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], null=True, size=48)),
                ('max_bid_event', models.IntegerField(default=0)),
                ('buyout_num_events', models.IntegerField(default=0)),
                ('buyout_total_earnings', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('buyout_star_event_time', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], null=True, size=48)),
                ('buyout_star_time', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], null=True, size=48)),
                ('buyout_join_event_time', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], null=True, size=48)),
                ('buyout_join_time', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], null=True, size=48)),
                ('max_profit_event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parties.Party')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
