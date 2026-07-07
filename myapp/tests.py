from django.contrib.auth.hashers import check_password
from django.test import TestCase

from .models import Member


class TestBasicSite(TestCase):
    def test_homepage_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_registration_hashes_password_and_redirects(self):
        response = self.client.post('/register/', {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'password': 'StrongPass123',
            'confirm_password': 'StrongPass123',
            'terms': 'on',
        }, follow=True)
        self.assertRedirects(response, '/dashboard/')
        member = Member.objects.get(email='jane@example.com')
        self.assertTrue(check_password('StrongPass123', member.password))
