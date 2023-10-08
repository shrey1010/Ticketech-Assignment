from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TodoTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_todo_list(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create some test todos
        response = self.client.post(
            '/todos/', {'title': 'Test Todo', 'priority': 1})
        self.assertEqual(response.status_code, 201)

        # Check if the todo is in the list
        response = self.client.get('/todos/')
        self.assertEqual(len(response.data), 1)

    def test_create_todo(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a test todo
        response = self.client.post(
            '/todos/', {'title': 'Test Todo', 'priority': 1})
        self.assertEqual(response.status_code, 201)

    def test_delete_todo(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a test todo
        response = self.client.post(
            '/todos/', {'title': 'Test Todo', 'priority': 1})
        self.assertEqual(response.status_code, 201)

        # Delete the todo
        response = self.client.delete(f'/todos/{response.data["id"]}/')
        self.assertEqual(response.status_code, 204)

    def test_update_todo_status(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a test todo
        response = self.client.post(
            '/todos/', {'title': 'Test Todo', 'priority': 1})
        self.assertEqual(response.status_code, 201)

        # Update the status
        response = self.client.put(
            f'/todos/{response.data["id"]}/', {'status': 'completed'})
        self.assertEqual(response.status_code, 200)
