ILLA
====

An implementation of a like-Lambda Calculus
-------------------------------------------

Need Python3, [PLY](http://www.dabeaz.com/ply/) and [argv](https://github.com/chbrown/argv)

It's possible use *call by name* or *call by value* for the evaluation.

Usage
-----

     testing_interpreter.py [-v|(-p|-n)] -f file_to_execute
    
       -v   call by value (by default is the strategy `call by name`)
       -p   print each reduction (default)
       -n   not print reductions (override `-p`)

Examples
--------

    $ # see: https://en.wikipedia.org/wiki/Lambda_calculus#Recursion_and_fixed_points
    $ testing_interpreter.py -f examples/factorial.lambda
    Y fac 2
    
    = Y fac 2
    = (λf.(λx.x x) (λx.f (x x))) fac 2
    = ((λx.x x) (λx.fac (x x))) 2 // β-reduc
    = (λx.x x) (λx.fac (x x)) 2 // left assoc λ aplications: (f x) y = f x y
    = ((λx.fac (x x)) (λx.fac (x x))) 2 // β-reduc
    = (λx.fac (x x)) (λx.fac (x x)) 2 // left assoc λ aplications: (f x) y = f x y
    = (fac ((λx.fac (x x)) (λx.fac (x x)))) 2 // β-reduc
    = fac ((λx.fac (x x)) (λx.fac (x x))) 2 // left assoc λ aplications: (f x) y = f x y
    = (λf.λx.if (x=0) 1 (x*f (x-1))) ((λx.fac (x x)) (λx.fac (x x))) 2
    = (λx.if (x=0) 1 (x*((λx.fac (x x)) (λx.fac (x x))) (x-1))) 2 // β-reduc
    = if (2=0) 1 (2*((λx.fac (x x)) (λx.fac (x x))) (2-1)) // β-reduc
     if|= 2=0
     if|= false
    = 2*((λx.fac (x x)) (λx.fac (x x))) (2-1)
      r-> ((λx.fac (x x)) (λx.fac (x x))) (2-1)
      |= ((λx.fac (x x)) (λx.fac (x x))) (2-1)
      |= (λx.fac (x x)) (λx.fac (x x)) (2-1) // left assoc λ aplications: (f x) y = f x y
      |= (fac ((λx.fac (x x)) (λx.fac (x x)))) (2-1) // β-reduc
      |= fac ((λx.fac (x x)) (λx.fac (x x))) (2-1) // left assoc λ aplications: (f x) y = f x y
      |= (λf.λx.if (x=0) 1 (x*f (x-1))) ((λx.fac (x x)) (λx.fac (x x))) (2-1)
      |= (λx.if (x=0) 1 (x*((λx.fac (x x)) (λx.fac (x x))) (x-1))) (2-1) // β-reduc
      |= if (2-1=0) 1 ((2-1)*((λx.fac (x x)) (λx.fac (x x))) (2-1-1)) // β-reduc
      | if|= 2-1=0
      | if|  l-> 2-1
      | if|  |= 2-1
      | if|  |= 1
      | if|= false
      |= (2-1)*((λx.fac (x x)) (λx.fac (x x))) (2-1-1)
      |  l-> 2-1
      |  |= 2-1
      |  |= 1
      |  r-> ((λx.fac (x x)) (λx.fac (x x))) (2-1-1)
      |  |= ((λx.fac (x x)) (λx.fac (x x))) (2-1-1)
      |  |= (λx.fac (x x)) (λx.fac (x x)) (2-1-1) // left assoc λ aplications: (f x) y = f x y
      |  |= (fac ((λx.fac (x x)) (λx.fac (x x)))) (2-1-1) // β-reduc
      |  |= fac ((λx.fac (x x)) (λx.fac (x x))) (2-1-1) // left assoc λ aplications: (f x) y = f x y
      |  |= (λf.λx.if (x=0) 1 (x*f (x-1))) ((λx.fac (x x)) (λx.fac (x x))) (2-1-1)
      |  |= (λx.if (x=0) 1 (x*((λx.fac (x x)) (λx.fac (x x))) (x-1))) (2-1-1) // β-reduc
      |  |= if (2-1-1=0) 1 ((2-1-1)*((λx.fac (x x)) (λx.fac (x x))) (2-1-1-1)) // β-reduc
      |  | if|= 2-1-1=0
      |  | if|  l-> 2-1-1
      |  | if|  |= 2-1-1
      |  | if|  |  l-> 2-1
      |  | if|  |  |= 2-1
      |  | if|  |  |= 1
      |  | if|  |= 0
      |  | if|= true
      |  |= 1
      |= 1
    = 2
    
    = 2

    $ testing_interpreter.py -nf examples/factorial.lambda
    2

    $ # see: https://en.wikipedia.org/wiki/99_Bottles_of_Beer
    $ testing_interpreter.py -vnf examples/beer.lambda
    
    99 bottles of beer on the wall, 99 bottles of beer.
    Take one down and pass it around, 98 bottles of beer on the wall.
    
    98 bottles of beer on the wall, 98 bottles of beer.
    Take one down and pass it around, 97 bottles of beer on the wall.
    
    ...
    
    1 bottle of beer on the wall, 1 bottle of beer.
    Take one down and pass it around, no more bottles of beer on the wall.
    
    No more bottles of beer on the wall, no more bottles of beer.
    Go to the store and buy some more, 99 bottles of beer on the wall.

TODO
----

- add lazy evaluation: *call by need*

Issues
------

- Currently, this mini-interpreter can only be executed in linux. Because, PLY
  has problems in windows.

PS
--

I'm sorry by my bad English.
