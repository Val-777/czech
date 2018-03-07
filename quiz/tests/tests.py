from django.urls import reverse
from django.test import TestCase


class homeTests(TestCase):
    def test_add_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
