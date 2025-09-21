from django.shortcuts import render
from django.views.generic import (ListView,
                                  ) 
from .models import Notifications
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class NotificationsView(LoginRequiredMixin,ListView):
    
    template_name="notifications/notifications.html"

    def get_queryset(self):
        queryset=Notifications.objects.order_by("-notification_time")
        print("check sorted ",queryset)
        return queryset