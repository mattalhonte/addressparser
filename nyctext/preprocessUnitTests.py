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
        'Change address with "in <Borough>" to just "<Borough>"'

        source = [r"15 86 Street in the Borough of Brooklyn"] 
        expected = [r"15 86 Street Brooklyn, NY"]
        
        processed = [preprocess.filter_boroughs(address) for address in source]

        for i in range(len(source)):
            print "ORIGINAL: " + source[i]
            print "PROCESSED: " + processed[i]
            print "EXPECTED: " + expected[i]

        self.assertEqual(processed, expected)

    

    def test_expand_directions(self):
        'Change "N 1 Street" to "North 1 Street"'

        source = [r"35 N. 1 Street Brooklyn, NY"]
        expected = ["35 NORTH 1 Street Brooklyn, NY"]
        
        processed = [preprocess.expand_directions(address) for address in source]

        for i in range(len(source)):
            print "ORIGINAL: " + source[i]
            print "PROCESSED: " + processed[i]
            print "EXPECTED: " + expected[i]

        self.assertEqual(processed, expected)


    def test_remove_number_suffixes(self):
        'Change "1st Street" to "1 Street"'

        source = [r"35 1st Street Brooklyn, NY"]
        expected = ["35 1 Street Brooklyn, NY"]
        
        processed = [preprocess.remove_number_suffixes(address) for address in source]

        for i in range(len(source)):
            print "ORIGINAL: " + source[i]
            print "PROCESSED: " + processed[i]
            print "EXPECTED: " + expected[i]

        self.assertEqual(processed, expected)


    def test_no_space_commas(self):
        'Change "Brooklyn , NY" to "Brooklyn, NY"'

        source = [r"35 1 Street Brooklyn , NY"]
        expected = ["35 1 Street Brooklyn, NY"]
        
        processed = [preprocess.no_space_commas(address) for address in source]

        for i in range(len(source)):
            print "ORIGINAL: " + source[i]
            print "PROCESSED: " + processed[i]
            print "EXPECTED: " + expected[i]

        self.assertEqual(processed, expected)

    def test_add_implied_street_to_dir_street(self):
        'Change "North 1 Brooklyn, NY" to "North 1 Street Brooklyn, NY"'

        source = [r"35 North 1 Brooklyn, NY"]
        expected = ["35 North 1 STREET Brooklyn, NY"]
        
        processed = [preprocess.add_implied_street_to_dir_street(address) for address in source]

        for i in range(len(source)):
            print "ORIGINAL: " + source[i]
            print "PROCESSED: " + processed[i]
            print "EXPECTED: " + expected[i]

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



