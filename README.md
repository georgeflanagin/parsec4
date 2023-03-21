# parsec4

Parsec 4 is an update to Parsec 3.3 by He Tao.
The changes fall into two groups, the minor updates and the
expansions. I have also provided a sketch of how to use
Parsec 4 for anyone just getting started with parsing.
Finally, the doc strings are included at the bottom of 
this file.

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



```python    
    class EndOfGenerator(builtins.StopIteration)
     |  EndOfGenerator(value)
     |  
     |  An exception raised when parsing operations terminate. Iterators raise
     |  a StopIteration exception when they exhaust the input; this mod gives
     |  us something useful.
     |  
     |  Method resolution order:
     |      EndOfGenerator
     |      builtins.StopIteration
     |      builtins.Exception
     |      builtins.BaseException
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, value)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from builtins.StopIteration:
     |  
     |  value
     |      generator return value
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from builtins.Exception:
     |  
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.BaseException:
     |  
     |  __delattr__(self, name, /)
     |      Implement delattr(self, name).
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __reduce__(...)
     |      Helper for pickle.
     |  
     |  __repr__(self, /)
     |      Return repr(self).
     |  
     |  __setattr__(self, name, value, /)
     |      Implement setattr(self, name, value).
     |  
     |  __setstate__(...)
     |  
     |  __str__(self, /)
     |      Return str(self).
     |  
     |  with_traceback(...)
     |      Exception.with_traceback(tb) --
     |      set self.__traceback__ to tb and return self.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from builtins.BaseException:
     |  
     |  __cause__
     |      exception cause
     |  
     |  __context__
     |      exception context
     |  
     |  __dict__
     |  
     |  __suppress_context__
     |  
     |  __traceback__
     |  
     |  args
    
    class EndOfParse(builtins.StopIteration)
     |  EndOfParse(value)
     |  
     |  As above, but this exception can be raised when we reach end of all parsing
     |  to signal the true "end" if we want/need to distinguish between them.
     |  
     |  Method resolution order:
     |      EndOfParse
     |      builtins.StopIteration
     |      builtins.Exception
     |      builtins.BaseException
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, value)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from builtins.StopIteration:
     |  
     |  value
     |      generator return value
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from builtins.Exception:
     |  
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.BaseException:
     |  
     |  __delattr__(self, name, /)
     |      Implement delattr(self, name).
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __reduce__(...)
     |      Helper for pickle.
     |  
     |  __repr__(self, /)
     |      Return repr(self).
     |  
     |  __setattr__(self, name, value, /)
     |      Implement setattr(self, name, value).
     |  
     |  __setstate__(...)
     |  
     |  __str__(self, /)
     |      Return str(self).
     |  
     |  with_traceback(...)
     |      Exception.with_traceback(tb) --
     |      set self.__traceback__ to tb and return self.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from builtins.BaseException:
     |  
     |  __cause__
     |      exception cause
     |  
     |  __context__
     |      exception context
     |  
     |  __dict__
     |  
     |  __suppress_context__
     |  
     |  __traceback__
     |  
     |  args
    
    class ParseError(builtins.RuntimeError)
     |  ParseError(expected: str, text: str, index: tuple)
     |  
     |  This exception is raised at the first unrecoverable syntax error.
     |  
     |  Method resolution order:
     |      ParseError
     |      builtins.RuntimeError
     |      builtins.Exception
     |      builtins.BaseException
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, expected: str, text: str, index: tuple)
     |      expected -- the text that should be present.
     |      text     -- the text that was found.
     |      index    -- where in the current text shred the error is located.
     |  
     |  __str__(self) -> str
     |      This function allows us to meaningfully print the exception.
     |  
     |  loc(self) -> int
     |      Locate the error position in the source code text.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  loc_info(text: object, index: int) -> tuple
     |      Location of `index` in source code `text`.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from builtins.RuntimeError:
     |  
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.BaseException:
     |  
     |  __delattr__(self, name, /)
     |      Implement delattr(self, name).
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __reduce__(...)
     |      Helper for pickle.
     |  
     |  __repr__(self, /)
     |      Return repr(self).
     |  
     |  __setattr__(self, name, value, /)
     |      Implement setattr(self, name, value).
     |  
     |  __setstate__(...)
     |  
     |  with_traceback(...)
     |      Exception.with_traceback(tb) --
     |      set self.__traceback__ to tb and return self.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from builtins.BaseException:
     |  
     |  __cause__
     |      exception cause
     |  
     |  __context__
     |      exception context
     |  
     |  __dict__
     |  
     |  __suppress_context__
     |  
     |  __traceback__
     |  
     |  args
    
    class Parser(builtins.object)
     |  Parser(fn: collections.abc.Callable)
     |  
     |  A Parser is an object that wraps a function to do the parsing work.
     |  Arguments of the function should be a string to be parsed and the index on
     |  which to begin parsing. Parser is intended to be used as a decorator.
     |  
     |  The function should return either Value.success(next_index, value) if
     |  parsing successfully, or Value.failure(index, expected) on the failure.
     |  
     |  Methods defined here:
     |  
     |  __add__(self, other: parsec4.Parser)
     |      Implements the `(+)` operator, means `joint`.
     |  
     |  __call__(self, text: str, index: int) -> parsec4.Value
     |      call wrapped function.
     |  
     |  __ge__(self, other: parsec4.Parser)
     |      Implements the `(>=)` operator, means `bind`.
     |  
     |  __gt__(self, other: parsec4.Parser)
     |      Implements the `(>)` operator, means `compose`.
     |  
     |  __init__(self, fn: collections.abc.Callable)
     |      fn -- is the function to wrap.
     |  
     |  __irshift__(self, other: parsec4.Parser)
     |      Implements the `(>>=)` operator, means `bind`.
     |  
     |  __lshift__(self, other: parsec4.Parser)
     |      Implements the `(<<)` operator, means `skip`.
     |  
     |  __lt__(self, other: parsec4.Parser)
     |      Implements the `(<)` operator, means `ends_with`.
     |  
     |  __or__(self, other: parsec4.Parser)
     |      Implements the `(|)` operator, means `choice`.
     |  
     |  __rshift__(self, other: parsec4.Parser)
     |      Implements the `(>>)` operator, means `compose`.
     |  
     |  __truediv__(self, other: parsec4.Parser)
     |      Implements the `(/)` operator, means `excepts`.
     |  
     |  __xor__(self, other: parsec4.Parser)
     |      Implements the `(^)` operator, means `try_choice`.
     |  
     |  bind(self, fn: collections.abc.Callable) -> parsec4.Parser
     |      This is the monadic binding operation. Returns a parser which, if
     |      parser is successful, passes the result to fn, and continues with the
     |      parser returned from fn.
     |  
     |  choice(self, other: parsec4.Parser) -> parsec4.Value
     |      (|) This combinator implements choice. The parser p | q first applies p.
     |      
     |      - If it succeeds, the value of p is returned.
     |      - If p fails **without consuming any input**, parser q is tried.
     |      
     |      NOTICE: without backtrack.
     |  
     |  compose(self, other: parsec4.Parser)
     |      (>>) Sequentially compose two actions, discarding any value produced
     |      by the first.
     |  
     |  desc(self, description)
     |      Describe a parser, when it failed, print out the description text.
     |  
     |  ends_with(self, other: parsec4.Parser) -> parsec4.Value
     |      (<) Ends with a specified parser, and at the end parser hasn't consumed
     |      any input.
     |  
     |  excepts(self, other: parsec4.Parser)
     |      Fail though matched when the consecutive parser `other` success for the rest text.
     |  
     |  joint(self, *parsers)
     |      (+) 
     |      Joint two or more parsers into one. Return the aggregate of two results
     |      from this two parser.
     |  
     |  mark(self)
     |      Mark the line and column information of the result of this parser.
     |  
     |  parse(self, text: str)
     |      text -- the text to be parsed.
     |  
     |  parse_partial(self, text: str) -> tuple
     |      Parse the longest possible prefix of a given string.
     |      
     |      Return a tuple of the result value and the rest of the string.
     |      
     |      If failed, raise a ParseError.
     |  
     |  parse_strict(self, text: str) -> parsec4.Value
     |      Parse the longest possible prefix of the entire given string.
     |      
     |      If the parser worked successfully and NONE text was rested, return the
     |      result value, else raise a ParseError.
     |      
     |      The difference between `parse` and `parse_strict` is that whether entire
     |      given text must be used.
     |  
     |  parsecapp(self, other: parsec4.Parser) -> parsec4.Parser
     |      Returns a parser that applies the produced value of this parser 
     |      to the produced value of `other`.
     |  
     |  parsecmap(self, fn: collections.abc.Callable) -> parsec4.Parser
     |      Returns a parser that transforms the result of the current parsing
     |      operation by invoking fn on the result. For example, if you wanted
     |      to transform the result from a text shred to an int, you would
     |      call xxxxxx.parsecmap(int). Note the *two* lambda functions.
     |  
     |  result(self, result: parsec4.Value) -> parsec4.Value
     |      Return a value according to the parameter res when parse successfully.
     |  
     |  skip(self, other: parsec4.Parser) -> parsec4.Value
     |      (<<) Ends with a specified parser, discarding any result from
     |      the parser on the RHS.
     |  
     |  try_choice(self, other: parsec4.Parser) -> parsec4.Value
     |      (^) Choice with backtrack. This combinator is used whenever arbitrary
     |      look ahead is needed. The parser p ^ q first applies p, if it success,
     |      the value of p is returned. If p fails, it pretends that it hasn't consumed
     |      any input, and then parser q is tried.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class Value(Value)
     |  Value(status, index, value, expected)
     |  
     |  Represent the result of the Parser. namedtuple is a little bit of 
     |  difficult beast, adding as much syntactic complexity as it removes.
     |  
     |  Method resolution order:
     |      Value
     |      Value
     |      builtins.tuple
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __bool__(self) -> bool
     |      This function allows for checking the status with an "if" before
     |      the Value object. Merely syntax sugar for neater code.
     |  
     |  __str__(self) -> str
     |      To allow for well-behaved printing.
     |  
     |  aggregate(self, other: parsec4.Value = None) -> parsec4.Value
     |      collect the furthest failure from self and other.
     |  
     |  update_index(self, index: int = None) -> parsec4.Value
     |      Change the index, and return a new object.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  combinate(values) -> parsec4.Value
     |      TODO: rework this one.
     |      Aggregate multiple values into tuple
     |  
     |  failure(index, expected) -> parsec4.Value
     |      Create failure value.
     |  
     |  success(index, actual) -> parsec4.Value
     |      Create success value.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Value:
     |  
     |  __getnewargs__(self)
     |      Return self as a plain tuple.  Used by copy and pickle.
     |  
     |  __repr__(self)
     |      Return a nicely formatted representation string
     |  
     |  _asdict(self)
     |      Return a new dict which maps field names to their values.
     |  
     |  _replace(self, /, **kwds)
     |      Return a new Value object replacing specified fields with new values
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from Value:
     |  
     |  _make(iterable) from builtins.type
     |      Make a new Value object from a sequence or iterable
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from Value:
     |  
     |  __new__(_cls, status, index, value, expected)
     |      Create new instance of Value(status, index, value, expected)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from Value:
     |  
     |  status
     |      Alias for field number 0
     |  
     |  index
     |      Alias for field number 1
     |  
     |  value
     |      Alias for field number 2
     |  
     |  expected
     |      Alias for field number 3
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from Value:
     |  
     |  _field_defaults = {}
     |  
     |  _fields = ('status', 'index', 'value', 'expected')
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.tuple:
     |  
     |  __add__(self, value, /)
     |      Return self+value.
     |  
     |  __contains__(self, key, /)
     |      Return key in self.
     |  
     |  __eq__(self, value, /)
     |      Return self==value.
     |  
     |  __ge__(self, value, /)
     |      Return self>=value.
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __getitem__(self, key, /)
     |      Return self[key].
     |  
     |  __gt__(self, value, /)
     |      Return self>value.
     |  
     |  __hash__(self, /)
     |      Return hash(self).
     |  
     |  __iter__(self, /)
     |      Implement iter(self).
     |  
     |  __le__(self, value, /)
     |      Return self<=value.
     |  
     |  __len__(self, /)
     |      Return len(self).
     |  
     |  __lt__(self, value, /)
     |      Return self<value.
     |  
     |  __mul__(self, value, /)
     |      Return self*value.
     |  
     |  __ne__(self, value, /)
     |      Return self!=value.
     |  
     |  __rmul__(self, value, /)
     |      Return value*self.
     |  
     |  count(self, value, /)
     |      Return number of occurrences of value.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from builtins.tuple:
     |  
     |  __class_getitem__(...) from builtins.type
     |      See PEP 585

FUNCTIONS

    any_character() -> parsec4.Parser
        Note the change in name in this version. This function was named any(), but
        any is a Python built in.
    
    bind(p, fn: collections.abc.Callable) -> parsec4.Parser
        Bind two parsers, implements the operator of `(>=)`.
    
    charseq() -> str
        Returns a sequence of characters, resolving any escaped chars.
    
    choice(pa: parsec4.Parser, pb: parsec4.Parser)
        Choice one from two parsers, implements the operator of `(|)`.
    
    compose(pa: parsec4.Parser, pb: parsec4.Parser) -> parsec4.Parser
        Compose two parsers, implements the operator of `(>>)`, or `(>)`.
    
    count(p: parsec4.Parser, n: int) -> list
        `count p n` parses n occurrences of p. If n is smaller or equal to zero,
        the parser equals to return []. Returns a list of n values returned by p.
    
    desc(p, description)
        Describe a parser, when it failed, print out the description text.
    
    digit() -> parsec4.Parser
        Parse a digit.
    
    endBy(p: parsec4.Parser, sep: str) -> list
        `endBy(p, sep)` parses zero or more occurrences of `p`, separated and
        ended by `sep`. Returns a list of values returned by `p`.
    
    endBy1(p: parsec4.Parser, sep: str) -> list
        `endBy1(p, sep) parses one or more occurrences of `p`, separated and
        ended by `sep`. Returns a list of values returned by `p`.
    
    ends_with(pa, pb)
        Ends with a specified parser, and at the end parser hasn't consumed any input.
        Implements the operator of `(<)`.
    
    eof() -> parsec4.Parser
        Parses EOF flag of a string.
    
    excepts(pa, pb)
        Fail `pa` though matched when the consecutive parser `pb` success for the rest text.
    
    exclude(p: parsec4.Parser, exclude: parsec4.Parser) -> parsec4.Parser
        Fails parser p if parser `exclude` matches
    
    fail_with(message) -> parsec4.Parser
        A trivial parser that always blows up.
    
    fix(fn: collections.abc.Callable) -> parsec4.Parser
        Allow recursive parser using the Y combinator trick.
        
           Note that this version still yields the stack overflow problem, and will be fixed
           in later version.
        
           See also: https://github.com/sighingnow/parsec.py/issues/39.
    
    generate(fn: collections.abc.Callable) -> parsec4.Parser
        Parser generator. (combinator syntax).
    
    integer() -> int
        Return a Python int, based on the commonsense def of a integer.
    
    joint(*parsers)
        Joint two or more parsers, implements the operator of `(+)`.
    
    letter() -> parsec4.Parser
        Parse a letter in alphabet.
    
    lexeme lambda p
    
    lookahead(p: parsec4.Parser) -> parsec4.Parser
        Parses without consuming
    
    many(p) -> list
        Repeat a parser 0 to infinity times. DO AS MUCH MATCH AS IT CAN.
        Return a list of values.
    
    many1(p: parsec4.Parser) -> list
        Repeat a parser 1 to infinity times. DO AS MUCH MATCH AS IT CAN.
        Return a list of values.
    
    mark(p)
        Mark the line and column information of the result of the parser `p`.
    
    none_of(s) -> parsec4.Parser
        Parses a char NOT from specified string.
    
    number() -> float
        Return a Python float, based on the IEEE754 character representation.
    
    one_of(s: str) -> parsec4.Parser
        Parses a char from specified string.
    
    optional(p: parsec4.Parser, default_value=None)
        Make a parser as optional. If success, return the result, otherwise return
        default_value silently, without raising any exception. If default_value is not
        provided None is returned instead.
    
    parse(p: parsec4.Parser, text: str, index: int = 0) -> parsec4.Value
        Parse a string and return the result or raise a ParseError.
    
    parsecapp(p, other)
        Returns a parser that applies the produced value of this parser to the produced
        value of `other`.
        
        There should be an operator `(<*>)`, but that is impossible in Python.
    
    parsecmap(p, fn)
        Returns a parser that transforms the produced value of parser with `fn`.
    
    regex(exp: str, flags: int = 0) -> parsec4.Parser
        Parses according to a regular expression.
    
    result(p, res)
        Return a value according to the parameter `res` when parse successfully.
    
    sepBy(p: parsec4.Parser, sep: str) -> list
        `sepBy(p, sep)` parses zero or more occurrences of p, separated by `sep`.
        Returns a list of values returned by `p`.
    
    sepBy1(p: parsec4.Parser, sep: str) -> list
        `sepBy1(p, sep)` parses one or more occurrences of `p`, separated by
        `sep`. Returns a list of values returned by `p`.
    
    sepEndBy(p: parsec4.Parser, sep: str) -> list
        `sepEndBy(p, sep)` parses zero or more occurrences of `p`, separated and
        optionally ended by `sep`. Returns a list of
        values returned by `p`.
    
    sepEndBy1(p: parsec4.Parser, sep: str) -> list
        `sepEndBy1(p, sep)` parses one or more occurrences of `p`, separated and
        optionally ended by `sep`. Returns a list of values returned by `p`.
    
    separated(p: parsec4.Parser, sep: str, min_times: int, max_times: int = 0, end=None) -> list
        Repeat a parser `p` separated by `s` between `min_times` and `max_times` times.
        
        - When `end` is None, a trailing separator is optional.
        - When `end` is True, a trailing separator is required.
        - When `end` is False, a trailing separator will not be parsed.
        
        MATCHES AS MUCH AS POSSIBLE.
        
        Return list of values returned by `p`.
    
    skip(pa, pb)
        Ends with a specified parser, and at the end parser consumed the end flag.
        Implements the operator of `(<<)`.
    
    space() -> parsec4.Parser
        Parses a whitespace character.
    
    spaces() -> parsec4.Parser
        Parses zero or more whitespace characters.
    
    string(s: str)
        Parses a string.
    
    time() -> datetime.time
        For 24 hour times.
    
    times(p: parsec4.Parser, min_times: int, max_times: int = 0) -> list
        Repeat a parser between min_times and max_times
        Execute it, and return a list containing whatever
        was collected.
    
    timestamp() -> datetime.datetime
        Convert an ISO timestamp to a datetime.
    
    try_choice(pa, pb)
        Choice one from two parsers with backtrack, implements the operator of `(^)`.
    
    unit(p: parsec4.Parser) -> parsec4.Parser
        Converts a parser into a single unit. Only consumes input if 
        the parser succeeds

