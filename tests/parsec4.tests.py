# -*- coding: utf-8 -*-

'''
Test the basic functions of parsec.py.
'''

__author__ = 'He Tao, sighingnow@gmail.com'

import random
import unittest

from parsec4 import *

class ParsecTest(unittest.TestCase):
    '''Test the implementation of Text.Parsec. (The final test for all apis)'''
    def test_times_with_then(self) -> None :
        parser = times(letter(), 3) >> digit()
        self.assertEqual(parser.parse('xyz1'), '1')
        self.assertRaises(ParseError, parser.parse, 'xy1')
        self.assertRaises(ParseError, parser.parse, 'xyz')
        self.assertRaises(ParseError, parser.parse, 'xyzw')

    def test_many_with_then(self) -> None:
        parser = many(string('x')) >> string('y')
        self.assertEqual(parser.parse('y'), 'y')
        self.assertEqual(parser.parse('xy'), 'y')
        self.assertEqual(parser.parse('xxxxxy'), 'y')

    def test_times_with_min_and_max(self) -> None:
        parser = times(letter(), 2, 4)
        self.assertEqual(parser.parse('xy'), ['x', 'y'])
        self.assertEqual(parser.parse('xyz'), ['x', 'y', 'z'])
        self.assertEqual(parser.parse('xyzw'), ['x', 'y', 'z', 'w'])
        self.assertEqual(parser.parse('xyzwv'), ['x', 'y', 'z', 'w'])
        self.assertRaises(ParseError, parser.parse, 'x')

    def test_times_with_min_and_max_and_then(self) -> None:
        parser = times(letter(), 2, 4) >> digit()
        self.assertEqual(parser.parse('xy1'), '1')
        self.assertEqual(parser.parse('xyz1'), '1')
        self.assertEqual(parser.parse('xyzw1'), '1')
        self.assertRaises(ParseError, parser.parse, 'xy')
        self.assertRaises(ParseError, parser.parse, 'xyzw')
        self.assertRaises(ParseError, parser.parse, 'xyzwv1')
        self.assertRaises(ParseError, parser.parse, 'x1')

class ParsecPrimTest(unittest.TestCase):
    '''Test the implementation of Text.Parsec.Prim.'''

    def test_bind(self) -> None:
        nonlocals = {'piped': None}

        def binder(x:str) -> str:
            nonlocals['piped'] = x
            return string('y')

        parser = string('x').bind(binder)
        self.assertEqual(parser.parse('xy'), 'y')
        self.assertEqual(nonlocals['piped'], 'x')
        self.assertRaises(ParseError, parser.parse, 'x')

    def test_compose(self) -> None:
        parser = string('x') >> string('y')
        self.assertEqual(parser.parse('xy'), 'y')
        self.assertRaises(ParseError, parser.parse, 'y')
        self.assertRaises(ParseError, parser.parse, 'z')

    def test_joint(self) -> None:
        parser = string('x') + string('y')
        self.assertEqual(parser.parse('xy'), ('x', 'y'))
        self.assertRaises(ParseError, parser.parse, 'y')
        self.assertRaises(ParseError, parser.parse, 'z')

        nonlocals = {'changed': False}

        @generate
        def fn() -> object:
            nonlocals['changed'] = True
            yield string('y')

        parser = string('x') + fn
        self.assertRaises(ParseError, parser.parse, '1')
        self.assertEqual(nonlocals['changed'], False)

    def test_choice(self) -> None:
        parser = string('x') | string('y')
        self.assertEqual(parser.parse('x'), 'x')
        self.assertEqual(parser.parse('y'), 'y')
        self.assertRaises(ParseError, parser.parse, 'z')

        parser = string('xy') | string('xz')
        self.assertEqual(parser.parse('xy'), 'xy')
        if os.getenv('PARSEC3_STRING') == 1:
            self.assertRaises(ParseError, parser.parse, 'xz')
        else:
            self.assertEqual(parser.parse('xz'), 'xz')
        self.assertRaises(ParseError, parser.parse, 'xx')

    def test_try_choice(self) -> None:
        parser = string('x') ^ string('y')
        self.assertEqual(parser.parse('x'), 'x')
        self.assertEqual(parser.parse('y'), 'y')
        self.assertRaises(ParseError, parser.parse, 'z')

        parser = string('xy') ^ string('xz')
        self.assertEqual(parser.parse('xy'), 'xy')
        self.assertEqual(parser.parse('xz'), 'xz')

    def test_ends_with(self) -> None:
        parser = string('x') < string('y')
        self.assertEqual(parser.parse('xy'), 'x')
        self.assertRaises(ParseError, parser.parse, 'xx')

    def test_parsecmap(self) -> None:

        def mapfn(p:object) -> object:
            return p + p

        parser = string('x').parsecmap(mapfn)
        self.assertEqual(parser.parse('x'), 'xx')

    def test_parsecapp(self) -> None:

        def genfn(p:object) -> object:
            return lambda c: 'fn:' + p + c + c

        parser = string('x').parsecmap(genfn).parsecapp(string('y'))
        self.assertEqual(parser.parse('xy'), 'fn:xyy')

    def test_desc(self) -> None:
        parser = string('x')
        self.assertEqual(parser.parse('x'), 'x')
        self.assertRaises(ParseError, parser.parse, 'y')

    def test_mark(self) -> None:
        parser = many(mark(many(letter())) << string("\n"))

        lines = parser.parse("asdf\nqwer\n")

        self.assertEqual(len(lines), 2)

        (start, letters, end) = lines[0]
        self.assertEqual(start, (0, 0))
        self.assertEqual(letters, ['a', 's', 'd', 'f'])
        self.assertEqual(end, (0, 4))

        (start, letters, end) = lines[1]
        self.assertEqual(start, (1, 0))
        self.assertEqual(letters, ['q', 'w', 'e', 'r'])
        self.assertEqual(end, (1, 4))

    def test_choice_with_compose(self) -> None:
        parser = (string('\\') >> string('y')) | string('z')
        self.assertEqual(parser.parse('\\y'), 'y')
        self.assertEqual(parser.parse('z'), 'z')
        self.assertRaises(ParseError, parser.parse, '\\z')

