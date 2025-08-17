from django import forms

from .models import BudgetHeader, BudgetLines

from django.forms.models import inlineformset_factory


class budgetForm(forms.ModelForm):
    class Meta:
        model = BudgetHeader
        fields = [
            #"budget_ID",
            "budget_month",
            "budget_year",
            "monthly_budget_available",
            "budget_created_at",


        ]

        labels = {

           # "projectID": "Project ID:",
            "budget_owner": "Budget owner: ",
            "budget_year": "Budget year:",
            "budget_month": "Budget month: ",
            "monthly_budget_available":"Monthly budget available: ",
            "budget_created_at": "Budget creation date: ",

     
        }


budgetLineFormSet = inlineformset_factory(
    BudgetHeader,
    BudgetLines,
    fields=("item_name",
            "item_quantity",
            "item_price",
            "is_recurrent",
    ),
    labels={
            "item_name": "Item name: ",
            "item_quantity": "Item quantity: ",
            "item_price":"Item price:" ,
            "is_recurrent":"Recurrent item: ",
    },
    form=budgetForm,
    extra=1,
    can_delete=1,
)


# projectName = forms.CharField(label="Project name: ", max_length=50)

# projectIndustry=forms.CharField(label="Industry: ",max_length=50)
# projectSubfield=forms.CharField(label="Subfield: ",max_length=50)
# projectBudget=forms.IntegerField(label="Budget: ")
# teamExperienceLevel=forms.CharField(label="Experience level",max_length=6)
# teamSize=forms.CharField(label="Size: ", max_length=6)
