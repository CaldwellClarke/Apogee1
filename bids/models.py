from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# from parties.models import Party

from .validators import validate_bid_amount
User = get_user_model()



# Model for bid which inludes bid amount, user (fk) and party pk (int)
class Bid(models.Model):
	bid_amount 	= models.DecimalField(max_digits=7, decimal_places=2, default=0,\
	 validators =[validate_bid_amount])
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL,
					on_delete=models.CASCADE)
	party 		= models.IntegerField(default = 0)
	def __str__(self):
		return str(self.bid_amount)



# set integrity constraints for database
	def clean(self, *args, **kwargs):
		return super(Bid, self).clean(*args,**kwargs)