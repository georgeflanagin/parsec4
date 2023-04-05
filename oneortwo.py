# -*- coding: utf-8 -*-
import typing
from   typing import *

min_py = (3, 8)

###
# Standard imports, starting with os and sys
###
import os
import sys
if sys.version_info < min_py:
    print(f"This program requires Python {min_py[0]}.{min_py[1]}, or higher.")
    sys.exit(os.EX_SOFTWARE)

###
# Other standard distro imports
###
import argparse
import contextlib
import getpass
mynetid = getpass.getuser()


###
# From hpclib
###
import linuxutils
from   urdecorators import trap

###
# imports and objects that are a part of this project
###
verbose = False
import parsec4
from   parsec4 import *

###
# Credits
###
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2023'
__credits__ = None
__version__ = 0.1
__maintainer__ = 'George Flanagin'
__email__ = []
__status__ = 'in progress'
__license__ = 'MIT'

vocab_word = lexeme(string('one')) | lexeme(string('two')) | lexeme(string('zero')) | lexeme(string('THREE')) | lexeme(string('four'))

next_word = regex(r'[a-z][-_a-z0-9]*')

one_or_two_words = vocab_word + optional(vocab_word)

and_one_more = one_or_two_words + next_word

# Test that all the vocab word parsers do things right.
try:
    print(vocab_word.parse('zero'))
    print(vocab_word.parse('THREE'))
    print(vocab_word.parse('one'))
    print(vocab_word.parse('two'))
    print(vocab_word.parse('four'))
    print(vocab_word.parse('two six'))
    print(vocab_word.parse('five')) # an error.

except Exception as e:
    print(e)

try:
    print(one_or_two_words.parse('one two programmers'))
    print(one_or_two_words.parse('two programmers'))
    print(one_or_two_words.parse('zero one two programmers'))
    print(one_or_two_words.parse('programmers')) # an error

except Exception as e:
    print(e)



try:
    print(and_one_more.parse('one two programmers'))
    print(and_one_more.parse('two programmers'))
    print(and_one_more.parse('zero one two programmers'))
    print(and_one_more.parse('programmers')) # an error

except Exception as e:
    print(e)


