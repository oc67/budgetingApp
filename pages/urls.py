from django.urls import path
from .views import (HomePageView, AboutPageView,
                     ReviewPerformanceView,NotificationsView)


urlpatterns=[
    path("",HomePageView.as_view(), name="home"),
    path("about/",AboutPageView.as_view(),name="about"),
    path("review_performance/",ReviewPerformanceView.as_view(),name="budget_performance"),
    path("notifications/",NotificationsView.as_view(),name="notifications"),
    
]