# Pinnacles of Permutations

Here we highlight two methods, `pinGen1` and `pinGen2`.

- `pinGen1` is the naive implementation for producing all permutations with a given pinnacle set.
- `pinGen2` is the new implementation, which is _much_ more efficient.

Note that each of these methods return iterators as opposed to lists.

### Breakdown of methods

###### Main Methods:

- `pinGen1(n, pins)`
  - Relatively simple.
  - Generates all permutations in _Sn_.
  - Only yields those permutations satisfying `pin(pi) == pins`.
- `altPinGen1(n, pins)`
  - Also relatively simple.
  - Alternative implementation of `pinGen1` using `filter` and `map` to improve efficiency.
- `pinGen2(n, pins)`
  - More complicated.
  - Generates all and only those permutations in _Sn_ with the desired pinnacle set.
  - For proof that this method produces what it claims, see paper ***link paper***.

###### Other Methods:

- `factorial(n)`
  - Just an implementation of factorial for non-negative integers.
- `serialize(pi) -> number, size`
  - Given a permutation `pi`, returns two integers which can be used to recover the permutation.
  - Reverse of `deserialize`.
- `deserialize(number, size) -> pi`
  - Given a `number` in `range(0, factorial(size))`, returns a permutation of that size.
  - Reverse of `serialize`
- `getPV(x) -> P, V`
  - Given a permutation, returns the pinnacle and vale set of the permutation.
- `pin(x) -> P`
  - Given a permutation, returns the pinnacle set of the permutation.
