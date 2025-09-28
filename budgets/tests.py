from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from budgets.models import BudgetHeader,BudgetLines

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
        self.assertTemplateUsed(response,"budgets/budget_list.html")

    def test_template_contains_text_sample(self):
        response=self.client.get(reverse("budget_list"))
        self.assertContains(response,"<h2><b><u>Budget list</u></b></h2>")



class NewBudgetTests(TestCase):
    @classmethod
    def setUpTestData(cls):

        # Creating user, required for testing authentication:
        User = get_user_model()
        cls.user = User.objects.create_user( # cls is used here when creating user object, later accessed to via self.user
            username="testuser", password="testpass1234"
        )

    # Log in using user details for all the tests of this class
    def setUp(self):
        self.client.login(username="testuser", password="testpass1234")



    ##Generic tests:
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
        self.assertTemplateUsed(response,"budgets/new_budget.html")

    def test_template_contains_text_sample(self):
        response=self.client.get(reverse("new_budget"))
        self.assertContains(response,"<h2><b><u>New budget</u></b></h2>")

    #Budget-specific tests:
    def new_budget_redirect_works(self):
  
        budget_entry={

                "budget_ID":500,
                "budget_owner":self.user,    
                "original_budget_owner":self.user,
                "budget_month":"January",
                "budget_year":2000,
                "monthly_budget_available":9000,

                "lines-TOTAL_FORMS": "1",
                "lines-INITIAL_FORMS": "1",
                "lines-MIN_NUM_FORMS": "0",
                "lines-MAX_NUM_FORMS": "1000",

                "lines-0-item_name": "Rent",
                "lines-0-item_quantity": 1,
                "lines-0-item_price":1970,
                "lines-0-item_category": "Rent / mortgage",
                "lines-0-isRecurrent": True,
                "lines-0-notes":"House in Newcastle",
            }
        response = self.client.post("/budgets/new/", budget_entry)
        self.assertEqual(response.status_code, 302)  

    def new_budget_urls_exists_at_correct_location(self):
  
        budget_entry={

                "budget_ID":500,
                "budget_owner":self.user,    
                "original_budget_owner":self.user,
                "budget_month":"January",
                "budget_year":2000,
                "monthly_budget_available":9000,

                "lines-TOTAL_FORMS": "1",
                "lines-INITIAL_FORMS": "1",
                "lines-MIN_NUM_FORMS": "0",
                "lines-MAX_NUM_FORMS": "1000",

                "lines-0-item_name": "Rent",
                "lines-0-item_quantity": 1,
                "lines-0-item_price":1970,
                "lines-0-item_category": "Rent / mortgage",
                "lines-0-isRecurrent": True,
                "lines-0-notes":"House in Newcastle",
            }
        post_response = self.client.post("budgets/new", budget_entry)
        
        budget = BudgetHeader.objects.get(budget_ID=500)  # or filter by some unique field
        get_response=self.client.get("/budgets/%d/"%(budget.pk))
        self.assertEqual(get_response.status_code, 200)
    
    def test_template_name_correct(self):
        response=self.client.get(reverse("new_budget"))
        self.assertTemplateUsed(response,"budgets/new_budget.html")

    def test_template_contains_text_sample(self):
        response=self.client.get(reverse("new_budget"))
        self.assertContains(response,"<h2><b><u>New budget</u></b></h2>")


#class BudgetDetailTests(TestCase):
#    @classmethod
#    def setUpTestData(cls):
#
#        # Creating user, required for testing authentication:
#        User = get_user_model()
#        cls.user = User.objects.create_user(
#            username="testuser", password="testpass1234")
#        
#        cls.budget=BudgetHeader.objects.create(
#            budget_ID=500,
#            budget_owner=cls.user,    
#            original_budget_owner=cls.user,
#            budget_month="January",
#            budget_year=2000,
#            monthly_budget_available=9000
#            )
#            #budget_created_at
#
#
#    # Log in using user details for all the tests of this class
#    def setUp(self):
#        self.client.login(username="testuser", password="testpass1234")
#
#
#
#    #ensure valid page exists at url specified
#    def test_url_exists_at_correct_location(self):
#        budget=BudgetHeader.objects.get(budget_ID=500)
#        response=self.client.get("/budgets/%d/"%budget.pk)
#        self.assertEqual(response.status_code, 200)
#
#    #checks name given to URL matches name rendered
#
#    def test_url_available_by_name(self):
#        response=self.client.get(reverse("budget_detail"))
#        self.assertEqual(response.status_code,200)
#
#    
#    def test_template_name_correct(self):
#        response=self.client.get(reverse("budget_detail"))
#        self.assertTemplateUsed(response,"budgets/budget_detail.html")
#
#    def test_template_contains_text_sample(self):
#        response=self.client.get(reverse("budget_detail"))
#        self.assertContains(response,"<h2>Budget ")



class BudgetTransferTests(TestCase):
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
        response=self.client.get("/budgets/transfer/")
        self.assertEqual(response.status_code, 200)

    #checks name given to URL matches name rendered

    def test_url_available_by_name(self):
        response=self.client.get(reverse("budget_transfer"))
        self.assertEqual(response.status_code,200)

    
    def test_template_name_correct(self):
        response=self.client.get(reverse("budget_transfer"))
        self.assertTemplateUsed(response,"budget_transfer/budget_transfer.html")

    def test_template_contains_text_sample(self):
        response=self.client.get(reverse("budget_transfer"))
        self.assertContains(response,"<h2><b><u>Transfer budgets</u></b></h2>")


