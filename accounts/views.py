from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, FormView
from django.contrib.auth import get_user_model

from .models import UserProfile
from .forms import UserRegisterForm

# Create your views here.
User = get_user_model()


class UserRegisterView(FormView):
	form_class = UserRegisterForm
	template_name = 'accounts/user_register_form.html'
	success_url = '/accounts/login'

	# actually create user here
	def form_valid(self, form):
		username = form.cleaned_data.get('username')
		email = form.cleaned_data.get('email')
		password = form.cleaned_data.get('password')
		new_user = User.objects.create(username=username, email=email)
		new_user.set_password(password)
		new_user.save()
		return super(UserRegisterView, self).form_valid(form)


class UserDetailView(DetailView):
	template_name = 'accounts/user_detail.html'
	queryset = User.objects.all()

	# this method allows us to get the username from the url and 
	# then search our User objects for a match on that username
	def get_object(self):
		return get_object_or_404(User, username__iexact=self.kwargs.get('username'))

	# allows us to use this info in the js and html
	def get_context_data(self, *args, **kwargs):
		context = super(UserDetailView, self).get_context_data(*args, **kwargs)
		following = UserProfile.objects.is_following(self.request.user, self.get_object())
		context['following'] = following
		context['recommended'] = UserProfile.objects.recommended(self.request.user)
		return context

# this is used to toggle following
class UserFollowView(View):
	def get(self, request, username, *args, **kwargs):
		toggle_user = get_object_or_404(User, username__iexact=username)
		if request.user.is_authenticated:
			is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)
		return redirect('profiles:detail', username=username)







