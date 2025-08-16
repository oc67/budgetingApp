from django.contrib import admin

# Register your models here.

from .models import BudgetHeader, BudgetLines


class BudgetLineInline(admin.StackedInline):
    model = BudgetLines





class budgetAdmin(admin.ModelAdmin):
    #add_form = budgetForm
    model = BudgetHeader
    inlines = [BudgetLineInline]
    list_display = [
        "budget_ID",
        "budget_owner",

    ]


admin.site.register(BudgetHeader, budgetAdmin)
admin.site.register(BudgetLines)