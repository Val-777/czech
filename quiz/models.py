from django.db import models

import random
from jsonfield import JSONField

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
    options = JSONField(blank=True)
    content = models.ForeignKey(Verb,
                                models.CASCADE,
                                blank=False,
                                null=False,)

    @classmethod
    def make_new(cls, verb):
        for i in range(6):
            pronouns = PersPronoun.objects.filter(role=i)
            opts = ",".join([p.german for p in pronouns])
            exercise = cls(chapter=verb.chapter,
                           czech=verb.cz["present"][str(i)],
                           german='OPT1' + ' ' +
                           verb.de["present"]["active"]["indicative"][str(i)],
                           options={"1": opts},
                           content=verb)
            exercise.save()


class ExPPV(Exercise):
    """
    The exercise for learning verb translations
    """
    content = models.ForeignKey(Verb,
                                models.CASCADE,
                                blank=False,
                                null=False,)

    @classmethod
    def make_new(cls, verb):
        for pronoun in PersPronoun.objects.all():
            if pronoun.role in [0, 1, 2]:
                czech = 's' + pronoun.gender
            elif pronoun.role in [3, 4, 5]:
                czech = 'p' + pronoun.gender
            german = pronoun.german
            if pronoun.role is not 2:
                german += '({})'.format(pronoun.gender)
            german += (' ' + verb.de['preterite']['active']['indicative'][str(
                pronoun.role)])
            exercise = cls(chapter=verb.chapter,
                           czech=verb.cz['participle']['active'][czech],
                           german=german,
                           content=verb)
            exercise.save()
