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

    if 'error' in result['body']:
        if result['body']['error']['code'] == 'missingtitle':
            return {'error': 'Fehler: {}'.format('Wort wurde im tschechischen Wiktionary nicht gefunden!')}
        else:
            return {'error': 'Fehler: {}'.format(result['body']['error']['info'])}
    else:
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

    if 'Nominativ Plural' in dic_temp:
        output['pnom'] = dic_temp['Nominativ Plural']
    elif 'Nominativ Plural 1' in dic_temp:
        output['pnom'] = dic_temp['Nominativ Plural 1']
    if 'Nominativ Plural*' in dic_temp:
        output['pnom'].append(dic_temp['Nominativ Plural*'][0])

    if 'Akkusativ Plural' in dic_temp:
        output['pacc'] = dic_temp['Akkusativ Plural']
    elif 'Akkusativ Plural 1' in dic_temp:
        output['pacc'] = dic_temp['Akkusativ Plural 1']
    if 'Akkusativ Plural*' in dic_temp:
        output['pacc'].append(dic_temp['Akkusativ Plural*'][0])

    if 'Dativ Plural' in dic_temp:
        output['pdat'] = dic_temp['Dativ Plural']
    elif 'Dativ Plural 1' in dic_temp:
        output['pdat'] = dic_temp['Dativ Plural 1']
    if 'Dativ Plural*' in dic_temp:
        output['pdat'].append(dic_temp['Dativ Plural*'][0])

    if 'Genitiv Plural' in dic_temp:
        output['pgen'] = dic_temp['Genitiv Plural']
    elif 'Genitiv Plural 1' in dic_temp:
        output['pgen'] = dic_temp['Genitiv Plural 1']
    if 'Genitiv Plural*' in dic_temp:
        output['pgen'].append(dic_temp['Genitiv Plural*'][0])

    output['genus'] = dic_temp['Genus'][0]
    return output


def standardize_german_verb_json(dic_temp):
    """
    Standardize German verb after dictifying
    """
    output = {}
    output['spre1'] = dic_temp['Präsens_ich']
    if 'Präsens_ich*' in dic_temp:
        output['spre1'].append(dic_temp['Präsens_ich*'][0])
    output['spre2'] = dic_temp['Präsens_du']
    if 'Präsens_du*' in dic_temp:
        output['spre2'].append(dic_temp['Präsens_du*'][0])
    output['spre3'] = dic_temp['Präsens_er, sie, es']
    if 'Präsens_er, sie, es*' in dic_temp:
        output['spre3'].append(dic_temp['Präsens_er, sie, es*'][0])
    output['ppre1'] = [dic_temp['german'], ]
    output['ppre2'] = output['spre3']
    output['ppre3'] = [dic_temp['german'], ]
    output['aux'] = dic_temp['Hilfsverb']

    return output


def get_wikitext_extended(verb):
    """
    Gets wikitext with expanded templates, used for getting Flexion:<Verb> for
    German verbs
    """
    verb = urllib.parse.quote(verb)
    QUERY = ("https://de.wiktionary.org/w/api.php?"
             "action=parse&"
             "format=json&"
             "page={}&"
             "prop=wikitext&"
             "utf8=1&"
             "redirects&"
             "formatversion=1").format(verb)
    with urlopen(QUERY) as url:
        http_info = url.info()
        raw_data = url.read().decode(http_info.get_content_charset())
    project_info = json.loads(raw_data)
    result = {'headers': http_info.items(), 'body': project_info}
    wikitext = result['body']['parse']['wikitext']['*']

    wikitext = urllib.parse.quote(wikitext)
    QUERY = ("https://de.wiktionary.org/w/api.php?"
             "action=expandtemplates&"
             "format=json&"
             "utf8=1&"
             "text={}&"
             "prop=wikitext&").format(wikitext)
    with urlopen(QUERY) as url:
        http_info = url.info()
        raw_data = url.read().decode(http_info.get_content_charset())
    project_info = json.loads(raw_data)
    wk = project_info['expandtemplates']['wikitext']
    return wk


