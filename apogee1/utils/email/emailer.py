from django.core.mail import EmailMessage
from django.template.loader import get_template

def email(subject, from_email, to_emails, template, email_data):
	""" Utility email function
		* template: takes a the file name of a email template in the templates directory, email dir is appended already
		* kwargs: takes a object with keys appropriate to the message
	"""
	template = get_template('emails/' + template)
	html_content = template.render(email_data)
	msg = EmailMessage(subject, html_content, from_email, to_emails)
	msg.content_subtype = "html"
	msg.send()