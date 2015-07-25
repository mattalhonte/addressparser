import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
import os.path
import unittest
# import codecs

from nyctext import nycaddress as parser

import preprocess

@SkipTest
class XXXXX(unittest.TestCase):
    '''Add description HERE
    '''

    def checkExpectation(self, source, expected, testFunction, verbose=True):
        addresses = testFunction(source)
        if verbose:
            print 'source: %s' % source
            print 'expected: %s' % expected
            print 'got: %s' % addresses
        for loc in addresses:
            self.assertIn(loc, expected)
            expected.remove(loc)
        self.assertEqual(expected, [])

    def testXXX(self):
        'put test description here'

        source = ''
        expected = ''

        self.checkExpectation(source, expected)


