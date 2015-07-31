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

    def checkExpectation(self, source, expected, testFunction, verbose=True):
        addresses = [testFunction(a) for a in source]
        if verbose:
            print 'source: %s' % source
            print 'expected: %s' % expected
            print 'got: %s' % addresses
        for loc in addresses:
            self.assertIn(loc, expected)
            expected.remove(loc)
        self.assertEqual(expected, [])


    def test_filter_boroughs(self):
        'Change address with "in <Borough>" to just "<Borough>"'

        source = [r"15 86 Street in the Borough of Brooklyn",
                r"66 John Street, in the Borough of Manhattan"
                r"11 Carmine Street in the Borough of Manhattan"
                r"135 N 5th St in the Borough of Brooklyn"
                r"1483 1st Ave in the Borough of Manhattan"
                r"33 W 54th St in the Borough of Manhattan"
                r"343 BROOME STREET in the Borough of Manhattan"
                r"2014 Broadway in the Borough of Manhattan"
                r"92 2nd Ave in the Borough of Manhattan"
                ] 
        expected = [r"15 86 Street Brooklyn, NY"
                r"66 John Street Manhattan, NY"
                r"11 Carmine Street Manhattan, NY"
                r"135 N 5th St Manhattan, NY"
                r"1483 1st Ave Manhattan, NY"
                r"Manhattan, NY"
                r"33 W 54th St Manhattan, NY"
                r"343 BROOME STREET Manhattan, NY"
                r"92 2nd Ave Manhattan, NY"
                ]

        self.checkExpectation(source, expected, preprocess.filter_boroughs)
    

    def test_expand_directions(self):
        'Change "N 1 Street" to "North 1 Street"'

        source = [r"35 N. 1 Street Brooklyn, NY"
                r"365 PARK AVE S Manhattan, NY"
                r"3233 E Tremont Ave Bronx, NY"
                r"60 W 55th St Manhattan, NY"]
        expected = [r"35 NORTH 1 Street Brooklyn, NY"
                r"365 PARK AVE SOUTH Manhattan, NY"
                r"3233 EAST Tremont Ave Bronx, NY"
                r"60 WEST 55th St Manhattan, NY"]
        
        self.checkExpectation(source, expected, preprocess.expand_directions)


    def test_remove_number_suffixes(self):
        'Change "1st Street" to "1 Street"'

        source = [r"35 1st Street Brooklyn, NY"
                r"92 2nd Ave Manhattan, NY"
                r"1576 3rd Ave Manhattan, NY"
                r"400 W 14th St Manhattan, NY"
                r"223 5th Ave Brooklyn, NY"]
        expected = ["35 1 Street Brooklyn, NY"
                r"92 2nd Ave Manhattan, NY"
                r"1576 3rd Ave Manhattan, NY"
                r"400 W 14th St Manhattan, NY"
                r"223 5th Ave Brooklyn, NY"]

        self.checkExpectation(source, expected, preprocess.remove_number_suffixes)


    def test_no_space_commas(self):
        'Change "Brooklyn , NY" to "Brooklyn, NY"'

        source = [r"35 1 Street Brooklyn , NY"]
        expected = ["35 1 Street Brooklyn, NY"]
        
        self.checkExpectation(source, expected, preprocess.no_space_commas)

    def test_add_implied_street_to_dir_street(self):
        'Change "North 1 Brooklyn, NY" to "North 1 Street Brooklyn, NY"'

        source = [r"35 North 1 Brooklyn, NY"
                r"241 West 97 Manhattan, NY"
                r"10 W 15 Manhattan, NY"
                r"115 E. 23 Manhattan, NY"]
        expected = ["35 North 1 STREET Brooklyn, NY"
                "241 West 97 STREET Manhattan, NY",
                r"10 W 15 STREET Manhattan, NY"
                r"115 E. 23 STREET Manhattan, NY"]

        self.checkExpectation(source, expected, preprocess.add_implied_street_to_dir_street)






#    def testXXX(self):
#        'put test description here'
#
#        source = r""
#        expected = r""
#
#        processed = preprocess.X(source)
#
#        self.assertEqual(processed, expected)



