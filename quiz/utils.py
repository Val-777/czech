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


def get_wikitext(czech):
    """
    Gets the wikitext for the passed in Czech word, which is then parsed with the wikitextparser,
    which breaks it up into a list of Section objects
    """
    czech = urllib.parse.quote(czech)
    QUERY = ("https://cs.wiktionary.org/w/api.php?"
             "action=parse&"
             "format=json&"
             "uselang=cs&"
             "page={}&"
             "prop=wikitext&"
             "utf8=1&"
             "formatversion=1").format(czech)
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


def german_article(gender_de):
    if gender_de is 'M':
        return 'der'
    elif gender_de is 'F':
        return 'die'
    elif gender_de is 'N':
        return 'das'
