from django.contrib import admin

# Register your models here.
from .models import AuditTrail





class auditTrailAdmin(admin.ModelAdmin):
    #add_form = budgetForm
    model = AuditTrail
    list_display = [
        #"budget_ID",
        "action_description",
        "action_time",
        "action_doer",
        "budget",

    ]


admin.site.register(AuditTrail, auditTrailAdmin)
