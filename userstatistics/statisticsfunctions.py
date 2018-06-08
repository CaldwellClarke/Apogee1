from .models import StatisticsInfo
from django.db.models import F
from bids.models import Bid
import datetime

# All functions related to userstastics.models.py
# and used in parties.models.py/parties.tasks.py

##########################BUYOUT EVENT FUNCTIONS################################
#Called when buyout event ends
#Updates statistic page for all relevant
#info in regards to the event ending
def buyout_update_end_stats(party_obj):
	event_earnings = party_obj.winners.all().count() * party_obj.cost
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	if event_earnings > user_stats_page.max_profit:
		user_stats_page.max_profit = event_earnings
		user_stats_page.max_profit_event = party_obj.pk

	user_stats_page.buyout_num_events = F('buyout_num_events') + 1
	user_stats_page.buyout_total_earnings = F('buyout_total_earnings')\
											 + event_earnings
	user_stats_page.save(update_fields=['buyout_num_events',\
										'buyout_total_earnings',\
										'max_profit',
										'max_profit_event'
										])
# On star button click
# updates the stats page
# by updating arrays using
# the time (converted to an index)
# as an implicit index to store
# count of star clicks
def buyout_update_star_stats(party_obj):
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	user_star_time = datetime.datetime.now().time()
	party_end_time = party_obj.party_time.time()
	#converts user_star_time/party_end_time to an int that
	#corresponds to an index of the array
	user_bucket = get_bucket(user_star_time)
	party_bucket = get_bucket(party_end_time)
	#Django doesn't like trying to modify individual cells in an array field
	#so, I copied the entire array over to a temp array, copied it back after
	#modifying it
	temp_array= user_stats_page.buyout_star_event_time
	temp_array[party_bucket] += 1
	user_stats_page.buyout_star_event_time = temp_array

	temp_array = user_stats_page.buyout_star_time
	temp_array[user_bucket] += 1
	user_stats_page.buyout_star_time = temp_array

	user_stats_page.save(update_fields=['buyout_star_time',\
										'buyout_star_event_time'\
										])
# On successful join of an event
# updates the stats page
# by updating arrays using
# the time (converted to an index)
# as an implicit index to store
# count of star clicks
def buyout_update_join_stats(party_obj):
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	user_join_time = datetime.datetime.now().time()
	party_end_time = party_obj.party_time.time()
	#converts user_star_time/party_end_time to an int that
	#corresponds to an index of the array
	user_bucket = get_bucket(user_join_time)
	party_bucket = get_bucket(party_end_time)
	#Django doesn't like trying to modify individual cells in an array field
	#so, I copied the entire array over to a temp array, copied it back after
	#modifying it
	temp_array= user_stats_page.buyout_join_event_time
	temp_array[party_bucket] += 1
	user_stats_page.buyout_join_event_time = temp_array

	temp_array = user_stats_page.buyout_join_time
	temp_array[user_bucket] += 1
	user_stats_page.buyout_join_time = temp_array

	user_stats_page.save(update_fields=['buyout_join_time',\
										'buyout_join_event_time'\
										])
######################LOTTO EVENT FUNCTIONS#####################################
#Called when lottery event ends
#Updates statistic page for all relevant
#info in regards to the event ending
def lottery_update_end_stats(party_obj):
	print("Updating Stats for Ending of lottery")
	total_participants = party_obj.joined.all().count()
	event_earnings = total_participants * party_obj.cost
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	if event_earnings > user_stats_page.max_profit:
		user_stats_page.max_profit = event_earnings
		user_stats_page.max_profit_event = party_obj.pk

	user_stats_page.lottery_total_participants =\
							F('lottery_total_participants')+total_participants

	user_stats_page.lottery_num_events = F('lottery_num_events') + 1

	user_stats_page.lottery_total_earnings = F('lottery_total_earnings')\
											 + event_earnings

	user_stats_page.save(update_fields=['lottery_num_events',\
										'lottery_total_earnings',\
										'lottery_total_participants',\
										'max_profit',
										'max_profit_event'])
# On successful join of an event
# updates the stats page
# by updating arrays using
# the time (converted to an index)
# as an implicit index to store
# count of star clicks
def lottery_update_star_stats(party_obj):
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	user_star_time = datetime.datetime.now().time()
	party_end_time = party_obj.party_time.time()
	#converts user_star_time/party_end_time to an int that
	#corresponds to an index of the array
	user_bucket = get_bucket(user_star_time)
	party_bucket = get_bucket(party_end_time)
	#Django doesn't like trying to modify individual cells in an array field
	#so, I copied the entire array over to a temp array, copied it back after
	#modifying it
	temp_array= user_stats_page.lottery_star_event_time
	temp_array[party_bucket] += 1
	user_stats_page.lottery_star_event_time = temp_array

	temp_array = user_stats_page.lottery_star_time
	temp_array[user_bucket] += 1
	user_stats_page.lottery_star_time = temp_array

	user_stats_page.save(update_fields=['lottery_star_time',\
										'lottery_star_event_time'\
										])