class ParsecCombinatorTest(unittest.TestCase):
    '''Test the implementation of Text.Parsec.Combinator.'''
    def test_times(self) -> None:
        parser = times(string('x'), 2, 10)
        self.assertEqual(parser.parse('xxx'), ['x', 'x', 'x'])
        self.assertRaises(ParseError, parser.parse, 'x')
        self.assertRaises(ParseError, parser.parse, 'xyyyyyyyyyyyyyyyyyyyyyy')

        parser = times(letter(), 0)
        self.assertEqual(parser.parse(''), [])
        self.assertEqual(parser.parse('x'), [])
        self.assertEqual(parser.parse('xxxxx'), [])

    def test_count(self) -> None:
        parser = count(letter(), 3)
        self.assertEqual(parser.parse('xyz'), ['x', 'y', 'z'])
        self.assertEqual(parser.parse('xyzwwwww'), ['x', 'y', 'z'])
        self.assertRaises(ParseError, parser.parse, 'xy')

    def test_optional(self) -> None:
        parser = optional(string('xx'))
        self.assertEqual(parser.parse('xx'), 'xx')
        self.assertEqual(parser.parse('xy'), None)

    def test_optional_default(self) -> None:
        parser = optional(string('xx'), 'k')
        self.assertEqual(parser.parse('xx'), 'xx')
        self.assertEqual(parser.parse('xy'), 'k')

    def test_many(self) -> None:
        parser = many(letter())
        self.assertEqual(parser.parse('x'), ['x'])
        self.assertEqual(parser.parse('xyz'), ['x', 'y', 'z'])
        self.assertEqual(parser.parse(''), [])
        self.assertEqual(parser.parse('1'), [])

    # from #28
    def test_many_many(self) -> None:
        parser = many(many(space()))
        self.assertEqual(parser.parse('    '), [[' ', ' ', ' ', ' ']])

        parser = times(spaces(), 4, 10)
        self.assertEqual(parser.parse(''), [[], [], [], []])
        self.assertEqual(parser.parse(' '), [[' '], [], [], []])
        self.assertEqual(parser.parse('  '), [[' ', ' '], [], [], []])

    def test_many1(self) -> None:
        parser = many1(letter())
        self.assertEqual(parser.parse('x'), ['x'])
        self.assertEqual(parser.parse('xyz'), ['x', 'y', 'z'])
        self.assertRaises(ParseError, parser.parse, '')
        self.assertRaises(ParseError, parser.parse, '1')

    def test_separated(self) -> None:
        parser = separated(string('x'), string(','), 2, 4)
        self.assertEqual(parser.parse('x,x,x') , ['x', 'x', 'x'])
        self.assertEqual(parser.parse('x,x,x,'), ['x', 'x', 'x'])
        self.assertRaises(ParseError, parser.parse, 'x')
        self.assertRaises(ParseError, parser.parse, 'x,')
        self.assertRaises(ParseError, parser.parse, 'x,y,y,y,y')
        self.assertRaises(ParseError, parser.parse, 'x,y,y,y,y,')
        self.assertEqual(parser.parse('x,x,y,y' ), ['x','x'])
        self.assertEqual(parser.parse('x,x,y,y,'), ['x','x'])

        parser = separated(letter(), string(','), 0)
        self.assertEqual(parser.parse('')          , [])
        self.assertEqual(parser.parse('x')         , [])
        self.assertEqual(parser.parse('x,')        , [])
        self.assertEqual(parser.parse('x,x,x,x,x') , [])
        self.assertEqual(parser.parse('x,x,x,x,x,'), [])

        # see GH-48
        parser = separated(string('a'), string(','), 3, 3, end=False)
        r, rest = parser.parse_partial('a,a,a,')
        self.assertEqual(r, ['a', 'a', 'a'])
        self.assertEqual(rest, ',')

        parser = separated(string('a'), string(','), 3, 3, end=True)
        r, rest = parser.parse_partial('a,a,a,')
        self.assertEqual(r, ['a', 'a', 'a'])
        self.assertEqual(rest, '')

        parser = separated(string('a'), string(','), 3, 3, end=None)
        r, rest = parser.parse_partial('a,a,a,')
        self.assertEqual(r, ['a', 'a', 'a'])
        self.assertEqual(rest, '')

        parser = separated(string('a'), string(','), 3, 6, end=True)
        r, rest = parser.parse_partial('a,a,a,a.')
        self.assertEqual(r, ['a', 'a', 'a'])
        self.assertEqual(rest, 'a.')

        # see GH-49
        parser = separated(string('a'), string(','), 3, 6, end=False)
        r, rest = parser.parse_partial('a,a,a,')
        self.assertEqual(r, ['a', 'a', 'a'])
        self.assertEqual(rest, ',')

    def test_sepBy(self) -> None:
        parser = sepBy(letter(), string(','))
        self.assertEqual(parser.parse_strict('x')     , ['x'])
        self.assertEqual(parser.parse       ('x,')    , ['x'])
        self.assertEqual(parser.parse_strict('x,y,z') , ['x', 'y', 'z'])
        self.assertEqual(parser.parse       ('x,y,z,'), ['x', 'y', 'z'])
        self.assertEqual(parser.parse       ('') , [])  # nothing consumed
        self.assertEqual(parser.parse       ('1'), [])  # nothing consumed
        self.assertEqual(parser.parse       ('1,'), []) # nothing consumed

    def test_sepBy1(self) -> None:
        parser = sepBy1(letter(), string(','))
        self.assertEqual(parser.parse_strict('x')     , ['x'])
        self.assertEqual(parser.parse       ('x,')    , ['x'])
        self.assertEqual(parser.parse_strict('x,y,z') , ['x', 'y', 'z'])
        self.assertEqual(parser.parse       ('x,y,z,'), ['x', 'y', 'z'])
        self.assertRaises(ParseError, parser.parse, (''))
        self.assertRaises(ParseError, parser.parse, ('1'))
        self.assertRaises(ParseError, parser.parse, ('1,'))

    def test_endBy(self) -> None:
        parser = endBy(letter(), string(','))
        self.assertEqual(parser.parse_strict('x,')    , ['x'])
        self.assertEqual(parser.parse_strict('x,y,z,'), ['x', 'y', 'z'])
        self.assertEqual(parser.parse       ('')      , [])
        self.assertEqual(parser.parse       ('1')     , [])
        self.assertEqual(parser.parse       ('1,')    , [])
        self.assertEqual(parser.parse       ('x')     , [])
        self.assertEqual(parser.parse       ('x,')    , ['x'])

    def test_endBy1(self) -> None:
        parser = endBy1(letter(), string(','))
        self.assertRaises(ParseError, parser.parse, ('x'))
        self.assertRaises(ParseError, parser.parse_strict, ('x,y,z'))
        self.assertEqual(parser.parse_strict('x,')    , ['x'])
        self.assertEqual(parser.parse_strict('x,y,z,'), ['x', 'y', 'z'])
        self.assertEqual(parser.parse('x,y,z')        , ['x', 'y'])
        self.assertRaises(ParseError, parser.parse, (''))
        self.assertRaises(ParseError, parser.parse, ('1'))
        self.assertRaises(ParseError, parser.parse, ('1,'))

    def test_sepEndBy(self) -> None:
        parser = sepEndBy(letter(), string(','))
        self.assertEqual(parser.parse_strict('x')     , ['x'])
        self.assertEqual(parser.parse_strict('x,')    , ['x'])
        self.assertEqual(parser.parse_strict('x,y,z') , ['x', 'y', 'z'])
        self.assertEqual(parser.parse_strict('x,y,z,'), ['x', 'y', 'z'])
        self.assertEqual(parser.parse       ('')      , [])
        self.assertEqual(parser.parse       ('1')     , [])
        self.assertEqual(parser.parse       ('1,')    , [])

    def test_sepEndBy1(self) -> None:
        parser = sepEndBy1(letter(), string(','))
        self.assertEqual(parser.parse_strict('x')     , ['x'])
        self.assertEqual(parser.parse_strict('x,')    , ['x'])
        self.assertEqual(parser.parse_strict('x,y,z') , ['x', 'y', 'z'])
        self.assertEqual(parser.parse_strict('x,y,z,'), ['x', 'y', 'z'])
        self.assertRaises(ParseError, parser.parse, (''))
        self.assertRaises(ParseError, parser.parse, ('1'))
        self.assertRaises(ParseError, parser.parse, ('1,'))

    def test_excepts(self) -> None:
        parser = (string('<') / string('=')) ^ string('<=')
        self.assertEqual(parser.parse('<'), "<")
        self.assertEqual(parser.parse('<='), "<=")

        parser = string('<') ^ string('<=')
        self.assertEqual(parser.parse('<'), "<")
        self.assertEqual(parser.parse('<='), "<")

    def test_fix(self) -> None:
        @Parser
        @fix
        def bracketed_expr(recur:object) -> object:
            return (string("(") >> recur << string(")")) | any_char()

        self.assertEqual(bracketed_expr.parse("((x))"), 'x')


