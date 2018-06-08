# serializers tell us what info from the model is visible in the API
from django.utils.timesince import timeuntil
from django.utils import timezone
from django.template.defaultfilters import truncatechars
from rest_framework import serializers
from django.contrib.auth.models import User

from notifications.models import Notification 
from parties.models import Party

class NotificationModelSerializer(serializers.ModelSerializer):
	# this is the name of the event the notif corresponds to
	party_title = serializers.SerializerMethodField()
	# this is a prettier display for the event time that converts to AM/PM
	party_time = serializers.SerializerMethodField()
	# this tells us the user 
	party_owner = serializers.SerializerMethodField()

	class Meta:
		# the API is built on the party model
		model = Notification
		# the fields tell us what is in the API. some are Serilaizermethodfields 
		# the others are directly from the model
		fields = [
			'id',
			'action', 
			'time_created', 
			'party', 
			'seen', 
			'party_title', 
			'party_time', 
			'party_owner', 
		]


	# The methods below define the SerializerMethodFields
	def get_party_title(self, obj):
		return obj.party.title

	def get_party_time(self, obj):
		# strftime is python datetime method. the localtime call 
		# converts it back to the local time because it is converted 
		# to UTC when it's stored in the database
		tz_converted = timezone.localtime(obj.party.party_time)
		# the % is just formatting
		return tz_converted.strftime('%b %d at %I:%M %p')

	def get_party_owner(self, obj):
		return obj.party.user.username
	