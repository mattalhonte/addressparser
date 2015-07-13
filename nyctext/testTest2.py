import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
import os.path
import unittest
# import codecs

import preprocess


class testPreprocess(unittest.TestCase):
    '''Tests individual functions in preprocess.py
    '''

    def test_filter_boroughs(self):
        'put test description here'

        source = r"15 86 Street in the Borough of Brooklyn" 
        expected = r"15 86 Street Brooklyn, NY"
        
        processed = preprocess.filter_boroughs(source)

        print "ORIGINAL: " + source
        print "PROCESSED: " + processed
        print "EXPECTED: " + expected

        self.assertEqual(processed, expected)

#    def testXXX(self):
#        'put test description here'
#
#        source = r""
#        expected = r""
#
#        processed = preprocess.X(source)
#
#        self.assertEqual(processed, expected)



