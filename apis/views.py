from django.shortcuts import render
from rest_framework import generics

from budgets.models import BudgetHeader, BudgetLines
from .serializers import BudgetSerializer
# Create your views here.

#In APIs, views return JSON not contents of page:

class BudgetAPIView(generics.ListAPIView):
    queryset=BudgetHeader.objects.all()
    serializer_class=BudgetSerializer
