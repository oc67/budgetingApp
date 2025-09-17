from rest_framework import serializers

from budgets.models import BudgetHeader, BudgetLines


class BudgetLinesSerializer(serializers.ModelSerializer):

    class Meta:
        model=BudgetLines
        #Choosing fields to expose via API:
        fields=("item_name","item_quantity","item_price")


        

class BudgetHeaderSerializer(serializers.ModelSerializer):
    
    
    lines=BudgetLinesSerializer(many=True,required=False)#required enables one to keep lines unchanged

    class Meta:
        model=BudgetHeader
        #Choosing fields to expose via API:
        fields=("budget_ID","budget_month","budget_year","monthly_budget_available","lines")


        def create(self, validated_data):
            lines_data = validated_data.pop("lines")
            header = BudgetHeaderSerializer.objects.create(**validated_data)
            for line_data in lines_data:
                BudgetLines.objects.create(header=header, **line_data)
            return header

        def update(self, instance, validated_data):
            lines_data = validated_data.pop("lines", [])
            instance.budget_ID = validated_data.get("budget_ID", instance.budget_ID)
            instance.budget_month = validated_data.get("budget_month", instance.budget_month)
            instance.budget_year = validated_data.get("budget_year", instance.budget_year)
            instance.monthly_budget_available = validated_data.get("monthly_budget_available", instance.monthly_budget_available)

            instance.save()

            instance.lines.all().delete()
            for line_data in lines_data:
                BudgetLines.objects.create(header=instance, **line_data)

            return instance