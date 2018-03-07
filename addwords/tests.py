from django.urls import reverse
from django.test import TestCase


class addTests(TestCase):
    def test_add_view_status_code(self):
        url = reverse('add')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


# class addVerbTests(TestCase):
#     def test_add_view_status_code(self):
#         url = reverse('add_verb')
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)


# class addNounTests(TestCase):
#     def test_add_view_status_code(self):
#         url = reverse('add_noun')
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)
