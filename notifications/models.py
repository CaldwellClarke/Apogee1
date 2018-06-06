from django.db import models
from django.conf import settings
# Create your models here.

class NotificationManager(models.Manager):
	# this changes the notifications seen boolean
	def make_seen(self, notif_obj):
		notif_obj.seen = True
		notif_obj.save(update_fields=['seen'])
		return True

class Notification(models.Model):
	action 				= models.CharField(max_length=15)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL,
						on_delete=models.CASCADE)
	time_created 		= models.DateTimeField(auto_now_add=True)
	party 				= models.IntegerField(default = 0)
	seen 				= models.BooleanField(default=False)

	# this just allows the notification objects to use the manager methods
	objects = NotificationManager()

	def __str__(self):
		return str(self.action)