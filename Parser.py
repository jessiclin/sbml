# -------------------------------------------------------------- #
# ------------------------ Parser.py --------------------------- #
# -------------------------------------------------------------- #

import Lexer as lexer 
from AST_Nodes import *
import sys 

tokens = lexer.getTokens()
# ------------------- Production Functions --------------------- #

# Prescedence list from lowest to highest prescedence
precedence = (('left', 'DISJUNCTION'),
              ('left', 'CONJUNCTION'),
              ('left', 'NEGATION'),
              ('left', 'LESS_THAN_EQUAL', 'LESS_THAN', 'EQUALS', 'NOT_EQUAL', 'GREATER_THAN_EQUAL', 'GREATER_THAN'),
              ('right', 'CONS'),
              ('left', 'MEMBERSHIP'),
              ('left', 'ADDITION', 'SUBTRACTION'),
              ('left', 'MULTIPLICATION', 'DIVISION', 'INTEGER_DIVISION', 'MODULUS'),
              ('right', 'UMINUS'),
              ('right', 'EXPONENTIATION'),
              ('left', 'LEFT_BRACKET', 'RIGHT_BRACKET'),
              ('left', 'HASHTAG'),
              ('left', 'COMMA'),
              ('left', 'LEFT_PARENTHESIS', 'COMMA','RIGHT_PARENTHESIS')
             )
             
             
def p_start(p):
    '''start : function_list block
             | block'''
    if len(p) == 3: p[0] = AST_Execute(p[1], p[2])
    else : p[0] = AST_Execute([], p[1])
    
def p_block(p):
    '''block : LEFT_BRACE statement_list RIGHT_BRACE
             | LEFT_BRACE RIGHT_BRACE'''
    if len(p) == 4 : p[0] = AST_Block(p[2])
    else : p[0] = AST_Block([])
   
def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3: 
        p[0] = p[1] + [p[2]]
    elif len(p) == 2: 
        p[0] = [p[1]]

def p_statement(p): 
    '''statement : print SEMICOLON
                 | assignment SEMICOLON
                 | while 
                 | if 
                 | if_else
                 | block
                 | function_call SEMICOLON
                 | variable SEMICOLON'''
    p[0] = p[1]

def p_variable(p): 
    'variable : VARIABLE'
    p[0] = AST_Assignment(AST_Variable(p[1]))

def p_function_list(p): 
    '''function_list : function_list function SEMICOLON
                     | function SEMICOLON '''
    if len(p) == 4 : p[0] = p[1] + [p[2]]
    else : p[0] = [p[1]]     
    
def p_function(p): 
    '''function : FUNCTION VARIABLE LEFT_PARENTHESIS parameter_list RIGHT_PARENTHESIS ASSIGNMENT block expr
                | FUNCTION VARIABLE LEFT_PARENTHESIS RIGHT_PARENTHESIS ASSIGNMENT block expr'''
    if len(p) == 9 : 
        p[0] = AST_Function(p[2], p[4], p[7], p[8])
    else : 
        p[0] = AST_Function(p[2], [], p[6], p[7])
        
def p_parameter_list(p): 
    '''parameter_list : parameter_list COMMA VARIABLE 
                      | VARIABLE'''
    if len(p) == 4 : p[0] = p[1] + [AST_Variable(p[3])]
    else : p[0] = [AST_Variable(p[1])]

def p_function_call(p): 
    '''function_call : VARIABLE LEFT_PARENTHESIS input_list RIGHT_PARENTHESIS
                     | VARIABLE LEFT_PARENTHESIS RIGHT_PARENTHESIS'''
    if len(p) == 5 : 
        p[0] = AST_FunctionCall(p[1],p[3])
    else : 
        p[0] = AST_FunctionCall(p[1], [])

def p_input_list(p): 
    '''input_list : input_list COMMA expr
                  | expr '''
    if len(p) == 4 : p[0] = p[1] + [p[3]]
    else : p[0] = [p[1]]                  

def p_print(p):
    'print : PRINT LEFT_PARENTHESIS expr RIGHT_PARENTHESIS'        
    p[0] = AST_Print(p[3])

def p_assignment(p): 
    '''assignment : VARIABLE index_list ASSIGNMENT expr
                  | VARIABLE ASSIGNMENT expr'''
    if len(p) == 4: p[0] = AST_Assignment(AST_Variable(p[1]), p[3])
    else : p[0] = AST_IndexAssignment(AST_Variable(p[1]), p[4], p[2])

def p_while(p): 
    'while : WHILE LEFT_PARENTHESIS expr RIGHT_PARENTHESIS block'
    p[0] = AST_While(p[3], p[5])
    
def p_if_else(p):
    'if_else : if ELSE block' 
    p[0] = AST_IfElse(p[1], p[3])

def p_if(p):
    'if : IF LEFT_PARENTHESIS expr RIGHT_PARENTHESIS block'
    p[0] = AST_If(p[3],p[5])

def p_index_statement(p): 
    'index_statement : expr index_list'
    p[0] = Index(p[2],p[1])
    
def p_prop_variable(p):
    'prop : VARIABLE'
    p[0] = AST_Variable(p[1])

