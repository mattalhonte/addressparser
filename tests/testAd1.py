import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr

from expectations import ParseExpectations


class DesignAndConstruction(ParseExpectations):

    def __init__(self, *args, **kwds):
        super(DesignAndConstruction, self).__init__(*args, **kwds)

    def testDesignAndConstruction(self):
        'design and construction sample'
        self.checkExpectation('ad-sample1.txt', 'ad-expected1.txt')

