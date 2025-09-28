from django.urls import path
from .views import PaymentHomeView, stripe_config, create_checkout_session
from . import views


urlpatterns=[
    path("",PaymentHomeView.as_view(), name="payments"),
    path('config/', stripe_config, name="stripe_config"), 
    path('create-checkout-session/', create_checkout_session, name="create_checkout_session"), 

    path('success/', views.success, name='success'),
    path('cancelled/', views.cancelled, name='cancelled'),









]
