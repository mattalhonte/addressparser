import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
import os.path
import unittest
# import codecs

from nyctext import preproces


@SkipTest
class testPreprocess(unittest.TestCase):
    '''Tests individual functions in preprocess.py
    '''

    def test_filter_boroughs(self):
        'put test description here'

        source = r"15 86 Street in Brookln" 
        expected = r"15 86 Street, Brooklyn, NY"
        
        processed = preprocess.filter_boroughs(source)

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



