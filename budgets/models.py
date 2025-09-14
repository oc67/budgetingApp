from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.

class BudgetHeader(models.Model):
    

    budget_ID=models.AutoField(primary_key=True)
    budget_owner=models.ForeignKey("accounts.CustomUser",null=False,blank=False,
                                   on_delete=models.CASCADE)

    all_months=[("January","January"),("February","February"),("March","March"),
                ("April","April"),("May","May"),("June","June"),
                ("July","July"),("August","August"),("September","September"),
                ("October","October"),("November","November"),("December","December")]
    
    budget_month=models.CharField(choices=all_months,max_length=15,null=False,blank=False,default="April")

    budget_year=models.IntegerField(null=False,blank=False,default=2025)

    budget_created_at=models.DateField(null=True,blank=True,default=timezone.now())
    monthly_budget_available=models.FloatField(null=False,blank=False)

    # Other possible fields: clientName,

    # Required to display correct plural in Admin view on Django:
    class Meta:
        verbose_name_plural = "budget headers"
        unique_together=["budget_month","budget_year"]

    def __str__(self):
        return str(self.budget_month)+str(self.budget_year)

    def get_absolute_url(self):
        return reverse("budget_detail", kwargs={"pk": self.pk})


class BudgetLines(models.Model):


    budgetHeader = models.ForeignKey(
        BudgetHeader, related_name="lines", on_delete=models.CASCADE
    )

    item_name=models.CharField(max_length=50,null=False,blank=False)
    item_quantity=models.IntegerField(null=False,blank=False)
    item_price=models.FloatField(null=False,blank=False)

    item_categories_list=[("Health","Health"),
                          ("Debt payments","Debt payments"),
                          ("Rent / mortgage","Rent / mortgage"),
                          ("Energy","Energy"),
                          ("Groceries","Groceries"),
                          ("Transport","Transport"),
                          ("Gym","Gym"),
                          ("Eating out", "Eating out"),
                          ("Entertainment","Entertainment"),
                          ("Other","Other")]

    item_category=models.CharField(max_length=20,choices=item_categories_list,null=False,blank=False)

    is_recurrent=models.BooleanField(default=True,null=True,blank=True)
    item_notes=models.CharField(max_length=500, null=True,blank=True)

    class Meta:
        verbose_name_plural = "budget lines"

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("budget_list")