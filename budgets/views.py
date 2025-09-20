from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse

from django.shortcuts import render, redirect
from django.views.generic import (ListView, DetailView, 
                                  UpdateView, DeleteView,
                                    CreateView,FormView,
                                    View)

from django.views.generic.detail import SingleObjectMixin
from .models import BudgetHeader, BudgetLines
from .forms import budgetForm, budgetLineFormSet

from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponse
import csv


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
            
            budget.save()
            formset.instance = budget
            formset.save()
            print("saved successfully-create view")
            messages.success(request, "Budget has been created successfully")

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
        queryset=BudgetHeader.objects.order_by("-budget_year","-budget_month")
        print("check sorted ",queryset)
        return BudgetHeader.objects.order_by("-budget_year","-budget_month")



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
        context["budgetHeaderForm"] = kwargs.get("form", budgetForm(instance=budget))
        context["budgetLinesForm"] = kwargs.get(
            "formset", budgetLineFormSet(instance=budget, prefix="lines")
        )
        #budget.budgetOrganisation = self.request.user

        #Variable that adds up of all the units of each item:
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
        context["total_expenses"] = expenses_across_lines
        #Variable that displays the variation of budget against spend:
        expenses_variance=budget.monthly_budget_available-expenses_across_lines

        if expenses_variance>0:
            context["monthly_performance"]="Well done, your profit for the month is £%.2f" %expenses_variance
        elif expenses_variance==0:
            context["monthly_performance"]="Your expenses exactly match your budget this month"
        else:
            context["monthly_performance"]="It seems you went out of budget. Your loss for the month is %.2f"%(-expenses_variance)

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

    def form_valid(self, form):
        budget=self.get_object()
        #form = budgetForm(
        #    self.request.POST, instance=budget) 
        formset = budgetLineFormSet(self.request.POST, instance=budget, prefix="lines")
        print("form in posting is", form)
        print("formset in posting is", formset)

        #checking whether formset is valid on top of form, which will always be valid because of method used
        if formset.is_valid():
            # Not comitting anything yet:
            budgetHeaderInfo = form.save(commit=False)
            print("budget header info var is", budgetHeaderInfo)
            # Saving header info:
            budgetHeaderInfo.save()

            formset.instance = budgetHeaderInfo
            print("formset:", formset)
            print("instance ", formset.instance)
            formset.save()
            #messages.success(request, "Budget has been updated successfully")

            print("budgetLinesPost - lines form saved")

            return super().form_valid(form)
        
        #if errors exist, these are due to formset problems
        print("ERRORS", form.errors)
        for subform in formset:
            print(subform.errors)
        print("Non-form errors (general formset errors):", formset.non_form_errors())
        print("POST data received:")
        for key, value in self.request.POST.items():
            print(f"{key}: {value}")
        print("Problems in updating:")
        print("form is fine: ", form.is_valid())
        print("formset is fine: ", formset.is_valid())

        #
        form_totals = []
        for form_item in formset:
            if form_item.is_valid():
                quantity = form_item.cleaned_data.get('item_quantity', 0)
                price = form_item.cleaned_data.get('item_price', 0)
            else:
                quantity = form_item.initial.get('item_quantity', 0)
                price = form_item.initial.get('item_price', 0)
            form_totals.append((form_item, quantity * price))
        
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
            print("line is ",line, "and tpye is ",type(line))

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