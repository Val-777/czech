from django.urls import reverse, resolve
from django.test import TestCase

from addwords.views import add


class addTests(TestCase):
    def test_add_view_status_code(self):
        url = reverse('add')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_add_url_resolves_add_view(self):
        view = resolve('/add/')
        self.assertEquals(view.func, add)

    # def test_add_Noun_view_status_code(self):
    #     url = reverse('add_word', kwargs={'kind': 'Noun'})
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)


# class addVerbTests(TestCase):
#     def test_add_view_status_code(self):
#         url = reverse('add_verb')
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)
