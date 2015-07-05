import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
from expectations import ParseExpectations


class StreetAbbreviations(ParseExpectations):

    def __init__(self, *args, **kwds):
        super(StreetAbbreviations, self).__init__(*args, **kwds)

    def testHandleStreetAbbreviation(self):
        'expand street abbreviations'
        self.checkExpectation('ad-sample6.txt', 'ad-expected6.txt')
