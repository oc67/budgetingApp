from django.urls import path
from .views import budgetsListView, budgetCreateView, budgetDetailView, budgetDeleteView


urlpatterns=[
    path("",budgetsListView.as_view(), name="budget_list"),
    path("new/",budgetCreateView.as_view(),name="new_budget"),
    path("<int:pk>/", budgetDetailView.as_view(), name="budget_detail"),
    path("<int:pk>/delete/", budgetDeleteView.as_view(), name="budget_delete"),

]
