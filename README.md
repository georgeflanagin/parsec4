# parsec4

Parsec 4 is an update to Parsec 3.3 by He Tao.
The changes fall into two groups, the minor updates and the
expansions, with one behavior change. I have also provided a sketch of how to use
Parsec 4 for anyone just getting started with parsing.

## One behavioral change / bug fix?

The `string` parser in Parsec 3.3 tried to match the first
n characters of the text shred to the parser's datum. This leads
to some unexpected behavior when there is a partial match of 
n characters where n is less than the length of either the 
text shred or the target.

There are now two `string` parsers, one that follows Parsec 3.3
behavior, and one that does not advance the index at all in cases
of a partial match. Users can select the legacy version by
setting the environment variable `PARSEC3_STRING`. No particular
value is required --- just set or not set.

## Minor updates to Parsec 3.3

- Added Explanatory comments.
- Provided more natural English grammar for He Tao's comments. His comments
  are included. New comments are marked with a preceding and following group
  of three # characters, and the original docstrings use triple single quotes
  rather than triple double quotes.
- Revised for modern Python; no longer compatible with Python 2. This version
- Require Python 3.8
- Inserted type hints.
- Added a `__bool__` function to the Value class.
- Changed some string searches to exploit constants in string module rather
  than str functions that might be affected by locale.
- Changed name of `any()` function to `any_char()` to avoid conflicts with 
  Python built-in of the same name.
- Where practical, f-strings are used for formatting.

## Expansions of the original.

### General additions

At University of Richmond, it is common to use parsec4 for user input processing.
I have added a 

- A number of definitions of characters are provided, and they
  are named as standard symbols: `TAB`, `NL`, `CR`, etc.
- Many custom parsers are likely to include parsers for common programming
  elements (dates, IP addresses, timestamps). These are now included.
  
```python
WHITESPACE  = regex(r'\s*', re.MULTILINE)
lexeme = lambda p: p << WHITESPACE

DIGIT_STR   = regex(r'(0|[1-9][\d]*)')
digit_str   = lexeme(DIGIT_STR)

HEX_STR     = regex(r'[0-9a-fA-F]+')
hex_str     = lexeme(DIGIT_STR)

IEEE754     = regex(r'-?(0|[1-9][\d]*)([.][\d]+)?([eE][+-]?[\d]+)?')
ieee754     = lexeme(IEEE754)

IPv4_ADDR   = regex(r'(?:(?:25[0-5]|2[0-4][\d]|[01]?[\d][\d]?)\.){3}(?:25[0-5]|2[0-4][\d]|[01]?[\d][\d]?)')
ipv4_addr   = lexeme(IPv4_ADDR)

PYINT       = regex(r'[-+]?[\d]+')
pyint       = lexeme(PYINT)

TIME        = regex(r'(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)')

TIMESTAMP   = regex(r'[\d]{1,4}/[\d]{1,2}/[\d]{1,2} [\d]{1,2}:[\d]{1,2}:[\d]{1,2}')

US_PHONE    = regex(r'[2-9][\d]{2}[ -]?[\d]{3}[ -]?[\d]{4}')
```

### Flow control

I have included two `Exception` classes that are identical except for name.
`EndOfGenerator` and `EndOfParse`. Each returns a `Value` object, and you
can write a `try` block to accept either one, both, or if you don't care, then
use:

```python
try:
  something()
except StopIteration as e:
  ...
```
The meaning of the exception is up to you.

There is a pre-existing `ParseError` that is reserved for use by Parsec,
and it is raised when Parsec cannot continue.

### Specific new functions for specific uses

There are two completely new functions.

1. `ascii_letter` has been added to restrict the definition of the a 
    letter to `[a-z][A-Z]`. Parsec 3.3 has a `letter` parser that succeeds
    if the character is anything the Unicode standard recognizes as a 
    letter. 

2. `parser_from_strings` is a factory method to create a sequence
    of parsers for each word in a white space delimited string or a sequence of
    strings. This is
    a fairly common need in the uses I have had for Parsec. For example,

```python
p = parser_from_strings("hello world")
p = parser_from_strings(['hello', 'world'])
```
 
produces:

```python
lexeme(string("hello")) ^ lexeme(string("world"))
```

There is an option second argument that is a callable or the name of a
callable that is to be applied to a successful parse. For (a not particularly useful) example, 

```python
p = parser_from_strings("HELLO WORLD", 'str.lower')
```

A more useful argument is likely to be a `lambda` function that invokes a
Python function in the code of your current project.

## Explanation of basic use.

First, monadic parsers represent a type of construction mechanism
rather than a type of underlying grammar. Thus a monadic parser could
be used for either LL or LR grammars. This stackoverflow article
explains the difference between LL and LR.

https://stackoverflow.com/questions/5975741/what-is-the-difference-between-ll-and-lr-parsing

Along with writing rich parsers in Python, Parsec is useful for reading 
user input and ensuring correct syntax. A top-level parser for the allowable
input may be built from the Parsec library, and the top level parser will
return the usefully transformed input. For example, if the top level parser
is named `p`, then

```python
    text = input('Type in some stuff:')
    results = p.parse(text)
```

.. will return a list of the objects retrieved from parsing `text`.

The simplest parser of all might be to read the user's text one word
at a time. A parser that retrieves a word could be written like this:

```python
import parsec4

shred = parsec4.regex(r'[a-z][A-Z][-_a-zA-Z0-9]*')
```

Note that `shred` is *not* the word that is retrieved. Instead, `shred`
is a *parser* that retrieves a word based on the regular expression 
supplied to the function `parsec4.regex`.

Every parser has a `parse()` function, and calling `shred` with a piece of
whitespace delimited text returns the first word of the text.

```python
>>> shred.parse('Your name')
Your
```

Of course, `shred` is not a top-level parser; it is an almost atomic
parser that merely gets a word from a whitespace string. 

## How does Parsec work?

Parsec is not itself a parser for *any* language; it is a parser construction
kit based on the idea of monads. Each monad, whether it is one provided "in the can" 
by Parsec or something you write or create by combining Parsec's parts, should do this:

- Accept arguments that are a `str` that your monad examines, and an `int` that
    represents the offset into the `str` where your parse should begin. This argument
    defaults to zero, which makes it very convenient to write statements like 
    `shred.parse('hello world')`
    
- Returns a `Value` object (defined in `parsec.py`) that is a named tuple: `(status:bool, index:int, found:object, expected:object)`

Both Parsec 3 and Parsec 4 provide convenience factories for the concepts of success and failure
of the parser. Success is `Value(True, index, found, None)` and failure is
`Value(False, index, None, expected)`. 
    
Other than `found` and `expected`, what do these terms mean and what values can
you expect?
    
- If the parsing operation is a success, the parser returns some partial string 
    from the `str` that meets the criteria of the parser, and the index that is 
    greater than or equal to where it was before the parsing operation.
- If the parsing operation fails, it returns what it was expecting, and the index
  is again, greater than or equal to the value when the parser began.
  
The parser never "rewinds" the input, but it does not always advance the index. 
If the parser does not advance the index, there could be a few reasons:

- It is performing look-ahead; it is seeing if something is present, but not operating on it.
- There is nothing left (i.e., you have reached the end of the input).
- It failed, and left the index unchanged. This is called "not consuming any input."

## What is the Parser part of this code?

Parsec contains a class named ... `Parser`. This class has all the methods in it that support
parsing. It also contains a method named `bind` that turns a functional operation into a 
parser by wrapping the function in Parser functionality. This is the monadic part of Parsec,
transforming a function into a Parser object. Huh? 



#### ADD MORE DOCUMENTATION HERE.

