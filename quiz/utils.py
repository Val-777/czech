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
    if gender_de is 'm':
        return masculine[case]
    elif gender_de is 'f':
        return feminine[case]
    elif gender_de is 'n':
        return neutral[case]
