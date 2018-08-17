Title: Introduction to OCaml, part 5: exceptions, lists, and structural induction
Date: 2018-08-14 00:00:00
Category: Programming languages
Tags: ocaml

# Exceptions

In OCaml, exceptions are not objects, and there are no exception hierarchies. It may look unusual now,
but in fact exceptions predate the rise of object oriented languages and it's more in line with original
implementations. The advantage is that they are very lightweight.

The syntax for defining exception is reminiscent of sum types with a single data constructors.
The data constructors can be either nullary or can have value or any type attached to them.

All exceptions are essentially members of a single extensible (_open_) sum type _exn_, with some language
magic to allow raising and catching them.

This is how you can define new exceptions:

```
exception Access_denied

exception Invalid_value of string
```

## Raising and catching exceptions

It is important to learn how to use exceptions because many functions from the standard library and third party
libraries alike use them, and it's impossible to avoid them even if you prefer to write your own code in
purely functional style.

For example, the division functions `/` and `/.` raise a `Division_by_zero` exception when the divisor is zero.

To learn how to raise an exception ourselves, we can reimplement the `/` function to raise our own exception.
They are raised using the `raise : exn -> 'a` function:

```
exception Invalid_value of string

let (//) x y =
  if y <> 0 then x / y
  else raise (Invalid_value "Attempted division by zero")
```

Now let's learn how to catch exceptions:

```
let _ =
  try
    let x = 4 // 0 in
    Printf.printf "%d\n" x
  with Invalid_value s -> print_endline s
```

Note that `try ... with` constructs are expressions rather than statements, and can be easily used
inside `let`-bindings, for example to provide a default value in case an exception is raised:

```
let x = try 4 / 0 with Division_by_zero -> 0 (* x = 0 *)

let _ = Printf.printf "%d\n" x
```

Another implication of the fact that `try ... with` is an expression is that all expressions in the
`try` and `with` clauses must have the same type. This would cause a type error:

```
let x = try 4 / 0 with Division_by_zero -> print_endline "Division by zero"
```

You can catch multiple exceptions using a syntax similar to that of `match` expressions:

```
let _ =
  try
    let x = 4 // 0 in
    Printf.printf "%d\n" x
  with
    Invalid_value s -> print_endline s
  | Division_by_zero -> print_endline "Division by zero"

```

So far our examples assumed that we know all exceptions our functions can possibly raise, or do not want
to catch any other exceptions, which is not always the case. Since there are no exception hierarchies,
we cannot catch a generic exception, but we can use the wildcard pattern to catch any possible exception.
The downside of course is that if an exception comes with an attached value, we cannot destructure
it and extract the value since the type of that value is not known in advance.

```
let _ =
  try
    let x = 4 // 0 in
    Printf.printf "%d\n" x
  with
    Invalid_value s -> print_endline s
  | _ -> print_endline "Something went wrong"

```

# Linked lists

Linked lists are among the most commonly used data structures.

This is how to create a non-empty list: `let xs = [1; 2; 3; 4]`.
Semicolon as a list element separator may look odd, but it has advantages,
since it makes it very easy to make a list of tuples: `let ys = ["foo", 1; "bar", 2]`.
If the separator for list and tuple element was the same, it would require a lot
more parentheses.

# Structural induction and recursion

Structural induction and its twin &mdash; structural recursion is a common technique for creating
data type and function definitions and reasoning about them. It is an essential tool, which you may have already
started used intuitively with experience, but knowing at least the correct terminology helps, so we'll discuss
the concept semi-formally.

Remember the factorial function:

```
let rec fact n =
  match n with
    0 -> 1
  | n -> n * (fact (n - 1))
```

That function is recursive. However, the definition of factorial that we used to implement it
is _inductive_.

An inductive definition of a function consists of two parts: a _base case_ that defines how to calculate it for the least possible element,
and an _induction step_ that defines how to do it for the next element assuming we know the value for the previous element.

Let's examine the factorial definition:

1. Base case: 0! = 1
2. Inductive step: (n+1)! = n! * (n+1)

In other words,

1. Factorial of zero equals 1
2. If we know the factorial of _n_, then we can calculate the factorial of (n+1) by multiplying _n!_ by _(n+1)_.

An inductive definition can be easily converted to a recursive algorithm, assuming we know how to calculate previous element.

When the domain of the function in question is natural numers, this is often called simply _mathematical induction_.
However, it can be generalized to any set (or type) that has the least element. This is known as _structural induction_.
Most common data structures naturally include a smallest possible element (an empty list, an empty binary tree and so on), so the idea is easily
applicable to them.

Recursion derived from inductive definitions is known as _structural recursion_. What's special about it is that it is guaranteed to terminate,
assuming it's implemented correctly. 
Since a structurally recursive function only applies itself to smaller parts of the original data, it is guaranteed to eventually reach the base case, which is not recursive.
The other kind &mdash; _generative recursion_, that creates new entirely data before recursively applying a function to it, doesn't have
this property, and is much harder to reason about.

Our factorial function is not structurally recursive because it takes an integer rather than a natural number, and substitutes destructuring with
decrement. If you give it a negative number, it will never terminate, so for real life use we would want it to check if the argument is not negative.

However, we can make it structurally recursive if we define the type of natural numbers inductively, by defining the smallest possible natural number (zero)
and an inductive step for creating bigger natural numbers from it:

1. Zero is a natural number
2. There exists a _successor function_ `Succ n` such that for any natural number `n`, `Succ n` is also a natural number.
3. Nothing else is a natural number.

If we substitute _function_ with a data constructor (since functions in OCaml cannot be directly destructured, while data constructors can),
we can translate it to the following type definition: `type nat = Zero | Succ of nat`. Then we can create natural numbers from zero by applying
the `Succ` constructor multiple times: `Succ Zero`, `Succ (Succ Zero)` and so on. It would be very bad for performance, but it's perfect for
demonstration. If you want to learn more about this approach, look up Peano axioms.

In this context it's just a stepping stone for inductive definitions of data structures, because they follow the same pattern: first we define
a data constructor for an empty data structure, and then a constructor for growind larger data structures from the empty data structure and
some values.

## Defining the list type

The list type is defined as follows:

1. An empty list (`[]`) is a list.
2. A pair of a value `x` and a list `xs` (`x :: xs`) is also a list.
3. Nothing else is a list.

In OCaml we cannot create our own infix data constructors, but in imaginary syntax it could be written like this:

```
type 'a list = [] | 'a :: 'a list
``` 

So the `'a list` type is simply a sum type with two data constructors, one for the empty list, and another for non-empty lists
made from a value (head) and another list (tail). The square brackets syntax is simply a syntactic sugar, and we could create
any list using the empty list value `[]` and the `::` constructor alone. The following definitions are equivalent:


```
let xs = []

let ys = [1]
let ys' = 1 :: []
let ys'' = 1 :: xs

let zs = [2; 1]
let zs' = 2 :: (1 :: []) 

let ws = [3; 2; 1]
let ws' = 3 :: zs
```

The true syntax that is using data constructors is important because it can be used in pattern matching.
Here are some list patterns:

```
let rec length xs =
  match xs with
    [] -> 0
  | _ :: xs' -> 1 + (length xs')
```

