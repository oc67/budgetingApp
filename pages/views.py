from django.shortcuts import render

from django.views.generic import TemplateView

from budgets.models import BudgetHeader, BudgetLines
from collections import defaultdict

# Create your views here.

class HomePageView(TemplateView):
    template_name="home.html"

class AboutPageView(TemplateView):
    template_name="about.html"

class ReviewPerformanceView(TemplateView):
    template_name="review_performance/budget_performance.html"

    def get_context_data(self,**kwargs):
    
        #Filters out data which does not belong to user:        
        
        allBudgetLinesBelongingToUser=BudgetLines.objects.filter(budgetHeader__budget_owner=self.request.user)


        #Obtains values of actionsOrDecisions and Insights worths:
        allBudgetsPrices=list(allBudgetLinesBelongingToUser.values_list("item_price",flat=True))
        print("all items",allBudgetsPrices)
       
        allBudgetsCategories=list(allBudgetLinesBelongingToUser.values_list("item_category",flat=True))
        print("all categories",allBudgetsCategories)


        #Aggregating cost of all items per category:
        allBudgetsCategoriesAndPrices=defaultdict(float)

        for cat,price in zip(allBudgetsCategories,allBudgetsPrices):
            allBudgetsCategoriesAndPrices[cat]+=price
        
        print("Does this dictionary work well?",allBudgetsCategoriesAndPrices)


        
        context=super().get_context_data(**kwargs)

        context["datapoints"] = [
        {"label": cat, "y": total_price} for cat, total_price in allBudgetsCategoriesAndPrices.items()
        ]


        return context  
    

