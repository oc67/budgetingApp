from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse

from django.shortcuts import render, redirect
from django.views.generic import (ListView, DetailView, 
                                  UpdateView, DeleteView,
                                    CreateView,FormView,
                                    View, TemplateView)

from django.views.generic.detail import SingleObjectMixin
from .models import BudgetHeader, BudgetLines
from notifications.models import Notifications
from auditTrails.models import AuditTrail

from .forms import budgetForm, budgetLineFormSet, transfersForm

from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.contrib.auth import get_user_model
from datetime import datetime
from . import services


# Create your views here.

class budgetCreateView(LoginRequiredMixin, CreateView):
    model = BudgetHeader
    fields = (
            "budget_owner",
            "budget_month",
            "monthly_budget_available",
            "budget_created_at",
    )

    template_name ="new_budget/new_budget.html"

    #Loads blank form and formset:
    def get(self, request, *args, **kwargs):
        print("getting in createView")
        form = budgetForm()
        formset = budgetLineFormSet()

        return render(request, self.template_name, {"form": form, "formset": formset})

    
    def post(self, request, *args, **kwargs):
        print("posting in createView")

        form = budgetForm(request.POST)
        formset = budgetLineFormSet(request.POST,prefix="lines")

        #form_valid method needs to be replicated since such method does not check formset validity
        if form.is_valid() and formset.is_valid():
            #links owner of budget to budget (info not collected on form):
            budget=form.save(commit=False)
            budget.budget_owner=request.user
            print("Budget id is",budget.budget_ID)
            
            budget.save()
            formset.instance = budget
            formset.save()
            print("saved successfully-create view")
            messages.success(request, "Budget has been created successfully")
            
            #Recording budget creation in audit trail:
            budget_creation_trail_message=AuditTrail.objects.create(
                                action_description="Budget %s has been created"%budget.budget_ID,
                                action_time=datetime.now(),
                                action_doer=request.user,
                                budget=budget)            

            budget_creation_trail_message.save()
            print("Trail created for budget %d"%budget.budget_ID)

            return redirect(
                "budget_list")
    
        #for debugging purposes:
        print("Invalid form/formset. Debugging: ")
        print("problem with header?", form.is_valid())
        print("problem with lines?", formset.is_valid())

        #NEEDS RETURN RENDER !!!



class budgetDeleteView(LoginRequiredMixin, DeleteView):
    model = BudgetHeader
    template_name = "new_budget/budget_delete.html"
    success_url = reverse_lazy("budget_list")



class budgetsListView(LoginRequiredMixin,ListView):
    model=BudgetHeader
    template_name="new_budget/budget_list.html"

    def get_queryset(self):
        queryset=BudgetHeader.objects
        print("check filtered ",queryset)
        return queryset.order_by("-budget_year","-budget_month")
    
    def get_context_data(self, **kwargs):
        #Required to get context from parent 
        context = super().get_context_data(**kwargs)

        #Load exchange rates from API connection, retrieving USD and EUR rates (hourly updated):
        exchange_rates=services.get_exchange_rates()
        print("exchange rates",exchange_rates)
        print("ex ",list(exchange_rates))
        pprint.pprint(exchange_rates)
        USD_gbp=exchange_rates["GGP"][1]["USD"]
        EUR_gbp=exchange_rates["GGP"][1]["EUR"]
        print("USD",USD_gbp)
        print("EUR",EUR_gbp)


        for budget in context["object_list"]:
            #Creating a list, if we used budget.lines.all() on template, calculated prices in USD and EUR
            #would not be retrieved since if a list is not used, the previous operation would retrieve a new queryset 
            budget.lines_list = list(budget.lines.all())

            for line in budget.lines_list:
                line.item_price_USD=line.item_price*USD_gbp
                line.item_price_EUR=line.item_price*EUR_gbp
                print("calculating ",line.item_price,"-->",line.item_price_USD)
                print("calculating ",line.item_price,"-->",line.item_price_EUR)

            budget.total_expenses=sum([line.item_price * line.item_quantity for line in budget.lines_list])            
            budget.total_expenses_USD=sum([line.item_price_USD * line.item_quantity for line in budget.lines_list])            
            budget.total_expenses_EUR=sum([line.item_price_EUR * line.item_quantity for line in budget.lines_list])            


        return context