class ParsecCharTest(unittest.TestCase):
    '''Test the implementation of Text.Parsec.Char.'''

    def test_string(self) -> None:
        parser = string('x')
        self.assertEqual(parser.parse('x'), 'x')
        self.assertRaises(ParseError, parser.parse, 'y')

    def test_regex(self) -> None:
        parser = regex(r'[0-9]')
        self.assertEqual(parser.parse('1'), '1')
        self.assertEqual(parser.parse('4'), '4')
        self.assertRaises(ParseError, parser.parse, 'x')

    def test_ieee754(self) -> None:
        parser = ieee754
        self.assertEqual(parser.parse('1'), '1')
        self.assertEqual(parser.parse('1.0'), '1.0')
        self.assertEqual(parser.parse('-1'), '-1')
        self.assertRaises(ParseError, parser.parse, 'x')

    def test_parsec4_string(self) -> None:
        parser = parser_from_strings("xxx xx x yx")
        self.assertEqual(parser.parse("x"), "x")
        self.assertEqual(parser.parse("yx"), "yx")  ## test passed
        self.assertEqual(parser.parse("xx"), "xx") ##test failed
        self.assertRaises(ParseError, parser.parse, 'yy') 

    def test_sting_strict(self) -> None:
        parser = parser_from_strings("x xx xxx xy")
        self.assertEqual(parser.parse_strict("x"), "x")
        self.assertEqual(parser.parse_strict("xx"), "xx")
        self.assertEqual(parser.parse_strict("xxx"), "xxx")
        

