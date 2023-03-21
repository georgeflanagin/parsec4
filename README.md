# parsec4

Parsec 4 is an update to Parsec 3.3 by He Tao.
The changes fall into two groups, the minor updates and the
expansions. 

## Minor updates to Parsec 3.3

- Added Explanatory comments.
- Provided more natural English grammar for He Tao's comments. His comments
  are included. New comments are marked with a preceding and following group
  of three # characters, and the original docstrings use triple single quotes
  rather than triple double quotes.
- Revised for modern Python; no longer compatible with Python 2. This version
- Require Python 3.8
- Inserted type hints.
- Added a __bool__ function to the Value class.
- Changed some string searches to exploit constants in string module rather
  than str functions that might be affected by locale.
- Changed name of any() function to any_char() to avoid conflicts with 
  Python built-in of the same name.
- Where practical, f-strings are used for formatting.
- A number of definitions of characters are provided, and they
  are named as standard symbols: TAB, NL, CR, etc.
- Many custom parsers are likely to include parsers for common programming
  elements (dates, IP addresses, timestamps). These are now included. 

