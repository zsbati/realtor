from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from agenda.models import Visit

User = get_user_model()

class VisitModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create a test visit
        now = timezone.now()
        self.visit = Visit.objects.create(
            title='Test Visit',
            name='Test User',
            address='123 Test St',
            description='Test description',
            visit_type='visit',
            scheduled_date=now,
            status='scheduled',
            email='test@example.com',
            phone='123456789',
            comment='Test comment',
            transaction_type='sale',
            price=100000,
            created_by=self.user
        )

    def test_visit_creation(self):
        """Test that a visit can be created"""
        self.assertEqual(Visit.objects.count(), 1)
        self.assertEqual(self.visit.title, 'Test Visit')
        self.assertEqual(self.visit.status, 'scheduled')
        # Update this line to match the actual __str__ format
        self.assertEqual(str(self.visit), f'Test Visit - Test User (Visita {"Presencial" if self.visit.visit_type == "visit" else "Online"})')

class VisitViewTest(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_staff=True
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Create a test visit
        now = timezone.now()
        self.visit = Visit.objects.create(
            title='Test Visit',
            name='Test User',
            address='123 Test St',
            description='Test description',
            visit_type='visit',
            scheduled_date=now,
            status='scheduled',
            email='test@example.com',
            phone='123456789',
            comment='Test comment',
            transaction_type='sale',
            price=100000,
            created_by=self.user
        )

    def test_visit_list_view(self):
        response = self.client.get(reverse('agenda:visit_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agenda/visits/visit_list.html')
        self.assertContains(response, 'Test Visit')
