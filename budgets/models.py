from django.db import models
from django.urls import reverse

# Create your models here.

class BudgetHeader(models.Model):
    

    budget_ID=models.AutoField(primary_key=True)
    budget_owner=models.ForeignKey("accounts.CustomUser",null=True,blank=True,on_delete=models.CASCADE)

    all_months=[("January","January"),("February","February"),("March","March"),("April","April"),("May","May"),("June","June")]
    budget_month=models.CharField(choices=all_months,max_length=15,null=False,blank=False)

    budget_created_at=models.DateField(null=True,blank=True)
    monthly_budget_available=models.FloatField(null=False,blank=False)

    # Other possible fields: clientName,

    # Required to display correct plural in Admin view on Django:
    class Meta:
        verbose_name_plural = "budget headers"

    def __str__(self):
        return str(self.budget_ID)

    def get_absolute_url(self):
        return reverse("budget_detail", kwargs={"pk": self.pk})


class BudgetLines(models.Model):


    budgetHeader = models.ForeignKey(
        BudgetHeader, related_name="lines", on_delete=models.CASCADE
    )

    item_name=models.CharField(max_length=20,null=False,blank=False)
    item_quantity=models.IntegerField(null=False,blank=False)
    item_price=models.FloatField(null=True,blank=True)

    is_recurrent=models.BooleanField(default=True,null=True,blank=True)

    class Meta:
        verbose_name_plural = "budget lines"

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("budget_list")