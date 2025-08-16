from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse

from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, FormView
from .models import BudgetHeader
from .forms import budgetForm, budgetLineFormSet


# Create your views here.

class budgetsListView(ListView):

    template_name="budgetsListView.html"
    model=BudgetHeader



##Supporting class to get the details of an existing budget
class budgetLinesGet(DetailView):
    print("SUPPORTING CLASS called - budgetLinesGet class called")
    model = BudgetHeader
    template_name = "new_budget/budget_detail.html"

    def get_context_data(self, **kwargs):

        budget = self.get_object()

        print("retrieving budget", budget)

        context = super().get_context_data(**kwargs)
        context["budgetHeaderForm"] = budgetForm(instance=budget)
        context["budgetLinesForm"] = budgetLineFormSet(instance=budget)
        #budget.budgetOrganisation = self.request.user

        #context["worksInSameCompany"]=budget.budgetOrganisation.isEqualNode(budget.budgetOrganisation)

        print("Context is ", context)

        return context


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
            request.POST, instance=budget
        )  # needs to be set to budget, else recreated
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

        else:

            print("ERRORS", form.errors)
            for subform in formset:
                print(subform.errors)
            print("Problems in updating:")
            print("form: ", form.is_valid())
            print("formset: ", formset.is_valid())

        return super().post(request, *args, **kwargs)

    """  def form_valid(self, request):

        print("form_valid - budgetLinesPost")

        form = budgetForm(request.POST)
        formset = budgetLineFormSet(request.POST)                         

        if form.is_valid() and formset.is_valid():

            #Not comitting anything yet:
            budgetHeaderInfo=form.save(commit=False)
            print("budgetLinesPost - lines form saved")
            print("budget header info var is",budgetHeaderInfo)
            #Saving header info:
            self.object.save()

            formset.instance = budgetHeaderInfo  
            print("formset:",formset)
            print("instance ",formset.instance)
            formset.save()
            print("budgetLinesPost - lines form saved")

            return super().form_valid() """

    def get_success_url(self):
        budget = self.object
        return reverse("budget_detail", kwargs={"pk": budget.pk})


# 2) Class to open the fields of an existing budget and update them if needed


class budgetDetailView(LoginRequiredMixin, View):
    print("CLASS 2 called - detail view called")
    context_object_name = "budget"

    def get(self, request, *args, **kwargs):
        print("getting-detail")
        view = budgetLinesGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("posting-detail")
        view = budgetLinesPost.as_view()
        return view(request, *args, **kwargs)