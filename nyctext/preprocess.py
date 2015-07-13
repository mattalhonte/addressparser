# -*- coding: utf-8 -*-
__author__ = "C. Sudama, Matthew Alhonte"
__credits__ = ["Mikael Hveem", ]
__license__ = "Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0"

import re
import historicMappings

from neighborhoods import rex_neighborhoods_queens
from neighborhoods import rex_neighborhoods_brooklyn
from neighborhoods import rex_neighborhoods_bronx
from neighborhoods import rex_neighborhoods_statenIsland
from neighborhoods import rex_neighborhoods_manhattan


def filter_boroughs(text):
    _rex_boroughs = re.compile('(in\s+the\s+)Borough\s+of\s+'
                               '(Brooklyn|Queens|Staten\s+Island|Bronx)',
                               re.I)

    _rex_manhattan = re.compile('(in\s+the\s+)Borough\s+of\s+'
                                '(Manhattan)',
                                re.I)
    text = _rex_manhattan.sub('Manhattan, NY', text)
    text = _rex_boroughs.sub('\\2, NY', text)
    return text


def filter_blockcodes(text):
    # match these...
    # BOROUGH OF QUEENS 15-5446-Block 1289, lot 15–
    # BOROUGH OF QUEENS 15-7412 - Block 8020, lot 6–
    # BOROUGH OF BROOKLYN 15-7494-Block 2382, lot 3–
    # BOROUGH OF MANHATTAN 15-6223 – Block 15, lot 22-
    _b = 'brooklyn|bronx|manhattan|staten\s+island|queens'
    _rex_blockcodes = "BOROUGH\s+of\s+(%s)\s+[^b]{7,15}Block\s+\d+,\slot\s\d+.\s*" % _b
    _rex_blockcodes = re.compile(_rex_blockcodes, re.I)
    return '.\n'.join([para for para in _rex_blockcodes.split(text)])




#The Street Name Dictionary uses 'NORTH' rather than 'N' or 'N.' or any other variation on that theme.  Interestingly, this is
#actually inconsistent with city signage - there is no streetsign that says "NORTH 1", it reads "N 1".  Still, streetsigns 
#are not machine-readable, while the DOT's SND is nice and digitized
def expand_directions(myString):
    myString = re.sub(r"""(?<=\s)(N\.?)(?=\s)""", "NORTH", myString)
    myString = re.sub(r"""(?<=\s)(S\.?)(?=\s)""", "SOUTH", myString)
    myString = re.sub(r"""(?<=\s)(E\.?)(?=\s)""", "EAST", myString)
    myString = re.sub(r"""(?<=\s)(W\.?)(?=\s)""", "WEST", myString)
    return myString

#Street name dictionary doesn't give suffixes to digits (though it does give it to spelled-out words, so we get "FIFTH AVENUE" and 
#"5 AVENUE", but not "5TH AVENUE").  This is again inconsistent with most signage, buuut machine-readable
def remove_number_suffixes(myString):
    return re.sub(r"""(\d)(st|nd|rd|th)""", r"""\1""", myString)

#No reason to have a space before a comma, in NYC addresses or otherwise
def no_space_commas(myString):
    return myString.replace(r""" ,""", r""",""")

# regex for streets with a direction but not the word "street". Works on addresses that have already been extracted, then extracts the street name
numberStreet = re.compile(r"""(?<=\d\s) #It'll be one space away from a digit
                              (?P<Direction>North|South|East|West) #It has a direction (either written or abbreviated)
                              (?P<streetNumber>\s\d{1,3}) #Street number
                              (?P<borAndState>(.*)(?<!Street),\s(New\sYork|Brooklyn|Queens|Staten\s+Island|Bronx),\s(New\sYork|NY))""",
                              re.IGNORECASE | re.X)

#Let's try and add the word "street" in a few places it's clearly implied
def add_implied_street_to_dir_street(myString):
    return re.sub(numberStreet, r"""\1\2 STREET\3""", myString)


