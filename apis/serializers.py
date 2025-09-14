from rest_framework import serializers

from budgets.models import BudgetHeader

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model=BudgetHeader
        #Choosing fields to expose via API:
        fields=("budget_owner","budget_month","budget_year")