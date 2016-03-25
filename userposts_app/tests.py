from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from django.test.client import RequestFactory
from userposts_app.serializers import UserSerializer


class AppTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = "test@gmail.com"
        cls.password = "testuser12345"
        cls.request = RequestFactory()

    def test_user_basic(self):
        def create_user():
            signup_url = reverse("signup")
            self.client.post(signup_url, {"email": self.user, "password": self.password})
            user_query = User.objects.filter(email=self.user)
            self.assertEqual(len(user_query), 1)
            user_data = UserSerializer(user_query[0], many=False).data
            self.assertEqual(user_data["email"], self.user)
            return True
        def login():
            signin_url = reverse("signin")
            response = self.client.post(signin_url, {"email": self.user, "password": self.password})
            return response
        if create_user():
            token = login().data["auth_token"]
            self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
            response = self.client.get("/api/users/my/")
            self.assertEqual(response.data["email"], self.user)