# On successful join of an event
# updates the stats page
# by updating arrays using
# the time (converted to an index)
# as an implicit index to store
# count of star clicks
def lottery_update_join_stats(party_obj):
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	user_join_time = datetime.datetime.now().time()
	party_end_time = party_obj.party_time.time()
	#converts user_star_time/party_end_time to an int that
	#corresponds to an index of the array
	user_bucket = get_bucket(user_join_time)
	party_bucket = get_bucket(party_end_time)
	#Django doesn't like trying to modify individual cells in an array field
	#so, I copied the entire array over to a temp array, copied it back after
	#modifying it
	temp_array= user_stats_page.lottery_join_event_time
	temp_array[party_bucket] += 1
	user_stats_page.lottery_join_event_time = temp_array

	temp_array = user_stats_page.lottery_join_time
	temp_array[user_bucket] += 1
	user_stats_page.lottery_join_time = temp_array

	user_stats_page.save(update_fields=['lottery_join_time',\
										'lottery_join_event_time'\
										])


#####################BID EVENT FUNCTIONS########################################
#Called when bid event ends
#Updates statistic page for all relevant
#info in regards to the event ending
def bid_update_end_stats(party_obj):
	bid_list = Bid.objects.filter(party=party_obj.pk)

	event_earnings = 0

	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)

	max_bid = user_stats_page.max_bid_event
	for bid in bid_list:
		event_earnings+=bid.bid_amount
		if bid.bid_amount > max_bid:
			max_bid = bid.bid_amount

	if event_earnings > user_stats_page.max_profit:
		user_stats_page.max_profit = event_earnings
		user_stats_page.max_profit_event = party_obj.pk
	user_stats_page.max_bid_event = max_bid
	user_stats_page.bid_num_events = F('bid_num_events') + 1
	user_stats_page.bid_total_earnings = F('bid_total_earnings')\
											 + event_earnings

	user_stats_page.save(update_fields=['bid_num_events',\
										'bid_total_earnings',\
										'max_bid_event',\
										'max_profit',
										'max_profit_event'
										])
# On successful join of an event
# updates the stats page
# by updating arrays using
# the time (converted to an index)
# as an implicit index to store
# count of star clicks
def bid_update_star_stats(party_obj):
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	user_star_time = datetime.datetime.now().time()
	party_end_time = party_obj.party_time.time()
	#converts user_star_time/party_end_time to an int that
	#corresponds to an index of the array
	user_bucket = get_bucket(user_star_time)
	party_bucket = get_bucket(party_end_time)
	#Django doesn't like trying to modify individual cells in an array field
	#so, I copied the entire array over to a temp array, copied it back after
	#modifying it
	temp_array= user_stats_page.bid_star_event_time
	temp_array[party_bucket] += 1
	user_stats_page.bid_star_event_time = temp_array

	temp_array = user_stats_page.bid_star_time
	temp_array[user_bucket] += 1
	user_stats_page.bid_star_time = temp_array

	user_stats_page.save(update_fields=['bid_star_time',\
										'bid_star_event_time'\
										])
# On successful join of an event
# updates the stats page
# by updating arrays using
# the time (converted to an index)
# as an implicit index to store
# count of star clicks
def bid_update_join_stats(party_obj):
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	user_join_time = datetime.datetime.now().time()
	party_end_time = party_obj.party_time.time()
	#converts user_star_time/party_end_time to an int that
	#corresponds to an index of the array
	user_bucket = get_bucket(user_join_time)
	party_bucket = get_bucket(party_end_time)
	#Django doesn't like trying to modify individual cells in an array field
	#so, I copied the entire array over to a temp array, copied it back after
	#modifying it
	temp_array= user_stats_page.bid_join_event_time
	temp_array[party_bucket] += 1
	user_stats_page.bid_join_event_time = temp_array

	temp_array = user_stats_page.bid_join_time
	temp_array[user_bucket] += 1
	user_stats_page.bid_join_time = temp_array

	user_stats_page.save(update_fields=['bid_join_time',\
										'bid_join_event_time'\
										])
#############################GENERAL EVENT FUNCTIONS############################

# given a time object (military time) returns an int
# the int is an index/implicit key
# for the arrays in the StatisticsInfo model
# ex: int of 0 = 12:00 AM, 1 = 12:30 AM, 2 = 1:00 AM
def get_bucket(time):
	# we count on 30 minute intervals, so 2 per hour
	data_partitions_per_hour = 2
	minutes_in_hour = 60
	# partitions * hour gives base bucket to work off of
	# and +1 occurs if it passesthe 30 minute mark
	# ex: 14:00 returns 28, 14:30 returns 29
	partition_bucket_number = data_partitions_per_hour*int(time.hour)
	if(int(time.minute)<minutes_in_hour/data_partitions_per_hour):
		return partition_bucket_number
	else:
		return partition_bucket_number+1

