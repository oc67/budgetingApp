from django import forms

from .models import BudgetHeader, BudgetLines

from django.forms.models import inlineformset_factory


#Budget forms for CRUD operations:

class budgetForm(forms.ModelForm):
    class Meta:
        model = BudgetHeader
        fields = [
            #"budget_ID",
            "budget_month",
            "budget_year",
            "monthly_budget_available",
            #"budget_created_at",
        ]

        labels = {

           # "projectID": "Project ID:",
            "budget_owner": "Budget owner: ",
            "budget_year": "Budget year:",
            "budget_month": "Budget month: ",
            "monthly_budget_available":"Money available for spending (in £): ",
            "budget_created_at": "Budget creation date: ",
        }


budgetLineFormSet = inlineformset_factory(
    BudgetHeader,
    BudgetLines,
    fields=("item_name",
            "item_quantity",
            "item_price",
            "item_category",
            "is_recurrent",
    ),
    labels={
            "item_name": "Item name: ",
            "item_quantity": "Item quantity: ",
            "item_price":"Item price (in £):" ,
            "item_category":"Item category: ",
            "is_recurrent":"Recurrent item: ",
    },
    form=budgetForm,
    extra=1,
    can_delete=1,
)

#Form used to enable users to select budgets and specify receiver of budget:

class transfersForm(forms.Form):

    all_months=[  ("January","January"),("February","February"),("March","March"),
        ("April","April"),("May","May"),("June","June"),
        ("July","July"),("August","August"),("September","September"),
        ("October","October"),("November","November"),("December","December")]
    
    budget_month=forms.ChoiceField(label="Budget month: ",choices=all_months)

    budget_year=forms.IntegerField(label="Budget year: ")

    recipient_ID=forms.CharField(label="Recipient name and surname (e.g., JohnSmith): ")
    
    