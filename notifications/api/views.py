# views tell us the templates and methods available to each page
# because this is the api, the views specify the action that happend upon visit
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import UserProfile
from notifications.models import Notification
from .pagination import NotificationsPagination
from .serializers import NotificationModelSerializer

# this creates the api view that our list pages pulls from
class NotificationListAPIView(generics.ListAPIView):
	serializer_class = NotificationModelSerializer
	pagination_class = NotificationsPagination

	# this interacts with the ajax call to this url
	def get_queryset(self, *args, **kwargs):
		qs = self.request.user.notifs_list.order_by('-time_created')
		# qs = Notification.objects.filter(user__id=self.request.user.id).order_by('-time_created')
		return qs

# this view sets the user profile as not having new notifs
class CheckedNotificationsAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, format=None):
		if request.user.is_authenticated:
			profile_obj = UserProfile.objects.get(user=request.user)
			UserProfile.objects.checked_notifications(profile_obj)
			return Response(True)

# this is the view that sets the notification as read
class SeenAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, pk, format=None):
		# gets the notification that is being seen
		notification_obj = Notification.objects.get(pk=pk)
		if request.user.is_authenticated:
			Notification.objects.make_seen(notification_obj)
			return Response(True)