#!/usr/bin/python3
import re
import math
from functools import reduce 

VERSION = 1.0
NAME = "Scheme.py LISP REPL"
INT = "integer"
FLO = "float"
SYM = "symbol"
FUN = "function"

class Tok:
  def __init__(self, value=0, kind="SYM"):
    self.value:str = value
    self.kind:str = kind

  def __add__(self, other):
    return self.value + other.value

  def __sub__(self, other):
    return self.value - other.value

  def __mul__(self, other):
    return self.value * other.value

  def __div__(self, other):
    return self.value / other.value

  def __hash__(self):
    return hash((self.value, self.kind))
  
  def __eq__(self, other):    
    return (self.value == other.value) and (self.kind == other.kind)
  
  def __repr__(self):
    if self.kind == INT:
      return f"Tok({self.value}, INT)"
    elif self.kind == FLO:
      return f"Tok({self.value}, FLO)"
    elif self.kind == SYM:
      return f"Tok('{self.value}', SYM)"
    elif self.kind == FUN:
      return f"Tok('{self.value}', FUN)"

  def __str__(self):
    if self.kind == INT:
      return f"i:{self.value}"
    elif self.kind == FLO:
      return f"f:{self.value}"
    elif self.kind == SYM:
      return f"s:{self.value}"
    elif self.kind == FUN:
      return f"λ:{self.value}"

    
def determine(string):
  if isinstance(string, str):

    # INTEGER
    if string.isnumeric():
      return Tok(int(string), INT)

    # FLOATING POINT
    if "." in string:
      split = string.split(".")
      if len(split) == 2:
        if split[0].isnumeric() and split[1].isnumeric():
          return Tok(float(string), FLO)

    else:
      return Tok(string, SYM)

  else:
    print(f"determine({string=}): Invalid type argument")
    return None

      
def toklv(tokens):
    "Compute the value for each element in a list of tokens"
    return list(map(tokv, tokens))

def tokt(token):
    "Return the type of a token"
    return token.kind

def tokv(token):
    if token.kind == INT:   return int(token.value)
    elif token.kind == FLO: return float(token.value)
    elif token.kind == SYM: return str(token.value)
    else:                   return token.value

def istok(token):
    "Is a token?"
    return isinstance(token, Tok)

def pp(string):
    print(string)
    
constant_table = {
    "e":  Tok(math.e, INT),
    "pi": Tok(math.pi, INT)
}
symbol_table = { }

function_table = {
    Tok("+", SYM): lambda args: Tok(reduce(lambda a, b: a + b, toklv(args)), FLO), # ==> Float
    Tok("-", SYM): lambda args: Tok(reduce(lambda a, b: a - b, toklv(args)), FLO), # ==> Float
    Tok("*", SYM): lambda args: Tok(reduce(lambda a, b: a * b, toklv(args)), FLO), # ==> Float
    Tok("/", SYM): lambda args: Tok(reduce(lambda a, b: a / b, toklv(args)), FLO)  # ==> Float
}
macro_table = {
    Tok("define", SYM): lambda args, scope: fun_define(args),      # Define values and Functions  
    Tok("let",    SYM): lambda args, scope: std_let(args, scope),         # Locally set variables inside a scope
    Tok("if",     SYM): lambda args, scope: std_if_then_else(args) # If Then Else
}
    
def tokenize(expression: str) -> [str]:
    "Tokenize the string expression"
    
    regex = re.compile(r"[()]|[-+]?[0-9]*\.?[0-9]+|[^\s\n\t()]+")
    tokens = regex.findall(expression)

    return  list(map(determine, tokens))


def parse(tokens: str): 
    "Parse a list of tokens"
    
    stack   = []      
    acc     = []          

    # Loop through the remaining tokens, if the  
    # current token is a open paren: Append ACC  [1]
    # to STACK then empty ACC, continue. If the  
    # current token is a close paren: Pop the    [2]
    # stack, set ACC to the popped value with
    # the old value of ACC appended. Otherwise
    # append the current token, the continue.    [3]

    for token in tokens:
        
        if token == Tok("(", SYM): #   [1]
            stack.append(acc)
            acc = []
            
        elif token == Tok(")", SYM): # [2]        
            tmp = acc
            acc = stack.pop()
            acc.append(tmp)
          
        else: acc.append(token) #      [3]
    return acc


