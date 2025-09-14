from django.urls import path

from .views import BudgetAPIView


urlpatterns=[

    path("",BudgetAPIView.as_view(),name="budget_api"),
]