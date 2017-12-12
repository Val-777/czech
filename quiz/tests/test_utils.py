from django.test import TestCase

from quiz.utils import get_wikitext

# class SignUpTests(TestCase):
#     def setUp(self):
#         url = reverse('signup')
#         self.response = self.client.get(url)


class UtilTests(TestCase):
    def wiki_test(self):
        self.assertEquals(str(type(get_wikitext('muž'))), "<class 'wikitextparser.wikitext.WikiText'>")
