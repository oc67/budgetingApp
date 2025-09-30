from django.db import models
from django.utils import timezone
from budgets.models import BudgetHeader

# Create your models here.
class AuditTrail(models.Model):
    
    audit_trail_ID=models.AutoField(primary_key=True)
    action_time=models.DateField(blank=False,null=False)
    action_description=models.CharField(max_length=500,null=False,blank=False)

    budget_ID=models.ForeignKey(BudgetHeader, on_delete=models.CASCADE)