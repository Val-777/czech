from django.db import models

import random

from addwords.models import Noun, Verb, PersPronoun
from .utils import german_article


class Exercise(models.Model):
    """
    The exercise motherclass
    """
    chapter = models.PositiveIntegerField(blank=True, null=True)
    czech = models.CharField(max_length=120, blank=False)
    german = models.CharField(max_length=120, blank=False)

    @classmethod
    def random(cls):
        last = cls.objects.count() - 1
        index1 = random.randint(0, last)
        return cls.objects.all()[index1]

    def __str__(self):
        return '{}'.format(self.czech)

    class Meta:
        abstract = True

    use_in_migrations = True


class ExNNS(Exercise):
    """
    The exercise for learning nouns.
    """
    content = models.ForeignKey(Noun,
                                models.CASCADE,
                                blank=False,
                                null=False,)

    @classmethod
    def make_new(cls, noun):
        exercise = cls(chapter=noun.chapter,
                       czech=noun.cz['snom'],
                       german='{} {}'.format(german_article(noun.de['genus'], 'nominativ'),
                                             noun.de['snom'][0]),
                       content=noun)
        exercise.save()


class ExAAS(Exercise):
    """
    The exercise for learning Accusative Case
    """
    content = models.ForeignKey(Noun,
                                models.CASCADE,
                                blank=False,
                                null=False,)

    @classmethod
    def make_new(cls, noun):
        exercise = cls(chapter=noun.chapter,
                       czech=noun.cz['sacc'],
                       german='Ich sehe {} {}.'.format(german_article(noun.de['genus'], 'akkusativ'),
                                                       noun.de['sacc'][0]),
                       content=noun)
        exercise.save()


class ExLNS(Exercise):
    """
    The exercise for learning Locative Case
    """
    content = models.ForeignKey(Noun,
                                models.CASCADE,
                                blank=False,
                                null=False,)

    @classmethod
    def make_new(cls, noun):
        exercise = cls(chapter=noun.chapter,
                       czech=noun.cz['sloc'],
                       german='Ich spreche über {} {}.'.format(german_article(noun.de['genus'], 'akkusativ'),
                                                               noun.de['sacc'][0]),
                       content=noun)
        exercise.save()


class ExIIV(Exercise):
    """
    The exercise for learning verb translations
    """
    content = models.ForeignKey(Verb,
                                models.CASCADE,
                                blank=False,
                                null=False,)

    @classmethod
    def make_new(cls, verb):
        exercise = cls(chapter=verb.chapter,
                       czech=[verb.czech, ],
                       german=verb.german,
                       content=verb)
        exercise.save()


class ExKKV(Exercise):
    """
    The exercise for learning conjugations
    """
    content = models.ForeignKey(Verb,
                                models.CASCADE,
                                blank=False,
                                null=False,)

    @classmethod
    def make_new(cls, verb):
        pronouns = PersPronoun.objects.all()
        for pronoun in pronouns:
            role = pronoun.role[0] + 'pre' + pronoun.role[1]
            exercise = cls(chapter=verb.chapter,
                           czech=verb.cz[role],
                           german=pronoun.german + ' ' + verb.de[role][0],
                           content=verb)
            exercise.save()
