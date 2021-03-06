from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from parties.models import Party
from parties.api.pagination import StandardResultsPagination
from parties.api.serializers import PartyModelSerializer
from hashtags.models import HashTag

# this creates the api view that our tags page pulls from
# it holds tweets only, no users
# Right now, you can only access the tag page by clicking on a hashtagged item
# it's not heavily used now, but I think we can use it to tag games 
class TagPartyAPIView(generics.ListAPIView):
	queryset = Party.objects.all().order_by('-time_created')
	# because the tags are all in the text of the events, 
	# the information passed to the API is just the same os the normal party
	serializer_class = PartyModelSerializer
	pagination_class = StandardResultsPagination

	# this allows us to pass a request into the serializer
	# it'll tell us if the user starred the event so we can display the 
	# correct verb at the outset
	def get_serializer_context(self, *args, **kwargs):
		context = super(TagPartyAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	# this interacts with the call to this url and does the actual search 
	# for the events containing the tag
	def get_queryset(self, *args, **kwargs):
		# gets the passed hashtag 
		hashtag = self.kwargs.get('hashtag')
		hashtag_obj = None
		try:
			hashtag_obj = HashTag.objects.get_or_create(tag=hashtag)[0]	
		except:
			pass
		if hashtag_obj:
			# gets all parties with hashtags matching the one passed in
			# it will return any with the hashtag in the title or description
			qs = hashtag_obj.get_parties()
			# query is currently unused
			query = self.request.GET.get('q', None)
			if query is not None:
				# this looks for tags in username, description, and title
				qs = qs.filter(
					Q(description__icontains=query) | 
					Q(user__username__icontains=query) | 
					Q(title__icontains=query)
					)
			return qs
		return None