#Class that loads all the information for an existing budget, enabling such info to be used on
# "budget_detail" template

class budgetLinesGet(DetailView):

    model=BudgetHeader
    template_name = "new_budget/budget_detail.html"
    context_object_name = "budget"


    def get_context_data(self, **kwargs):

        #Getting info from base class:
        context = super().get_context_data(**kwargs) 

        budget = self.get_object()
        print("retrieving budget ",budget.budget_ID)
        context["budgetHeaderForm"] = kwargs.get("form", budgetForm(instance=budget))
        context["budgetLinesForm"] = kwargs.get(
            "formset", budgetLineFormSet(instance=budget, prefix="lines")
        )
        #budget.budgetOrganisation = self.request.user



        #Variable that adds up  all the units of each item:
        total_price_per_line = [
        line.item_price * line.item_quantity for line in budget.lines.all()    ]
        context["total_price_per_line"]=total_price_per_line

        formset = kwargs.get("formset", budgetLineFormSet(instance=budget, prefix="lines"))
        context["formset"] = formset

        #0 required in list comprehension below to deal with case where price or quantity is None:
        form_totals = [(form, (form.instance.item_price or 0) * (form.instance.item_quantity
                                                                  or 0)) for form in formset]
        context["form_totals"] = form_totals


        #Variable that computes the sum of all lines of the budget:
        expenses_across_lines=budget.lines.aggregate(total=Sum("item_price"))["total"] or 0
        context["monthly_expenses_total"] = expenses_across_lines

        #Loading hourly-updated exchange rates from API connection:
        # Required to convert total of expenses to other currencies (USD and EUR)
        exchange_rates=services.get_exchange_rates()
        print("exchange rates",exchange_rates)
        print("ex ",list(exchange_rates))
        pprint.pprint(exchange_rates)
        USD_gbp=exchange_rates["GGP"][1]["USD"]
        EUR_gbp=exchange_rates["GGP"][1]["EUR"]
        print("USD",USD_gbp)
        print("EUR",EUR_gbp)

        context["monthly_expenses_total_USD"]=expenses_across_lines*USD_gbp
        context["monthly_expenses_total_EUR"]=expenses_across_lines*EUR_gbp

        #Variable that displays the variation of budget against spend:
        monthly_profit=budget.monthly_budget_available-expenses_across_lines
        monthly_profit_USD,monthly_profit_EUR=monthly_profit*USD_gbp, monthly_profit*EUR_gbp


        if monthly_profit>0:
            context["monthly_performance"]="Well done, your profit for the month is £%.2f | $%.2f | €%.2f"%(
                monthly_profit,monthly_profit_USD,monthly_profit_EUR)
        elif monthly_profit==0:
            context["monthly_performance"]="Your expenses exactly match your budget this month"
        else:
            context["monthly_performance"]="It seems you went out of budget. Your loss for the month is £%.2f | $%.2f | €%.2f"%(
                -monthly_profit,-monthly_profit_USD,-monthly_profit_EUR)

        #context["worksInSameCompany"]=budget.budgetOrganisation.isEqualNode(budget.budgetOrganisation)

        print("Context is ", context)
        return context




