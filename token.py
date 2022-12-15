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


