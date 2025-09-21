from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.
class NotificationsPageTests(TestCase):
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

        response=self.client.get("/notifications/")
        self.assertEqual(response.status_code,200)

    def test_url_available_by_name(self):
        response=self.client.get(reverse("notifications"))
        self.assertEqual(response.status_code,200)
    
    def test_template_name_correct(self):
        response=self.client.get(reverse("notifications"))
        self.assertTemplateUsed(response,"notifications/notifications.html")

    def test_template_name_correct(self):
        response=self.client.get(reverse("notifications"))
        self.assertContains(response,"<h2><b><u>Notifications</u></b></h2>")
