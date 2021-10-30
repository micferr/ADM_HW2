TQ1
===

TQ1.1
---

Given an array of real numbers `A` of length `n` and an integer `k` such that `1 <= k <= n`, the algorithm computes the `k`-th smallest value in A.

The algorithm works as follows:
1. First it picks a random element `s` from A, and splits `A` in two subarrays `L` and `R`, with the former containing all values `v` of `A` such that `v <= s`, and the latter the remaining ones (which is, all `v'` in `A` such that `v' > s`). Note that `A` is not sorted (otherwise computing the `k`-th smallest value would be trivial), and by construction neither are `L` and `R`.

2. Now, three possible scenarios are possible depending on the relationship between `len(L)` and `k`:

    - If `len(L) == k` then `s` is returned, since it must be the `k`-th smallest element in A. This is because, since there are exactly `k` values in `A` that are no greater than `s`, and `s` is actually in the array `A`, then `s` must be the `k`-th smallest.
    - If `len(L) < k`, then the algorithm recurses using `L` as the new value of `A` and `k` as itself.
    - If `len(L) > k`, then the algorithm recurses using `R` as the new value of `A`. Concerning the `k` parameter, `k-len(L)` is used to account for the elements in `L` that have to be skipped when searching looking for the desired value, since the `n`-th smallest element in `R` is the `n+len(L)` in `A`.

    In the second and third case, the algorithm may recurse indefinitely until `len(A) == 1`, in which case the only value in `A` is returned.

TQ1.2
---

The algorithm's running time depends on the random selections of `s` at each invocation of the algorithm (either the first call or recursive ones). The worst case happens when either the smallest or biggest value in the array is repeatedly picked as `s` and `k` is close to the other extreme (i.e. either `k` is low and a high value is repeatedly picked as `s`, or vice versa).
In that case, at each step the algorithm `A` gets split into two subarrays, one of length equal to 1, which gets discarded, and another of length `len(A)-1` on which the algorithm recurses.

Considering that splitting `A` into `L` and `R` has a complexity of O(n), the big-O complexity analysis in this case yields a complexity of O(n^2) either by applying the Master Theorem, or by explicitly summing the complexity of splitting `A` at each recursion level, with `len(A)` splitting operations of linear complexity applied to arrays of size `2,3,...,len(A)` yielding again O(n^2) by Gauss sum.

TQ1.3
---

In the best case, the `k`-th smallest value in `A` is randomly picked as `s` the first time the algorithm is executed.

Since the recursion step is never executed, the resulting complexity is given by the time required to split `A` into `L` and `R`, which by being linear yields a best-case complexity of O(n).

TQ2
===

TQ2.1
---

The algorithm reverses the array that is passed as its first argument (provided that in the initial invocation 0 and the array's length are passed as second and third argument).

The complexity of `swapList` is trivially linear in the length of its array argument (actually half its length, but the `0.5` factor is discarded in big-O analysis), leading to `splitSwap` having a recurrence relation of T(n) = 2T(n/2) + O(n).

By applying the Master Theorem, the result for overall algorithm's complexity is `O(n*log(n))` since the complexities of splitting and recombining the problem are comparable.

The same result can be easily computed by summation, and the algorithm's running time is actually `Θ(n*log(n))`, since the algorithm recurses for `log2(n)` levels and at each step computes a number of `swapList`s equal to `2^level`, each on an array of size `len(a)/(2^level)`, totalling `O(n)` complexity for each recursion level.

TQ2.2
---

The algorithm works recursively by first reversing its first and second halves independently (in the recursive step), then by swapping these halves by assuming them to be reversed.

In the recursive step, recursion proceeds indefinitely until the two halves are of length equal to 1. The recursive steps are no-ops as they return immediately, then `swapList` just swaps these two elements (the description assumes the array to be of size `2^n` for some integer `n` for simplicity, but the algorithm works even when that's not the case).

More generally, `swapList` iterates an array up to its midpoint, swapping its `i`-th element with the `i`-th after the midpoint, effectively swapping the array's first and second halves.

After the last recursion level is reached, the recombination step runs on bigger and bigger arrays, each with its two halves in the correct order, until the whole array is finally reversed.

We noted above that the algorithm's complexity is linearithmic in the array's size, though now that we know what it does it's trivial to show its not optimal by providing an optimal implementation running in `Θ(n)`, shown next:

```
function reverseArray(a,l,n):
    for i=0 to n/2:
        tmp = a[i]
        a[i] = a[n-1-i]
        a[n-1-i] = tmp
```

Just as `splitSwap`, `reverseArray` is meant to be called as `reverseArray(a,0,len(a))`.

TQ3
===

TQ3.1
---

```
W = 2

w_1 = 1, v_1 = 1
w_2 = 2, v_2 = 2
```

The first heuristic select `i_1` to be included, then stops as it has no more room for `i_2`. The resulting value in the knapsack is 1, but it would have been `2` by selecting only `i_2`.

TQ3.2
---

```
W = 2

w_1 = 2, v_1 = 3
w_2 = 1, v_2 = 2
w_3 = 1, v_3 = 2
```

The second heuristic selects only `i_1` to be included, since it has the highest value and then there's no more room for other items.
The resulting value is 3, but it would have been 4 by selecting `i_2` and `i_3`, which could fit together in the knapsack.

TQ3.3
---

```
W = 4

w_1 = 3, v_1 = 4
w_2 = 2, v_2 = 2.5
w_3 = 2, v_3 = 2.5
```

The third heuristic only selects `i_1` since it has the highest value-to-cost ratio and then there's no more room for other items.
The resulting value is 4, but it would have been 5 by selecting `i_2` and `i_3`, which could fit together in the knapsack.
