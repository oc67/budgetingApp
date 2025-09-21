from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

 
class BudgetListTests(TestCase):
    @classmethod
    def setUpTestData(cls):


        # Creating user, required for testing authentication:
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="testuser", password="testpass1234"
        )

    # Log in using user details for all the tests of this class
    def setUp(self):
        self.client.login(username="testuser", password="testpass1234")


    #ensure valid page exists at url specified
    def test_url_exists_at_correct_location(self):
        response=self.client.get("/budgets/")
        self.assertEqual(response.status_code, 200)

    #checks name given to URL matches name rendered

    def test_url_available_by_name(self):
        response=self.client.get(reverse("budget_list"))
        self.assertEqual(response.status_code,200)

    
    def test_template_name_correct(self):
        response=self.client.get(reverse("budget_list"))
        self.assertTemplateUsed(response,"new_budget/budget_list.html")

    def test_template_contains_text_sample(self):
        response=self.client.get(reverse("budget_list"))
        self.assertContains(response,"<h2><b><u>Budget list</u></b></h2>")



class NewBudgetTests(TestCase):
    @classmethod
    def setUpTestData(cls):

        # Creating user, required for testing authentication:
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="testuser", password="testpass1234"
        )

    # Log in using user details for all the tests of this class
    def setUp(self):
        self.client.login(username="testuser", password="testpass1234")


    #ensure valid page exists at url specified
    def test_url_exists_at_correct_location(self):
        response=self.client.get("/budgets/new/")
        self.assertEqual(response.status_code, 200)

    #checks name given to URL matches name rendered

    def test_url_available_by_name(self):
        response=self.client.get(reverse("new_budget"))
        self.assertEqual(response.status_code,200)

    
    def test_template_name_correct(self):
        response=self.client.get(reverse("new_budget"))
        self.assertTemplateUsed(response,"new_budget/new_budget.html")

    def test_template_contains_text_sample(self):
        response=self.client.get(reverse("new_budget"))
        self.assertContains(response,"<h2><b><u>New budget</u></b></h2>")



#Missing tests for detail, delete, transfer budgets...