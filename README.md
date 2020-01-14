# Pinnacles of Permutations

Here we highlight two methods, `pinGen1` and `pinGen2`.

- `pinGen1` is the naive implementation for producing all permutations with a given pinnacle set.
- `pinGen2` is the new implementation, which is _much_ more efficient.

Note that each of these methods return iterators as opposed to lists.

Also note here the natural numbers are taken to be the non-negative (as opposed to positive) integers.

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

###### Examples:

`>>> [*pinGen1(5, {3, 4})]`
`[[0, 3, 1, 4, 2], [1, 3, 0, 4, 2], [2, 3, 0, 4, 1], [0, 4, 1, 3, 2],`<br/>
&nbsp`[1, 4, 0, 3, 2], [2, 4, 0, 3, 1], [0, 3, 2, 4, 1], [1, 3, 2, 4, 0],`<br/>
&nbsp`[2, 3, 1, 4, 0], [0, 4, 2, 3, 1], [1, 4, 2, 3, 0], [2, 4, 1, 3, 0]]`

`>>> [*pinGen2(5, {3, 4})]`

`[[0, 4, 1, 3, 2], [0, 4, 2, 3, 1], [1, 3, 2, 4, 0], [2, 3, 1, 4, 0], [1, 4, 0, 3, 2], [1, 4, 2, 3, 0], [0, 3, 2, 4, 1], [2, 3, 0, 4, 1], [2, 4, 0, 3, 1], [2, 4, 1, 3, 0], [0, 3, 1, 4, 2], [1, 3, 0, 4, 2]]`

`>>> [*pinGen1(5, set())]`

`[[0, 1, 2, 3, 4], [1, 0, 2, 3, 4], [2, 0, 1, 3, 4], [3, 0, 1, 2, 4], [4, 0, 1, 2, 3], [2, 1, 0, 3, 4], [3, 1, 0, 2, 4], [4, 1, 0, 2, 3], [3, 2, 0, 1, 4], [4, 2, 0, 1, 3], [4, 3, 0, 1, 2], [3, 2, 1, 0, 4], [4, 2, 1, 0, 3], [4, 3, 1, 0, 2], [4, 3, 2, 0, 1], [4, 3, 2, 1, 0]]`

`>>> [*pinGen2(5, set())]`

`[[0, 1, 2, 3, 4], [1, 0, 2, 3, 4], [2, 0, 1, 3, 4], [2, 1, 0, 3, 4], [3, 0, 1, 2, 4], [3, 1, 0, 2, 4], [3, 2, 0, 1, 4], [3, 2, 1, 0, 4], [4, 0, 1, 2, 3], [4, 1, 0, 2, 3], [4, 2, 0, 1, 3], [4, 2, 1, 0, 3], [4, 3, 0, 1, 2], [4, 3, 1, 0, 2], [4, 3, 2, 0, 1], [4, 3, 2, 1, 0]]`

`>>> x = [*pinGen2(10, {})]`

`>>> len(x) -> 239232`

`>>> w = [*pinGen2(12, {7,9,11})]`

`>>> len(w) -> 11542272`

`>>> factorial(12) -> 479001600`

Note that `w` was computed in under a minute, generating just over 11.5 million permutations.
`pinGen1` would need to generate all ~479 million permutations in *S*12, discarding the vast majority of them.
On other tests, `pinGen1` took ~300ms in *S*8.  Noting the factorial growth of this function, *S*12 would take roughly an hour.
