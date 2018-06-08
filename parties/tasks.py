# tasks manages all of the celery processes we want 
# to happen with parties at their close time
from __future__ import absolute_import
from celery import shared_task

from userstatistics import statisticsfunctions
from .models import Party
from notifications.models import Notification
from parties import partyHandling
# the shared task just makes it so the celery app can access this
@shared_task
# this method takes the list of joined, reorders it randomly, and picks one
def pick_winner(party_id):
	try:
		# gets the correct party
		# filter would return a queryset, we want an object.
		party = Party.objects.get(pk=party_id)
	except Party.DoesNotExist:
		# if the party is deleted, it does nothing
		return 
	# for any party that hasnt closed by end time, tell the owner its closing
	if party.is_open:
		Notification.objects.create(user=party.user, party=party,\
		action="owner_event_close")
	# if there are people that joined the event
	if party.joined.all().count() > 0:
		# gets all users in joined, orders them randomly
		pool = party.joined.all().order_by('?')
		# if the party is a lottery that isnt closed, take the max number of winners
		# off of the top and add them to winners
		if party.event_type==1 and party.is_open:
			for i in range(0,party.num_possible_winners):
				if pool:
					winner = pool.first()
					partyHandling.win_toggle(winner, party)
					pool = pool.exclude(pk=winner.pk)
			statisticsfunctions.lottery_update_end_stats(party)
		#If the party event is a bid and hasnt closed for some reason
		elif party.event_type==2 and party.is_open:
			#Anyone in the joined list at the end of the event is a winner
			winners = party.joined.all()
			for w in winners:
				print (w)
			#add winners in
			for i in winners:
				partyHandling.win_toggle(i, party)
			statisticsfunctions.bid_update_end_stats(party)
		elif party.event_type==3 and party.is_open:
			print("Buyout event is over")	
			statisticsfunctions.buyout_update_end_stats(party)

		# this closes all parties that had any joins
		party.is_open = False
		party.save2(update_fields=['is_open'])
	# this is if no one has joined the event
	else:
		if party.event_type==1 and party.is_open:
			statisticsfunctions.lottery_update_end_stats(party)
		elif party.event_type==2 and party.is_open:
			statisticsfunctions.bid_update_end_stats(party)
		elif party.event_type==3 and party.is_open:
			statisticsfunctions.buyout_update_end_stats(party)
		print ('it didnt work')
		# this closes the unjoined event
		party.is_open = False
		party.save2(update_fields=['is_open'])	
	# this sends a reminder to the event owner and all the winners 
	if party.winners.all().count() > 0:
		notification_list = party.winners.all()
		for n in notification_list:
			Notification.objects.create(user=n, party=party,\
			action="fan_reminder")
	Notification.objects.create(user=party.user, party=party,\
	action="owner_reminder")