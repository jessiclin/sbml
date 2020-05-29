# sbml

# Run Instructions 
> python sbml.py [text_file]

# Code Semantics 
An input program contains zero or more function definitions followed by a single main block that gets executed. 

## Literal Representation of Data Types 

| Data Type    | Description  |
|      ---     |     ---      |
| **Integer:** | Positive (no sign) or negative (unary -) whole numbers in base-10 representation (decimal representation) <br/> An integer literal is one or more digits, 0-9 |
| **Real:**    | Represented by 0 or more digits (0-9), followed by a decimal point, ".", followed by 0 or more digits (0-9), except that a decimal point by itself with no leading or trailing digit is not a real <br/> Can also contain exponents as in scientific notation| 
| **Boolean:** | True, False  |
| **String:**  | Begins with a single or double quote, followed by zero or more non-quote characters, and ends with a matching quote <br/> The value of the string literal does not include the starting and ending quotes | 
| **List:**    | Composed by a left square bracket, followed by a comma-separated sequence of zero or more expressions, followed by a right square bracket <br/> Elements of the list need not be of the same type |
| **Tuple:**   | Finite, ordered sequence of elements separated by commas and enclosed within matching parentheses <br/> Elements of the tuple need not be of the same type| 

 
## Operators 
| Operator | Description| 
| --- | ---| 
| **( expression )**                 | A parenthesized expression 
| **( expression1, expression2, …)** | Tuple constructor <br/> A singleton tuple can be constructed by including a comma after the expressio <br/> There are no empty tuples 
| **\#i(tuple)**                     | Returns the argument at index i in the tuple <br/> Indices start at 1 
| **a[b]**                           | Indexing Operation <br/> b can be any expression <br/> Indices start at 0 
| **a \*\* b**                       | Exponentiation <br/> base a raised to the power b 
| **a \* b**                         | Multiplication <br/> Overloaded for integers and reals 
| **a / b**                          | Division <br/> Overloaded for integers and reals, but result is always a real value 
| **a div b**                        | Integer Division <br/> Returns just the quotient <br/> a and b are integers 
| **a mod b**                        | Modulus<br/> Divides a by b and returns just the remainder <br/> a and b are integers 
| **a + b**                          | Addition <br/> Overloaded for integers, reals, strings, and lists
| **a – b**                          | Subtraction <br/> Overloaded for integers and reals
| **a in b**                         | Membership <br/> Evaluates to True if it finds the value of a inside the string or list represented by b
| **a::b**                           | Cons <br/> Adds operand a to the front of the list referred to by operand b
| **not a**                          | Boolean negation
| **a andalso b**                    | Boolean Conjunction 
| **a orelse b**                     | Boolean Disjunction
| **a < b**                          | Less than
| **a <= b**                         | Less than or equal to
| **a == b**                         | Equal to
| **a <> b**                         | Not equal to
| **a >= b**                         | Greater than or equal to
| **a > b**                          | Greater than

## Operator Prescedence (ordered from lowest to highest)
All operators are left-associative, except for exponentiation (**) and cons (::), which are right-associative. Operators on the same line have the same precedence. 
01. orelse 
02. andalso 
03. not
04. <, <=, ==, <>, >=, > 
05. h::t 
06. in 
07. +, - 
08. \*, /, div, mod 
09. \*\*
10. a[b] 
11. \#i(tuple) 
12. (exp1, exp2,...) 
13. (exp) 

## Operator Semantics 
| Operator | Semantics | 
| --- | --- |
| **Indexing:**       | Operand a must be either a string or a list <br/> Operand b must be an integer <br/> If a is a string, then return the b-th character as a string <br/> If a is a list, then return the b-th element as an instance of whatever type it is <br/> The index is 0-based. If the index is out of bounds, then this is a semantic error
| **Addition:**       | Operands must either both be numbers, or both be strings, or both be lists <br/> If they are integers or reals, then addition with standard (Python) semantics is performed <br/> If a and b are both strings, then string concatenation is performed <br/> If a and b are both lists, then list concatenation is performed |
| **Subtraction:**    | Operands must both be integers or reals |
| **Multiplication:** | Operands must both be integers or reals|
| **Division:**       | Operands must both be integers or reals |
| **Booleans:**       | Operands for Boolean operations (not, andalso, orelse) must be Boolean values |
| **Comparisons:**    | Operands must either both be numbers or both be strings <br/> Comparison of numbers (integers and strings) should follow standard semantics <br/> Comparison of strings should follow the Python semantics <br/> Returns True if comparison is true, and False if comparison is False. |

## Statements 
| Statement | Description | 
| --- | --- | 
| **Block:** |  Consists of zero or more statements enclosed in curly-braces, "{…}" <br/> When the block executes, each of the statements is executed in sequential order. 
| **Assignment:** | Consists of "exp1 = exp2;" <br/> When the assignment statement executes the lefthand side expression is assigned the value evaluated for the right-hand side expression. 
| **Print:** |  Consists of "print(exp)" <br/> When the statement executes, the expression is evaluated for its value 
| **Conditional:** | **If Statements:** Consist of "if (exp) {…}" <br/> When the If statement executes, if the expression evaluates to True, then the block statement composing the body is executed. <br/> **If-Else Statements:** Consist of "if (exp) {…} else {…}" <br/> When the IF-Else statement executes, if the expression is True, then execute the block statement that is the body of the If clause. Otherwise, execute the block statement that is the body of the Else clause. 
| **Loop:** | **While Loops:** Consists of "while(exp){…}" <br/> Executing the while statement begins by evaluating the condition expression for its value <br/> If the expression evaluates to False, then the While statement terminates. Otherwise, execute the block of statements that compose the body of the While statement, and then repeat the execution of the While statement from the evaluation of the condition expression.
| **Function Definition:** | Consists of "fun [function_name] ( [comma_separated_parameters] ) = {…} exp;" <br/> When the function is called, the block is executed first. Then the expression is evaluated and the result of the expression evaluation is returned to the caller. 
| **Function Call:** | Consists of "[function_name] ( [argument_expressions] )" <br/> The number of arguments passed to the call must match the number of parameters in the function definition. 



