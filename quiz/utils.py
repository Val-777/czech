"""
Utility functions for the quiz app
"""
import wikitextparser as wtp
from urllib.request import urlopen
import urllib
import json


def dictify_template(templ):
    """
    Turns a Template object into dictionary
    """
    output = {}
    for arg in templ.arguments:
        val = arg.value.strip().split(' / ')
        va = []
        for v in val:
            va.append(v.strip('[]'))
        output[arg.name.strip()] = va
    return output


def get_wikitext(word, language):
    """
    Gets the wikitext for the passed in Czech word, which is then parsed with the wikitextparser,
    which breaks it up into a list of Section objects
    """
    word = urllib.parse.quote(word)
    QUERY = ("https://{}.wiktionary.org/w/api.php?"
             "action=parse&"
             "format=json&"
             "uselang={}&"
             "page={}&"
             "prop=wikitext&"
             "utf8=1&"
             "formatversion=1").format(language, language, word)
    with urlopen(QUERY) as url:
        http_info = url.info()
        raw_data = url.read().decode(http_info.get_content_charset())

    project_info = json.loads(raw_data)
    result = {'headers': http_info.items(), 'body': project_info}

    wikitext = result['body']['parse']['wikitext']['*']
    return wtp.parse(wikitext)


def update_attrs(instance, **kwargs):
    """ Updates model instance attributes and saves the instance
    :param instance: any Model instance
    :param kwargs: dict with attributes
    :return: updated instance, reloaded from database
    """
    # instance_pk = instance.pk
    for key, value in kwargs.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
        else:
            raise KeyError("Failed to update non existing attribute {}.{}".format(
                instance.__class__.__name__, key
            ))
    instance.save()  # force_update=True)
    # return instance.__class__.objects.get(pk=instance_pk)


def german_article(gender_de, case):
    masculine = {
        'nominativ': 'der',
        'genitiv': 'des',
        'dativ': 'dem',
        'akkusativ': 'den',
    }
    feminine = {
        'nominativ': 'die',
        'genitiv': 'der',
        'dativ': 'der',
        'akkusativ': 'die',
    }
    neutral = {
        'nominativ': 'das',
        'genitiv': 'des',
        'dativ': 'dem',
        'akkusativ': 'das',
    }
    if gender_de is 'M':
        return masculine[case]
    elif gender_de is 'F':
        return feminine[case]
    elif gender_de is 'N':
        return neutral[case]


def standardize_german_noun_json(dic_temp):
    """
    Standardize German noun after dictifying
    """
    output = {}
    output['snom'] = dic_temp['Nominativ Singular']
    if 'Nominativ Singular*' in dic_temp:
        output['snom'].append(dic_temp['Nominativ Singular*'][0])
    output['sacc'] = dic_temp['Akkusativ Singular']
    if 'Akkusativ Singular*' in dic_temp:
        output['sacc'].append(dic_temp['Akkusativ Singular*'][0])
    output['sdat'] = dic_temp['Dativ Singular']
    if 'Dativ Singular*' in dic_temp:
        output['sdat'].append(dic_temp['Dativ Singular*'][0])
    output['sgen'] = dic_temp['Genitiv Singular']
    if 'Genitiv Singular*' in dic_temp:
        output['sgen'].append(dic_temp['Genitiv Singular*'][0])

    output['pnom'] = dic_temp['Nominativ Plural']
    if 'Nominativ Plural*' in dic_temp:
        output['pnom'].append(dic_temp['Nominativ Plural*'][0])
    output['pacc'] = dic_temp['Akkusativ Plural']
    if 'Akkusativ Plural*' in dic_temp:
        output['pacc'].append(dic_temp['Akkusativ Plural*'][0])
    output['pdat'] = dic_temp['Dativ Plural']
    if 'Dativ Plural*' in dic_temp:
        output['pdat'].append(dic_temp['Dativ Plural*'][0])
    output['pgen'] = dic_temp['Genitiv Plural']
    if 'Genitiv Plural*' in dic_temp:
        output['pgen'].append(dic_temp['Genitiv Plural*'][0])

    output['genus'] = dic_temp['Genus'][0]
    return output