DATA
    AT_SIGN = '@'
    AbstractSet = typing.AbstractSet
        A generic version of collections.abc.Set.
    
    Any = typing.Any
        Special type indicating an unconstrained type.
        
        - Any is compatible with every type.
        - Any assumed to have all methods.
        - All values assumed to be instances of Any.
        
        Note that all the above statements are true from the point of view of
        static type checkers. At runtime, Any should not be used with instance
        or class checks.
    
    AnyStr = ~AnyStr
    AsyncContextManager = typing.AsyncContextManager
        A generic version of contextlib.AbstractAsyncContextManager.
    
    AsyncGenerator = typing.AsyncGenerator
        A generic version of collections.abc.AsyncGenerator.
    
    AsyncIterable = typing.AsyncIterable
        A generic version of collections.abc.AsyncIterable.
    
    AsyncIterator = typing.AsyncIterator
        A generic version of collections.abc.AsyncIterator.
    
    Awaitable = typing.Awaitable
        A generic version of collections.abc.Awaitable.
    
    BACKSLASH = r'\'
    BANG = '!'
    BSPACE = '\x08'
    ByteString = typing.ByteString
        A generic version of collections.abc.ByteString.
    
    CIRCUMFLEX = '^'
    COLON = ':'
    COMMA = ','
    CR = '\r'
    ChainMap = typing.ChainMap
        A generic version of collections.ChainMap.
    
    ClassVar = typing.ClassVar
        Special type construct to mark class variables.
        
        An annotation wrapped in ClassVar indicates that a given
        attribute is intended to be used as a class variable and
        should not be set on instances of that class. Usage::
        
          class Starship:
              stats: ClassVar[Dict[str, int]] = {} # class variable
              damage: int = 10                     # instance variable
        
        ClassVar accepts only types and cannot be further subscribed.
        
        Note that ClassVar is not a class itself, and should not
        be used with isinstance() or issubclass().
    
    Collection = typing.Collection
        A generic version of collections.abc.Collection.
    
    Container = typing.Container
        A generic version of collections.abc.Container.
    
    ContextManager = typing.ContextManager
        A generic version of contextlib.AbstractContextManager.
    
    Coroutine = typing.Coroutine
        A generic version of collections.abc.Coroutine.
    
    Counter = typing.Counter
        A generic version of collections.Counter.
    
    DIGIT_STR = <parsec4.Parser object>
    DOLLAR = '$'
    DefaultDict = typing.DefaultDict
        A generic version of collections.defaultdict.
    
    Deque = typing.Deque
        A generic version of collections.deque.
    
    Dict = typing.Dict
        A generic version of dict.
    
    EMPTY_STR = ''
    EQUAL = '='
    Final = typing.Final
        Special typing construct to indicate final names to type checkers.
        
        A final name cannot be re-assigned or overridden in a subclass.
        For example:
        
          MAX_SIZE: Final = 9000
          MAX_SIZE += 1  # Error reported by type checker
        
          class Connection:
              TIMEOUT: Final[int] = 10
        
          class FastConnector(Connection):
              TIMEOUT = 1  # Error reported by type checker
        
        There is no runtime checking of these properties.
    
    FrozenSet = typing.FrozenSet
        A generic version of frozenset.
    
    Generator = typing.Generator
        A generic version of collections.abc.Generator.
    
    Hashable = typing.Hashable
        A generic version of collections.abc.Hashable.
    
    IEEE754 = <parsec4.Parser object>
    IPv4_ADDR = <parsec4.Parser object>
    ItemsView = typing.ItemsView
        A generic version of collections.abc.ItemsView.
    
    Iterable = typing.Iterable
        A generic version of collections.abc.Iterable.
    
    Iterator = typing.Iterator
        A generic version of collections.abc.Iterator.
    
    KeysView = typing.KeysView
        A generic version of collections.abc.KeysView.
    
    LBRACE = '{'
    LBRACK = '['
    LF = '\n'
    List = typing.List
        A generic version of list.
    
    Literal = typing.Literal
        Special typing form to define literal types (a.k.a. value types).
        
        This form can be used to indicate to type checkers that the corresponding
        variable or function parameter has a value equivalent to the provided
        literal (or one of several literals):
        
          def validate_simple(data: Any) -> Literal[True]:  # always returns True
              ...
        
          MODE = Literal['r', 'rb', 'w', 'wb']
          def open_helper(file: str, mode: MODE) -> str:
              ...
        
          open_helper('/some/path', 'r')  # Passes type check
          open_helper('/other/path', 'typo')  # Error in type checker
        
        Literal[...] cannot be subclassed. At runtime, an arbitrary value
        is allowed as type argument to Literal[...], but type checkers may
        impose restrictions.
    
    MINUS = '-'
    Mapping = typing.Mapping
        A generic version of collections.abc.Mapping.
    
    MappingView = typing.MappingView
        A generic version of collections.abc.MappingView.
    
    Match = typing.Match
        A generic version of re.Match.
    
    MutableMapping = typing.MutableMapping
        A generic version of collections.abc.MutableMapping.
    
    MutableSequence = typing.MutableSequence
        A generic version of collections.abc.MutableSequence.
    
    MutableSet = typing.MutableSet
        A generic version of collections.abc.MutableSet.
    
    NoReturn = typing.NoReturn
        Special type indicating functions that never return.
        Example::
        
          from typing import NoReturn
        
          def stop() -> NoReturn:
              raise Exception('no way')
        
        This type is invalid in other positions, e.g., ``List[NoReturn]``
        will fail in static type checkers.
    
    OCTOTHORPE = '#'
    Optional = typing.Optional
        Optional type.
        
        Optional[X] is equivalent to Union[X, None].
    
    OrderedDict = typing.OrderedDict
        A generic version of collections.OrderedDict.
    
    PERCENT = '%'
    PLUS = '+'
    PYINT = <parsec4.Parser object>
    Pattern = typing.Pattern
        A generic version of re.Pattern.
    
    QUOTE1 = "'"
    QUOTE2 = '"'
    QUOTE3 = '`'
    RBRACE = '}'
    RBRACK = ']'
    Reversible = typing.Reversible
        A generic version of collections.abc.Reversible.
    
    SEMICOLON = ';'
    SLASH = '/'
    STAR = '*'
    Sequence = typing.Sequence
        A generic version of collections.abc.Sequence.
    
    Set = typing.Set
        A generic version of set.
    
    Sized = typing.Sized
        A generic version of collections.abc.Sized.
    
    TAB = '\t'
    TIME = <parsec4.Parser object>
    TIMESTAMP = <parsec4.Parser object>
    TYPE_CHECKING = False
    Tuple = typing.Tuple
        Tuple type; Tuple[X, Y] is the cross-product type of X and Y.
        
        Example: Tuple[T1, T2] is a tuple of two elements corresponding
        to type variables T1 and T2.  Tuple[int, float, str] is a tuple
        of an int, a float and a string.
        
        To specify a variable-length tuple of homogeneous type, use Tuple[T, ...].
    
    Type = typing.Type
        A special construct usable to annotate class objects.
        
        For example, suppose we have the following classes::
        
          class User: ...  # Abstract base for User classes
          class BasicUser(User): ...
          class ProUser(User): ...
          class TeamUser(User): ...
        
        And a function that takes a class argument that's a subclass of
        User and returns an instance of the corresponding class::
        
          U = TypeVar('U', bound=User)
          def new_user(user_class: Type[U]) -> U:
              user = user_class()
              # (Here we could write the user object to a database)
              return user
        
          joe = new_user(BasicUser)
        
        At this point the type checker knows that joe has type BasicUser.

    UNDERSCORE = '_'
    US_PHONE = <parsec4.Parser object>
    Union = typing.Union
        Union type; Union[X, Y] means either X or Y.
        
        To define a union, use e.g. Union[int, str].  Details:
        - The arguments must be types and there must be at least one.
        - None as an argument is a special case and is replaced by
          type(None).
        - Unions of unions are flattened, e.g.::
        
            Union[Union[int, str], float] == Union[int, str, float]
        
        - Unions of a single argument vanish, e.g.::
        
            Union[int] == int  # The constructor actually returns int
        
        - Redundant arguments are skipped, e.g.::
        
            Union[int, str, int] == Union[int, str]
        
        - When comparing unions, the argument order is ignored, e.g.::
        
            Union[int, str] == Union[str, int]
        
        - You cannot subclass or instantiate a union.
        - You can use Optional[X] as a shorthand for Union[X, None].
    
    VTAB = '\x0c'
    ValuesView = typing.ValuesView
        A generic version of collections.abc.ValuesView.
    
    WHITESPACE = <parsec4.Parser object>
    __copyright__ = 'Copyright 2023'
    __email__ = ['gflanagin@richmond.edu', 'me@georgeflanagin.com']
    __license__ = 'MIT'
    __maintainer__ = 'George Flanagin'
    __status__ = 'in progress'
    min_py = (3, 8)
    quoted = <parsec4.Parser object>

VERSION
    4.0

AUTHOR
    George Flanagin

CREDITS
    He Tao, sighingnow@gmail.com
```
