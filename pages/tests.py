from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


# Create your tests here.

#Tests use CamelCase because unittest is based on jUnit from Java.

class HomePageTests(SimpleTestCase):

    #ensure valid page exists at url specified
    def test_url_exists_at_correct_location(self):
        response=self.client.get("/")
        self.assertEqual(response.status_code, 200)

    #checks name given to URl matches name rendered

    def test_url_available_by_name(self):
        response=self.client.get(reverse("home"))
        self.assertEqual(response.status_code,200)

    
    def test_template_name_correct(self):
        response=self.client.get(reverse("home"))
        self.assertTemplateUsed(response,"home.html")

    def test_template_name_correct(self):
        response=self.client.get(reverse("home"))
        self.assertContains(response,"<h1> Personal budgeting app</h1>")


class AboutPageTests(SimpleTestCase):

    def test_url_exists_at_correct_location(self):

        response=self.client.get("/about/")
        self.assertEqual(response.status_code,200)


    def test_url_available_by_name(self):
        response=self.client.get(reverse("about"))
        self.assertEqual(response.status_code,200)
    
    def test_template_name_correct(self):
        response=self.client.get(reverse("about"))
        self.assertTemplateUsed(response,"about.html")

    def test_template_name_correct(self):
        response=self.client.get(reverse("about"))
        self.assertContains(response,"<h2><b><u>About</u></b></h2>")



class ReviewPerformancePageTests(TestCase):
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


    def test_url_exists_at_correct_location(self):

        response=self.client.get("/review_performance/")
        self.assertEqual(response.status_code,200)

    def test_url_available_by_name(self):
        response=self.client.get(reverse("budget_performance"))
        self.assertEqual(response.status_code,200)
    
    def test_template_name_correct(self):
        response=self.client.get(reverse("budget_performance"))
        self.assertTemplateUsed(response,"review_performance/review_performance.html")

    def test_template_name_correct(self):
        response=self.client.get(reverse("budget_performance"))
        self.assertContains(response,"<h2><b><u>Review Performance</u></b></h2>")


