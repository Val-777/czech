from django.db import models
# from django.db.models.aggregates import Count

import random
from jsonfield import JSONField

from .utils import (dictify_template,
                    get_wikitext,
                    german_article,
                    )


class Word(models.Model):
    """
    The Word class, all other words inherit from this abstract class.
    It has the chapter (for the chapter in the Tschechisch Kommunikativ book),
    the Czech and the German translations.
    """
    CHAPTER_CHOICES = ((x, str(x)) for x in range(11))
    chapter = models.PositiveIntegerField(
        blank=True, null=True, choices=CHAPTER_CHOICES)
    czech = models.CharField(unique=True, max_length=48, blank=False)
    german = models.CharField(max_length=48, blank=True)

    def __str__(self):
        return self.czech

    @staticmethod
    def get_word_type_class(word_type):
        """
        Factory pattern that returns the correct word type class for passes in strings.
        """
        if word_type == 'Noun':
            return Noun
        else:
            return 'Unknown'

    @staticmethod
    def get_word_json(czech):
        wk = get_wikitext(czech)
        word = {'czech': czech}
        for section in wk.sections:
            if 'čeština' in section.title:
                if 'podstatné jméno' in section.contents:
                    word['type'] = 'Noun'
                    if 'rod ženský' in section.contents:
                        word['gender_cz'] = 'F'
                    elif 'rod střední' in section.contents:
                        word['gender_cz'] = 'N'
                    elif 'rod mužský' in section.contents:
                        word['gender_cz'] = 'M'
                        if 'rod mužský neživotný' in section.contents:
                            word['animate'] = False
                        elif 'rod mužský životný' in section.contents:
                            word['animate'] = True
                    templates = []
                    for template in section.templates:
                        if 'Překlady' in template:
                            templates.append(dictify_template(template))
                    template = max(templates, key=(
                        lambda dic: len(dic.keys())))
                    de = template['de']
                    de_list = de[0].split(', ')[0].strip('{}').split('|')
                    word['german'], word['gender_de'] = de_list[2], de_list[3].upper()
                elif 'sloveso' in section.contents:
                    word['type'] = 'Verb'
                elif 'přídavné jméno' in section.contents:
                    word['type'] = 'Adjective'
                elif 'příslovce' in section.contents:
                    word['type'] = 'Adverb'
                elif 'zájmeno' in section.contents:
                    word['type'] = 'Pronoun'
                elif 'spojka' in section.contents:
                    word['type'] = 'Conjunction'
                elif 'předložka' in section.contents:
                    word['type'] = 'Preposition'
                elif 'číslovka' in section.contents:
                    word['type'] = 'Numeral'
                else:
                    word['type'] = 'Unknown'
            if 'skloňování' in section.title:
                if 'Substantivum (cs)' in section:
                    t = section.templates[0]
                    word['dec'] = dictify_template(t)
        return word

    class Meta:
        abstract = True

    use_in_migrations = True


class Noun(Word):
    """The Noun class"""

    MASCULINE = 'M'
    FEMININE = 'F'
    NEUTER = 'N'
    GENDER_CHOICES = (
        (MASCULINE, 'Masculine'),
        (FEMININE, 'Feminine'),
        (NEUTER, 'Neuter'),
    )

    gender_cz = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=MASCULINE,
        blank=False,
    )
    gender_de = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=MASCULINE,
        blank=False,
    )

    animate = models.NullBooleanField()

    dec = JSONField(blank=True)


class Exercise(models.Model):
    """The exercise motherclass"""
    chapter = models.PositiveIntegerField(blank=True, null=True)
    czech = models.CharField(unique=True, max_length=120, blank=False)
    german = models.CharField(max_length=120, blank=False)

    @classmethod
    def random(cls):
        last = cls.objects.count() - 1
        index1 = random.randint(0, last)
        return cls.objects.all()[index1]
        # count = cls.objects.all().aggregate(count=Count('id'))['count']
        # random_index = randint(0, count - 1)
        # return cls.all()[random_index]

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
                       czech=noun.czech,
                       german='{} {}'.format(german_article(noun.gender_de, 'nominativ'),
                                             noun.german),
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
                       czech=noun.dec['sacc'][0],
                       german='Ich sehe {} {}.'.format(german_article(noun.gender_de, 'akkusativ'),
                                                       noun.german),
                       content=noun)
        exercise.save()
