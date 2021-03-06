import sys
import re


RESERVED = "RESERVED"
INT = "INT"
ID = "ID"


token_expressions = [
    (r'[ \t]+',                None),  # Whitespace
    (r'^[ \t]*$\n',            None),  # Blank lines
    (r'\n',                    RESERVED),  # New line, can terminate statements
    (r'\(',                    RESERVED),  # Left bracket
    (r'\)',                    RESERVED),  # Right bracket
    (r'\+',                    RESERVED),  # Addition operator
    (r'-',                     RESERVED),  # Subtraction operator
    (r'\*',                    RESERVED),  # Multiplication operator
    (r'/',                     RESERVED),  # Division operation
    (r';',                     RESERVED),  # Statement terminator
    (r'<=',                    RESERVED),  # Less than or equal to operator
    (r'<',                     RESERVED),  # Less than operator
    (r'>=',                    RESERVED),  # Greater than or equal to operator
    (r'>',                     RESERVED),  # Greater than  operator
    (r'==',                    RESERVED),  # Equality operator
    (r'!=',                    RESERVED),  # Not equal operator
    (r'=',                     RESERVED),  # Assignment operator
    (r'up',                    RESERVED),  # Move up keyword
    (r'down',                  RESERVED),  # Move down keyword
    (r'left',                  RESERVED),  # Move left keyword
    (r'right',                 RESERVED),  # Move right keyword
    (r'and',                   RESERVED),  # Logical and
    (r'or',                    RESERVED),  # Logical for
    (r'not',                   RESERVED),  # Negation
    (r'if',                    RESERVED),  # If
    (r'else',                  RESERVED),  # else
    (r'for',                   RESERVED),  # For
    (r'do',                    RESERVED),  # For/if x do
    (r'end',                   RESERVED),  # For/if end keyword
    (r'movement_list',         RESERVED),  # Reserved keyword for internal usage
    (r'[0-9]+',                INT),  # Integers
    (r'[A-Za-z][A-Za-z0-9_]*', ID),  # Identifiers
]


def lex_internal(characters, token_expressinos):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expression in token_expressinos:
            pattern, tag = token_expression
            regex = re.compile(pattern, re.MULTILINE)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                #print("Matched text: " + text + " against: " + pattern)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % characters[pos])
            return None
        else:
            pos = match.end(0)
    return tokens


def seek_lex(characters):
    return lex_internal(characters, token_expressions)
