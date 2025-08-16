from django.urls import path
from .views import MonthlyBudgetsView


urlpatterns=[
    path("",MonthlyBudgetsView.as_view(), name="budget_list"),
    path("<int:pk>/", budgetDetailView.as_view(), name="budget_detail"),
]