def evaluate(expression, scope={}):
    """ Evaluate an expression and return value. 

    expression: A token structure, result of parse()
    """

    # If expression is a Token, then it can be a symbol, constant,
    # function, integer, function or floating point
    if isinstance(expression, list) and len(expression) == 1:
        return evaluate(expression[0], scope)
    
    if isinstance(expression, Tok):
        # token is of type INTEGER
        if expression.kind == INT:  
            return expression

        # token is of type FLO
        elif expression.kind == FLO: 
            return expression
      
        # token has a value if the scope
        elif expression in scope: 
            return scope[expression]
        
        # token has a value if the symbol table
        elif expression in symbol_table: 
            return symbol_table[expression]

        # token has a value in the function table
        elif expression in function_table: 
            return function_table[expression]

        # token has a value in the constant table
        elif expression in constant_table:            
            return constant_table[expression]

        # token has a undefined, non-numerical value
        else:
            return expression

    else:
        # Lookup function 
        fst  = expression[0]
        rest = expression[1:]
        # Is function predefined?
        if fst in function_table:
            fun       = function_table[fst]
            args      = list(map(lambda x: evaluate(x, scope), rest))            
            return fun(args)
        
        if fst in macro_table:
            fun       = macro_table[fst]
            args      = rest           
            return fun(args, scope)
        
        elif fst.kind == FUN:
            fun       = tokv(fst)
            args      = list(map(lambda x: evaluate(x, scope), rest))
            return fun(args)
        
        elif fst.kind == SYM:
            if (tokv(fst) == "quote") or (tokv(fst) == "q"):
                return expression                    
            else:
                print(f"Error: evaluate() invalid quote application")
        else:
            print(f"Error: evaluate() invalid type {fst=}")
            return -1
        

def repl():
    print(f" :: {NAME} {VERSION} ")    
    while True:

        query = input(">>> ")        
        if query == ".q": break
        else:
            print(">>> " + str(eval_expr(query)))

            
def eval_expr(expression: str):
    "Evaluate an expression"

    tokens  = tokenize(expression)

    # Determine if there are an equal amount of right
    # and left parenthesizes before evaluation    
    balance = 0    
    for token in tokens:
        if   token == Tok('(', SYM): balance += 1
        elif token == Tok(')', SYM): balance -= 1
        else: pass
        
    if balance != 0:
        print(f"Error: Invalid expression, unbalanced parenthesizes")
        return None
    else:
        return evaluate(parse(tokens)[0])



    
def run_tests(fun, *tests) -> bool: 
    """Run tests on Fun.

    fun:   Function to test
    tests: Each test is formatted as a tuple of (input, output).
    """

    for i, test in zip(range(len(tests)), tests):
        res = fun(test[0])

        if res == test[1]:
            print(f"[{i}] {test[0]}")
        else:
            print(f"INCORRECT: [{i}] {test[0]}")
            print(f" ==> ", end="")
            pp(test[1])
            
            return False
    return True


# [[Tok('let', SYM),
#   [[Tok('x', SYM), Tok(1, INT)], [Tok('y', SYM), Tok(2, INT)]],
#   [Tok('+', SYM), Tok('x', SYM), Tok('y', SYM)]]]

def std_let(args, scope={}):
  declrs       = args[0]
  body         = args[1:]
  lookup_table = scope

  for decl in declrs:
    symbol_table[decl[0]] = evaluate(decl[1])

  return evaluate(body, scope=lookup_table)

def std_if_then_else(args):
  "The IF case for the LISP: (if a b c)"
  
  if len(args) == 3:  # (if a b c)

    tok_Pred = args[0]
    tok_Then = args[1]
    tok_Else = args[2]
    
    if (tok_Pred != tok_NIL):
      return tok_Then
    else: return tok_Else

tok_NIL = Tok("nil", SYM)
tok_t   = Tok("t", SYM)

# These will compare tokens, where the boolean result will be composed
# of either NIL or t
std_greq  = {Tok(">=", SYM): lambda p1, p2: tok_t if p1 >= p2 else tok_NIL}
std_sreq  = {Tok("<=", SYM): lambda p1, p2: tok_t if p1 <= p2 else tok_NIL}
std_gr    = {Tok(">", SYM):  lambda p1, p2: tok_t if p1 > p2  else tok_NIL}
std_sr    = {Tok("<", SYM):  lambda p1, p2: tok_t if p1 < p2  else tok_NIL}

def construct_lambda(args, body):
    "Construct a lambda function as a fun token"
    return lambda args: Tok("LAMBDA", FUN)


def call_lambda(token, args):
    "Call a token containing a lambda function" 
    if istok(token) and tokt(token) == FUN:
        return token.value(args)

def fun_define(args):
    "Function to handle definitions"

    # A definition call looks like this:
    # (definition <symbol> <value>)
    if len(args) == 2:
        name = args[0]
        body = args[1]
        
        if istok(name):
            # If the body is a symbol
            if tokt(body) == SYM:
                symbol_table[name] = body
                return body
            # If the body is a function
            elif tokt(body) == FUN:
                function_table[token] = construct_lambda(body) # HACK
                return construct_lambda(body)
            else:
                # If body is not a symbol or function such as an integer
                symbol_table[name] = body

                return body
              
        else: print(f"Error: fun_define({args=}) invalid name")
    else: print(f"Error: fun_define({args=}) Too many arguments for definition")

    

