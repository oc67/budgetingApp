from django.urls import path

from .views import BudgetAPIList, BudgetAPIDetail


urlpatterns=[

    path("",BudgetAPIList.as_view(),name="API_budget_list"),
    path("<int:pk>",BudgetAPIDetail.as_view(),name="API_budget_detail"),

]