from django.urls import path
from .views import budgetAuditTrailView


urlpatterns=[
    path("",budgetAuditTrailView.as_view(), name="budget_audit_trail"),]