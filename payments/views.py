from django.views.generic.base import TemplateView
from django.conf import settings 
from django.http.response import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from django.urls import reverse  # new
from django.shortcuts import render, redirect  # new

import stripe

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (View, TemplateView)


# products/views.py
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
import stripe


class PaymentHomeView(View):
    template_name = "payments/payments.html"

    def get(self, request, *args, **kwargs):
        """Handles GET requests - simply render the home page."""
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """Handles POST requests - create Stripe checkout session."""
        stripe.api_key = settings.STRIPE_SECRET_KEY

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": "price_1SCMJIHNGjkTZcPNwlq80sDL",  # Replace with your price ID
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("cancel")),
        )

        return redirect(checkout_session.url, code=303)


class SuccessView(TemplateView):
    template_name = "payments/success.html"


class CancelView(TemplateView):
    template_name = "payments/cancelled.html"