#Class that applies input validation on budget entry that is updated. If forms and formsets checks are passed, updated budget.
class budgetLinesPost(SingleObjectMixin, FormView):
    print("SUPPORTING CLASS called - budget lines post method called")
    model = BudgetHeader
    form_class = budgetForm
    template_name = "new_budget/budget_detail.html"
    context_object_name = "budget"


    def post(self, request, *args, **kwargs):
        print("posting - budgetLinesPost")
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        print("ERRORS", form.errors)

        return self.render_to_response(self.get_context_data(form=form))


    def form_valid(self, form):
        budget=self.get_object()
        form = budgetForm(
            self.request.POST, instance=budget) 
        formset = budgetLineFormSet(self.request.POST, instance=budget, prefix="lines")
        print("form in posting is", form)
        print("formset in posting is", formset)

   

        #checking whether formset is valid on top of form, which will always be valid because of method used
        if formset.is_valid():
            # Not comitting anything yet:
            budgetHeaderInfo = form.save()
            print("budget header info var is", budgetHeaderInfo)

            formset.instance = budgetHeaderInfo
            print("formset:", formset)
            print("instance ", formset.instance)
            formset.save()
            #Recording budget modification in audit trail:
            budget_update_trail_message=AuditTrail.objects.create(
                                action_description="Budget %s has been modified"%budget.budget_ID,
                                action_time=datetime.now(),
                                action_doer=self.request.user,
                                budget=budget)            

            budget_update_trail_message.save()
            print("Trail updated for budget %d"%budget.budget_ID)


            print("budgetLinesPost - lines form saved")

            #Required for total price per line
            form_totals = []
            for form_item in formset:
                if form_item.is_valid():
                    quantity = form_item.cleaned_data.get('item_quantity', 0)
                    price = form_item.cleaned_data.get('item_price', 0)
                else:
                    quantity = form_item.initial.get('item_quantity', 0)
                    price = form_item.initial.get('item_price', 0)
                form_totals.append((form_item, quantity * price))#

            return super().form_valid(form)
        
        else:  
            #if errors exist, these are due to formset problems
            print("ERRORS", form.errors)
            for subform in formset:
                    #Error logging:
                print(subform.errors)
            print("Non-form errors (general formset errors):", formset.non_form_errors())
            print("POST data received:")
            for key, value in self.request.POST.items():
                print(f"{key}: {value}")
            print("Problems in updating:")
            print("form is fine: ", form.is_valid())
            print("formset is fine: ", formset.is_valid())
            
            return self.render_to_response(
            self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        budget = self.object
        return reverse("budget_detail", kwargs={"pk": budget.pk})


#Class that invokes the get and post classes when needed:
class budgetDetailView(LoginRequiredMixin, View):
    model = BudgetHeader
    print("CLASS 2 called - detail view called")
    template_name = "new_budget/budget_detail.html"
    form_class=budgetForm


    def get(self, request, *args, **kwargs):
        
        view=budgetLinesGet.as_view()
        return view(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):

        view=budgetLinesPost.as_view()
        return view(request, *args, **kwargs)


    #Class that enables users to export budget info to csv format:
    
class budgetExportToCSVView(LoginRequiredMixin, View):

    def get(self,request, pk):

        #Getting info from budget that is passed on:
        budgetHeaderInfo = BudgetHeader.objects.get(budget_ID=pk) 

        print("BudgetHeaderInfo is", budgetHeaderInfo)

        budgetLinesInfo=list(BudgetLines.objects.filter(budgetHeader__budget_ID=pk).values())


        print("BudgetLinesInfo is", budgetLinesInfo)

        for line in budgetLinesInfo:
            print("line is ",line, "and type is ",type(line))

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="sample_budget_export_%s_%d.csv"'%(
                            budgetHeaderInfo.budget_month,
                            budgetHeaderInfo.budget_year)},
        )

        #Creating csv file and adding constant header first row:
        writer = csv.writer(response)

        header_file_line=["Budget ID", "Budget author", "Budget month", "Budget year","Budget available",
                          "Line number","Item name",  "Item quantity", "Item price","Item category",
                          "Is recurrent"]
        writer.writerow(header_file_line)

        #Adding values of budget selected:
        
        for line_num,line in enumerate(budgetLinesInfo):
            writer.writerow([budgetHeaderInfo.pk,
                            budgetHeaderInfo.budget_owner,
                            budgetHeaderInfo.budget_month,
                            budgetHeaderInfo.budget_year,
                            budgetHeaderInfo.monthly_budget_available,
                            line_num+1, # start line numbering with 1
                            line["item_name"],
                            line["item_quantity"],
                            line["item_price"],
                            line["item_category"],
                            line["is_recurrent"],

                            ])


        return response
    

