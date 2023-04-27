# parsec4

Parsec 4 is an update to Parsec 3.3 by He Tao.  The changes fall into
two groups, the minor updates and the expansions, with one behavior
change. I have also provided a sketch of how to use Parsec 4 for anyone
just getting started with parsing.

## Two behavioral changes.

### Selectable string parsing

The `string` parser in Parsec 3.3 tried to match the first n characters
of the text shred to the parser's datum. This leads to some unexpected
behavior when there is a partial match of n characters where n is less
than the length of either the text shred or the target.

There are now two `string` parsers, one that follows Parsec 3.3 behavior,
and one that does not advance the index at all in cases of a partial
match. Users can select the legacy version by setting the environment
variable `PARSEC3_STRING=1`.

### Renamed the "any" parser

I changed name of the `any()` parser to `any_char()` to avoid conflicts with
Python built-in of the same name. 

## Updates to Parsec 3.3

- Added Explanatory comments to help programmers who are less familiar
  with the concepts of parsing.

- Provided more natural English grammar for He Tao's comments. His comments
  are often included *in situ*, with additional comments by me. New comments 
  are marked with a preceding and following group
  of three # characters, and the original docstrings use triple single quotes
  rather than triple double quotes.

- Revised for modern Python; no longer compatible with Python 2. This version 
  requires Python 3.8

- Inserted type hints.

- Added a `__bool__` function to the Value class.

- Changed some string searches to exploit constants in string module rather
  than str functions that might be affected by locale.

- Where practical, f-strings are used for formatting.

- An explicit `Value.__str__` is now provided so that the `Value` objects
  are more aesthetically pleasing when printed.

**NOTE:** There are a number of vestigal functions for which I have run
across no reason to use.  These functions have been left *in situ* so that
existing code that works with Parsec 3.3 will also work with Parsec 4.

## Expansions of the original.

### Application specific parsers

At University of Richmond, it is common to use parsec4 for user input
processing.  I have added:

- Symbolic names for characters commonly involved in parsing.
  They are named with standard symbols: `TAB`, `NL`, `CR`, etc.
- Many custom parsers are likely to include parsers for common programming
  elements (dates, IP addresses, timestamps). These are now included. Note
  the pattern that the core `regex` parsers are in uppercase, and the 
  corresponding `lexeme` parser is in lower case. 

```python
WHITESPACE  = regex(r'\s*', re.MULTILINE)
lexeme      = lambda p: p << WHITESPACE

DIGIT_STR   = regex(r'(0|[1-9][\d]*)')
digit_str   = lexeme(DIGIT_STR)

HEX_STR     = regex(r'[0-9a-fA-F]+')
hex_str     = lexeme(HEX_STR)

IEEE754     = regex(r'-?(0|[1-9][\d]*)([.][\d]+)?([eE][+-]?[\d]+)?')
ieee754     = lexeme(IEEE754)

IPv4_ADDR   = regex(r'(?:(?:25[0-5]|2[0-4][\d]|[01]?[\d][\d]?)\.){3}(?:25[0-5]|2[0-4][\d]|[01]?[\d][\d]?)')
ipv4_addr   = lexeme(IPv4_ADDR)

PYINT       = regex(r'[-+]?[\d]+')
pyint       = lexeme(PYINT)

TIME        = regex(r'(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)')
time        = lexeme(TIME)

TIMESTAMP   = regex(r'[\d]{1,4}/[\d]{1,2}/[\d]{1,2} [\d]{1,2}:[\d]{1,2}:[\d]{1,2}')
timestamp   = lexeme(TIMESTAMP)

US_PHONE    = regex(r'[2-9][\d]{2}[ -]?[\d]{3}[ -]?[\d]{4}')
us_phone    = lexeme(US_PHONE)
```

### Flow control

#### Errors

There is a pre-existing `ParseError` that is reserved for use by Parsec,
and it is raised when Parsec cannot continue.

#### Exceptions used for communication

I have included two `Exception` classes that are identical except
for name:  `EndOfGenerator` and `EndOfParse`. Each is derived from
`StopIteration`. Each returns a `Value` object, and you can write 
a `try` block to accept either one, both, or if you don't care, then use:

```python
try:
  something()
except StopIteration as e:
  ...
```

The meaning of the exception is up to you.

### Specific new functions for specific uses

There are two completely new functions.

1. `ascii_letter` has been added to restrict the definition of the a 
    letter to `[a-zA-Z]`. Parsec 3.3 has a `letter` parser that succeeds
    if the character is anything the Unicode standard recognizes as a 
    letter. 

