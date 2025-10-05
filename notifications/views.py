from django.shortcuts import render
from django.views.generic import (ListView,
                                  ) 
from .models import Notifications
from accounts.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.utils import timezone

# Create your views here.


class NotificationsView(LoginRequiredMixin,ListView):
    
    template_name="notifications/notifications.html"

    def get_queryset(self):
        user=self.request.user
        if user.first_time_on_platform:
            Notifications.objects.create(
                
                notification_text="Welcome to the platform!",
                notification_time=datetime.now(),
                notification_viewer=self.request.user,
                )
            user.first_time_on_platform=False 
            user.save()
             

            
        queryset=Notifications.objects.order_by("-notification_time")
        print("check sorted ",queryset)
        return queryset