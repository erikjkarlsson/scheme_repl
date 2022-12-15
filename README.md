# scheme_repl
Scheme Evaluator, Parser and Tokenizer written in Python

Functions 
============
- `determine(string):` Will determine the type a STRING should have
  (such as `INT` or `SYM`), and will return a token created from the
  STRING.
- `toklv(tokens):` Will return a list of values belonging to those in
  the provided list TOKENS, used for example when evaluating `(+ 1 2
  3)` where the list of tokens `[Tok(1, INT), Tok(2, INT), Tok(3,
  INT)]` needs to be added. `toklv([Tok(1, INT), Tok(2, INT), Tok(3,
  INT)]) = [1, 2, 3]` .
- `tokt(token):` Returns TOKENs type.
- `tokv(token):` Returns TOKENs value.
- `istok(token):` Returns True if TOKEN is of type `Tok`.
- `pp(string):` Pretty Print STRING.
- `tokenize(expression: str) -> [str]:` Tokenize the string
  EXPRESSION, which should be a arbituary lisp syntax expression (such
  as `(define x (+ 1 2 3)`. The function will use `determine` to
  choose what kind of tokens to create. Tokens are separated using
  "\n", "\t" and " ", numbers can be floating point or (negative and
  positive) integers. Parenthesizes are made into tokens `Tok('(',
  SYM)` etc.
- `parse(tokens: str): ` Will take the output from `tokenize`
  and create nested lists according to the parenthesis structure. I.e
  each lisp list will be represented as a list.
- `evaluate(expression, scope={}):` Will reduce / evaluate EXPRESSION (which is a
  parsed / tokenized structure) as far as possible.
- `repl():` Open a Read Eval `evaluate(parse(tokenize(...)))` Print
  Loop. Typing ".q" will exit the REPL.
- `eval_expr(expression: str):` Eval expression is a shortened form of
`evaluate(parse(tokenize()))` checks for an equal amount of open /
close parens of the user input before evaluating expression.
- `run_tests(fun, *tests) -> bool: ` Will create a unit test on FUN,
  where *TESTS all following arguments formatted as tuples of
  `(<input> <expected output>)`.
- `std_let(args, scope={}):` Used to evaluate `let` expressions
  (scoped variable declarations).
- `std_if_then_else(args):` Used to evaluate `if` expressions.
- `construct_lambda(args, body):` Used to construct a `lambda`
  function (token will have type `FUN`).
- `call_lambda(token, args):` Used to call lambda expressions.
- `fun_define(args):` Used to define values and functions (i.e
  `(define x 12)`).
- `test():`Will run all of the unit tests,
  will return False on first error otherwise True if succeeded.

Types
=====
- `INT` | `FLO` | `SYM` | `FUN`

1. `INT` defines Integers
2. `FLO` defines Floating point numbers
3. `SYM` defines Symbols (such as "+" and "define")
4. `FUN` marks the token as containing a lambda function.

Classes
=======
- `Tok(value:str, kind:str)`

	`Tok` is used to define tokens, where as a token can have a type
    (or "kind"), which can be one of those previously defined. 