2. `parser_from_strings` is a factory method to create a sequence
    of parsers for each word in a white space delimited string or a 
    sequence of strings. This is a fairly common need in the uses I 
    have had for Parsec. For example,

```python
p = parser_from_strings("hello world")
p = parser_from_strings(['hello', 'world'])
```
 
produces:

```python
p = lexeme(string("hello")) ^ lexeme(string("world"))
```

There is an option second argument that is a callable or the name of
a callable that is to be applied to a successful parse. For (a not
particularly useful) example,

```python
p = parser_from_strings("HELLO WORLD", 'str.lower')
```

A more useful argument is likely to be a `lambda` function that invokes
a Python function in the code of your current project.

## Explanation of use.

First, monadic parsers represent a type of construction mechanism rather
than a type of underlying grammar. Thus a monadic parser could be used
for either LL or LR grammars. This stackoverflow article explains the
difference between LL and LR.

https://stackoverflow.com/questions/5975741/what-is-the-difference-between-ll-and-lr-parsing

Along with writing rich parsers in Python, Parsec is useful for reading
user input and ensuring correct syntax. A top-level parser for the
allowable input may be built from the Parsec library, and the top level
parser will return the usefully transformed input. For example, if the
top level parser is named `p`, then

```python
text = input('Type in some stuff:')
results = p.parse(text)
```

.. should return the objects retrieved from parsing `text`.  The simplest
parser of all might be to read the user's text one word at a time. A
parser that retrieves a word could be written like this:

```python
import parsec4

shred = parsec4.regex(r'[a-zA-Z]+')
```

Note that `shred` is *not* the word that is retrieved. Instead, `shred`
is a *parser* that retrieves a word based on the regular expression
supplied to the function `parsec4.regex`.  Every parser has a `parse()`
function, and calling `shred` with a piece of whitespace delimited text
returns the first word of the text.

```python
>>> shred.parse('Your name')
Your
```

Of course, `shred` is not a top-level parser; it is an almost atomic
parser that merely gets the first word from a whitespace string.

## Tutorial

### Terminology.

As it proceeds, when the parser finds one or more consecutive bytes that it
both recognizes and expects that block of bytes is called a **lexeme**. A
lexeme is the smallest unit of whatever language is being parsed other
than the character. Lexemes contain characters, but do not contain other
lexemes.

A *token* is the intersection of a lexeme and the semantics of the
language, and each lexeme is a member of exactly one token class.  As an
example, let's consider the "less than or equal" operator in Python,
`<=`. It is a lexeme, and although the `<` and the `=` are lexemes in
other cases (*cf*. the less than and the assignment operator), they
are just component characters here. As a token, `<=` is a "comparison
operator token."

The current position in the text is called the index. As lexemes are
identified the index advances. In parsers like Parsec, the current
position is referred to as index zero. In other kinds of parsers, the
absolute position might be used.

### How does *any* parser work?

A parser crawls along a string from the beginning to the end if all
goes well, and stopping when it has an unrecoverable error if there
are problems.  The string is often called the *text*. At some level
deep enough inside the parser, it reads the text one byte at a time.
I mention this because while a parser may be aware of the lines in a
file containing the text, it does not proceed a line at a time like
the Python function `f.readlines()`. To treat the lines as significant,
you must parse the characters that represent the end-of-line.

### How does Parsec work?

Parsec is not itself a parser for *any* language; it is a parser
construction kit based on the idea of monads. An informal definition 
of a monad is that it is a function, generally a short function, that 
transforms its input in some way, returning the transformed object. 
Each monad, whether it is
one provided "in the can" by Parsec or something you write or create by
combining Parsec's parts, should do this:

- Accept arguments that are a `str` that your monad examines, and an
`int` that represents the offset into the `str` where your parse should
begin. This argument defaults to zero, which makes it very convenient
to write statements like `shred.parse('hello world')`

- Returns a `Value` object (defined in `parsec.py`) that is a named tuple:
`(status:bool, index:int, found:object, expected:object)`

Both Parsec 3 and Parsec 4 provide convenience factories for the concepts
of success and failure of the parser. Success is `Value(True, index,
found, None)` and failure is `Value(False, index, None, expected)`.

Other than `found` and `expected`, what do these terms mean and what
values can you expect?

- If the parsing operation is a success, the parser returns some
partial string from the `str` that meets the criteria of the parser,
and the index that is greater than or equal to where it was before the
parsing operation.