def filter_ny_ny(text):
    _ny_ny = r"\b((new\s*york|ny)\b[\s,]*)\b(new\s*york|ny)\b"
    _ny_ny = re.compile(_ny_ny, re.I)
    return _ny_ny.sub('Manhattan, NY.\n', text)


def filter_neighborhoods(text):
    text = rex_neighborhoods_queens.sub(', \\1, Queens, ', text)

    text = rex_neighborhoods_brooklyn.sub(', \\1, Brooklyn, ', text)

    text = rex_neighborhoods_statenIsland.sub(', \\1, Staten Island, ', text)

    text = rex_neighborhoods_manhattan.sub(', \\1, Manhattan, ', text)

    # Marble Hill can be both manhattan and bronx
    # if not _bronx.match(_t):
    # if 'marble hill' not in _t and 'bronx' not in _t:
    text = rex_neighborhoods_bronx.sub(', \\1, Bronx, ', text)

    text = text.replace(',,', ',')
    return text


# Entry point for preprocessing. Add more methods within this
# function
def prepare_text(text, verbose=False):
    # There should be a section of removing all unicode
    # and non ascii characters.
    #
    text = text.replace(u'\xa0', ' ')

    text = filter_boroughs(text)
    if verbose:
        print 'filter_boroughs:\n\t%s\n' % text

    text = filter_ny_ny(text)
    if verbose:
        print 'filter_ny_ny:\n\t%s\n' % text

    text = filter_blockcodes(text)
    if verbose:
        print 'filter_blockcodes:\n\t%s\n' % text

    text = historicMappings.preprocess(text)
    if verbose:
        print 'historicMappings:\n\t%s\n' % text

    text = filter_neighborhoods(text)
    if verbose:
        print 'filter_neighborhoods:\n\t%s\n' % text

    text = expand_directions(text)
    if verbose:                                         
        print 'expand_directions:\n\t%s\n' % text

    text = remove_number_suffixes(text)
    if verbose:                                         
        print 'remove_number_suffixes:\n\t%s\n' % text
  
    text = no_space_commas(text)
    if verbose:                                         
        print 'no_space_commas:\n\t%s\n' % text

    text = add_implied_street_to_dir_street(text)
    if verbose:                                         
        print 'add_implied_street_to_dir_street:\n\t%s\n' % text

    return text

def location_to_string(tree):
    return ' '.join([c[0] for c in tree]).replace(' ,', ',')


# Some filters for other address formats
# For instances such as "22 Reade Street, Spector Hall, Borough of Manhattan"
# boroughOf = re.compile(r"""(Borough\s+of\s+)
#                            (Brooklyn|Queens|Staten\s+Island|Bronx)""",
#                            re.IGNORECASE | re.VERBOSE)
#
# boroughOfManhattan = re.compile(r"""(Borough\s+of\s+)
#                            (Manhattan)""",
#                            re.IGNORECASE | re.VERBOSE)
#
# def filterBoroughOf(text):
#     return re.sub(boroughOf, r"""\g<2>, NY""", text)
#
# def filterBoroughOfManhattan(text):
#     return re.sub(boroughOfManhattan, r"""New York, NY""", text)
#
#
# # For instances such as "1 Centre Street in Manhattan"
#
# inBorough = re.compile(r"""(\sin\s)
#                            (Brooklyn|Queens|Staten\s+Island|Bronx)""",
#                            re.IGNORECASE | re.VERBOSE)
#
#
# inManhattan = re.compile(r"""(\sin\s)
#                            (Manhattan)""",
#                            re.IGNORECASE | re.VERBOSE)
#
#
# def filterInBorough(text):
#     return re.sub(inBorough, r', \g<2>, NY', text)
#
#
# def filterInManhattan(text):
#     return re.sub(inManhattan, r', New York, NY', text)
