from django.shortcuts import render
from rest_framework import generics

from budgets.models import BudgetHeader, BudgetLines
from .serializers import BudgetSerializer

from django.contrib.auth import get_user_model
from rest_framework import permissions


# Create your views here.

#In APIs, views return JSON not contents of page:

class BudgetAPIList(generics.ListAPIView):
    queryset=BudgetHeader.objects.all()
    serializer_class=BudgetSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    #Required to display API only to budget owners
    def get_queryset(self):
        return BudgetHeader.objects.filter(budget_owner=self.request.user)

class BudgetAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=BudgetHeader.objects.all()
    serializer_class=BudgetSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    #Required to display API only to budget owners
    def get_queryset(self):
        return BudgetHeader.objects.filter(budget_owner=self.request.user)