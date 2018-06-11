# this handles the data associated with parties 
import re
import pytz
from django.db.models import F
from datetime import timedelta
from django.db.models.signals import post_save
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

import math
import sys
#I am changing stuff here
from .models import Party
from bids.models import Bid
from userstatistics import statisticsfunctions
from notifications.models import Notification
from .validators import validate_title
from hashtags.signals import parsed_hashtags
from apogee1.settings import celery_app

############################ GLOBAL VARIABLES #################################
max_acceptable_bid = 99999.99

############################ GLOBAL VARIABLES #################################


################################################################################
############################ HELPER FUNCTIONS ##################################
################################################################################

######################### GENERAL EVENT FUNCTIONS ##############################

#Returns dict with event information
#error = event closed
#joined = False
def event_is_closed():
	return {'added':False, 'error_message':"Event is closed"}

#Returns dict with event information
#error = user already in event
#added = False
#uses party_obj to determine what error message to send
def event_user_already_in_event(party_obj):
	if party_obj.event_type == 1:
		error_message = "You have already joined this event"
	elif party_obj.event_type == 3:
		error_message = "You have already bought this event"
	else:
		error_message = "You have already bid on this event"
	return {'added':False,\
	'error_message': error_message}
#Returns dict with event information
#error = event at max capacity
#joined = False
def event_at_max_capacity():
	return {'added':False,\
	'error_message':"This event is already at max capacity"}

####################### END GENERAL EVENT FUNCTIONS ############################

############################ LOTTERY FUNCTIONS #################################

#Returns dict with event information
#Adds user that is passed to party joined list
#error = None
#joined = True
def lottery_add_user(user,party_obj):
	statisticsfunctions.lottery_update_join_stats(party_obj)
	party_obj.joined.add(user)
	return {'added':True, 'error_message':""}
#Ends the lottery event
#1.Party that is passed to it has its joined list shuffled
#2.For loop iterates (stops at the parties max winners)
#3. (during for loop): users are popped off the shuffled "pool" list and
#added to party's winner list
#4.Closes the party by setting party's is_open to false
def lottery_end(party_obj):
	# this creates the owner close notification, alerts the fans that they have won
	Notification.objects.create(user=party_obj.user, party=party_obj,\
	action="owner_event_close")
	print("Closing lottery")
	pool = party_obj.joined.all().order_by('?')
	print("The max entrants are: "+str(party_obj.max_entrants))
	for i in range(0,party_obj.num_possible_winners):
		if pool:
			winner = pool.first()
			party_obj.winners.add(winner)
			Notification.objects.create(user=winner, party=party_obj,\
			action="fan_win")
			pool = pool.exclude(pk=winner.pk)
	statisticsfunctions.lottery_update_end_stats(party_obj)
	party_obj.is_open = False
	party_obj.save2(update_fields=['is_open'])

########################## END LOTTERY FUNCTIONS ###############################

############################ BUYOUT FUNCTIONS ##################################
#Returns dict with event information
#Adds user that is passed to party winner list
#Create Notification for user, buyout_win
#error_message = None
#added = True
def buyout_add_user(user, party_obj):
	statisticsfunctions.buyout_update_join_stats(party_obj)
	party_obj.winners.add(user)
	party_obj.joined.add(user)
	#Creating a notification for the user on buyout win
	print("Creating Notifiaction for buyout win on buyout click")
	Notification.objects.create(user=user, party=party_obj,\
	action="fan_win")
	print("Notification Created")
	return {'added':True, 'error_message':""}
#Ends the buyout event
#1. event that is passed is closed
#2. Create notification for event owner
def buyout_end(user, party_obj):
	print("Closing buyout")
	statisticsfunctions.buyout_update_end_stats(party_obj)
	Notification.objects.create(user=party_obj.user, party=party_obj,\
	action="owner_event_close")
	party_obj.is_open = False
	party_obj.save2(update_fields=['is_open'])

########################## END BUYOUT FUNCTIONS ################################

############################## BID FUNCTIONS ###################################
def bid_add_user_when_open_spots(party_obj, bid, user):
	statisticsfunctions.bid_update_join_stats(party_obj)
	party_obj.joined.add(user)
	new_bid = Bid.objects.create(user=user, party=party_obj, bid_amount=bid)
	print("New bid is: "+str(new_bid.bid_amount)+" by "+str(new_bid.user)+\
	" from open slot")
	return{'added':True, 'error_message':""}

def bid_get_min_bid_number(party_obj):
	print("Bid reached max slots")
	# bid_list = Bid.objects.filter(party=party_obj)
	bid_list = party_obj.bids_list.all()
	min_bid = bid_list.first()
	for bs in bid_list:
		if min_bid.bid_amount>bs.bid_amount:
			min_bid=bs
	return min_bid.bid_amount
