Wisp
====
Hello, my name is Walt and I made a Lisp, so it is named Wisp.

Installing & Running
--------------------
Requires Python 3.7+

```
$ python setup.py install
```
to install

```
$ wisp
```
to start the wisp REPL

Things You Can Wisp
-------------------

math!
```
wisp => (3 (2 4 *) -)
Integer(val=5)
```

equality!
```
wisp => ("abc" "abc" eq?)
Bool(val=True)
wisp => (12 "abc" eq?)
Bool(val=False)
```

quote!
```
wisp => ((1 2 3) quote)
List(items=[Integer(val=1), Integer(val=2), Integer(val=3)])
```

cons, car & cdr!
```
wisp => (((() 3 cons) 2 cons) 1 cons)
List(items=[Integer(val=1), Integer(val=2), Integer(val=3)])
wisp => (((1 2 3) quote) car)
Integer(val=1)
wisp => (((1 2 3) quote) cdr)
List(items=[Integer(val=2), Integer(val=3)])
wisp => ((((1 2 3) quote) cdr) car)
Integer(val=2)
```

atom!
```
wisp => (4 atom?)
Bool(val=True)
wisp => (((1 2 3) quote) atom?)
Bool(val=False)
```

define!
```
wisp => (3 x define)
Symbol(name='x')
wisp => (4 y define)
Symbol(name='y')
wisp => (x y +)
Integer(val=7)
```

lambda!
```
wisp => (4 ((x x *) (x) lambda))
Integer(val=16)
wisp => (((x x *) (x) lambda) square define)
Symbol(name='square')
wisp => (4 square)
Integer(val=16)
```

lambdas are evaluated in their own scope!
```
wisp => (3 x define)
Symbol(name='x')
wisp => (2 ((x x *) (x) lambda))
Integer(val=4)
wisp => x
Integer(val=3)
```


conditional expressions!
```
wisp => (1 a define)
Symbol(name='a')
wisp => (("something-else" else) ("two" (2 a eq?)) ("one" (1 a eq?)) cond)
String(val='one')
wisp => (2 a define)
Symbol(name='a')
wisp => (("something-else" else) ("two" (2 a eq?)) ("one" (1 a eq?)) cond)
String(val='two')
wisp => (3 a define)
Symbol(name='a')
wisp => (("something-else" else) ("two" (2 a eq?)) ("one" (1 a eq?)) cond)
String(val='something-else')
```

Notes
-----
I may have been having a bit too much fun and spent more like six to
eight than four to six hours on this. Still need to do a bit more work
for useful recursion and closures, though!
