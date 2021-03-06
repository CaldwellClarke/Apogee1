# These views manage all the rendering and data for party based pages
# as a note, Delete, Create, Update, List, Detail are all built in views 
# for Django, so htye are a bit magicky
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.urls import reverse
from django.views import View
from django.core.exceptions import PermissionDenied
from apogee1.utils.auth.auth import get_blocking_lists
from django.views.generic.detail import SingleObjectMixin

# from django.core.urlresolvers import reverse
# from django.shortcuts import render
# from paypal.standard.forms import PayPalPaymentsForm
from django.views.generic import (
		ListView, 
		DetailView, 
		CreateView, 
		UpdateView, 
		DeleteView
	)

from .forms import PartyModelForm
from .api.pagination import StandardResultsPagination
from .api.serializers import PartyModelSerializer
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .models import Party
from accounts.models import UserProfile



# Create your views here.



# userownermixin doesnt work here. it only works on the update view 
# because it is based on a form submission. It needs to be based purely
# on the requesting user. Right now that check is on the delete-confirm HTML
class PartyDeleteView(UserOwnerMixin, LoginRequiredMixin, DeleteView):
	model = Party
	template_name = 'parties/delete_confirm.html'
	success_url = reverse_lazy('parties:list')


# update takes the data from the already-created event and fill sthe form with it
# the mixins ensure only a logged in owner can access the page
# class PartyUpdateView(UserOwnerMixin, LoginRequiredMixin, UpdateView):
# 	queryset = Party.objects.all()
# 	form_class = PartyModelForm
# 	template_name = 'parties/update_view.html'


# the two mixins both ensure that the user is logged so that no event can be created 
# without a user attached 
class PartyDuplicateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	# as of right now, the form does not have an easy way to input 
	# the date, it just has to be formatted properly.

	# for using a hybrid create/form view
	form_class = PartyModelForm
	template_name = 'parties/create_view.html'

	def get_queryset(self, *args, **kwargs):
		party_id = self.kwargs.get('pk')
		qs = Party.objects.filter(pk=party_id)
		return qs

	def get_initial(self, *args, **kwargs):
		dup = self.get_object()
		dupinfo = { 
				'title': dup.title,
				'description': dup.description, 
				'party_time': dup.party_time, 
				'num_possible_winners': dup.num_possible_winners, 
				'max_entrants': dup.max_entrants, 
				'cost': dup.cost, 
				'thumbnail': dup.thumbnail,
				}
		return dupinfo



# the two mixins both ensure that the user is logged so that no event can be created 
# without a user attached 
class PartyCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	# as of right now, the form does not have an easy way to input 
	# the date, it just has to be formatted properly.

	# for using a hybrid create/form view

	form_class = PartyModelForm
	template_name = 'parties/create_view.html'
	# def form_valid(self, form):
	# 	print("11111111111111111111111111111111")
	# 	return reverse('parties:detail', kwargs={'pk':self.pk})
	# def get_form_kwargs(self):
	# 	kwargs = super(PartyCreateView, self).get_form_kwargs() #put your view name in the super
	# 	user = self.request.user
	# 	if user:
	# 		kwargs['user'] = user

	# 	return kwargs

# the mixin requires you to be logged in to view events
# because of the way the detail HTML is named, we don't need to 
# specify it here. model_view (party_detail this time) is recognized automatically
class PartyKickallView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			print(1)
			party_id = self.kwargs.get('pk')
			objs = Party.objects.filter(pk=party_id)
			qs = objs.first()
			if request.user == qs.user and qs.event_type==4 or request.user.is_staff and qs.event_type==4:
				print(2)
				winners_list = qs.winners.all()
				for w in winners_list:
					print(3)
					qs.winners.remove(w)
		return redirect('parties:detail', pk=party_id)

class PartyKickView(View):
	def get(self, request, username, *args, **kwargs):
		if request.user.is_authenticated:
			party_id = self.kwargs.get('pk')
			objs = Party.objects.filter(pk=party_id)
			qs = objs.first()
			if request.user == qs.user and qs.event_type==4 or request.user.is_staff and qs.event_type==4:
				winners_list = qs.winners.all()
				for w in winners_list:
					if w.username == username:
						qs.winners.remove(w)
						break
		return redirect('parties:detail', pk=party_id)

class PartyCloseView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			party_id = self.kwargs.get('pk')
			objs = Party.objects.filter(pk=party_id)
			qs = objs.first()
			if request.user == qs.user and qs.event_type==4:
				qs.is_open = False
				qs.save2(update_fields=['is_open'])
		return redirect('parties:detail', pk=party_id)