class budgetTransfersView(LoginRequiredMixin,View):

    template_name="budget_transfer/budget_transfer.html"

    def get(self, request, *args, **kwargs):
        print("getting  budget transfer menu")
        form = transfersForm()

        return render(request, self.template_name, {"form": form})
    
    def post(self, request, *args, **kwargs):
        print("posting budget transfer")
        form = transfersForm(request.POST)

        #form_valid method needs to be replicated since such meth
        if form.is_valid():

            #Since we are using a simple form - not a modelform- we need to use cleaned_date instad of save():

            transfer_details=form.cleaned_data
            print("Transfer details ",transfer_details)
            requested_month,requested_year=transfer_details["budget_month"],transfer_details["budget_year"]
            print("Requested date: ",requested_month," ",requested_year)

            
            #Check combination of month and year exist and that the budget belongs to user:
            print("all results: ",BudgetHeader.objects)
            budgetMatchHeaderDetails=BudgetHeader.objects.filter(budget_month=requested_month,
                                                                      budget_year=requested_year,
                                                                      budget_owner=request.user,
                                                                      )
            print("Details of matches: ",budgetMatchHeaderDetails, " whose type is ",type(budgetMatchHeaderDetails))
            
            if not budgetMatchHeaderDetails.exists():
                messages.info(request, "No budget matching the date chosen exists")
                return render(request, self.template_name, {"form": form})

            #Get budget id from month and year:
            print("Iterating: ")
            for line in list(budgetMatchHeaderDetails):
                print("line is ",line, "and id is ",line.budget_ID)
                budget_ID=line.budget_ID

            #Ensuring recipient does not own a budget with dates matching the one being transfered(pending):


            #Makes the recipient the new budget owner:
            new_owner_full_name=transfer_details["recipient_ID"]
            User = get_user_model()
            try:
                new_owner = User.objects.get(username=new_owner_full_name)
                print("Recipient will be: ",new_owner)

            except:
                messages.info(request, "Recipient %s does not exist"%new_owner_full_name)
                return render(request, self.template_name, {"form": form})


            
            budget=BudgetHeader.objects.get(budget_ID=budget_ID)

            #Recording original original budget owner:
            if not budget.original_budget_owner: 
                budget.original_budget_owner=budget.budget_owner

            #Changing ownership of budget to transfer the budget:
            budget.budget_owner=new_owner
            
            budget.save()

            #Add a transfer notification on the notification menu:
            transfer_notification=Notifications.objects.create(
                        notification_text="Budget for %s %d transfered to %s"%(requested_month,
                                                                           requested_year,
                                                                           new_owner_full_name),
                        notification_time=datetime.now(),
                        notification_viewer=request.user)            

            transfer_notification.save()

            #Redirects user to budget list menu and shows success message   
            messages.success(request, "Budget has been assigned successfully to %s"%new_owner_full_name)
            return redirect(
                "budget_list")
        
        #for debugging purposes:
        print("Invalid transfers form. Debugging: ")
        print("problem with header?", form.is_valid())
        return render
    
import pprint







# Create your views here.

#Budget--> Budget_ID: 1,2,3

#Audit Trail--> Audit trail ID: 1,2,3
#               Linked to budget with ID 10,20,30

# view: budget_ID--> audit Trail linked to that budget

class budgetAuditTrailView(LoginRequiredMixin,ListView):
    template_name="new_budget/budget_audit_trail.html"
    model=AuditTrail

    def get_queryset(self): # for audit trail values (each audit action, doer...)
        budget_ID = self.kwargs.get("pk")  
        print("budget id is",budget_ID)
        print("filter output is ",AuditTrail.objects.filter(budget__budget_ID=budget_ID, budget__budget_owner=self.request.user))
        return AuditTrail.objects.filter(budget__budget_ID=budget_ID, budget__budget_owner=self.request.user)

    def get_context_data(self, **kwargs): # ok
        context= super().get_context_data(**kwargs)

        #Retrieving budget ID and dateL
        budget_ID=self.kwargs.get("pk")
        budget=BudgetHeader.objects.get(budget_ID=budget_ID)
        context["budget"]=budget

        #Filter based on owner of budget
        #...
        #print("retrieving ",auditTrail)

        return context