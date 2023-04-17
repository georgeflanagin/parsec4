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

At University of Richmond, it is common to use parsec4 for user input processing.
I have added a 

- A number of definitions of characters are provided, and they
  are named as standard symbols: `TAB`, `NL`, `CR`, etc.
- Many custom parsers are likely to include parsers for common programming
  elements (dates, IP addresses, timestamps). These are now included. 

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

Every parser has a `parse()` function, and calling it with a piece of
whitespace delimited text returns the first word of the text.

```python
>>> shred.parse('Your name')
Your
```

Of course, `shred` is not a top-level parser; it is an almost atomic
parser that merely gets a word from a whitespace string. If whitespace
delimited text is all you have, then something like this will do:

#### ADD MORE DOCUMENTATION HERE.

