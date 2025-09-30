from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (ListView,)

from .models import AuditTrail



# Create your views here.

# Create your views here.
class budgetAuditTrailView(LoginRequiredMixin,ListView):
    template_name="new_budget/budget_audit_trail.html"
    model=AuditTrail