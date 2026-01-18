from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Expense

User = get_user_model()

class ExpenseAPITests(APITestCase):
    def setUp(self):
        # Create normal user
        self.user = User.objects.create_user(username="tester", password="Passw0rd!")
        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)

        # Create admin user
        self.admin = User.objects.create_user(username="adminuser", password="AdminPass123", is_staff=True)
        self.admin_token = Token.objects.create(user=self.admin)

        # Create banned user
        self.banned_user = User.objects.create_user(username="banned", password="Banned123", is_banned=True)
        self.banned_token = Token.objects.create(user=self.banned_user)

    def test_create_expense(self):
        url = reverse("expense-list")
        data = {"amount": "20.00", "category": "food", "description": "Lunch", "date": "2025-12-31"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], "20.00")

    def test_banned_user_cannot_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.banned_token.key)
        url = reverse("expense-list")
        data = {"amount": "10", "category": "transport", "description": "Bus", "date": "2025-12-31"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_view_all_expenses(self):
        # Create an expense for normal user
        Expense.objects.create(user=self.user, amount=15, category="food", description="Dinner", date="2025-12-30")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse("expense-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_user_can_only_view_their_own_expenses(self):
        # Create an expense for another user
        Expense.objects.create(user=self.admin, amount=50, category="rent", description="House", date="2025-12-31")
        url = reverse("expense-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User should not see admin's expense
        for exp in response.data:
            self.assertNotEqual(exp["user"], self.admin.id)
