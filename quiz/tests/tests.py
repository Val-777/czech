from django.urls import reverse, resolve
from django.test import TestCase

from quiz.views import home, exercise
from addwords.models import Noun


class homeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class ExerciseTests(TestCase):
    def setUp(self):
        Noun.objects.create(
            chapter=1,
            czech='hudba',
            german='Musik',
            animate=False,
            cz={
                "snom": [
                    "hudba"
                ],
                "sgen": [
                    "hudby"
                ],
                "sdat": [
                    "hudbě"
                ],
                "sacc": [
                    "hudbu"
                ],
                "svoc": [
                    "hudbo"
                ],
                "sloc": [
                    "hudbě"
                ],
                "sins": [
                    "hudbou"
                ],
                "pnom": [
                    "hudby"
                ],
                "pgen": [
                    "hudeb"
                ],
                "pdat": [
                    "hudbám"
                ],
                "pacc": [
                    "hudby"
                ],
                "pvoc": [
                    "hudby"
                ],
                "ploc": [
                    "hudbách"
                ],
                "pins": [
                    "hudbami"
                ],
                "genus": "f"
            },
            de={
                "snom": [
                    "Musik"
                ],
                "sacc": [
                    "Musik"
                ],
                "sdat": [
                    "Musik"
                ],
                "sgen": [
                    "Musik"
                ],
                "pnom": [
                    "Musiken"
                ],
                "pacc": [
                    "Musiken"
                ],
                "pdat": [
                    "Musiken"
                ],
                "pgen": [
                    "Musiken"
                ],
                "genus": "f"
            })

    def test_ExNNS_url_resolves_exercise_view(self):
        view = resolve('/exercises/ExNNS/')
        self.assertEquals(view.func, exercise)

    def test_ExNNS_view_success_status_code(self):
        url = reverse('exercise', kwargs={'kind': 'ExNNS'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_ExAAS_view_success_status_code(self):
        url = reverse('exercise', kwargs={'kind': 'ExAAS'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_ExLNS_view_success_status_code(self):
        url = reverse('exercise', kwargs={'kind': 'ExLNS'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_exercise_view_not_found_status_code(self):
        url = reverse('exercise', kwargs={'kind': 'whatever'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
