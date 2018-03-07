from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Party

class PartyModelForm(forms.ModelForm):
	# the altered form fields are for formatting on the create page
	title = forms.CharField(label='', max_length=140, widget=forms.Textarea(
		attrs={'placeholder': 'Title', 'class': 'form-control', 'rows': 3}
		))
	description = forms.CharField(label='', max_length=280, widget=forms.Textarea(
		attrs={'placeholder': 'Description', 'class': 'form-control', 'rows': 7}
		))
	# localize tells us that this is in localtime so it converts to UTC for storage
	party_time = forms.SplitDateTimeField(label='', localize=True, widget=forms.SplitDateTimeWidget(
		date_attrs={'placeholder': 'Date: mm/dd/yy', 'class': 'form-control'}, 
		time_attrs={'placeholder': 'Time: hh:mm AM/PM or hh:mm 24-hr', 'class': 'form-control'}
		), input_time_formats=['%I:%M %p', '%H:%M', '%H:%M:%S'], help_text='specify AM or PM if using a 12 hour clock')
	
	thumbnail = forms.ImageField(label='Thumbnail')

	class Meta:
		model = Party
		fields = [
			'title',
			'description',
			'party_time', 
			'thumbnail'
		]

		# dont think these will ever appear cause the fields have length limits on them 
		# like it just doesnt accept any more input after it hits the limit. 
		error_messages = {
            'title': {
                'max_length': "This title is too long.",
            },
            'description': {
                'max_length': "This description is too long.",
            },
        }

	# ensures that the event cannot be scheduled for the past. 
	# def clean_party_time(self, *args, **kwargs):
	# 	party_time = self.cleaned_data.get('party_time')
	# 	if party_time < timezone.now():
	# 		raise forms.ValidationError('Event cannot be in the past.')
	# 	return party_time