# Testing 

def test():
    print("\nTest: tokenize()")
    print("      ¨¨¨¨¨¨¨¨")

    r1 = run_tests(tokenize,
                   ("(+ 1 2)",
                    [Tok(value='(', kind=SYM),
                     Tok(value='+', kind=SYM),
                     Tok(value=1, kind=INT),
                     Tok(value=2, kind=INT),
                     Tok(value=')', kind=SYM)]),
                   ("(+ x y)",
                    [Tok(value='(', kind=SYM),
                     Tok(value='+', kind=SYM),
                     Tok(value='x', kind=SYM),
                     Tok(value='y', kind=SYM),
                     Tok(value=')', kind=SYM)]),
                   ("(+ (* a b) (expt c d))",
                    [Tok(value='(', kind=SYM),
                     Tok(value='+', kind=SYM),
                     Tok(value='(', kind=SYM),
                     Tok(value='*', kind=SYM),
                     Tok(value='a', kind=SYM),
                     Tok(value='b', kind=SYM),
                     Tok(value=')', kind=SYM),
                     Tok(value='(', kind=SYM),
                     Tok(value='expt', kind=SYM),
                     Tok(value='c', kind=SYM),
                     Tok(value='d', kind=SYM),
                     Tok(value=')', kind=SYM),
                     Tok(value=')', kind=SYM)]))
    
    print("\nTest: parse()")
    print("      ¨¨¨¨¨")

    
    r2 = run_tests(lambda x: parse(tokenize(x)),
                   ("(+ 1 2)",
                    [[Tok(value='+', kind=SYM),
                      Tok(value=1, kind=INT),
                      Tok(value=2, kind=INT)]]),
                   ("(* (- 1 2) 2)",
                    [[Tok(value='*', kind=SYM),
                      [Tok(value='-', kind=SYM),
                       Tok(value=1, kind=INT),
                       Tok(value=2, kind=INT)],
                      Tok(value=2, kind=INT)]]),
                   ("(* a (+ b (- c (* d (+ e f) (+ g h i)) j k) l) m)",
                    [[Tok(value='*', kind=SYM),
                      Tok(value='a', kind=SYM),
                      [Tok(value='+', kind=SYM),
                       Tok(value='b', kind=SYM),
                       [Tok(value='-', kind=SYM),
                        Tok(value='c', kind=SYM),
                        [Tok(value='*', kind=SYM),
                         Tok(value='d', kind=SYM),
                         [Tok(value='+', kind=SYM),
                          Tok(value='e', kind=SYM),
                          Tok(value='f', kind=SYM)],
                         [Tok(value='+', kind=SYM),
                          Tok(value='g', kind=SYM),
                          Tok(value='h', kind=SYM),
                          Tok(value='i', kind=SYM)]],
                        Tok(value='j', kind=SYM),
                        Tok(value='k', kind=SYM)],
                       Tok(value='l', kind=SYM)],
                      Tok(value='m', kind=SYM)]]))


    print(f"\nTest: evaluate()")
    print(f"      ¨¨¨¨¨¨¨¨")
    r3 = run_tests(
        eval_expr,
        ("(+ 1 2 3)",                                                     Tok(6, FLO)),
        ("(/ 1 2 3)",                                                     Tok(1 / 2 / 3, FLO)),
        ("(* (+ 1 2) (- 2 4) (/ 1 2))",                                   Tok(-3.0, FLO)),
        ("(+ 1 (+ (+ 1 1) 1) (+ (+ (+ (+ 1 1) 1) 1) (+ 1 1)))",           Tok(10, FLO)),
        ("(* 1 (* 4 4) (* 4 4) (* 4 4) (* 4 4) (* 4 4) (* 4 4) (* 4 4))", Tok(268435456, FLO)),
        ("(* (/ 1 3) 3)",                                                 Tok(1.0, FLO)),
        ("(let ((a 10) (b 20) (c 30)) (+ a b c))",                        Tok(60, FLO)),
        ("(let ((a 1)) (let ((b 2)) (+ a b)))",                           Tok(3, FLO)), 
        ("(let ((a (* 29 1))) (let ((b (+ a a 2))) (+ a b)))",            Tok(89.0, FLO)
    
    ))
    

    result = [r1, r2, r3]

    # Count Success 
    acc = 0
    for res in result:
        acc += 1 if res else 0

    print()
    
    if acc < len(result):
        print(f"\nTest: {acc}/{len(result)} Tests Failed")
    else:
        print(f"Test: All Tests Succeeded")
        print(f"                ¨¨¨¨¨¨¨¨¨")

if __name__ == "__main__":
    test()
    repl()
