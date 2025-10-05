from django.urls import path
from .views import PaymentHomeView, SuccessView, CancelView
from . import views


urlpatterns=[
    path("",PaymentHomeView.as_view(), name="payments"),

    path('success/', SuccessView.as_view(), name='success'),
    path('cancelled/', CancelView.as_view(), name='cancel'),









]