def bid_get_min_bid_object(party_obj):
	print("Bid reached max slots")
	# bid_list = Bid.objects.filter(party=party_obj)
	bid_list = party_obj.bids_list.all()
	min_bid = bid_list.first()
	for bs in bid_list:
		if min_bid.bid_amount>bs.bid_amount:
			min_bid=bs
	return min_bid

def bid_add_user_replace_lowest_bid(party_obj, bid, user, min_bid):
	statisticsfunctions.bid_update_join_stats(party_obj)
	print("Removing smallest bid by: "+str(min_bid.user))
	Bid.objects.filter(pk=min_bid.pk).delete()
	# notifies the lowest bidder that they have been knocked off
	Notification.objects.create(user=min_bid.user, party=party_obj,\
	action="fan_outbid")
	party_obj.joined.remove(min_bid.user)
	party_obj.joined.add(user)
	new_bid = Bid.objects.create(user=user, party=party_obj, bid_amount=bid)
	print("New bid is: "+str(new_bid.bid_amount)+" by "+str(new_bid.user)+\
	" from winning slot")
	party_obj.minimum_bid = bid_get_min_bid_number(party_obj)
	party_obj.save2(update_fields=['minimum_bid'])
	return{'added':True, 'error_message':""}

def bid_bid_too_low():
	return{'added':False, 'error_message':"You must beat the minimum bid"}


############################ END BID FUNCTIONS #################################

################################################################################
########################## END HELPER FUNCTIONS ################################
################################################################################

########################## FUNCTIONS USED BY API ###############################


# this both adds or removes the user and tells us if they're on it
def star_toggle(user, party_obj):
	print("STAR TOGGLE TOGGLE TOGGLE TOGGLE STAR TOGGLE")
	if party_obj.event_type==1:
		statisticsfunctions.lottery_update_star_stats(party_obj)
	if party_obj.event_type==2:
		statisticsfunctions.bid_update_star_stats(party_obj)
	if party_obj.event_type==3:
		statisticsfunctions.buyout_update_star_stats(party_obj)
	if user in party_obj.starred.all():
		is_starred = False
		party_obj.starred.remove(user)
	else:
		is_starred = True
		party_obj.starred.add(user)
	return is_starred

# Used for managing users (Winners/joined) in lottery event
#lottery event ending is handled here (if max slots is not none and reached)
# or in scheduler (when time expires)
def lottery_add(user, party_obj):
	# If party is closed
	# returns dict with joined = False and error_message
	# = Event is closed
	if not party_obj.is_open:
		event_info = event_is_closed()
	# If user is already in the lottery
	# returns dict with joined = False and error_message 
	# = You have already joined this event
	elif user in party_obj.joined.all():
		event_info = event_user_already_in_event(party_obj)
	# If there is no cap on how many users can enter the party
	# add user to joined list
	# returns dict with joined = True and error_message
	# = ""
	elif party_obj.max_entrants is None:
		event_info = lottery_add_user(user, party_obj)
	# if the party has reached its max cap
	# returns dict with joined = False and error_message
	# = This event is already at max capacity
	elif party_obj.joined.all().count()>=party_obj.max_entrants:
		event_info = event_at_max_capacity()
	# No constraints left
	# add user to joined list
	# returns dict with joined = True and error_message
	# = ""
	else:
		event_info = lottery_add_user(user, party_obj)
	#if there is a cap on entrants and
	#that cap has been reached in the 
	#joined list, end the lottery and
	#select the winners	
		if party_obj.max_entrants is not None and\
		party_obj.joined.all().count()== party_obj.max_entrants:
			lottery_end(party_obj)
	#get information from the dictionaries	
	is_joined = event_info["added"]
	error_message = event_info["error_message"]
	#Send dictonary info and number of joined
	#to parties/api/views under JoinToggleAPIView
	return {'is_joined':is_joined,\
	'num_joined':party_obj.joined.all().count(),\
	'error_message':error_message}

