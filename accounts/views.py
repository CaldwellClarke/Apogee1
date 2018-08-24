from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth import get_user_model
# views tell us what info is displayed, what methods we have acess to, 
# and what our rendering files are
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
import urllib
import json
from django.core.mail import send_mail

from decouple import config

from .models import UserProfile
from .forms import UserRegisterForm, UserProfileModelForm
from .mixins import ProfileOwnerMixin
from apogee1.utils.email import emailer
from parties.api.serializers import PartyModelSerializer
from parties.models import Party

# Create your views here.
User = get_user_model()

welcome_message = "You have successfully registered your account with Apogee.\nWe are excited to have you join the Apogee community!"

# this view is for signing up a new user
class UserRegisterView(FormView):
    # specifies form, location, and where to redirect after submission
    form_class = UserRegisterForm
    template_name = 'accounts/user_register_form.html'
    success_url = '/accounts/login'
    # actually create user here. not sure why we do this, but i believe the cleaning
    # prevents some security issues
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        captcha_good = True

        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
        'secret': config('CAPTCHA_SECRET_KEY'),
        'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if result['success']:
            #Set this config variable to TRUE on heroku to enable account registration
            captcha_good = config('ALLOW_REGISTRATION')
        else:
            captcha_good = config('CAPTCHA_OFF')
        # captcha_good = True
        #Do captcha validation
        print(captcha_good)
        print(self.request.POST.get('tos'))
        if captcha_good and self.request.POST.get('tos'):
            new_user = User.objects.create(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            email_data = {'username': username}
            emailer.email('Account Registration Success', 'team@apogee.gg', [email], 'creation_email.html', email_data)

        else:
            return HttpResponseRedirect("/register")
           # return HttpResponseRedirect("/register")
        return super(UserRegisterView, self).form_valid(form)
        



# this is the view for an individual profile
class UserDetailView(DetailView, LoginRequiredMixin):
    # this tells us where the rendering is
    template_name = 'accounts/user_detail.html'
    # queryset is required for a django detail view. it tells us what data 
    # we are searching
    queryset = User.objects.all()

    # this method allows us to get the username from the url and 
    # then search our User objects for a match on that username
    def get_object(self):
        return get_object_or_404(User, username__exact=self.kwargs.get('username'))

    # allows us to use this info in the js and html
    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            # in the html, we call both following and recommended. this is how those 
            # variables get passed through
            context['following'] = UserProfile.objects.is_following(self.request.user, self.get_object())
            context['blocking'] = UserProfile.objects.is_blocking(self.request.user, self.get_object())
            context['blocked'] = UserProfile.objects.is_blocked(self.request.user, self.get_object())
            context['recommended'] = UserProfile.objects.recommended(self.request.user)

        requested_user = self.kwargs.get('username')
        if requested_user:
            qs = Party.objects.filter(user__username=requested_user).order_by('-time_created')
            serialized_parties = PartyModelSerializer(qs, many=True, context={'request': self.request}).data


        # in the html, we call both following and recommended. this is how those 
        # variables get passed through
        context['events'] = serialized_parties
        context['request'] = self.request
        return context

class FundsView(LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        context = {'user': self.request.user}
        return render(request, 'accounts/funds.html', context)


# this is used to toggle following
class UserFollowView(View, LoginRequiredMixin):
    def get(self, request, username, *args, **kwargs):
        # this returns the object user we are trying to follow or nothing
        toggle_user = get_object_or_404(User, username__iexact=username)
        # you can only follow if you are signed in
        if request.user.is_authenticated:
            is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)
            # it redirects you to the same page you were on and updates the text on the button
            return redirect('profiles:detail', username=username)

# this is used to toggle blocking
class UserBlockView(LoginRequiredMixin, View):
    def get(self, request, username, *args, **kwargs):
        # this returns the object user we are trying to follow or nothing
        toggle_user = get_object_or_404(User, username__iexact=username)
        # you can only follow if you are signed in
        if request.user.is_authenticated:
            is_blocking = UserProfile.objects.toggle_block(request.user, toggle_user)
            # it redirects you to the same page you were on and updates the text on the button
            return redirect('profiles:detail', username=username)


# this is the profile settings page
# the mixins ensure that you are both authenticated and the owner of the profile
class UserProfileUpdateView(LoginRequiredMixin, ProfileOwnerMixin, UpdateView):
    # this tells us what form we are using. its in forms.py
    form_class = UserProfileModelForm
    template_name = 'accounts/profile_settings_form.html'
    queryset = UserProfile.objects.all()
    # success_url = reverse_lazy('profiles:detail', kwargs={'username': request.user.username})

    # this gets the profile object, not the user object
    # we arent trying to edit the user object here. 
    def get_object(self):
        return get_object_or_404(UserProfile.objects.all(), user__username__iexact=self.kwargs.get('username'))