- If the parsing operation fails, it returns what it was expecting,
and the index is again, greater than or equal to the value when the
parser began.

The parser never "rewinds" the input, but it does not always advance
the index.  If the parser does not advance the index, there could be a
few reasons:

- It is performing look-ahead; it is seeing if something is present, but not operating on it.
- There is nothing left (i.e., you have reached the end of the input).
- It failed, and left the index unchanged. This is called "not consuming any input."

### How about a few more details?

Let's revisit the `shred` parser.

```python
>>> shred.parse('Your name')
Your
```

In this example, *"Your name"* is the text. It is nine characters, and
the index corresponds to the positions used by Python's slicing operator.
Conceptually, `shred` applies the regex, and extracts "Your". The index is 
now set to 4, and the remaining string is *" name"* (note the leading space).

Assuming that `shred` is a component of some other parser, the 
other parser will send `s[4:]` to the next parser to
invoke according to its rules. 

### What is the Parser part of this code?

Parsec contains a class named ... `Parser`. This class has all the
methods in it that support parsing. It also contains a method named
`bind` that turns a functional operation into a parser by wrapping the
function in Parser functionality. This is the monadic part of Parsec:
transforming a function into a Parser object.

Parsec also contains a function named `generate` that is used as a
decorator in front of a function that does the parsing. The `@generate`
decoration creates a Russian Doll structure of wrappings around the
functions. While it is not "efficient" in the computational sense,
parsers of all kinds are generally executed only once to get the result,
unlike a computation that might be executed millions of times in a data
analysis program.

### What are some common built-in parsers in Parsec?

Here is an alphabetized list of the most useful built-ins, with
a description of what is success, what it returns, and under what
circumstances the parser advances the index ("consumes input").


Parser | Description | Success |  Returns | Index 
|---|---|---|---|---|
`eof` | tests for end of a string | index at or beyond the end of the string | boolean | always unchanged.
`regex` | regular expression match of a string | matches the regex | first matched string | moved ahead by length of the matched string; unchanged on failure

### What are the "combinator" parts of Parsec?

As a translation of the Parsec library in Haskell, and getting a breath
of new-old life from operator overloading in C++, the combinator 
operations (combining simple parsers to do more complex things) is
done with overloaded operators. There are constraints:

- Python's order of operations is based on the symbols used, not the meanings of the symbols. 
- Binary operations remain binary. Uniary operations remain uniary.
- The order of operations can be controlled with parentheses, just like in Python.

The uniary operations are not of much use when "combining" elements,
so it is no surprise that the binary operators are the ones used. Let's 
use letters familiar to those of us with a little math background, and we
will call one parser `f` and the other `g`. 

Operation | Meaning 
|---|---|
`f >> g` or `f > g` | If `f` fails, return its failure. Otherwise, ignore the successful result, and execute `g`.
`f << g` | If `f` fails, return its failure. Otherwise, execute `g`. If `g` succeeds, return the success value of `f` and discard the success of `g`. Index is always the  index of `g`. 
`f < g` | If `f` fails, return its failure. Otherwise, execute `g`. If `g` succeeds, return the success value of `f` and discard the success of `g`. Use the index of `f` on success of both `f` and `g`, but the index of `g` on failure of `g`. 
`f \| g` | If `f` succeeds, return its success. If `f` failed and the index has not moved, execute `g`. If `f` failed and the index has moved, return the moved index position.
`f ^ g` | If `f` succeeds, return its success.  If `f` failed, execute `g` with the same index tried with `f`.
`f + g` | If `f` succeeds, aggregate with the result of `g` as a tuple. If `f` fails, return its failure.
`f / g` | If `f` succeeds and `g` fails, return the result of `f`. If `f` fails or `g` succeeds, then the index is unchanged. The idea is that "f is not followed by g."

## An example

At University of Richmond, we have many Linux workstations that are
used in Academic Research Computing. To avoid continually logging in on
one workstation after another to answer questions such as, "what kernel
version is running?" or "what kinds of GPUs are installed?" we have a
program that conducts a nightly inventory of the configurations. The
results are kept in a database, and we have a small non-SQL program that
allows users to ask these questions about any workstation at University
of Richmond.

We used the `cmd` module to construct the program, and we tried to make
the query language English-like and at least a little flexible. Some
workstations are named for well-known jazz musicians, and commands look
like this:

```python
show gpus on dextergordon, billieholiday
```

`show` is a legitimate command to ask about things in the database,
and the program supports others such as `help`, `status`, `exit`, and
others. Another command might be:

```python
show latest kernel of billieholiday
```

