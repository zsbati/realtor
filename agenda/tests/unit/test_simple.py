from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class SimpleTest(TestCase):
    def test_home_page_redirects_to_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertIn('/login/', response.url)  # Check if redirecting to login

    def test_authenticated_user_can_access_home(self):
        # Create and login a test user
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Now the home page should be accessible
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