def get_flexion(word):
    wk = wtp.parse(get_wikitext_extended('Flexion:{}'.format(word)))

    PRESENT = '[[Hilfe:Präsens|Präsens]]'
    PRETERITUM = '[[Hilfe:Präteritum|Präteritum]]'
    FUTUR1 = '[[Hilfe:Futur|Futur I]]'

    output = {
        "present":
        {"active": {
            "indicative": {
                "0": '',
                "1": '',
                "2": '',
                "3": '',
                "4": '',
                "5": ''
            }
        }},
            "preterite":
                {"active": {
                    "indicative": {
                        "0": '',
                        "1": '',
                        "2": '',
                        "3": '',
                        "4": '',
                        "5": ''
                    }
                }},
            "futur1":
                {"active": {
                    "indicative": {
                        "0": '',
                        "1": '',
                        "2": '',
                        "3": '',
                        "4": '',
                        "5": ''
                    }
                }
        }}

    for section in wk.sections:
        if 'Indikativ' in section.title:
            for table in section.tables:
                for i in range(len(table.data())):
                    if PRESENT in table.data()[i][0]:
                        for ind in range(len(table.data()[i + 2])):
                            if 'Indikativ' in table.data()[i + 2][ind]:
                                break
                        for j in range(6):
                            word = table.data()[i + 3 + j][ind].split(' ')[-1]
                            output["present"]["active"]["indicative"][str(
                                j)] = word

                    if PRETERITUM in table.data()[i][0]:
                        for ind in range(len(table.data()[i + 2])):
                            if 'Indikativ' in table.data()[i + 2][ind]:
                                break
                        for j in range(6):
                            word = table.data()[i + 3 + j][ind].split(' ')[-1]
                            output["preterite"]["active"]["indicative"][str(
                                j)] = word

                    if FUTUR1 in table.data()[i][0]:
                        for ind in range(len(table.data()[i + 2])):
                            if 'Indikativ' in table.data()[i + 2][ind]:
                                break
                        for j in range(6):
                            word = table.data()[i + 3 + j][ind].split(' ')
                            word = word[-2] + ' ' + word[-1]
                            output["futur1"]["active"]["indicative"][str(
                                j)] = word
    return output


def normalize_czech_verb_flexion(t):
    output = {
        "present": {
            "0": t['spre1'],
            "1": t['spre2'],
            "2": t['spre3'],
            "3": t['ppre1'],
            "4": t['ppre2'],
            "5": t['ppre3']},
        "imperative": {
            "s": t['simp2'],
            "p": t['pimp2'],
            "1pp": t['pimp1'],
        },
        "participle": {
            "active": {
                "sm": t['sactm'],
                "sf": t['sactf'],
                "sn": t['sactn'],
                "pm": t['pactm'],
                "pf": t['pactf'],
                "pn": t['sactf'],
            }}
    }
    if 'spasm' in t:
        output['participle']["passive"] = {
            "sm": t['spasm'],
            "sf": t['spasf'],
            "sn": t['spasn'],
            "pm": t['ppasm'],
            "pf": t['ppasf'],
            "pn": t['spasf'],
        }
    if 'ptram' in t:
        output['transgressive'] = {
            "m": t['ptram'],
            "f": t['ptraf'],
            "p": t['ptrap'],
        }
    if 'sfut1' in t:
        output["futur"] = {
            "0": t['sfut1'],
            "1": t['sfut2'],
            "2": t['sfut3'],
            "3": t['pfut1'],
            "4": t['pfut2'],
            "5": t['pfut3'],
        }
    return output


def check_futur_one(czverb):
    budet = ['budu', 'budeš', 'bude', 'budeme', 'budete', 'budou']
    if 'futur' not in czverb['cz']:
        futur = {}
        for i in range(6):
            futur[str(i)] = [budet[i] + ' ' +
                             czverb['czech'], ] if czverb['imperfect'] else czverb['cz']['present'][str(
                                 i)]
        czverb['cz']['futur'] = futur
        return czverb
    else:
        return czverb