class ParserGeneratorTest(unittest.TestCase):
    '''Test the implementation of Parser Generator.(generate)'''
    def test_generate_desc(self) -> None:
        description = 'expected description for fn'

        @generate(description)
        def fn() -> None:
            yield string('t')

        with self.assertRaises(ParseError) as err: fn.parse('x')

        ex = err.exception

        self.assertEqual(ex.expected, description)
        self.assertEqual(ex.text, 'x')
        self.assertEqual(ex.index, 0)

    def test_generate_backtracking(self) -> None:
        @generate
        def xy() -> None:
            yield string('x')
            yield string('y')
            assert False
        parser = xy | string('z')
        # should not finish executing xy()
        self.assertEqual(parser.parse('z'), 'z')

    def test_generate_raise(self) -> None:

        # `return` with argument inside generator is not supported in Python 2.
        # Instead, we can raise a `StopIteration` directly with the intended
        # result in generator for Python 2.
        #
        # Before Python 3.3, the `StopIteration` didn't have the `value` attribute,
        # we need to assign the attribute manually.
        #
        # See #15.

        @generate
        def xy() -> None:
            yield string('x')
            yield string('y')
            r = StopIteration('success')
            r.value = 'success'  # for pre-3.3 Python
            raise r

        parser = xy
        self.assertEqual(parser.parse('xy'), 'success')

if __name__ == '__main__':
    unittest.main()
