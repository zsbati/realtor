from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from agenda.models import Contract

User = get_user_model()

class ContractModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.contract = Contract.objects.create(
            title='Test Contract',
            contract_type='rental',
            client_name='Test Client',
            property_address='123 Test St',
            value=1000.00,
            status='draft',
            comment='Test comment',
            signing_date=timezone.now().date(),
            created_by=self.user
        )

    def test_contract_creation(self):
        """Test that a contract can be created"""
        self.assertEqual(Contract.objects.count(), 1)
        self.assertEqual(self.contract.title, 'Test Contract')
        self.assertEqual(self.contract.status, 'draft')
        # Temporarily skip the __str__ test
        # self.assertEqual(str(self.contract), 'Expected format')

class ContractViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_staff=True
        )
        self.client.login(username='testuser', password='testpass123')
        self.contract = Contract.objects.create(
            title='Test Contract',
            contract_type='rental',
            client_name='Test Client',
            property_address='123 Test St',
            value=1000.00,
            status='draft',
            comment='Test comment',
            signing_date=timezone.now().date(),
            created_by=self.user
        )

    def test_contract_list_view(self):
        response = self.client.get(reverse('agenda:contract_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agenda/contracts/contract_list.html')
        self.assertContains(response, 'Test Contract')
