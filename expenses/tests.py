from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class ExpenseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="Passw0rd!")
        self.client.force_authenticate(user=self.user)

    def test_create_expense(self):
        url = reverse("expense-list")
        data = {"amount": "10.00", "category": "food", "description": "Test lunch", "date": "2025-12-31"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], "10.00")