In this skeletal, imperative grammar, the request consists of:

- verb -- one of a small number of commands.
- subject -- something you want to inquire about.
- location -- a workstation or a list of workstations that you are inquiring about. 

Of course, if the verb is `exit`, then the rest of those terms might well
be irrelevant, and if `help` is the command, then there might be a topic
(subject?) but location no longer makes sense.

At the highest level we have:

```python
language = show_command ^ help_command ^ status_command ^ exit
```

## The simplest case: parsing just one word.

Let's start with the easiest of these to work with: `exit`. Just "exit"
all by itself, or in the language of Parsec, ...

```python
exit = string('exit') < eof()
```

Before we go forward, we must have a clear understanding of the expression
above. Since the type of the expressions on each side of the assignment
operator (`=`) must be the same, the left-hand-side (LHS) is a *parser*,
not something we have parsed. In fact, `exit` is a `Parsec.Parser`
that we built by combining two other `Parsec.Parser` objects, [1]
a parser whose successful result is finding the string "exit" and [2]
a parser that expects to find the end of the string.

The most common question I have been asked is "How does `exit` parse
*anything*??" The answer is that it inherits the `.parse()` method
because `string` and `eof` are constructed by the `@generate` decorator
that wraps the operations in the `Parser` class. The `<` operator Takes
a parser on both the LHS and RHS and returns a parser that also has a
`.parse()` method.

Now that we have a better understanding of the revolutionary syntax,
let's see if the above is really what we want.  It will fail if the user
adds a space, and types "exit " followed by the return key:

```python
>>> exit = string('exit') < eof()
>>> exit.parse('exit')
'exit'
>>> exit.parse('exit ')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/milesdavis/parsec4/parsec4.py", line 290, in parse
    return self.parse_partial(text)[0]
  File "/home/milesdavis/parsec4/parsec4.py", line 305, in parse_partial
    raise ParseError(result.expected, text, result.index)
parsec4.ParseError: expected: ends with EOF at <bound method ParseError.loc of ParseError('ends with EOF', 'exit ', 4)>
```

We can use the predefined `lexeme` parser that vacuums trailing whitespace
to forgive this extra keystroke:

```python
# from parsec4.py
lexeme = lambda p: p << WHITESPACE 

>>> exit = lexeme(string('exit')) < eof()
>>> exit.parse('exit ')
'exit'
```

Sadly, this will still fail if the user types " exit". In this case,
another builtin comes to our rescue, and it is almost common-sense
*readable*:

```python
exit = WHITESPACE >> lexeme(string('exit')) < eof()
```

What else could go wrong?  Many users might try leaving the program with
*quit*, so perhaps we should go with:

```python
exit = WHITESPACE >> lexeme(string('exit')) ^ lexeme(string('quit')) < eof()
```

And there is always someone with the caps-lock engaged, knowingly or
unknowingly, and that user will scream in all caps, *EXIT*. One choice
in Parsec 4 is to use the parser factory method `parser_from_strings`,
and write:

```python
exit = WHITESPACE >> parser_from_strings('exit EXIT quit QUIT') < eof()
```

Assuming the user is typing in the commands, or that they are being
read from a file, perhaps via I/O redirection, it is fair to ask this
questions: "Why not take the user's input string, `s`, and place a line
of Python in the function that reads the input that says the following?"

```python
s = s.strip().lower()
```

This approach definitely works, and parsers of all types for all languages
like well behaved data. Great idea. It is also a lot simpler than running
the text through a number of parsers. And with a nod to the efficiency
police, it is no doubt more efficient to use Python's built-ins than it
is to use Parsec's functions.

So let's go with the idea that the input has been stripped of tailing
whitespace and pounded down to lower case. What else could Parsec
offer us? Let's consider our desire to treat *exit* and *quit* as
the same action. Written as it is above, the Parsec code that says
`lexeme(string('exit')) ^ lexeme(string('quit'))` has two results (i.e.,
the text literal "exit" or the text literal "quit") when what we want
is exactly *one* result that represents the request to exit.

The reason to have only one result may not be obvious, and I will explain
it this way: We want our parser to make the decision that the user is
requesting to exit the program. The rest of our code should not care
how the user provided this information to our program. It would
be clumsy to execute the parsing code and then check again to see that
the user typed either *exit* or *quit* when either is satisfactory. Why bother to
parse the input if you still need to write the following?

```python
if user_command in ('quit', 'exit'): 
    sys.exit(os.EX_OK)
```

