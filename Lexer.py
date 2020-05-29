# -------------------------------------------------------------- #
# ------------------------ Lexer.py ---------------------------- #
# -------------------------------------------------------------- #

import AST_Nodes as nodes

# ------------------------- Tokens ----------------------------- #
reserved = {'mod': 'MODULUS',
            'div': 'INTEGER_DIVISION',
            'in': 'MEMBERSHIP',
            'not': 'NEGATION',
            'andalso': 'CONJUNCTION',
            'orelse': 'DISJUNCTION',
            'True': 'TRUE',
            'False': 'FALSE',
            'print' : 'PRINT',
            'if' : 'IF',
            'else' : 'ELSE',
            'while' : 'WHILE',
            'fun': 'FUNCTION'
           }

tokens = ('LEFT_PARENTHESIS',
          'RIGHT_PARENTHESIS',
          'COMMA',
          'HASHTAG',
          'LEFT_BRACKET',
          'RIGHT_BRACKET',
          'LEFT_BRACE',
          'RIGHT_BRACE',
          'EXPONENTIATION',
          'DIVISION',
          'MULTIPLICATION',
          'SUBTRACTION',
          'ADDITION',
          'CONS',
          'GREATER_THAN_EQUAL',
          'GREATER_THAN',
          'NOT_EQUAL',
          'EQUALS',
          'LESS_THAN_EQUAL',
          'LESS_THAN',
          'ASSIGNMENT',
          'SEMICOLON',
          # --- DATA TYPES --- #
          'VARIABLE',
          'INTEGER',
          'REAL',
          'STRING'
         ) + tuple(reserved.values())
         
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_COMMA = r','
t_HASHTAG = r'\#'
t_LEFT_BRACKET = r'\['
t_RIGHT_BRACKET = r'\]'
t_LEFT_BRACE = r'\{'
t_RIGHT_BRACE = r'\}'
t_EXPONENTIATION = r'\*\*'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'/'
t_ADDITION = r'\+'
t_SUBTRACTION = r'-'
t_CONS = r'::'
t_LESS_THAN_EQUAL = r'<=' 
t_LESS_THAN = r'<'
t_EQUALS = r'=='
t_NOT_EQUAL = r'<>'
t_GREATER_THAN_EQUAL = r'>='
t_GREATER_THAN = r'>'
t_ASSIGNMENT = r'='
t_SEMICOLON = r';'

def t_REAL(t): 
    r'(\d*[.]\d*([e][-]?)?\d+) | (\d+[.]\d*([e][-]?)?\d*)'
    try: 
        t.value = float(t.value)
    except ValueError: 
        m = "Decimal value too large " + str(t.value)
        raise ValueError(m)
    return t

def t_INTEGER(t):
    r'\d+'
    try: 
        t.value = int(t.value)
    except ValueError:
        m = "Integer value too large " + str(t.value)
        raise ValueError(m)
    return t
    
def t_STRING(t): 
    r'(["] ([^"])* ["]) | ([\'] [^\']* [\'])'
    t.value = t.value[1:-1]
    return t
    
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE')
    # if (t.type == None):
        # t.type = 'VARIABLE'
    return t

def t_error(t): 
    raise SyntaxError()   
    t.lexer.skip(1)

# Ignore whitespace 
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")    
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

def tokenize(inp):
    lexer.input(inp)
    while True:
        try: 
            tok = lexer.token()
            if not tok: 
                break 
           # print(tok)
        except SyntaxError as e:
            print(e.message)
            break

# ------------------------- Tokens ----------------------------- #

def getTokens(): 
    return tokens 