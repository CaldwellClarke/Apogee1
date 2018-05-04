# views tell us the templates and methods available to each page
# because this is the api, the views specify the action that happend upon visit
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Count

from parties.models import Party
from .pagination import StandardResultsPagination
from .serializers import PartyModelSerializer

# star toggle is a method from the model that just adds the user to the 
# list containing the people who have starred it
class StarToggleAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request, pk, format=None):
		# gets the object that is being starred
		party_qs = Party.objects.filter(pk=pk)
		if request.user.is_authenticated:
			is_starred = Party.objects.star_toggle(request.user, party_qs.first())
			return Response({'starred': is_starred})
		return Response({'message': 'Not Allowed'})

# join works much like star. its a method from the model. however, its
# built not to toggle. it only adds at the moment
class JoinToggleAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request, pk, format=None):
		# gets the object that is being liked
		party_qs = Party.objects.filter(pk=pk)
		if request.user.is_authenticated:
			is_joined = Party.objects.join_toggle(request.user, party_qs.first())
			return Response({'joined': is_joined})
		return Response({'message': 'Not Allowed'})


# used to async create events and push them to the api list
# so that we can update the main page with the new tweet
# CURRENTLY UNUSED
class PartyCreateAPIView(generics.CreateAPIView):
	serializer_class = PartyModelSerializer
	# ensures user is logged in to create
	permission_classes = [permissions.IsAuthenticated]

	# allows the api to create event with user data
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


# used for the single detail view. it searches the query on a single ID
class PartyDetailAPIView(generics.ListAPIView):
	queryset = Party.objects.all()
	serializer_class = PartyModelSerializer
	permission_classes = [permissions.AllowAny]
	pagination_class = StandardResultsPagination

	def get_queryset(self, *args, **kwargs):
		party_id = self.kwargs.get('pk')
		qs = Party.objects.filter(pk=party_id)
		return qs


# this creates the api view that our search page pulls from
# it differs from the list view in that it includes users we arent following
class SearchPartyAPIView(generics.ListAPIView):
	queryset = Party.objects.all().order_by('-time_created')
	serializer_class = PartyModelSerializer
	pagination_class = StandardResultsPagination

	# this allows us to pass a request into the serializer
	# it'll tell us if the user starred the event so we can display the 
	# correct verb at the outset
	def get_serializer_context(self, *args, **kwargs):
		context = super(SearchPartyAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	# this interacts with the call to this url
	def get_queryset(self, *args, **kwargs):		
		# this return the string form of the search passed into the url
		qs = self.queryset
		query = self.request.GET.get('q', None)
		if query is not None:
			# Q is a lookup function
			qs = qs.filter(
				Q(description__icontains=query) | 
				Q(user__username__icontains=query) | 
				Q(title__icontains=query)
				)
		return qs


# this creates the api view that our list pages pulls from
class PartyListAPIView(generics.ListAPIView):
	serializer_class = PartyModelSerializer
	pagination_class = StandardResultsPagination

	# this allows us to pass a request into the serializer
	# it'll tell us if the user starred the event so we can display the 
	# correct verb at the outset
	def get_serializer_context(self, *args, **kwargs):
		context = super(PartyListAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context
	
	# this interacts with the ajax call to this url
	def get_queryset(self, *args, **kwargs):
		# gets user for if we have a user detail view
		requested_user = self.kwargs.get('username')
		if requested_user:
			# includes only the requested users events in the feed
			# sets the ordering. party_time would be soonest expiration at the top
			qs = Party.objects.filter(user__username=requested_user).order_by('-time_created')
		else:
			# uses methods form the userprofile model
			im_following = self.request.user.profile.get_following()
			qs1 = Party.objects.filter(user__in=im_following)
			# includes our own events in our feed
			qs2 = Party.objects.filter(user=self.request.user)
			# sets the ordering. party_time would be soonest expiration at the top
			qs = (qs1 | qs2).distinct().order_by('-time_created')
		
		# this return the string form of the search passed into the url
		query = self.request.GET.get('q', None)
		if query is not None:
			# Q is a lookup function
			qs = qs.filter(
				Q(description__icontains=query) | 
				Q(user__username__icontains=query) | 
				Q(title__icontains=query)
				)
		return qs



# this creates the api view that our starred list page pulls from
class StarredListAPIView(generics.ListAPIView):
	serializer_class = PartyModelSerializer
	pagination_class = StandardResultsPagination

	# this allows us to pass a request into the serializer
	# it'll tell us if the user starred the event so we can display the 
	# correct verb at the outset
	def get_serializer_context(self, *args, **kwargs):
		context = super(StarredListAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context
	
	# this interacts with the ajax call to this url
	def get_queryset(self, *args, **kwargs):
		qs = self.request.user.starred_by.all().order_by('-time_created')
		return qs

# this works the same way as the starred list
class JoinedListAPIView(generics.ListAPIView):
	serializer_class = PartyModelSerializer
	pagination_class = StandardResultsPagination

	# this allows us to pass a request into the serializer
	# it'll tell us if the user starred the event so we can display the 
	# correct verb at the outset
	def get_serializer_context(self, *args, **kwargs):
		context = super(JoinedListAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context
	
	# this interacts with the ajax call to this url
	def get_queryset(self, *args, **kwargs):
		qs = self.request.user.joined_by.all().order_by('-time_created')
		return qs


# this creates the api view that the trending list of our home page pulls from
# its currently not working
class TrendingListAPIView(generics.ListAPIView):
	serializer_class = PartyModelSerializer
	pagination_class = StandardResultsPagination

	# this allows us to pass a request into the serializer
	# it'll tell us if the user starred the event so we can display the 
	# correct verb at the outset
	def get_serializer_context(self, *args, **kwargs):
		context = super(TrendingListAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context
	
	# this interacts with the ajax call to this url
	def get_queryset(self, *args, **kwargs):
		# uses methods form the userprofile model
		im_following = self.request.user.profile.get_following()
		qs1 = Party.objects.filter(user__in=im_following)
		# includes our own events in our feed
		qs2 = Party.objects.filter(user=self.request.user)
		# sets the ordering. party_time would be soonest expiration at the top
		qs = (qs1 | qs2).distinct().order_by('starred')
		return qs






		