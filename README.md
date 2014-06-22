ILLA
====

An implementation of a like-Lambda Calculus
-------------------------------------------

Need Python3 and [PLY](http://www.dabeaz.com/ply/)

Usage
-----

    $ python3 testing_interpreter.py <code.lambda>


Examples
--------

    $ python3 testing_interpreter.py examples/an_if.lambda
    
    if ((5=0)) ((a 2 3) a) 6
    
    = if ((5=0)) ((a 2 3) a) 6
     if|= (5=0)
     if|= false
    = 6
    
    = 6

    $ python3 testing_interpreter.py examples/factorial.code
    
    Y fac 5
    
    = Y fac 5
    = (λf.(λx.x x) (λx.f (x x))) fac 5
    = ((λx.x x) (λx.fac (x x))) 5 // β-reduc
    = (λx.x x) (λx.fac (x x)) 5 // left assoc λ aplications: (f x) y = f x y
    = ((λx.fac (x x)) (λx.fac (x x))) 5 // β-reduc
    = (λx.fac (x x)) (λx.fac (x x)) 5 // left assoc λ aplications: (f x) y = f x y
    = (fac ((λx.fac (x x)) (λx.fac (x x)))) 5 // β-reduc
    = fac ((λx.fac (x x)) (λx.fac (x x))) 5 // left assoc λ aplications: (f x) y = f x y
    = (λf.λx.if ((x=0)) 1 ((x*f ((x-1))))) ((λx.fac (x x)) (λx.fac (x x))) 5
    = (λx.if ((x=0)) 1 ((x*((λx.fac (x x)) (λx.fac (x x))) ((x-1))))) 5 // β-reduc
    = if ((5=0)) 1 ((5*((λx.fac (x x)) (λx.fac (x x))) ((5-1)))) // β-reduc
     if|= (5=0)
     if|= false
    = (5*((λx.fac (x x)) (λx.fac (x x))) ((5-1)))
      r-> ((λx.fac (x x)) (λx.fac (x x))) ((5-1))
      |= ((λx.fac (x x)) (λx.fac (x x))) ((5-1))
      |= (λx.fac (x x)) (λx.fac (x x)) ((5-1)) // left assoc λ aplications: (f x) y = f x y
      |= (fac ((λx.fac (x x)) (λx.fac (x x)))) ((5-1)) // β-reduc
      |= fac ((λx.fac (x x)) (λx.fac (x x))) ((5-1)) // left assoc λ aplications: (f x) y = f x y
      |= (λf.λx.if ((x=0)) 1 ((x*f ((x-1))))) ((λx.fac (x x)) (λx.fac (x x))) ((5-1))
      |= (λx.if ((x=0)) 1 ((x*((λx.fac (x x)) (λx.fac (x x))) ((x-1))))) ((5-1)) // β-reduc
      |= if (((5-1)=0)) 1 (((5-1)*((λx.fac (x x)) (λx.fac (x x))) (((5-1)-1)))) // β-reduc
      | if|= ((5-1)=0)
      | if|  l-> (5-1)
      | if|  |= (5-1)
      | if|  |= 4
      | if|= false
      |= ((5-1)*((λx.fac (x x)) (λx.fac (x x))) (((5-1)-1)))
      |  l-> (5-1)
      |  |= (5-1)
      |  |= 4
      |  r-> ((λx.fac (x x)) (λx.fac (x x))) (((5-1)-1))
      |  |= ((λx.fac (x x)) (λx.fac (x x))) (((5-1)-1))
      |  |= (λx.fac (x x)) (λx.fac (x x)) (((5-1)-1)) // left assoc λ aplications: (f x) y = f x y
      |  |= (fac ((λx.fac (x x)) (λx.fac (x x)))) (((5-1)-1)) // β-reduc
      |  |= fac ((λx.fac (x x)) (λx.fac (x x))) (((5-1)-1)) // left assoc λ aplications: (f x) y = f x y
      |  |= (λf.λx.if ((x=0)) 1 ((x*f ((x-1))))) ((λx.fac (x x)) (λx.fac (x x))) (((5-1)-1))
      |  |= (λx.if ((x=0)) 1 ((x*((λx.fac (x x)) (λx.fac (x x))) ((x-1))))) (((5-1)-1)) // β-reduc
      |  |= if ((((5-1)-1)=0)) 1 ((((5-1)-1)*((λx.fac (x x)) (λx.fac (x x))) ((((5-1)-1)-1)))) // β-reduc
      |  | if|= (((5-1)-1)=0)
      |  | if|  l-> ((5-1)-1)
      |  | if|  |= ((5-1)-1)
      |  | if|  |  l-> (5-1)
      |  | if|  |  |= (5-1)
      |  | if|  |  |= 4
      |  | if|  |= 3
      |  | if|= false
      |  |= (((5-1)-1)*((λx.fac (x x)) (λx.fac (x x))) ((((5-1)-1)-1)))
      |  |  l-> ((5-1)-1)
      |  |  |= ((5-1)-1)
      |  |  |  l-> (5-1)
      |  |  |  |= (5-1)
      |  |  |  |= 4
      |  |  |= 3
      |  |  r-> ((λx.fac (x x)) (λx.fac (x x))) ((((5-1)-1)-1))
      |  |  |= ((λx.fac (x x)) (λx.fac (x x))) ((((5-1)-1)-1))
      |  |  |= (λx.fac (x x)) (λx.fac (x x)) ((((5-1)-1)-1)) // left assoc λ aplications: (f x) y = f x y
      |  |  |= (fac ((λx.fac (x x)) (λx.fac (x x)))) ((((5-1)-1)-1)) // β-reduc
      |  |  |= fac ((λx.fac (x x)) (λx.fac (x x))) ((((5-1)-1)-1)) // left assoc λ aplications: (f x) y = f x y
      |  |  |= (λf.λx.if ((x=0)) 1 ((x*f ((x-1))))) ((λx.fac (x x)) (λx.fac (x x))) ((((5-1)-1)-1))
      |  |  |= (λx.if ((x=0)) 1 ((x*((λx.fac (x x)) (λx.fac (x x))) ((x-1))))) ((((5-1)-1)-1)) // β-reduc
      |  |  |= if (((((5-1)-1)-1)=0)) 1 (((((5-1)-1)-1)*((λx.fac (x x)) (λx.fac (x x))) (((((5-1)-1)-1)-1)))) // β-reduc
      |  |  | if|= ((((5-1)-1)-1)=0)
      |  |  | if|  l-> (((5-1)-1)-1)
      |  |  | if|  |= (((5-1)-1)-1)
      |  |  | if|  |  l-> ((5-1)-1)
      |  |  | if|  |  |= ((5-1)-1)
      |  |  | if|  |  |  l-> (5-1)
      |  |  | if|  |  |  |= (5-1)
      |  |  | if|  |  |  |= 4
      |  |  | if|  |  |= 3
      |  |  | if|  |= 2
      |  |  | if|= false
      |  |  |= ((((5-1)-1)-1)*((λx.fac (x x)) (λx.fac (x x))) (((((5-1)-1)-1)-1)))
      |  |  |  l-> (((5-1)-1)-1)
      |  |  |  |= (((5-1)-1)-1)
      |  |  |  |  l-> ((5-1)-1)
      |  |  |  |  |= ((5-1)-1)
      |  |  |  |  |  l-> (5-1)
      |  |  |  |  |  |= (5-1)
      |  |  |  |  |  |= 4
      |  |  |  |  |= 3
      |  |  |  |= 2
      |  |  |  r-> ((λx.fac (x x)) (λx.fac (x x))) (((((5-1)-1)-1)-1))
      |  |  |  |= ((λx.fac (x x)) (λx.fac (x x))) (((((5-1)-1)-1)-1))
      |  |  |  |= (λx.fac (x x)) (λx.fac (x x)) (((((5-1)-1)-1)-1)) // left assoc λ aplications: (f x) y = f x y
      |  |  |  |= (fac ((λx.fac (x x)) (λx.fac (x x)))) (((((5-1)-1)-1)-1)) // β-reduc
      |  |  |  |= fac ((λx.fac (x x)) (λx.fac (x x))) (((((5-1)-1)-1)-1)) // left assoc λ aplications: (f x) y = f x y
      |  |  |  |= (λf.λx.if ((x=0)) 1 ((x*f ((x-1))))) ((λx.fac (x x)) (λx.fac (x x))) (((((5-1)-1)-1)-1))
      |  |  |  |= (λx.if ((x=0)) 1 ((x*((λx.fac (x x)) (λx.fac (x x))) ((x-1))))) (((((5-1)-1)-1)-1)) // β-reduc
      |  |  |  |= if ((((((5-1)-1)-1)-1)=0)) 1 ((((((5-1)-1)-1)-1)*((λx.fac (x x)) (λx.fac (x x))) ((((((5-1)-1)-1)-1)-1)))) // β-reduc
      |  |  |  | if|= (((((5-1)-1)-1)-1)=0)
      |  |  |  | if|  l-> ((((5-1)-1)-1)-1)
      |  |  |  | if|  |= ((((5-1)-1)-1)-1)
      |  |  |  | if|  |  l-> (((5-1)-1)-1)
      |  |  |  | if|  |  |= (((5-1)-1)-1)
      |  |  |  | if|  |  |  l-> ((5-1)-1)
      |  |  |  | if|  |  |  |= ((5-1)-1)
      |  |  |  | if|  |  |  |  l-> (5-1)
      |  |  |  | if|  |  |  |  |= (5-1)
      |  |  |  | if|  |  |  |  |= 4
      |  |  |  | if|  |  |  |= 3
      |  |  |  | if|  |  |= 2
      |  |  |  | if|  |= 1
      |  |  |  | if|= false
      |  |  |  |= (((((5-1)-1)-1)-1)*((λx.fac (x x)) (λx.fac (x x))) ((((((5-1)-1)-1)-1)-1)))
      |  |  |  |  l-> ((((5-1)-1)-1)-1)
      |  |  |  |  |= ((((5-1)-1)-1)-1)
      |  |  |  |  |  l-> (((5-1)-1)-1)
      |  |  |  |  |  |= (((5-1)-1)-1)
      |  |  |  |  |  |  l-> ((5-1)-1)
      |  |  |  |  |  |  |= ((5-1)-1)
      |  |  |  |  |  |  |  l-> (5-1)
      |  |  |  |  |  |  |  |= (5-1)
      |  |  |  |  |  |  |  |= 4
      |  |  |  |  |  |  |= 3
      |  |  |  |  |  |= 2
      |  |  |  |  |= 1
      |  |  |  |  r-> ((λx.fac (x x)) (λx.fac (x x))) ((((((5-1)-1)-1)-1)-1))
      |  |  |  |  |= ((λx.fac (x x)) (λx.fac (x x))) ((((((5-1)-1)-1)-1)-1))
      |  |  |  |  |= (λx.fac (x x)) (λx.fac (x x)) ((((((5-1)-1)-1)-1)-1)) // left assoc λ aplications: (f x) y = f x y
      |  |  |  |  |= (fac ((λx.fac (x x)) (λx.fac (x x)))) ((((((5-1)-1)-1)-1)-1)) // β-reduc
      |  |  |  |  |= fac ((λx.fac (x x)) (λx.fac (x x))) ((((((5-1)-1)-1)-1)-1)) // left assoc λ aplications: (f x) y = f x y
      |  |  |  |  |= (λf.λx.if ((x=0)) 1 ((x*f ((x-1))))) ((λx.fac (x x)) (λx.fac (x x))) ((((((5-1)-1)-1)-1)-1))
      |  |  |  |  |= (λx.if ((x=0)) 1 ((x*((λx.fac (x x)) (λx.fac (x x))) ((x-1))))) ((((((5-1)-1)-1)-1)-1)) // β-reduc
      |  |  |  |  |= if (((((((5-1)-1)-1)-1)-1)=0)) 1 (((((((5-1)-1)-1)-1)-1)*((λx.fac (x x)) (λx.fac (x x))) (((((((5-1)-1)-1)-1)-1)-1)))) // β-reduc
      |  |  |  |  | if|= ((((((5-1)-1)-1)-1)-1)=0)
      |  |  |  |  | if|  l-> (((((5-1)-1)-1)-1)-1)
      |  |  |  |  | if|  |= (((((5-1)-1)-1)-1)-1)
      |  |  |  |  | if|  |  l-> ((((5-1)-1)-1)-1)
      |  |  |  |  | if|  |  |= ((((5-1)-1)-1)-1)
      |  |  |  |  | if|  |  |  l-> (((5-1)-1)-1)
      |  |  |  |  | if|  |  |  |= (((5-1)-1)-1)
      |  |  |  |  | if|  |  |  |  l-> ((5-1)-1)
      |  |  |  |  | if|  |  |  |  |= ((5-1)-1)
      |  |  |  |  | if|  |  |  |  |  l-> (5-1)
      |  |  |  |  | if|  |  |  |  |  |= (5-1)
      |  |  |  |  | if|  |  |  |  |  |= 4
      |  |  |  |  | if|  |  |  |  |= 3
      |  |  |  |  | if|  |  |  |= 2
      |  |  |  |  | if|  |  |= 1
      |  |  |  |  | if|  |= 0
      |  |  |  |  | if|= true
      |  |  |  |  |= 1
      |  |  |  |= 1
      |  |  |= 2
      |  |= 6
      |= 24
    = 120
    
    = 120

TODO
----

- improve printing (add `myPrint` variable to almost all the functions)
- add options to the main file (in `testing_interpreter.py`)
- add support to `fst` and `snd` primitive functions
- add primitive `toString`

PS
--

I'm sorry by my bad English.
