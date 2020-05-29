# -------------------------------------------------------------- #
# ---------------------- AST_Nodes.py -------------------------- #
# -------------------------------------------------------------- #

import sys 

# ------------------- Error Handling Classes ------------------- #
import errno

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

# Syntax Error 
class SyntaxError(Error):
    def __init__(self):
        self.message = "SYNTAX ERROR"
# Semantic Error 
class SemanticError(Error):
    def __init__(self):
        self.message = "SEMANTIC ERROR"
        
# ------------------- Error Handling Classes ------------------- #

# Variable stack -> Initialized with empty global variable list
var_list = [dict()]
# Dictionary of functions 
fun_list = dict() 

class Node(): 
    def __init__(self):
        self.parent = None 
        
    def parentCount(self):
        count = 0
        current = self.parent 
        while current is not None:
            count += 1
            current = current.parent
        return count
        
class Disjunction(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        
    def typeCheck(self, left, right):
        if type(left) == bool and type(right) == bool:
            return True
        return False
        
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        
        if self.typeCheck(left, right):
            return left or right
        raise SemanticError() 
    
    def isBoolean(child): 
        if type(child) == bool:
            return True 
        return False

class Conjunction(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
    
    def typeCheck(self, left, right):
        if type(left) == bool and type(right) == bool:
            return True
        return False
        
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        
        if self.typeCheck(left, right):
            return left and right
        raise SemanticError() 
                
class Negation(Node):
    def __init__(self, child):
        super().__init__()
        self.child = child
        
    def typeCheck(self, child):
        if type(child) == bool:
            return True
        return False

    def eval(self):
        child = self.child.eval()
        if self.typeCheck(child):
            return not child
        raise SemanticError() 
        
# ---- Compare Node Handles all the comparison operators 
class Compare(Node):
    def __init__(self, left, right, operation):
        super().__init__()
        self.left = left # Expression to the left of operator 
        self.right = right # Expression to the right of the operator 
        self.value = operation # Operator 
        
    def typeCheck(self, left, right):
        if type(left) != str and type(left) != int and type(left) != float:
            return False
        if type(right) != str and type(right) != int and type(right) != float:
            return False      
        return True
        
    def eval(self):   
        try:
            left = self.left.eval()
            right = self.right.eval()
            if self.typeCheck(left, right):
                if self.value == '<=' : value = left <= right
                elif self.value == '<' : value = left < right
                elif self.value == '==' : value = left == right
                elif self.value == '<>' : value = left != right
                elif self.value == '>=' : value = left >= right
                elif self.value == '>' : value = left > right
                return value 
                
            raise SemanticError()    
            
        except : raise SemanticError()       

# ---- BinOp Node Handles all the comparison Binary Operations 
class BinOp(Node):
    def __init__(self, left, right, operation):
        super().__init__()
        self.left = left # Expression to the left of operator 
        self.right = right # Expression to the right of operator 
        self.value = operation # Operation 

    def typeCheck(self, left, right):
        if type(left) != int and type(left) != float:
            return False
        if type(right) != int and type(right) != float:
            return False  
        return True
    
    def typeCheckAdd(self, left, right): 
        if type(left) != int and type(left) != float and type(left) != str and type(left) != list: 
            return False 
        if type(right) != int and type(right) != float and type(right) != str and type(right) != list: 
            return False 
        return True 
    
    def typeCheckInt(self, left, right): 
        if type(left) != int or type(right) != int: 
            return False
        return True
        
    def eval(self):   
        try:
            left = self.left.eval()
            right = self.right.eval()
            # Addition allows Strings 
            if self.value == '+': 
                if self.typeCheckAdd(left, right): 
                    value = left + right 
                    return value
                else : raise SemanticError()
            
            # Other operation only allows Numbers      
            if self.typeCheck(left, right):
                if self.value == '-' : value = left - right 
                elif self.value == '*' : value = left * right 
                elif self.value == '/' : value = left / right 
                elif self.value == '**': value = left ** right 
                
                # Div and mod only allows Integers 
                elif self.value == 'div' : 
                    if self.typeCheckInt(left, right): 
                        value = left // right 
                    else : raise SemanticError()
                elif self.value == 'mod': 
                    if self.typeCheckInt(left, right): 
                        value = left % right 
                    else : raise SemanticError()
                
                return value
                
            raise SemanticError()
            
        except : raise SemanticError()
        
class UMinus(Node): 
    def __init__(self, expression):
        super().__init__()
        self.child = expression
    
    def typeCheck(self,child):
        if type(child) != int and type(child) != float: 
            return False
        return True
        
    def eval(self):
        child = self.child.eval()      
        if self.typeCheck(child): return -1 * child
        
        raise SemanticError()

class Membership(Node): 
    def __init__(self, left, right): 
        super().__init__()
        self.left = left  # Expression to the left of "in"  
        self.right = right  # Expression to the right of "in"
    
    def typeCheck(self, left, right): 
        if type(left) != str and type(right) == str: 
            return False 
        if type(right) != str and type(right) != list: 
            return False
        return True;
        
    def eval(self): 
        try: 
            left = self.left.eval()
            right = self.right.eval() 

            if self.typeCheck(left, right): 
                return left in right 
            else : raise SemanticError()
            
        except : raise SemanticError()

class Cons(Node): 
    def __init__(self, left, right): 
        super().__init__()
        self.left = left # Expression to the left of ::
        self.right = right # Expression to the right of ::

    def typeCheck(self, right): 
        if type(right) != list: 
            return False
        return True;
        
    def eval(self): 
        try: 
            left = self.left.eval()
            right = self.right.eval() 

            if self.typeCheck(right): return [left] + right 
            else : raise SemanticError()
        except : raise SemanticError()
    
class Index(Node): 
    def __init__(self, indices, value): 
        super().__init__()
        self.value = indices # List of indexes 
        self.child = value # List or String 

    def typeCheck(self, value, indices):  
        for i in indices: 
            if type(i) != int: 
                return False 
                
        if type(value) != list and type(value) != str: 
            return False
        return True;
        
    def eval(self): 
        try: 
            indices = []
            for i in self.value: #Evaluate indices 
                indices.append(i.eval())

            # Evaluate the value 
            if type(self.child) != str : value = self.child.eval() 
            else : value = self.child
            
            # Get the desired indexed value 
            if self.typeCheck(value, indices) : 
                for i in indices: 
                    if i >= len(value): raise SemanticError() # Index of of Bounds 
                    value = value[i] 
                return value 
                
            else : raise SemanticError()
     
        except: 
            raise SemanticError()

        
class Tuple_Index(Node): 
    def __init__(self, index, value): 
        super().__init__()
        self.value = index 
        self.child = value

    def typeCheck(self, value): 
        if type(value) != tuple: 
            return False
        return True
        
    def eval(self): 
        try: 
            if type(self.child) == str: 
                if self.child in var_list[0]:
                    value = var_list[0][self.child]
                else: value = var_list[-1][self.child]
            else : value = self.child.eval() 
            
            if self.typeCheck(value): 
                return value[self.value - 1]
            else : raise SemanticError()
        except :     
            raise SemanticError()
   
        
class AST_Boolean(Node): 
    def __init__(self, value):
        super().__init__()
        self.value = value
        
    def eval(self):
        return self.value

class AST_Number(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value
        
    def eval(self):
        return self.value

class AST_String(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def eval(self):
        return self.value


class AST_List(Node): 
    def __init__(self, element):
        super().__init__()
        self.value = element
        
    def eval(self): 
        list = []
        for i in self.value:
            list.append(i.eval())

        return list
 
class AST_Tuple(Node): 
    def __init__(self, element):
        super().__init__()
        self.value = element
        
    def eval(self): 
        list = []

        for i in self.value:
            list.append(i.eval())
        return tuple(list)
 
# --- Statements 
class AST_Assignment(Node): 
    def __init__(self, variable, value): 
        super().__init__()
        self.value = variable 
        self.child = value 
        
    def eval(self): 
        try: 
            var_name = self.value.getName()
            var_value = self.child.eval()

            # Look for in local list 
            if var_name in var_list[0]: 
                var_list[0][var_name] = var_value
            # Look for in global list                
            elif var_name in var_list[-1]:
                var_list[-1][var_name] = var_value
            # Else add into the local list on stack 
            else: 
                var_list[0][var_name] = var_value

            return var_value
        except: 
            raise SemanticError()
            
class AST_IndexAssignment(Node): 
    def __init__(self, variable, assignement_value, index_values): 
        super().__init__()
        self.value = index_values
        self.left = variable 
        self.right = assignement_value 

    # Iterate through list recursively and change the desired index 
    def indexAssignment(self, variable, index_values, assignement_value): 
        if len(index_values) > 1: 
            self.indexAssignment(variable[index_values[0]], index_values[1:], assignement_value)
        else:
            variable[index_values[0]] = assignement_value # End recursive function 
        
    def eval(self): 
        try: 
            index_values = []
            for i in self.value: 
                index_values.append(i.eval())
            
            if self.left.getName() in var_list[0]:
                self.indexAssignment(var_list[0][self.left.getName()], index_values, self.right.eval())
            else: 
                self.indexAssignment(var_list[-1][self.left.getName()], index_values, self.right.eval())
        except: 
            raise SemanticError()
            
 
class AST_Variable(Node): 
    def __init__(self, name): 
        super().__init__()
        self.value = name
        
    def getName(self): 
        return self.value 
        
    def eval(self):
        try: 
            var_name = self.value 

            # Look for in local list 
            if var_name in var_list[0]:
                return var_list[0][var_name] 
            # Look for in global list 
            else:           
                return var_list[-1][var_name] 
        except: 
            raise SemanticError()

class AST_Block(Node): 
    def __init__ (self, statements): 
        super().__init__()
        if type(statements) == list : self.value = statements 
        else :  self.value = [statements]
            
    def eval(self):        
        # Evaluate each line of code in the block
        try: 
            for i in self.value:
                i.eval()
        except: 
            raise SemanticError()
         
class AST_Print(Node): 
    def __init__ (self, element): 
        super().__init__()
        self.value = element 

    def eval(self): 
        try: 
            value = self.value.eval()
            print(value)
            return value
        except: 
            raise SemanticError()

class AST_If(Node):
    def __init__(self, expression, block): 
        super().__init__()
        self.value = expression 
        self.child = block
        
    def typeCheck(self, value): 
        if type(value) != bool: 
            return False
        return True
    
    def eval(self):
        expr = self.value.eval() 
        try: 
            
            if self.typeCheck(expr):
                if expr == True: return self.child.eval() 
                else : return False
            raise SemanticError()
        except: 
            raise SemanticError()

class AST_IfElse(Node): 
    def __init__(self, if_block, else_block): 
        super().__init__()
        self.left = if_block
        self.right = else_block
    def eval(self):
        try: 
            result = self.left.eval()
 
            if result == False: result = self.right.eval()
            return result
        except: 
            raise SemanticError() 
        
class AST_While(Node): 
    def __init__(self, expression, block):
        super().__init__()
        self.value = expression
        self.child = block 
    
    def eval(self): 
        try: 
            while self.value.eval() != False: 
                self.child.eval()
        except: 
            raise SemanticError()

class AST_Execute(Node): 
    def __init__(self, function_list, block): 
        super().__init__()
        self.left = function_list
        self.right = block 
        
    def eval(self): 
        for func in self.left: 
            func.eval() 

        self.right.eval() 
        
 #-- Functions --> Make a copy of the original variable. After executing block, revert variable back to original value 
class AST_Function(Node): 
    def __init__(self, name, parameter_list, block, expression ): 
        super().__init__() 
        self.value = name 
        self.left = parameter_list
        self.right = block 
        self.child = expression 
        
    def eval(self): 
        try: 
            # [parameter_list, block, expression]
            fun_list[self.value] = [self.left, self.right, self.child]
            return fun_list[self.value]
        except: 
            raise SemanticError()

      
class AST_FunctionCall(Node): 
    def __init__(self, name, parameter_list): 
        super().__init__()
        self.value = name 
        self.child = parameter_list
        
    def eval(self): 
        try: 
            func = fun_list[self.value]
            param = func[0]
            expr = func[2]
            func = func[1] 

            #Check arguments 
            if len(param) != len(self.child): 
                raise SemanticError() 
                
            local_var = dict() 
            #Add the parameter values into the local variable list 
            for i in range(0, len(param)): 
                var_name = param[i].getName()
                var_value = self.child[i].eval() 
                local_var[var_name] = var_value
                
            #Push the local variable list into the stack 
            var_list.insert(0, local_var) 
                            
            func.eval() 
            result = expr.eval()
            #Pop the local variable list from the stack 
            var_list.pop(0)

            return result

        except: 
            raise SemanticError() 