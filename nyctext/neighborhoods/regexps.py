import re
from throughways import names as throughway_names

def make_neighorbood_regex(lHoods):

    # neighborhood name:
    #    begins with a whitespace
    #    ends with a comma, or whitespace
    lst = [r'\s%s[\s,]' % n for n in lHoods]
    lst = '|'.join(lst)

    # Don't match if neighborhood is followed
    # by a thoroughfare name
    # lst = '(%s)(?!(Ave|Avenue|Boulevard|Street|Parkway|Piers|Plaza|Place|Road))' % lst
    lst = '(%s)(?!%s)' % (lst, throughway_names)
    return  re.compile(lst, re.I)

def make_neighorbood_regex(lHoods, city):

    hoods = '|'.join(lHoods)

    # Don't match if neighborhood is followed
    # by a thoroughfare name
    names = throughway_names[1:-1]  # remove parens
    names = '(%s|%s|north|south|east|west|n[\s\.,]|s[\s\.,]|w[\s\.,]|e[\s\.,])' % (names, city)

    rex = '\\s((%s)(\\s|,))(?!([\\s|,]*(%s)))' % (hoods, names)
    return re.compile(rex, re.I)
