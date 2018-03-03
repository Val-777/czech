from django.db import models

from jsonfield import JSONField
import random

from .utils import (dictify_template,
                    get_wikitext,
                    get_flexion,
                    standardize_german_noun_json,
                    normalize_czech_verb_flexion,
                    # standardize_german_verb_json,
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
    def get_czech_word_type_and_wiki(czech):
        wk = get_wikitext(czech, 'cs')
        word = {'czech': czech, 'wk': wk}
        for section in wk.sections:
            if 'čeština' in section.title:
                if 'podstatné jméno' in section.contents:
                    word['type'] = 'Noun'
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
        return word

    class Meta:
        abstract = True

    use_in_migrations = True


class Noun(Word):
    """The Noun class"""

    # MASCULINE = 'm'
    # FEMININE = 'f'
    # NEUTER = 'n'
    # GENDER_CHOICES = (
    #     (MASCULINE, 'Masculine'),
    #     (FEMININE, 'Feminine'),
    #     (NEUTER, 'Neuter'),
    # )

    # gender_cz = models.CharField(
    #     max_length=1,
    #     choices=GENDER_CHOICES,
    #     default=MASCULINE,
    #     blank=False,
    # )
    # gender_de = models.CharField(
    #     max_length=1,
    #     choices=GENDER_CHOICES,
    #     default=MASCULINE,
    #     blank=False,
    # )

    animate = models.NullBooleanField()

    cz = JSONField(blank=True)

    de = JSONField(blank=True)

    @staticmethod
    def make_czech_noun_json(word):
        wk = word['wk']
        output = {'czech': word['czech']}
        for section in wk.sections:
            if 'čeština' in section.title:
                if 'rod ženský' in section.contents:
                    genus = 'f'
                elif 'rod střední' in section.contents:
                    genus = 'n'
                elif 'rod mužský' in section.contents:
                    genus = 'm'
                    if 'rod mužský neživotný' in section.contents:
                        output['animate'] = False
                    elif 'rod mužský životný' in section.contents:
                        output['animate'] = True
                templates = []
                for template in section.templates:
                    if 'Překlady' in template.name:
                        templates.append(dictify_template(template))
                template = max(templates, key=(
                    lambda dic: len(dic.keys())))
                de = template['de']
                de_list = de[0].split(', ')[0].strip('{}').split('|')
                output['german'] = de_list[2]
                for template in section.templates:
                    if 'Substantivum (cs)' in template.name:
                        output['cz'] = dictify_template(template)
                        output['cz']['genus'] = genus
        return output

    @staticmethod
    def make_german_word_json(german):
        """
        Get JSON representation of German Noun from wiktionary
        """
        wk = get_wikitext(german, 'de')
        wk = wk.sections[1]
        for template in wk.templates:
            if ('Substantiv Übersicht') in template.name:
                temp = dictify_template(template)
                return standardize_german_noun_json(temp)


class Verb(Word):
    """
    The Verb class
    """

    imperfect = models.NullBooleanField()

    cz = JSONField(blank=True)

    de = JSONField(blank=True)

    @staticmethod
    def make_czech_verb_json(word):
        wk = word['wk']
        output = {'czech': word['czech']}
        for section in wk.sections:
            if 'časování' in section.title:
                for template in section.templates:
                    if 'Sloveso (cs)' in template.name:
                        output['cz'] = normalize_czech_verb_flexion(
                            dictify_template(template))
            if 'čeština' in section.title:
                templates = []
                for template in section.templates:
                    if 'Překlady' in template.name:
                        templates.append(dictify_template(template))
                template = max(templates, key=(
                    lambda dic: len(dic.keys())))
                de = template['de']
                de_list = de[0].split(', ')[0].strip('{}').split('|')
                output['german'] = de_list[2]
                for s in section.sections:
                    if 'sloveso' in s.title:
                        if 'nedokonavé' in section.contents:
                            output['imperfect'] = True
                        elif 'dokonavé' in section.contents:
                            output['imperfect'] = False
        return output

    @staticmethod
    def make_german_verb_json(german):
        """
        Get JSON representation of German Verb from wiktionary
        """

        return get_flexion(german)


class PersPronoun(Word):
    """
    The Personal Pronoun class
    """
    # cz = JSONField(blank=True)
    # de = JSONField(blank=True)
    czech = models.CharField(max_length=12, blank=False)
    role = models.PositiveIntegerField()

    P1S = 0
    P2S = 1
    P3S = 2
    P1P = 3
    P2P = 4
    P3P = 5
    ROLE_CHOICES = (
        (P1S, '1st Sin'),
        (P2S, '2nd Sin'),
        (P3S, '3rd Sin'),
        (P1P, '1st Plu'),
        (P2P, '2nd Plu'),
        (P3P, '3rd Plu'),
    )
    role = models.PositiveIntegerField(
        choices=ROLE_CHOICES,
        default=P1S,
    )

    MALE = 'm'
    FEMALE = 'f'
    NEUTER = 'n'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NEUTER, 'Neuter'),
    )
    gender = models.CharField(
        choices=GENDER_CHOICES,
        default=MALE,
        max_length=1,
    )

    def __str__(self):
        return "{} ({}), {}".format(self.czech, self.role, self.gender)

    @classmethod
    def random(cls):
        last = cls.objects.count() - 1
        index1 = random.randint(0, last)
        return cls.objects.all()[index1]
