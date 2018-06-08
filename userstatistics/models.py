from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()
# Create your models here.
time_interval_in_minutes = 30
time_in_day_in_minutes = 1440
partitions = int(time_in_day_in_minutes/time_interval_in_minutes)
default_array = [0] * (partitions)
class StatisticsInfo(models.Model):
	
#To link back to user's account
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL,
						on_delete=models.CASCADE)
	max_profit_event 	= models.IntegerField(default = -1)
	max_profit 			= models.DecimalField(max_digits=12,\
	 							decimal_places=2, default=0)
	#LOTTERY STATISTICS
	lottery_num_events 			= models.IntegerField(default = 0)
	lottery_total_earnings 		= models.DecimalField(max_digits=12,\
	 							decimal_places=2, default=0)
	lottery_total_participants 	= models.IntegerField(default = 0)
	lottery_star_event_time 	= ArrayField(models.IntegerField(),size = \
								partitions, null=True, default = default_array)
	lottery_star_time			= ArrayField(models.IntegerField(), size = \
								partitions, null=True, default = default_array)
	lottery_join_event_time 	= ArrayField(models.IntegerField(), size = \
								partitions, null=True, default = default_array)
	lottery_join_time			= ArrayField(models.IntegerField(),	size = \
								partitions, null=True, default = default_array)

	#BID STATISTICS
	bid_num_events 			= models.IntegerField(default = 0)
	bid_total_earnings		= models.DecimalField(max_digits=12,\
	 						decimal_places=2, default=0)
	bid_star_event_time 	= ArrayField(models.IntegerField(),	size = \
							partitions, null=True, default = default_array)
	bid_star_time			= ArrayField(models.IntegerField(),	size = \
							partitions, null=True, default = default_array)
	bid_join_event_time 	= ArrayField(models.IntegerField(),	size = \
							partitions, null=True, default = default_array)
	bid_join_time			= ArrayField(models.IntegerField(),	size = \
							partitions, null=True, default = default_array)

	max_bid_event			= models.IntegerField(default = 0)

	#BUYOUT STATISTICS
	buyout_num_events 		= models.IntegerField(default = 0)
	buyout_total_earnings	= models.DecimalField(max_digits=12,\
	 						decimal_places=2, default=0)
	buyout_star_event_time 	= ArrayField(models.IntegerField(),	size = \
							partitions, null=True, default = default_array)
	buyout_star_time		= ArrayField(models.IntegerField(),	size = \
							partitions, null=True, default = default_array)
	buyout_join_event_time 	= ArrayField(models.IntegerField(), size = \
							partitions, null=True, default = default_array)
	buyout_join_time		= ArrayField(models.IntegerField(), size = \
							partitions, null=True, default = default_array)

	

	def __str__(self):
		return str(str(self.user)+"'s statistics page")