If we are satisfied with "exit" as the representation, then we can write
our parsing expression in Parsec's language as

```python
lexeme(string('exit')) ^ lexeme(string('quit')).result('exit')
```

Parsec offers two transformation functions that are common and useful in a
great many circumstances. The one shown above is `.result()`, a function
that provides a result value for a parser that has succeeded. Whatever
the argument to `.result()` is, that becomes the result of the parsing
operation.

In fact, the value supplied for result can be anything you think is
useful! If you were using a function lookup table, you might want to
use something like

```python
(lexeme(string('exit')) ^ lexeme(string('quit'))).result(sys.exit)
```

OK, you *could* do this. A more usual approach inside a Python parsing program
might be to define each of these results as a unique member of an 
`enum.Enum` because the value of the result is unimportant --- our program
only needs to recognize it. They are usually given names in all caps
for historical reasons; assembly languages were developed before
all computers even supported lower case letters, and it helps with
recognition.

```python
(lexeme(string('exit')) ^ lexeme(string('quit'))).result(OpCode.EXIT)
```



The conventional term for this kind of symbolic
result is an *opcode*, or if you are going down the route of full compilation,
an instruction for the processor. The opcodes might be keys in a `dict`, and the values in
this `dict` would be functions to be executed, perhaps `sys.exit` in this
case.


The other widely used transformation is `.parsecmap()`. Its argument
is a function that is applied to the successful result of the parsing.
Where `.result()` just provides a substitute value to be used explicity,
`.parsecmap()` *uses* the value of the parsing, and transforms it
in someway.

The use cases for `.parsecmap()` are different, and they fall into two
groups:

- the argument is another function that is a part of the current parser, or ...
- the argument is a native function of Python such as `math.sqrt`. 

Let's say you wanted to parse a sentence like "sqrt 3". You might go about
it this way:

```python
square_roots = lexeme(string('sqrt')) >> lexeme(ieee754).parsecmap(math.sqrt)
```

The first part recognizes the word *sqrt*. We only advance in the
`square_roots` parser if we find the text "sqrt". `lexeme` vacuums up
trailing whitespace, and then `ieee754` looks for a number. If it finds
one, it invokes `math.sqrt` on the number. It will blowup if the IEEE 
number is negative, a problem that can be dealt with in a number of ways --- 
perhaps using `cmath.sqrt` as the function.

A key point is that we can discard the *sqrt* text because we only care
about the **fact** that it was found. We need do nothing else with it.

## Let's parse a little more ....

Suppose you were writing a program to convert `csh` to `bash`. You will find
that shell and environment variables are introduced with 

```csh
set refextz = "${refext}.gz"
set colon=":"

setenv GAUSS_MDEF "$2"
```

The equivalent statements in `bash` are

```bash
refextz="${refext}.gz"
colon=":"

export GAUSS_MDEF="$2"
```

`setenv` is easier, so let's start there. We probably need a parser for 
identifiers --- tokens made of printable characters that will represent
the names of objects in the program. Depending on the specifics of the
language, this simple parser will do the job:

`identifier = lexeme(regex(r'[^\s]+'))`

That's not very elegant, so perhaps something like this, instead:

`identifier = lexeme(regex(r'[a-zA-Z][a-zA-Z0-9_]*'))`

```python
@generate
def setenv():
    yield lexeme(string('setenv'))
    k = yield identifier
    v = yield quoted ^ identifier
    raise EndOfGenerator(f'export {k}="{v}"')
```

The first statement in `setenv()` will recognize the string literal 'setenv' and removes 
the trailing space. We don't need to retrieve anything from the operation. The parser
will terminate if the string is not found, and only if execution continues are we 
in a setenv statement.

The next statement retrieves the identifier -- in this case, the name of the environment
variable. The next statement looks to see if the text is quoted and if it is not 
assumes that the text is not quoted. 

The value is communicated back to the calling parser with the `EndOfGenerator` 
exception that contains a text shred in `bash` syntax that represents the same
information.

Simple `set` statements like the ones pictured could be handled similarly, but if the
expression is something like the following, we are going to need another
parser:

`set path = (/usr/local/anaconda/anaconda3/bin $path)`

The value, in this case will be something like:

`v = quoted ^ parenthetical ^ identifier`

Note that we need to check first to see if it is quoted so that we are able
to understand expressions like this one, and correctly recognize the value
as a string rather than the result of a concatenation expression.

`set path = "(/usr/local/anaconda/anaconda3/bin $path)"`

























#### ADD MORE DOCUMENTATION HERE.