def p_expr(p):
    '''expr : prop
            | list 
            | tuple
            | index_statement
            | tuple_index
            | function_call'''
    p[0] = p[1]
    
def p_prop_disjunction(p):
    'prop : expr DISJUNCTION expr'
    p[0] = Disjunction(p[1], p[3])

def p_prop_conjunction(p):
    'prop : expr CONJUNCTION expr'
    p[0] = Conjunction(p[1], p[3])

def p_prop_negation(p):
    'prop : NEGATION expr'
    p[0] = Negation(p[2])

def p_prop_membership(p): 
    'prop : expr MEMBERSHIP expr'
    p[0] = Membership(p[1], p[3])

def p_prop_cons(p): 
    'prop : expr CONS expr'
    p[0] = Cons(p[1], p[3])
    
def p_prop_comparison(p):
    '''prop : expr LESS_THAN_EQUAL expr 
            | expr LESS_THAN expr
            | expr EQUALS expr
            | expr NOT_EQUAL expr 
            | expr GREATER_THAN_EQUAL expr
            | expr GREATER_THAN expr '''
    p[0] = Compare(p[1], p[3], p[2])
    
def p_prop_uminus(p):
    'prop : SUBTRACTION expr %prec UMINUS'
    p[0] = UMinus(p[2])
    
def p_prop_binop(p):
    '''prop : expr ADDITION expr 
            | expr SUBTRACTION expr 
            | expr MULTIPLICATION expr
            | expr DIVISION expr 
            | expr INTEGER_DIVISION expr 
            | expr MODULUS expr
            | expr EXPONENTIATION expr '''
    p[0] = BinOp(p[1], p[3], p[2])

# --- Indexing production functions 
def p_index_tuple(p): 
    '''tuple_index : HASHTAG INTEGER tuple
                   | HASHTAG INTEGER LEFT_PARENTHESIS VARIABLE RIGHT_PARENTHESIS
                   | HASHTAG INTEGER VARIABLE'''

    if len(p) == 6:  
        p[0] = Tuple_Index(p[2], AST_Variable(p[4]))
    elif type(p[3]) == str: 
        p[0] = Tuple_Index(p[2], AST_Variable(p[3]))
    else : 
        p[0] = Tuple_Index(p[2], p[3])

def p_index_list(p):
    '''index_list : index_list index
                  | index '''
    if len(p) == 3: 
        p[0] = p[1] + [p[2]]
    else : p[0] = [p[1]]
    
def p_index(p):
    'index : LEFT_BRACKET prop RIGHT_BRACKET'
    p[0] = p[2]
# --- Indexing production functions 
     
def p_prop_boolean(p):
    '''prop : TRUE      
            | FALSE '''
    if p[1] == 'True' : p[0] = AST_Boolean(True)
    elif p[1] == 'False' : p[0] = AST_Boolean(False)

def p_prop_number(p):
    '''prop : REAL   
            | INTEGER'''
    p[0] = AST_Number(p[1])        
   
def p_prop_string(p):
    'prop : STRING'
    p[0] = AST_String(p[1])

# --- List production functions 
def p_list(p):
    '''list : LEFT_BRACKET  RIGHT_BRACKET
            | LEFT_BRACKET element RIGHT_BRACKET'''
    if len(p) == 3 : p[0] = AST_List([])
    else : 
        p[0] = AST_List(p[2])
    
def p_element(p):
    '''element : expr 
               | expr COMMA element'''
    if len(p) == 2 : p[0] = [p[1]]
    else : 
        try: p[0] = [p[1]] + p[3]
        
        except: p[0] = [p[1]] + [p[3]]
# --- List production functions 

# --- Tuple production functions             
def p_tuple(p):
    '''tuple : LEFT_PARENTHESIS expr COMMA RIGHT_PARENTHESIS
             | LEFT_PARENTHESIS tup RIGHT_PARENTHESIS'''
    p[0] = AST_Tuple(p[2])

def p_tup(p):
    '''tup : expr 
           | expr COMMA tup'''
    if len(p) == 2 : p[0] = p[1]
    else : 
        if type(p[1]) == tuple : 
            if type(p[3]) == tuple: 
                p[0] = p[1] + p[3]
            else : p[0] = p[2] + (p[3],)
        elif type(p[3]) == tuple: 
            p[0] = (p[1],) + p[3]
        else : p[0] = (p[1], p[3])
# --- Tuple production functions 

def p_prop_parenthetical(p):
    '''prop : LEFT_PARENTHESIS expr RIGHT_PARENTHESIS'''
    p[0] = p[2]     
# ------------------- Production Functions --------------------- #

def p_error(p):
    raise SyntaxError()

import ply.yacc as yacc
parser = yacc.yacc()

def parse(inp):
    result = parser.parse(inp)
    return result

def parseAll(contents): 
    try: 
        result = parse(contents) 

        if result is not None: 
            r = result.eval()
    except SyntaxError as e:
        print(e.message)
    except SemanticError as e:
        print(e.message)
    except ValueError as e:
        print(e)
    except Exception as e: 
        print("SYNTAX ERROR")        
            