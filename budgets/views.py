from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse

from django.shortcuts import render, redirect
from django.views.generic import (ListView, DetailView, 
                                  UpdateView, DeleteView,
                                    CreateView,View)
from .models import BudgetHeader, BudgetLines
from .forms import budgetForm, budgetLineFormSet

from django.db.models import Sum, F
from django.contrib import messages


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

    def get(self, request, *args, **kwargs):
        print("getting in createView")
        form = budgetForm()
        formset = budgetLineFormSet()

        return render(request, self.template_name, {"form": form, "formset": formset})

    def post(self, request, *args, **kwargs):
        print("posting in createView")

        form = budgetForm(request.POST)
        formset = budgetLineFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            #links owner of budget to budget (info not collected on form):
            budget=form.save(commit=False)
            budget.budget_owner=request.user
            
            budget = budget.save()
            formset.instance = budget
            formset.save()
            print("saved successfully-create view")
            messages.success(request, "Budget has been created successfully")

            return redirect(
                "budget_list"
)
        else:
            print()
            print("problems!")
            print("problem with header?", form.is_valid())
            print("problem with lines?", formset.is_valid())

        return render(request, self.template_name, {"form": form, "formset": formset})



class budgetDeleteView(LoginRequiredMixin, DeleteView):
    model = BudgetHeader
    template_name = "new_budget/budget_delete.html"
    success_url = reverse_lazy("budget_list")



class budgetsListView(LoginRequiredMixin,ListView):
    model=BudgetHeader
    template_name="new_budget/budget_list.html"




##Supporting class to get the details of an existing budget
class budgetLinesGet(DetailView):
    print("SUPPORTING CLASS called - budgetLinesGet class called")
    model = BudgetHeader
    template_name = "new_budget/budget_detail.html"

    def get(self, request, *args, **kwargs):
        budget=self.get_object()
        form = budgetForm(instance=budget)
        formset = budgetLineFormSet(instance=budget)

        parent_view = budgetDetailView()
        parent_view.request = request
        parent_view.kwargs = kwargs
        context = parent_view.get_context_data(form=form, formset=formset)

        return render(request,
                       self.template_name, 
                      context)

    


##Supporting class to update the details of an existing budget


class budgetLinesPost(UpdateView):
    print("SUPPORTING CLASS called - budget lines post method called")
    model = BudgetHeader
    form_class = budgetForm
    template_name = "new_budget/budget_detail.html"

    def post(self, request, *args, **kwargs):
        print("posting - budgetLinesPost")
        budget = self.get_object()

        form = budgetForm(
            request.POST, instance=budget) 
        formset = budgetLineFormSet(request.POST, instance=budget, prefix="lines")
        print("form in posting is", form)
        print("formset in posting is", formset)

        if form.is_valid() and formset.is_valid():

            # Not comitting anything yet:
            budgetHeaderInfo = form.save(commit=False)
            print("budgetLinesPost - lines form saved")
            print("budget header info var is", budgetHeaderInfo)
            # Saving header info:
            budgetHeaderInfo.save()

            formset.instance = budgetHeaderInfo
            print("formset:", formset)
            print("instance ", formset.instance)
            formset.save()
            print("budgetLinesPost - lines form saved")
            return redirect("budget_detail", pk=budget.pk)


        else:

            print("ERRORS", form.errors)
            for subform in formset:
                print(subform.errors)
            print("Problems in updating:")
            print("form: ", form.is_valid())
            print("formset: ", formset.is_valid())

            #parent view (budgetDetailView is used for providing error details:)
            parent_view = budgetDetailView()
            parent_view.request = request
            parent_view.kwargs = kwargs
            context = parent_view.get_context_data(form=form, formset=formset)
            return render(request, self.template_name, context)



    def get_success_url(self):
        budget = self.object
        return reverse("budget_detail", kwargs={"pk": budget.pk})


# 2) Class to open the fields of an existing budget and update them if needed


class budgetDetailView(LoginRequiredMixin, View):
    print("CLASS 2 called - detail view called")
    context_object_name = "budget"


    def get_context_data(self, **kwargs):

        budget = self.get_object()
    
        print("retrieving budget", budget)

        context = {}
        context["budgetHeaderForm"] = kwargs.get("form", budgetForm(instance=budget))
        context["budgetLinesForm"] = kwargs.get("formset", budgetLineFormSet(instance=budget, prefix="lines"))


        #budget.budgetOrganisation = self.request.user

        #Variable that adds up of all the units of each item:
        total_price_per_line = [
        line.item_price * line.item_quantity for line in budget.lines.all()    ]
        context["total_price_per_line"]=total_price_per_line
        context["form_totals"] = list(zip(budgetLineFormSet(instance=budget).forms, total_price_per_line))


        #Variable that computes the sum of all lines of the budget:
        expenses_across_lines=budget.lines.aggregate(total=Sum("item_price"))["total"] or 0
        context["total_expenses"] = expenses_across_lines
        #Variable that displays the variation of budget against spend:
        expenses_variance=budget.monthly_budget_available-expenses_across_lines

        if expenses_variance>0:
            context["monthly_performance"]="Well done, your profit for the month is %.2f" %expenses_variance
        elif expenses_variance==0:
            context["monthly_performance"]="Your expenses exactly match your budget this month"
        else:
            context["monthly_performance"]="It seems you went out of budget. Your loss for the month is " %(-expenses_variance)


        #context["worksInSameCompany"]=budget.budgetOrganisation.isEqualNode(budget.budgetOrganisation)

        print("Context is ", context)

        return context
    

    def get(self, request, *args, **kwargs):
        print("getting-detail")
        view = budgetLinesGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("posting-detail")
        view = budgetLinesPost.as_view()
        return view(request, *args, **kwargs)
    


