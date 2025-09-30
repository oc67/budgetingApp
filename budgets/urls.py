from django.urls import path
from .views import (budgetsListView, budgetCreateView, 
budgetDetailView, budgetDeleteView, budgetExportToCSVView,
budgetTransfersView, budgetAuditTrailView)


urlpatterns=[
    path("",budgetsListView.as_view(), name="budget_list"),
    path("new/",budgetCreateView.as_view(),name="new_budget"),
    path("<int:pk>/", budgetDetailView.as_view(), name="budget_detail"),
    path("<int:pk>/delete/", budgetDeleteView.as_view(), name="budget_delete"),
    path("<int:pk>/export/", budgetExportToCSVView.as_view(), name="budget_export"),
    path("transfer/",budgetTransfersView.as_view(),name="budget_transfer"),
    path("<int:pk>/audit/", budgetAuditTrailView.as_view(), name="budget_audit_trail"),





]