class PartyLeaveView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			party_id = self.kwargs.get('pk')
			objs = Party.objects.filter(pk=party_id)
			qs = objs.first()
			if qs.event_type==4:
				qs.joined.remove(request.user)
		return redirect('parties:detail', pk=party_id)

class PartyDetailView(DetailView):
	template_name = 'parties/party_detail.html'

	def get_queryset(self, *args, **kwargs):
		party_id = self.kwargs.get('pk')
		qs = Party.objects.filter(pk=party_id)
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		party_id = self.kwargs['pk']
		qs = Party.objects.get(pk=party_id)
		serialized_context = PartyModelSerializer(qs, context={'request': self.request}).data
		if not self.request.user.is_anonymous:
			context['blocked'] = UserProfile.objects.is_blocked(self.request.user, qs.user)
			if context['blocked']:
				raise PermissionDenied
		context['request'] = self.request
		context['serialized'] = serialized_context
		if qs.event_type == 4:
			try:
				winners_list = qs.winners.all()
				joined_list = qs.joined.all()
				context['place_in_queue'] = 'Not in queue'
				count = 0
				for j in joined_list:
					count+=1
					if str(j.username) == str(self.request.user.username):
						context['place_in_queue'] = count
				# context['place_in_queue'] = qs.joined_list.index(self.request.user)
			except Exception as e: 
				print(e)
				context['place_in_queue'] = 'Not in queue'

		else:
			context['place_in_queue'] = 'None'
		return context

	# use 'template_name' to use a custom template name
	# pk == id by default. theyre the same term


# this is the main home page view. all the rendering is handled by the api and 
# JS in base. I believe the queryset isn't even used, its just required by Django
class PartyListView(ListView):
	def get_queryset(self, *args, **kwargs):
		qs = Party.objects.filter(user__username='crasskitty')
		def view_that_asks_for_money(request):

			# What you want the button to do.
			paypal_dict = {
				"business": "receiver_email@example.com",
				"amount": "10000000.00",
				"item_name": "name of the item",
				"invoice": "unique-invoice-id",
			}

			# Create the instance.
			form = PayPalPaymentsForm(initial=paypal_dict)
			context = {"form": form}
			return render(request, "payment.html", context)

		# currently unused because the search goes to a different view
		# this return the string form of the search passed into the url
		# query = self.request.GET.get('q', None)
		# if query is not None:
		# 	# Q is a lookup function
		# 	qs = qs.filter(
		# 		Q(description__icontains=query) | 
		# 		Q(user__username__icontains=query) | 
		# 		Q(title__icontains=query)
		# 		)
		return qs

	# I believe that context is needed so that we can access the request user in the HTML
	def get_context_data(self, *args, **kwargs):
		context = super(PartyListView, self).get_context_data(*args, **kwargs)
		return context


# following list requires the same info as the party list, plus a template name
class FollowingListView(LoginRequiredMixin, ListView):
	def get(self, request, *args, **kwargs):
		im_following = self.request.user.profile.get_following()
		blocked_by_list, blocking_list = get_blocking_lists(request)
		following =  Party.objects.filter(user__in=im_following).order_by('-time_created') \
									.exclude(user__profile__in=blocked_by_list) \
									.exclude(user__in=blocking_list)
		following_serialized = PartyModelSerializer(following, many=True, context={'request': request}).data
		context = {'following' : following_serialized}
		return render(request, 'parties/following_list.html', context)


# almost identical to party list. the query is handled by the API
class StarredListView(LoginRequiredMixin, ListView):
	def get(self, request, *args, **kwargs):
		blocked_by_list, blocking_list = get_blocking_lists(request)
		starred = self.request.user.starred_by.all().order_by('-time_created') \
									.exclude(user__profile__in=blocked_by_list) \
									.exclude(user__in=blocking_list)
		starred_serialized = PartyModelSerializer(starred, many=True, context={'request': request}).data
		context = {'starred' : starred_serialized}
		return render(request, 'parties/starred_list.html', context)


# almost identical to party list. the query is handled by the API
class JoinedListView(LoginRequiredMixin, ListView):
	def get(self, request, *args, **kwargs):
		blocked_by_list, blocking_list = get_blocking_lists(request)
		joined = self.request.user.joined_by.all().order_by('-time_created') \
												.exclude(user__profile__in=blocked_by_list) \
												.exclude(user__in=blocking_list)
		joined_serialized = PartyModelSerializer(joined, many=True, context={'request': request}).data
		context = {'joined' : joined_serialized}
		return render(request, 'parties/joined_list.html', context)

		
# these are the inner workings of how the class based views actually render
# def party_detail_view(request, id=1):
# 	obj = Party.objects.get(id=id) # gets from database
# 	print(obj)
# 	context = {
# 		'object': obj
# 	}
# 	return render(request, 'parties/detail_view.html', context)