# Used for managing users (winners/joined) in buyout event
#buyout event ending is handled here (if max slots reached)
# or in scheduler (when time expires)
def buyout_add(user, party_obj):
	# If party is closed
	# returns dict with added = False and error_message
	# = Event is closed
	if not party_obj.is_open:
		event_info = event_is_closed()
	# If user already bought this event
	# returns dict with added = False and error_message 
	# = You have bought this event
	elif user in party_obj.winners.all():
		event_info = event_user_already_in_event(party_obj)
	# if the party has reached its max cap
	# returns dict with added = False and error_message
	# = This event is already at max capacity
	elif party_obj.winners.all().count()>=party_obj.num_possible_winners:
		event_info = event_at_max_capacity()
	# No constraints
	# adds user to winners list of event
	# returns dict with added=True and error_message
	# = ""
	#Also checks, after adding user, if winners has reached max cap
	#if so, ends buyout event
	else:
		event_info = buyout_add_user(user, party_obj)

		if party_obj.winners.all().count()==party_obj.num_possible_winners:
			buyout_end(user, party_obj)
	#Send dictonary info and number of joined
	#to parties/api/views under JoinToggleAPIView
	won = event_info["added"]
	error_message = event_info["error_message"]
	return {'winner':won,\
	'num_winners':party_obj.winners.all().count(),\
	'error_message':error_message}

# Used for managing users (winners/joined) in bid event
# Bid event ending is handled in scheduler (when time expires)
def bid_add(user, party_obj, bid):
	#Checks if bid is a number
	#if not returns error
	try:
		bid = float(bid)
	except ValueError:
		f_min_bid = '%.2f' % party_obj.minimum_bid
		return {'bid_accepted':False,\
		'min_bid':f_min_bid,\
		'error_message':"Improper bid value"}

	#Floors bid at two decimal places
	if bid >= max_acceptable_bid:
		f_min_bid = '%.2f' % party_obj.minimum_bid
		return {'bid_accepted':False,\
		'min_bid':f_min_bid ,\
		'error_message':"Bid value too large"}

	bid = math.floor(bid*100)/100


	print("bid_add:")
	print(bid)
	# If party is closed
	# returns dict with added = False and error_message
	# = Event is closed
	if not party_obj.is_open:
		print("Party closed - bid")
		event_info = event_is_closed()
	# If user already bought this event
	# returns dict with added = False and error_message 
	# = You have already bid on this event
	elif user in party_obj.joined.all():
		print("Already in party - bid")
		event_info = event_user_already_in_event(party_obj)
	#bid must beat the current minimum_bid
	elif not bid:
		print("Bid doesn't exist - bid")
		event_info = bid_bid_too_low()
	elif bid <= party_obj.minimum_bid:
		print("Bid is too low - bid")
		event_info = bid_bid_too_low()
	# If there are still slots available
	# add user to joined list
	# returns dict with added = True and error_message
	# = ""
	# if this results in there being no slots remaining
	# get min bid on this party, and set as party's minimum bid
	elif party_obj.joined.all().count()<party_obj.num_possible_winners:
		print("Free spot - bid")
		event_info = bid_add_user_when_open_spots(party_obj, bid, user)
		if party_obj.joined.all().count()==party_obj.num_possible_winners:
			print("Max spots reached - bid")
			party_obj.minimum_bid = bid_get_min_bid_number(party_obj)		
			party_obj.save2(update_fields=['minimum_bid'])
	#if no slots available
	# get min bid on party object, and check if current bid beats it
	#if so, add user to joined list, and find new lowest bid and set that
	# as party's min bid
	#returns dict with added = True and error_message
	#=""
	#if not
	#return dict with added = False and error_message
	#="Bid Too low"
	#sets min bid again (probably unecessary)
	else:
		min_bid = bid_get_min_bid_object(party_obj)
		if min_bid.bid_amount<bid:
			event_info = bid_add_user_replace_lowest_bid(party_obj, 
			bid, user, min_bid)
		else:
			event_info = bid_bid_too_low()
			party_obj.minimum_bid = min_bid.bid_amount
			party_obj.save2(update_fields=['minimum_bid'])

	#Send dictonary info and number of joined
	#to parties/api/views under JoinToggleAPIView
	bid_accepted = event_info["added"]
	error_message = event_info["error_message"]	
	print("end of bid_add - bid")	
	#This is done for formatting purposes on front end
	# to display only two decimal places
	f_min_bid = '%.2f' % party_obj.minimum_bid
	return {'bid_accepted':bid_accepted,\
	'min_bid':f_min_bid,\
	'error_message':error_message}


# this isnt really a toggle. once you've been added, it sticks
def win_toggle(user, party_obj):
	if user in party_obj.winners.all():
		won = True

	else:
		if(party_obj.event_type==1):
			Notification.objects.create(user=user, party=party_obj,\
			action="fan_win")
		elif(party_obj.event_type==2):
			Notification.objects.create(user=user, party=party_obj,\
			action="fan_win")
		else:
			Notification.objects.create(user=user, party=party_obj,\
			action="fan_win")
		won = True
		party_obj.winners.add(user)
	return won
