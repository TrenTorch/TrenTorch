> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Basics)

This page is about one habit: **thinking in counts of operations**. Before you write a program, you ask "how many little steps will this take when the input is big?" Once you can answer that, you can tell a fast idea from a slow one, and you can fix slow ideas with a handful of classic tricks: remembering what you have seen (hashing), keeping running totals (prefix sums), sliding a window, and jumping ahead with doubling. The page ends with a tour of the Python tools (sorting with keys, `Counter`, `heapq`, `bisect`, `itertools`, `math`) that save a lot of typing.

The page is a staircase. **Chapter 1 is deliberately gentle**: we just count how many times a loop runs, with tiny examples. Each chapter after it adds one idea, and the maths grows slowly. By the last chapters you will be able to look at a slow solution, say why it is slow, and replace it with a fast one. Every code example is shown in Python and in C++.

# Chapter 1. Counting what a program does

## 1.1 Steps instead of seconds

How long does a program take? If you time it with a stopwatch, the answer depends on your computer, on what else it is doing, and on the input. That is not very useful for comparing ideas. So we count **steps** instead. A step is one small thing the computer does: one addition, one comparison, one read from a list. We do not care whether a step takes a nanosecond or two. We care how the _number of steps_ grows when the input grows.

Look at this tiny function.

```python
def sum_to(n):
    total = 0                 # 1 step
    for i in range(1, n + 1):
        total += i            # runs n times
    return total              # 1 step


assert sum_to(4) == 10
assert sum_to(100) == 5050
```

```cpp
long long sum_to(long long n) {
    long long total = 0;
    for (long long i = 1; i <= n; i++) {
        total += i;
    }
    return total;
}
```

The line inside the loop runs once for every value of `i`, so it runs `n` times. Together with the two single lines, that is about `n + 2` steps. If `n` doubles, the work doubles. That is all there is to it: **look at the loops and count how often the inside runs.**

## 1.2 Two loops, one inside the other

When one loop sits inside another, the inside runs once for every pass of the outside. If both loops go over `n` values, the inside body runs $n \times n$ times.

```python
def square_count(n):
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1
    return count


assert square_count(3) == 9
assert square_count(10) == 100
```

```cpp
long long square_count(long long n) {
    long long count = 0;
    for (long long i = 0; i < n; i++) {
        for (long long j = 0; j < n; j++) {
            count++;
        }
    }
    return count;
}
```

For `n = 10` that is 100 steps. For `n = 1000` it is a million. For `n = 100000` it is ten billion, which no computer will finish quickly. Notice how fast the number grows: ten times more input made it a hundred times more work.

## 1.3 Pairs and the staircase

Now a small change: let the inner loop start just _after_ `i`. This is the usual way to look at every **pair** of positions once, without repeating a pair or pairing a position with itself.

```python
def pairs_loop(n):
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            count += 1
    return count


assert pairs_loop(4) == 6
assert pairs_loop(1) == 0
```

```cpp
long long pairs_loop(long long n) {
    long long count = 0;
    for (long long i = 0; i < n; i++) {
        for (long long j = i + 1; j < n; j++) {
            count++;
        }
    }
    return count;
}
```

How many times does the inside run? When `i = 0` the inner loop sees `n - 1` values. When `i = 1` it sees `n - 2`. It keeps shrinking like a staircase, down to `0` for the last `i`. For `n = 4` that is $3 + 2 + 1 + 0 = 6$.

There is a neat way to add up $1 + 2 + \dots + m$ without a loop. Write the numbers forwards, then backwards underneath, and add the columns:

```
  1   2   3  ...  m-1   m
  m  m-1 m-2  ...   2   1
  -----------------------
 m+1 m+1 m+1  ... m+1  m+1      (m columns)
```

Every column adds to $m + 1$, and there are $m$ columns, so twice the sum is $m(m+1)$. Therefore

$$1 + 2 + \dots + m = \frac{m(m+1)}{2}.$$

Our staircase adds up $1 + 2 + \dots + (n-1)$, so we put $m = n - 1$ and get $\frac{(n-1)n}{2}$ steps. Here is the formula next to the loop:

```python
def pairs_formula(n):
    return n * (n - 1) // 2


assert all(pairs_formula(n) == pairs_loop(n) for n in range(0, 30))
```

```cpp
long long pairs_formula(long long n) {
    return n * (n - 1) / 2;
}
```

Why can we use whole-number division here? Because $n(n-1)$ is always even: one of two neighbouring numbers is even. This is exactly the problem _Count the Pairs_: look at the shape of the loops, find the staircase, and write the formula instead of running the loops.

## 1.4 Check yourself

1. How many times does `count += 1` run in a loop `for i in range(5)` that contains `for j in range(3)`?
2. Why do we count steps instead of measuring seconds?
3. What does $1 + 2 + 3 + 4 + 5$ equal, using the formula in this chapter?
4. If a function has two nested loops over `n` values, what happens to the work when `n` becomes ten times bigger?

# Chapter 2. Growth and Big-O in plain words

## 2.1 How fast does it grow?

In Chapter 1 we saw that some programs do about $n$ steps and others about $n^2$. What matters is the _shape_ of the growth. Here are the usual shapes, from slowest-growing to fastest-growing, with the number of steps for three sizes of input. A logarithm, written $\log_2 n$, just answers "how many times can I halve $n$ before I reach 1?" For $n = 1000$ that is about 10, because $2^{10} = 1024$.

| Name        | Formula      | $n = 10$ | $n = 1000$          | $n = 10^6$          |
| ----------- | ------------ | -------- | ------------------- | ------------------- |
| constant    | $1$          | 1        | 1                   | 1                   |
| logarithmic | $\log_2 n$   | about 3  | about 10            | about 20            |
| linear      | $n$          | 10       | 1000                | 1,000,000           |
| n log n     | $n \log_2 n$ | about 33 | about 10,000        | about 20,000,000    |
| quadratic   | $n^2$        | 100      | 1,000,000           | $10^{12}$           |
| exponential | $2^n$        | 1024     | astronomically huge | astronomically huge |

Look at the last two columns. A logarithmic algorithm barely notices that the input grew a thousand times. A quadratic one does a trillion steps for a million items, which would take hours or days. An exponential one is hopeless beyond $n$ of about 30.

## 2.2 Throwing away the small stuff

Suppose counting gives $3n^2 + 5n + 2$ steps. For $n = 1000$ that is $3{,}005{,}002$. The $5n + 2$ part adds almost nothing. And the $3$ in front of $n^2$ is "just a constant": it changes the speed by a fixed factor, but it does not change the shape. So we write the cost as $O(n^2)$ and say "order $n$ squared" or "big-O of $n$ squared". The rule is easy:

> Keep only the fastest-growing part, and forget the number multiplied in front of it.

So $3n^2 + 5n + 2$ is $O(n^2)$, a loop that runs `n` times doing five things each time is $O(n)$, and "do this thing once" is $O(1)$. Big-O is a promise about the shape of growth, not an exact count. It is a rough ruler, and that is exactly what we want when comparing ideas.

Memory counts too. We write space the same way: a program that builds a list of `n` numbers uses $O(n)$ space, one that keeps just a few variables uses $O(1)$ space.

## 2.3 How big can n be?

Big-O is useful because it tells you how large an input a program can handle. A good rule of thumb: a computer does about $10^8$ simple steps in a second or so in C++, and about $10^7$ in plain Python. These are rough numbers, but they are enough to rank ideas.

Take a budget of $10^8$ steps and ask for the largest `n` for each shape. For a linear program, $n$ can be $10^8$. For $n^2$ we need $n^2 \le 10^8$, so $n \le 10^4$. For $n^3$ we need $n \le 464$, since $464^3 = 99{,}897{,}344$. For $2^n$ we need $n \le 26$. For $n \log n$, the answer is a bit above four million.

When there is no easy formula, you can simply try values. This function finds the largest `n` with $n^2 \le$ `budget` by walking up one at a time. (Do not use it for huge budgets; we will make this much faster in the next chapter.)

```python
def largest_n_quadratic(budget):
    n = 0
    while (n + 1) * (n + 1) <= budget:
        n += 1
    return n


assert largest_n_quadratic(100) == 10
assert largest_n_quadratic(99) == 9
assert largest_n_quadratic(10**6) == 1000
```

```cpp
long long largest_n_quadratic(long long budget) {
    long long n = 0;
    while ((n + 1) * (n + 1) <= budget) {
        n++;
    }
    return n;
}
```

Walking up one by one works for the quadratic case because the answer is only about the square root of the budget. For the faster-growing and slower-growing shapes you would use a smarter search: because each cost only gets bigger as `n` grows, you can halve the search range again and again. We will see exactly that halving idea in Chapter 3, and that is the plan for the largest-`n` question. This is exactly the problem _How Big Can n Be?_: pick the right search for each growth shape and find the largest `n` that fits the budget.

## 2.4 Check yourself

1. What is the big-O of $4n^2 + 100n + 7$?
2. Roughly how many steps does a linear algorithm do for $n = 10^6$, and how many does a quadratic one do?
3. Why can we ignore the constant in front of $n^2$ when we only want the shape of growth?
4. If a computer does $10^8$ steps per second, can an $O(n^2)$ program with $n = 10^5$ finish in a second?

# Chapter 3. Loops that halve, double, or stop at the square root

## 3.1 Halving gives a logarithm

Some loops do not step one at a time. This loop cuts the number in half each time:

```python
def halving_count(n):
    count = 0
    while n > 1:
        n //= 2        # whole-number division: 1000 becomes 500
        count += 1
    return count


assert halving_count(8) == 3
assert halving_count(1000) == 9
```

```cpp
int halving_count(long long n) {
    int count = 0;
    while (n > 1) {
        n /= 2;
        count++;
    }
    return count;
}
```

Start at 1000: 1000, 500, 250, 125, 62, 31, 15, 7, 3, 1. That is 9 halvings. In general, the number of halvings is $\lfloor \log_2 n \rfloor$ (the logarithm rounded down). A loop that halves is therefore very cheap: even for $n = 10^{18}$ it runs only 59 times.

There is a lovely connection to binary numbers. Each halving (with rounding down) drops the last binary digit of $n$. So the number of halvings is the number of binary digits minus one. Python gives the digit count directly as `n.bit_length()`:

```python
assert (1000).bit_length() == 10           # 1000 is 1111101000 in binary
assert halving_count(1000) == (1000).bit_length() - 1
```

```cpp
int halving_count_fast(long long n) {
    // 63 minus the number of leading zero bits is the position of the top 1 bit
    return 63 - __builtin_clzll(n);   // valid for n >= 1
}
```

This is exactly the problem _Halving Steps_: you can run it, or you can read the answer straight from the binary length.

## 3.2 Doubling is halving in reverse

Now run the film backwards. Start with `i = 1` and keep doubling until `i` reaches `n`:

```python
def doubling_count(n):
    count = 0
    i = 1
    while i < n:
        i *= 2
        count += 1
    return count


assert doubling_count(8) == 3        # i goes 1, 2, 4, 8
assert doubling_count(9) == 4        # i goes 1, 2, 4, 8, 16
assert doubling_count(1) == 0
```

```cpp
int doubling_count(long long n) {
    int count = 0;
    long long i = 1;
    while (i < n) {
        i *= 2;
        count++;
    }
    return count;
}
```

The answer is the smallest `k` with $2^k \ge n$. This is $\lceil \log_2 n \rceil$, the logarithm rounded _up_. Here is a way to get it without a loop. Saying $2^k \ge n$ is the same as saying $2^k > n - 1$ for whole numbers, and the smallest `k` with $2^k > m$ is the number of binary digits of `m`. So the answer is `(n - 1).bit_length()` for $n \ge 1$.

```python
assert (8 - 1).bit_length() == 3
assert (9 - 1).bit_length() == 4
assert all(doubling_count(n) == (n - 1).bit_length() for n in range(1, 200))
```

```cpp
int doubling_count_fast(long long n) {
    if (n <= 1) return 0;
    return 64 - __builtin_clzll(n - 1);   // number of binary digits of n - 1
}
```

This is exactly the problem _Doubling Steps_. Both halving and doubling loops are $O(\log n)$. Whenever you see a loop that multiplies or divides its counter, think "logarithm".

## 3.3 Loops that stop at the square root

Another important shape: a loop that goes up by one but stops when `i * i` passes `n`. It runs about $\sqrt{n}$ times. The most famous user is checking whether a number is prime. If `n` has a divisor larger than $\sqrt{n}$, then it also has a partner divisor smaller than $\sqrt{n}$ (because the two multiply to `n`), so it is enough to look at divisors up to the square root.

```python
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


assert is_prime(97)
assert not is_prime(91)          # 91 = 7 * 13
assert not is_prime(1)
```

```cpp
bool is_prime(long long n) {
    if (n < 2) return false;
    for (long long i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}
```

For $n$ near $10^{12}$ this does at most a million checks, which is fine. But if the _question_ is just "how many times does a loop of this shape run?", then running it is wasteful when $n$ is as large as $10^{18}$: that would be a billion steps. The loop counts every `i` with $i^2 \le n$, which is exactly the largest `r` with $r^2 \le n$. That number is the **integer square root** of `n`. We can find it without any such loop by halving the search range again and again:

```python
def isqrt_search(n):
    lo, hi = 0, n          # the answer is somewhere in [lo, hi]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= n:
            lo = mid       # mid is small enough, maybe something bigger works
        else:
            hi = mid - 1   # mid is too big
    return lo


assert isqrt_search(16) == 4
assert isqrt_search(17) == 4
assert isqrt_search(24) == 4
assert isqrt_search(25) == 5
assert isqrt_search(0) == 0
```

```cpp
long long isqrt_search(long long n) {
    long long lo = 0, hi = min(n, (long long)3037000499LL);  // 3037000499^2 still fits in long long
    while (lo < hi) {
        long long mid = (lo + hi + 1) / 2;
        if (mid * mid <= n) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}
```

Each round throws away half of the candidates, so this takes only about $\log_2 n$ rounds. The `+ 1` in `mid` makes sure we round up, so `lo = mid` always moves forward and the loop cannot get stuck. In Python you also have `math.isqrt(n)`, which does the same thing and works on numbers of any size. This is exactly the problem _Square Root Loop_: the loop's count is the integer square root of `n`.

## 3.4 Check yourself

1. How many times does `while n > 1: n //= 2` run for $n = 64$?
2. What is the number of doublings needed for `i` to reach at least 100, starting from 1?
3. Why is it enough to test divisors only up to $\sqrt{n}$ when checking for a prime?
4. Why is halving the search range each round so much faster than trying every value?

# Chapter 4. Harder loop counts

## 4.1 Three nested loops

Chapter 1 gave us two nested loops where the inner one starts where the outer one is. Let us add a third. Here the middle loop starts at `i` and the inner one starts at `j`, so the values never go down:

```python
def triple_count(n):
    count = 0
    for i in range(n):
        for j in range(i, n):
            for k in range(j, n):
                count += 1
    return count


assert triple_count(1) == 1
assert triple_count(2) == 4
assert triple_count(3) == 10
```

```cpp
long long triple_count(long long n) {
    long long count = 0;
    for (long long i = 0; i < n; i++)
        for (long long j = i; j < n; j++)
            for (long long k = j; k < n; k++)
                count++;
    return count;
}
```

The counts for $n = 1, 2, 3, 4, 5, 6$ are 1, 4, 10, 20, 35, 56. Where does this come from? Each time the count equals the number of triples $(i, j, k)$ with $0 \le i \le j \le k < n$. Here is a trick that turns this into something we know. Add 0 to `i`, 1 to `j` and 2 to `k`. The new triple $(i, j+1, k+2)$ is now **strictly** increasing, and its values lie between $0$ and $n + 1$. Every strictly increasing triple from the $n + 2$ numbers $0, 1, \dots, n+1$ can be undone back to exactly one of ours. So we are counting how many ways to _choose 3 different numbers out of $n + 2$_, ignoring order. That count is written $\binom{n+2}{3}$ and equals

$$\binom{n+2}{3} = \frac{(n+2)(n+1)n}{3 \cdot 2 \cdot 1} = \frac{n(n+1)(n+2)}{6}.$$

(Why? There are $(n+2)(n+1)n$ ways to pick three numbers one after the other, and every group of three gets counted $3! = 6$ times, once for each order.) Check with $n = 3$: $3 \cdot 4 \cdot 5 / 6 = 10$. ✓.

```python
def triple_formula(n):
    return n * (n + 1) * (n + 2) // 6


assert all(triple_formula(n) == triple_count(n) for n in range(0, 25))
```

```cpp
long long triple_formula(long long n) {
    return n * (n + 1) * (n + 2) / 6;
}
```

One warning for C++: the product $n(n+1)(n+2)$ is about $n^3$ and can overflow a 64-bit number before the division, even when the final answer fits. For very large `n` you can first divide the factor that is a multiple of 2 and the one that is a multiple of 3, then multiply. Python never overflows, so you do not need to worry there. This is exactly the problem _Three Nested Loops_.

## 4.2 A loop whose inner step jumps

Next, a loop whose inner step is `i` instead of 1:

```python
def jump_loop(n):
    count = 0
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            count += 1
    return count


assert jump_loop(5) == 10
```

```cpp
long long jump_loop(long long n) {
    long long count = 0;
    for (long long i = 1; i <= n; i++)
        for (long long j = i; j <= n; j += i)
            count++;
    return count;
}
```

For a given `i`, the inner loop visits `i, 2i, 3i, ...` up to `n`, which is $\lfloor n / i \rfloor$ values. So the total is

$$\sum_{i=1}^{n} \left\lfloor \frac{n}{i} \right\rfloor.$$

This sum behaves like $n$ times $\left(1 + \frac12 + \frac13 + \dots + \frac1n\right)$, and that bracket grows like $\ln n$. So the whole loop is about $O(n \log n)$. That is great as a program, but for $n = 10^{10}$ even a _single_ loop over `i` is too slow. We need to add the sum $\lfloor n/1 \rfloor + \lfloor n/2 \rfloor + \dots$ faster.

## 4.3 Grouping equal quotients

Look at the values of $\lfloor 12 / i \rfloor$ for $i = 1, \dots, 12$:

```
i      1   2   3   4   5   6   7   8   9  10  11  12
12//i 12   6   4   3   2   2   1   1   1   1   1   1
```

Many neighbours are equal. The quotient stays the same over whole runs. So instead of adding one term at a time, add a whole run in one go: `quotient * (length of run)`. The only question is how to find where a run ends. If `q = n // i`, the largest `j` with `n // j == q` is `n // q`. (Reason: `n // j == q` means $q \le n / j$, i.e. $j \le n / q$, and the biggest whole `j` is $\lfloor n/q \rfloor$.)

```python
def sum_of_quotients(n):
    total = 0
    i = 1
    while i <= n:
        q = n // i
        j = n // q               # last position with the same quotient
        total += q * (j - i + 1)
        i = j + 1                # jump to the start of the next run
    return total


assert sum_of_quotients(12) == 35
assert sum_of_quotients(5) == 10
assert all(sum_of_quotients(n) == sum(n // i for i in range(1, n + 1)) for n in range(1, 60))
```

```cpp
long long sum_of_quotients(long long n) {
    long long total = 0;
    long long i = 1;
    while (i <= n) {
        long long q = n / i;
        long long j = n / q;
        total += q * (j - i + 1);
        i = j + 1;
    }
    return total;
}
```

For $n = 12$ the runs are $i = 1, 2, 3, 4$ (one each, with quotients 12, 6, 4, 3), then $i = 5..6$ (quotient 2, so $2 \cdot 2 = 4$), then $i = 7..12$ (quotient 1, so $6$). The total is $12 + 6 + 4 + 3 + 4 + 6 = 35$. ✓.

How many runs can there be? For $i \le \sqrt n$ there are at most $\sqrt n$ values of `i`. For $i > \sqrt n$ the quotient is below $\sqrt n$, so there are at most $\sqrt n$ different quotients. Altogether there are at most $2\sqrt n$ runs, so the loop is $O(\sqrt n)$: about $2 \times 10^5$ steps for $n = 10^{10}$. This is exactly the problem _Divisor Loop_: the grouping trick is the whole solution.

## 4.4 Check yourself

1. How many triples $(i, j, k)$ with $0 \le i \le j \le k < 4$ are there?
2. Why does the loop `for j in range(i, n + 1, i)` run $\lfloor n/i \rfloor$ times?
3. For $n = 10$, how many times do you add a term if you group equal quotients: is it fewer than 10?
4. Why are there at most about $2\sqrt n$ different values of $\lfloor n/i \rfloor$?

# Chapter 5. Remembering what you have seen: hashing

## 5.1 A set that answers "seen it?" instantly

Here is a very common question: _does this list contain the same value twice?_ The first idea compares every pair, which by Chapter 1 costs about $n^2/2$ steps. A second idea is to sort the list and compare neighbours, which costs $O(n \log n)$.

A third idea is much faster. Walk through the list and keep a **set** of the values seen so far. A set is a collection with no repeats that can answer "is this value in here?" in about one step, no matter how big it is. (It does this with a **hash table**: a function turns the value into a number, the number says which slot of a big array to look in, so there is no searching.) We say membership tests are $O(1)$ on average.

```python
def first_repeat(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return x
        seen.add(x)
    return None


assert first_repeat([4, 7, 1, 7, 4]) == 7
assert first_repeat([1, 2, 3]) is None
```

```cpp
int first_repeat(const vector<int>& nums) {
    unordered_set<int> seen;
    for (int x : nums) {
        if (seen.count(x)) return x;
        seen.insert(x);
    }
    return -1;   // -1 means "no repeat" in this version
}
```

In `[4, 7, 1, 7, 4]` we add 4, 7, 1, and then meet 7 again, which is already in the set, so we return 7. The whole thing is one pass, so it is $O(n)$ time and $O(n)$ extra space. We traded memory for speed. This is exactly the problem _Has Duplicate_: replace the all-pairs check by a set, or if you prefer, compare the number of distinct values with the length.

## 5.2 A dictionary that counts

A **dictionary** (a hash map) does the same trick but stores a value next to each key. A very handy use is counting. Suppose we want the number of pairs `i < j` with `nums[i] == nums[j]`. The slow way tries all pairs. The fast way asks, for each new number, "how many _earlier_ numbers are equal to me?" and adds that:

```python
def count_equal_pairs(nums):
    seen = {}                       # value -> how many times so far
    pairs = 0
    for x in nums:
        pairs += seen.get(x, 0)     # earlier copies of x each form a pair with this one
        seen[x] = seen.get(x, 0) + 1
    return pairs


assert count_equal_pairs([3, 1, 3, 3, 1]) == 4
assert count_equal_pairs([1, 2, 3]) == 0
```

```cpp
long long count_equal_pairs(const vector<int>& nums) {
    unordered_map<int, long long> seen;
    long long pairs = 0;
    for (int x : nums) {
        auto it = seen.find(x);
        if (it != seen.end()) pairs += it->second;
        seen[x]++;
    }
    return pairs;
}
```

For `[3, 1, 3, 3, 1]`: the first 3 finds nothing. The 1 finds nothing. The second 3 finds one earlier 3 (+1). The third 3 finds two earlier 3s (+2). The last 1 finds one earlier 1 (+1). The total is 4. ✓

Notice the order inside the loop: we first _look up_ the earlier copies, and only then add the current number. If we added first, a number would pair with itself.

## 5.3 Looking for a complement

Now change the question. We want pairs `i < j` whose values differ by exactly `d`, that is `nums[j] - nums[i] == d`. For each new number `x` we need the count of earlier numbers equal to `x - d`. The code has the same shape; only the thing we look up changes.

```python
def count_pairs_with_difference(nums, d):
    seen = {}
    pairs = 0
    for x in nums:
        pairs += seen.get(x - d, 0)
        seen[x] = seen.get(x, 0) + 1
    return pairs


assert count_pairs_with_difference([1, 3, 2, 4, 5], 2) == 3   # (1,3) (2,4) (3,5) by value
assert count_pairs_with_difference([2, 2, 2], 0) == 3
```

```cpp
long long count_pairs_with_difference(const vector<int>& nums, int d) {
    unordered_map<int, long long> seen;
    long long pairs = 0;
    for (int x : nums) {
        auto it = seen.find(x - d);
        if (it != seen.end()) pairs += it->second;
        seen[x]++;
    }
    return pairs;
}
```

The value we search for, `x - d`, is called the **complement** (the partner that completes the pair). For a target _sum_ the complement of `x` is `target - x`, because we need `x + partner == target`. So counting pairs with a given sum is the same loop with `seen.get(target - x, 0)`. Equal values at different positions count separately, which is exactly what the counts in the dictionary do. This is exactly the problem _Count Pairs With Sum_. Time is $O(n)$ and space is $O(n)$, against $O(n^2)$ time for trying every pair.

## 5.4 Check yourself

1. What is the average cost of asking "is `x` in this set?"
2. Why do we look up earlier numbers _before_ adding the current number to the dictionary?
3. For a target sum 10 and current number 3, what complement do we look up?
4. What do we pay (in memory) to make duplicate-checking fast?

# Chapter 6. Prefix sums and running best

## 6.1 Prefix sums for many range questions

Suppose you are asked many times, "what is the sum of the numbers from position `l` to position `r`?" Adding them up each time costs up to $n$ steps per question. If there are $q$ questions, that is $O(nq)$.

The fix is to do some work once, before any question arrives. Build a list `prefix` where `prefix[i]` is the sum of the _first `i`_ numbers. So `prefix[0] = 0` (nothing added), `prefix[1]` is the first number, and so on. Then any range sum is a subtraction:

$$\text{sum}(l..r) = \text{prefix}[r+1] - \text{prefix}[l].$$

```python
def build_prefix(nums):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    return prefix


def range_total(prefix, l, r):
    return prefix[r + 1] - prefix[l]


p = build_prefix([3, 1, 4, 1, 5, 9, 2, 6])
assert p == [0, 3, 4, 8, 9, 14, 23, 25, 31]
assert range_total(p, 2, 5) == 19        # 4 + 1 + 5 + 9
assert range_total(p, 0, 7) == 31
```

```cpp
vector<long long> build_prefix(const vector<int>& nums) {
    vector<long long> prefix(1, 0);
    for (int x : nums) prefix.push_back(prefix.back() + x);
    return prefix;
}

long long range_total(const vector<long long>& prefix, int l, int r) {
    return prefix[r + 1] - prefix[l];
}
```

Why does the subtraction work? `prefix[r+1]` is everything up to `r`, and `prefix[l]` is everything before `l`. Take the second away from the first and what remains is exactly positions `l` through `r`. Building costs $O(n)$ once, and then every query costs $O(1)$. That makes the total $O(n + q)$. This is exactly the problem _Range Sum Queries_.

Prefix sums mix beautifully with a dictionary. How many ranges add up to exactly `k`? A range `l..r` sums to `k` when `prefix[r+1] - prefix[l] == k`, which says `prefix[l] == prefix[r+1] - k`. That is the complement trick of Chapter 5 applied to prefix values:

```python
def count_ranges_with_sum(nums, k):
    seen = {0: 1}          # prefix value -> how many times it appeared
    total = 0
    answer = 0
    for x in nums:
        total += x
        answer += seen.get(total - k, 0)
        seen[total] = seen.get(total, 0) + 1
    return answer


assert count_ranges_with_sum([1, 2, 3, -3, 3], 3) == 5
assert count_ranges_with_sum([1, 1, 1], 2) == 2
```

```cpp
long long count_ranges_with_sum(const vector<int>& nums, long long k) {
    unordered_map<long long, long long> seen;
    seen[0] = 1;
    long long total = 0, answer = 0;
    for (int x : nums) {
        total += x;
        auto it = seen.find(total - k);
        if (it != seen.end()) answer += it->second;
        seen[total]++;
    }
    return answer;
}
```

## 6.2 Best sum ending here

Here is a different kind of question. Given a list of numbers (some negative), what is the largest sum of a **contiguous run** (a stretch of neighbours)? Trying every start and end costs $O(n^2)$ even with prefix sums. Let us do better with a different idea: for each position, find the best run **that ends exactly at that position**.

If we know the best run ending at the previous position, the best run ending here is one of two things: just this number alone (starting fresh), or this number glued onto the best run ending before it. We glue only when that earlier best is positive (otherwise it only hurts). In symbols:

$$\text{ending}[i] = \max(a_i,\ \text{ending}[i-1] + a_i).$$

Here it is on `[2, -5, 3, 4, -1, 2, -8, 5]`:

```
number          2   -5    3    4   -1    2   -8    5
best ending    2   -3    3    7    6    8    0    5
```

For example at the number 3: the previous best was $-3$, which is negative, so starting fresh gives 3, which beats $-3 + 3 = 0$. The overall answer is the largest value in the bottom row, 8 (the run `3, 4, -1, 2`).

```python
def best_ending_here(nums):
    out = []
    current = 0
    for i, x in enumerate(nums):
        current = x if i == 0 else max(x, current + x)
        out.append(current)
    return out


row = best_ending_here([2, -5, 3, 4, -1, 2, -8, 5])
assert row == [2, -3, 3, 7, 6, 8, 0, 5]
assert max(row) == 8
```

```cpp
vector<long long> best_ending_here(const vector<int>& nums) {
    vector<long long> out;
    long long current = 0;
    for (size_t i = 0; i < nums.size(); i++) {
        current = (i == 0) ? nums[i] : max((long long)nums[i], current + nums[i]);
        out.push_back(current);
    }
    return out;
}
```

We do not really need the whole list: just the previous value and the maximum so far. That means $O(n)$ time and $O(1)$ space. This "keep only what the previous step needs, and combine with the current item" is the first taste of dynamic programming. This is exactly the problem _Maximum Subarray Sum_: the answer is the largest value of this row. (Be careful with the all-negative list: the answer is then the largest single number, which this recurrence handles, since each step may restart from `x` alone.)

## 6.3 Check yourself

1. If `prefix = [0, 5, 7, 12]`, what is the sum of positions 1 to 2?
2. Why is `prefix[0]` set to 0?
3. In the "best ending here" idea, when is it better to start fresh instead of extending?
4. What is the best ending-here value for the list `[-4, -2]`?

# Chapter 7. A sliding window, and jumping ahead with doubling

## 7.1 A window that grows and shrinks

Many questions ask about the longest or shortest _contiguous stretch_ that obeys a rule. Checking every start and end is $O(n^2)$ or worse. A **sliding window** does it in one pass. Keep two positions, `left` and `right`, that mark the current stretch. Move `right` forward one step at a time to add a new element. Whenever the rule breaks, move `left` forward to drop elements until the rule holds again. Neither pointer ever goes backwards, so together they move at most $2n$ times.

Example: given non-negative numbers and a limit, find the longest stretch whose sum is at most the limit.

```python
def longest_within_budget(nums, limit):
    left = 0
    total = 0
    best = 0
    for right, x in enumerate(nums):
        total += x                      # add the new element on the right
        while total > limit:            # rule broken: drop from the left
            total -= nums[left]
            left += 1
        best = max(best, right - left + 1)
    return best


assert longest_within_budget([3, 1, 2, 7, 4, 2, 1, 1, 5], 8) == 4
assert longest_within_budget([9, 9], 5) == 0
```

```cpp
int longest_within_budget(const vector<int>& nums, long long limit) {
    int left = 0, best = 0;
    long long total = 0;
    for (int right = 0; right < (int)nums.size(); right++) {
        total += nums[right];
        while (total > limit) {
            total -= nums[left];
            left++;
        }
        best = max(best, right - left + 1);
    }
    return best;
}
```

Trace with limit 8: the window grows to `[3, 1, 2]` (sum 6). Adding 7 gives 13, so we drop 3, 1, 2 until only `[7]` remains (sum 7). Later the window `[4, 2, 1, 1]` has sum 8 and length 4, the best. Adding 5 would give 13, so we drop 4 and 2, leaving `[1, 1, 5]`, still length 3 only. The answer is 4.

The window can also track more than a sum. Here we want the longest stretch containing **at most two different values**. A dictionary of counts tells us how many different values the window holds:

```python
def longest_two_distinct(nums):
    counts = {}
    left = 0
    best = 0
    for right, x in enumerate(nums):
        counts[x] = counts.get(x, 0) + 1
        while len(counts) > 2:
            counts[nums[left]] -= 1
            if counts[nums[left]] == 0:
                del counts[nums[left]]
            left += 1
        best = max(best, right - left + 1)
    return best


assert longest_two_distinct([1, 2, 1, 2, 3, 3, 3, 2]) == 5   # 2 3 3 3 2
assert longest_two_distinct([7]) == 1
```

```cpp
int longest_two_distinct(const vector<int>& nums) {
    unordered_map<int, int> counts;
    int left = 0, best = 0;
    for (int right = 0; right < (int)nums.size(); right++) {
        counts[nums[right]]++;
        while (counts.size() > 2) {
            if (--counts[nums[left]] == 0) counts.erase(nums[left]);
            left++;
        }
        best = max(best, right - left + 1);
    }
    return best;
}
```

This is exactly the problem _Longest Substring Without Repeats_, the same machine with a different rule: "no letter appears twice". Keep a count of the letters in the window, and whenever the newest letter's count becomes 2, move `left` forward until it drops back to 1. Trace for `"pwwkew"`: the window grows to `pw` (length 2); the second `w` breaks the rule, so `left` jumps past the first `w`, giving `w`; then `wk`, then `wke` (length 3, the best); adding `w` breaks it again, giving `kew`, still length 3. The answer is 3. Time is $O(n)$.

## 7.2 Fibonacci, slowly and then very quickly

The Fibonacci numbers are $F(0) = 0$, $F(1) = 1$, and each next one is the sum of the previous two: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ... The definition written as a recursive function recomputes the same values again and again and takes about $2^n$ steps. A plain loop that keeps just the last two values is $O(n)$:

```python
def fib_loop(n):
    a, b = 0, 1                # F(0), F(1)
    for _ in range(n):
        a, b = b, a + b
    return a


assert fib_loop(10) == 55
assert fib_loop(20) == 6765
```

```cpp
long long fib_loop(int n, long long mod) {
    long long a = 0, b = 1 % mod;
    for (int i = 0; i < n; i++) {
        long long next = (a + b) % mod;
        a = b;
        b = next;
    }
    return a;
}
```

(In C++ the numbers grow past 64 bits very quickly, so we take everything modulo some `mod`. Python integers never overflow, so Python can keep exact answers.)

A loop of $n$ steps is fine for $n = 50{,}000$, but you can do much better. Think of the pair $(F(k), F(k+1))$ as a snapshot. Using the rule $F(m+1) = F(m) + F(m-1)$ a few times, you can go from the snapshot for `k` straight to the snapshot for `2k`:

$$F(2k) = F(k)\,\bigl(2F(k+1) - F(k)\bigr), \qquad F(2k+1) = F(k)^2 + F(k+1)^2.$$

(One way to see this: the matrix $\begin{pmatrix}1&1\\1&0\end{pmatrix}$ raised to the power `k` contains $F(k+1), F(k), F(k-1)$, and squaring it gives these formulas.) To get $F(n)$ we recurse on $n // 2$ and then fix up for the odd case by stepping one forward. This is called **fast doubling**, and it needs only about $\log_2 n$ levels.

```python
def fib_pair(k, mod):
    # returns (F(k) % mod, F(k+1) % mod)
    if k == 0:
        return (0, 1 % mod)
    a, b = fib_pair(k // 2, mod)           # F(h), F(h+1) where h = k // 2
    c = a * ((2 * b - a) % mod) % mod      # F(2h)
    d = (a * a + b * b) % mod              # F(2h+1)
    if k % 2 == 0:
        return (c, d)
    return (d, (c + d) % mod)              # F(2h+1), F(2h+2)


def fib_fast(n, mod):
    return fib_pair(n, mod)[0]


assert fib_fast(10, 10**9 + 7) == 55
assert fib_fast(30, 10**9 + 7) == 832040
assert all(fib_fast(n, 1000) == fib_loop(n) % 1000 for n in range(0, 80))
big = 10**500                              # pass a huge modulus to get exact answers
assert fib_fast(300, big) == fib_loop(300)
```

```cpp
pair<long long, long long> fib_pair(long long k, long long mod) {
    // returns (F(k) % mod, F(k+1) % mod); mod up to about 3e9 keeps products inside 64 bits
    if (k == 0) return {0, 1 % mod};
    auto [a, b] = fib_pair(k / 2, mod);
    long long c = a * (((2 * b - a) % mod + mod) % mod) % mod;
    long long d = (a * a + b * b) % mod;
    if (k % 2 == 0) return {c, d};
    return {d, (c + d) % mod};
}

long long fib_fast(long long n, long long mod) {
    return fib_pair(n, mod).first;
}
```

For example, to get $F(10)$: $k = 10$ asks for $k = 5$, which asks for $k = 2$, then $k = 1$, then $k = 0$. Only five levels instead of ten additions, and for $n = 10^{18}$ only about 60 levels instead of $10^{18}$ additions. This is exactly the problem _Nth Fibonacci Number_, which asks for the exact huge value, so in Python you skip the `mod` (or pass a huge one, as in the last assert). Then the numbers have thousands of digits and big multiplications dominate the time.

## 7.3 Check yourself

1. Why does a sliding window run in $O(n)$ even though it has a loop inside a loop?
2. When the window breaks the rule, which pointer do we move?
3. What does the pair $(F(k), F(k+1))$ let us compute in one jump?
4. Why does C++ need a modulus for large Fibonacci numbers?

# Chapter 8. The Python toolbox: sorting, counting and slicing

## 8.1 Sorting with a key

Python's `sorted(items, key=...)` sorts by whatever the `key` function returns for each item. If the key returns a **tuple** (a small fixed group like `(a, b)`), Python compares the first parts, and only if they tie, the second parts, and so on. To sort one part from big to small, put a minus sign in front of a number.

```python
def order_words(words):
    # shortest first; words of the same length in alphabetical order
    return sorted(words, key=lambda w: (len(w), w))


def order_by_score(records):
    # records are [name, score]; highest score first, ties alphabetical
    return [name for name, score in sorted(records, key=lambda r: (-r[1], r[0]))]


assert order_words(["pear", "fig", "apple", "kiwi"]) == ["fig", "kiwi", "pear", "apple"]
assert order_by_score([["ann", 3], ["bob", 5], ["cy", 3]]) == ["bob", "ann", "cy"]
```

```cpp
vector<string> order_words(vector<string> words) {
    sort(words.begin(), words.end(), [](const string& a, const string& b) {
        if (a.size() != b.size()) return a.size() < b.size();
        return a < b;
    });
    return words;
}

vector<string> order_by_score(vector<pair<string, int>> records) {
    sort(records.begin(), records.end(), [](const auto& a, const auto& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    vector<string> names;
    for (auto& r : records) names.push_back(r.first);
    return names;
}
```

Sorting costs $O(n \log n)$. The `key` function is called once per item, and in C++ you write a comparison function (a lambda) that says whether `a` should come before `b`. Python's sort is also **stable**: items that compare equal keep their original order. This is exactly the problem _Leaderboard Order_: a key with `-score` first and the name second. Because a name may appear in several records, we keep every record and just sort them.

## 8.2 Counting with Counter

`collections.Counter` is a dictionary specialised for counting. `Counter("banana")` gives `{'a': 3, 'n': 2, 'b': 1}`. Two counters are equal when they hold the same counts, which gives a one-line anagram check: two strings are anagrams exactly when their letter counts match. Subtracting counters drops anything that reaches zero, which is handy for "can I build this word from these tiles?".

```python
from collections import Counter


def can_build(word, tiles):
    # each tile may be used once
    return not (Counter(word) - Counter(tiles))


def same_letters(a, b):
    return Counter(a) == Counter(b)


assert can_build("tea", "eat") is True
assert can_build("tee", "eat") is False
assert same_letters("listen", "silent")
assert not same_letters("abc", "abd")
```

```cpp
bool can_build(const string& word, const string& tiles) {
    map<char, int> need, have;
    for (char c : word) need[c]++;
    for (char c : tiles) have[c]++;
    for (auto& [c, cnt] : need) {
        if (have[c] < cnt) return false;
    }
    return true;
}

bool same_letters(const string& a, const string& b) {
    map<char, int> ca, cb;
    for (char c : a) ca[c]++;
    for (char c : b) cb[c]++;
    return ca == cb;
}
```

Counting is $O(n)$. That is faster than sorting both strings and comparing, which is $O(n \log n)$. This is exactly the problem _Anagram Check_.

`Counter` also has `most_common(k)`, but it breaks ties in the order the items were first seen, not alphabetically. When a problem wants a specific tie rule, sort the items yourself with a key, exactly as in 8.1: count first, then `sorted(counter.items(), key=lambda p: (-p[1], p[0]))`.

```python
def top_words(words, k):
    counts = Counter(words)
    ranked = sorted(counts.items(), key=lambda p: (-p[1], p[0]))
    return [[w, c] for w, c in ranked[:k]]


assert top_words(["b", "a", "b", "c", "a", "d"], 2) == [["a", 2], ["b", 2]]
assert top_words(["x"], 5) == [["x", 1]]
```

```cpp
vector<pair<string, int>> top_words(const vector<string>& words, int k) {
    map<string, int> counts;
    for (auto& w : words) counts[w]++;
    vector<pair<string, int>> ranked(counts.begin(), counts.end());
    sort(ranked.begin(), ranked.end(), [](const auto& a, const auto& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    if ((int)ranked.size() > k) ranked.resize(k);
    return ranked;
}
```

Slicing `[:k]` quietly handles the case where there are fewer than `k` items. This is exactly the problem _Most Frequent Characters_: the same function, run on the characters of a string.

## 8.3 Slicing and zip

A **slice** `a[i:j]` copies the part from position `i` up to (not including) `j`. Leaving out a number means "from the start" or "to the end". Negative numbers count from the end. These slices cover a lot of small tasks:

```python
nums = [10, 20, 30, 40, 50]
assert nums[1:3] == [20, 30]
assert nums[:2] == [10, 20]
assert nums[-2:] == [40, 50]
assert nums[::-1] == [50, 40, 30, 20, 10]     # reversed copy
assert nums[::2] == [10, 30, 50]               # every second item
```

```cpp
// C++ has no slice syntax; build the part you need from two iterators.
vector<int> slice(const vector<int>& a, int i, int j) {
    return vector<int>(a.begin() + i, a.begin() + j);
}
```

To rotate a list to the right by `k` places, the last `k` elements move to the front. When `k` is bigger than the length, rotating by the full length changes nothing, so we first reduce `k` with the remainder `%`:

```python
def rotate_right(nums, k):
    if not nums:
        return []
    k %= len(nums)
    if k == 0:
        return nums[:]
    return nums[-k:] + nums[:-k]


assert rotate_right([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
assert rotate_right([1, 2, 3], 7) == [3, 1, 2]       # 7 % 3 == 1
assert rotate_right([], 3) == []
```

```cpp
vector<int> rotate_right(vector<int> nums, long long k) {
    if (nums.empty()) return nums;
    k %= (long long)nums.size();
    rotate(nums.begin(), nums.end() - k, nums.end());
    return nums;
}
```

Rotating left is the mirror image: `nums[k:] + nums[:k]` after `k %= len(nums)`. Watch the special case `k == 0`: `nums[-0:]` means the whole list, which is a classic bug. This is exactly the problem _Rotate Left_. Slicing copies, so it costs $O(n)$ time and space.

`zip(a, b)` walks several lists side by side and pairs up their items. With a star, `zip(*rows)` hands the rows over as separate arguments, which "turns rows into columns":

```python
pairs = [(1, "a"), (2, "b"), (3, "c")]
numbers, letters = zip(*pairs)                 # unzip
assert numbers == (1, 2, 3) and letters == ("a", "b", "c")

grid = [[1, 2, 3], [4, 5, 6]]
assert [list(col) for col in zip(*grid)] == [[1, 4], [2, 5], [3, 6]]
assert [list(col) for col in zip(*[])] == []
```

```cpp
vector<vector<int>> columns_of(const vector<vector<int>>& grid) {
    if (grid.empty()) return {};
    vector<vector<int>> out(grid[0].size(), vector<int>(grid.size()));
    for (size_t i = 0; i < grid.size(); i++)
        for (size_t j = 0; j < grid[0].size(); j++)
            out[j][i] = grid[i][j];
    return out;
}
```

The grid example _is_ the transpose: element at row `i`, column `j` lands at row `j`, column `i`. The empty cases also work: `zip(*[])` is empty. This is exactly the problem _Transpose a Matrix_.

## 8.4 Cleaning up text

Strings come with useful methods. `s.lower()` makes letters lower case, `s.split()` with no argument cuts on any amount of whitespace and drops empty pieces, `" ".join(pieces)` glues pieces with single spaces, and `c.isalnum()` tells whether a character is a letter or digit. Put them together and you can clean messy text in one line.

```python
def keep_letters_and_spaces(s):
    # letters stay, everything else becomes a space, then extra spaces collapse
    return " ".join("".join(c if c.isalpha() else " " for c in s).split())


assert keep_letters_and_spaces("Hi!!  you--there") == "Hi you there"
assert keep_letters_and_spaces("   ") == ""
```

```cpp
string keep_letters_and_spaces(const string& s) {
    string out;
    bool pendingSpace = false;
    for (char c : s) {
        if (isalpha((unsigned char)c)) {
            if (pendingSpace && !out.empty()) out += ' ';
            out += c;
            pendingSpace = false;
        } else {
            pendingSpace = true;
        }
    }
    return out;
}
```

The trick is the order: first turn every unwanted character into a space, then `split()` throws away the empty pieces, and `join` puts back exactly one space between pieces. Take care with `isalnum()`: for non-English text it also accepts letters like "é". If a problem says only `a-z` and `0-9`, test with `c.isascii() and c.isalnum()` or compare against the character range. This is exactly the problem _Normalize Text_: it is this recipe with lower-casing and digits allowed. Time is $O(n)$.

## 8.5 Check yourself

1. How do you sort records by score from high to low, breaking ties by name?
2. Why does `Counter("abc") == Counter("cab")` mean the strings are anagrams?
3. What does `nums[-3:]` give for `[1, 2, 3, 4, 5]`?
4. What does `zip(*[[1, 2], [3, 4]])` produce?

# Chapter 9. The Python toolbox: heaps, bisect, itertools and maths

## 9.1 Heaps and merging

A **heap** (a priority queue) is a structure that always hands you the smallest item quickly. Python's `heapq` module keeps a plain list arranged so that `heap[0]` is the smallest; pushing and popping each cost $O(\log n)$.

```python
import heapq


def smallest_k(nums, k):
    return heapq.nsmallest(k, nums)


def smallest_via_heap(nums):
    heap = list(nums)
    heapq.heapify(heap)                         # O(n)
    out = []
    while heap:
        out.append(heapq.heappop(heap))         # always the smallest left
    return out


assert smallest_k([5, 1, 4, 2, 3], 3) == [1, 2, 3]
assert smallest_k([2, 2, 1], 5) == [1, 2, 2]
assert smallest_via_heap([4, 1, 3]) == [1, 3, 4]
```

```cpp
vector<int> smallest_k(vector<int> nums, int k) {
    // keep a max-heap of the k smallest seen so far
    priority_queue<int> heap;
    for (int x : nums) {
        heap.push(x);
        if ((int)heap.size() > k) heap.pop();
    }
    vector<int> out;
    while (!heap.empty()) { out.push_back(heap.top()); heap.pop(); }
    reverse(out.begin(), out.end());
    return out;
}
```

`nsmallest(k, nums)` costs about $O(n \log k)$, which is better than a full sort when `k` is small. It handles `k` larger than the list too. This is exactly the problem _K Smallest Numbers_; either `sorted(nums)[:k]` or `heapq.nsmallest` works for the tests. If you want a truly linear-time idea, the quickselect method in the sorting page does it.

Heaps also merge sorted lists. If several lists are each already sorted, the next output is always the smallest of the _front_ items. A heap holds one front item per list:

```python
def merge_lists(lists):
    heap = []
    for idx, lst in enumerate(lists):
        if lst:
            heap.append((lst[0], idx, 0))       # (value, which list, position in it)
    heapq.heapify(heap)
    out = []
    while heap:
        value, idx, pos = heapq.heappop(heap)
        out.append(value)
        if pos + 1 < len(lists[idx]):
            heapq.heappush(heap, (lists[idx][pos + 1], idx, pos + 1))
    return out


assert merge_lists([[1, 4, 7], [2, 5], [], [3, 6]]) == [1, 2, 3, 4, 5, 6, 7]
assert merge_lists([]) == []
assert list(heapq.merge([1, 4], [2, 3])) == [1, 2, 3, 4]
```

```cpp
vector<int> merge_lists(const vector<vector<int>>& lists) {
    using T = tuple<int, int, int>;     // value, list index, position
    priority_queue<T, vector<T>, greater<T>> heap;
    for (int i = 0; i < (int)lists.size(); i++)
        if (!lists[i].empty()) heap.push({lists[i][0], i, 0});
    vector<int> out;
    while (!heap.empty()) {
        auto [value, idx, pos] = heap.top();
        heap.pop();
        out.push_back(value);
        if (pos + 1 < (int)lists[idx].size())
            heap.push({lists[idx][pos + 1], idx, pos + 1});
    }
    return out;
}
```

With `m` lists and `N` values in total this is $O(N \log m)$. Python has this built in as `heapq.merge(*lists)`, as the last assert shows. This is exactly the problem _Merge Sorted Lists_.

## 9.2 Binary search with bisect

When a list is sorted, you can find a place in it by repeatedly halving, as we did in Chapter 3. Python's `bisect` module does this for you. `bisect_left(a, x)` returns the first position where `x` could be inserted keeping the list sorted (before any equal values). `bisect_right(a, x)` returns the position after any equal values.

```python
from bisect import bisect_left, bisect_right

a = [1, 3, 3, 3, 8, 10]
assert bisect_left(a, 3) == 1        # first 3 sits at index 1
assert bisect_right(a, 3) == 4       # index just after the last 3
assert bisect_left(a, 5) == 4        # 5 would be inserted before 8


def count_between(sorted_nums, lo, hi):
    # how many values v satisfy lo <= v <= hi
    return bisect_right(sorted_nums, hi) - bisect_left(sorted_nums, lo)


assert count_between(a, 3, 8) == 4          # 3, 3, 3, 8
assert count_between(a, 4, 7) == 0
assert count_between(a, 0, 100) == 6
```

```cpp
int count_between(const vector<int>& sorted_nums, int lo, int hi) {
    auto first = lower_bound(sorted_nums.begin(), sorted_nums.end(), lo);   // like bisect_left
    auto last = upper_bound(sorted_nums.begin(), sorted_nums.end(), hi);    // like bisect_right
    return (int)(last - first);
}
```

The count of values from `lo` to `hi` is "how many are at most `hi`" minus "how many are less than `lo`". Each answer takes $O(\log n)$ after the one-time sort. This is exactly the problem _Count in Range_. (Remember to use `bisect_right` for the upper end so that values equal to `hi` count, and `bisect_left` for the lower end so that values equal to `lo` count.)

## 9.3 Combinations, permutations and meeting in the middle

The `itertools` module builds arrangements for you. `combinations(items, r)` yields every group of `r` items (order does not matter); `permutations(items)` yields every ordering. They work on positions, so equal values at different positions are treated as different items.

```python
from itertools import combinations, permutations

assert list(combinations([1, 2, 3], 2)) == [(1, 2), (1, 3), (2, 3)]
assert len(list(permutations([1, 2, 3]))) == 6


def count_subsets_slow(nums, k, target):
    return sum(1 for group in combinations(nums, k) if sum(group) == target)


assert count_subsets_slow([1, 2, 3, 4], 2, 5) == 2          # (1,4) and (2,3)
assert count_subsets_slow([5, 5, 5], 2, 10) == 3            # three different position pairs
assert count_subsets_slow([], 0, 0) == 1                    # choosing nothing: one way
```

```cpp
long long count_subsets_slow(const vector<int>& nums, int k, int target) {
    int n = nums.size();
    long long ways = 0;
    for (int mask = 0; mask < (1 << n); mask++) {          // every subset as a bit pattern
        if (__builtin_popcount(mask) != k) continue;
        long long sum = 0;
        for (int i = 0; i < n; i++)
            if (mask >> i & 1) sum += nums[i];
        if (sum == target) ways++;
    }
    return ways;
}
```

There are $\binom{n}{k}$ groups, up to $2^n$ over all `k`, so for $n = 22$ the slow way tries about 4 million subsets. Fast enough only when `n` is small. A clever fix is **meet in the middle**: split the numbers into two halves of size $n/2$. Each half has only $2^{n/2}$ subsets, so you can list the sums of each half separately (about 2,000 each for $n = 22$ instead of 4 million together). Every full subset is one subset from the left half plus one from the right half, so you match them up with a dictionary lookup, as in Chapter 5. Here is the idea for the simplest version, counting subsets of any size that hit a target:

```python
from collections import Counter


def subset_sums(values):
    sums = Counter({0: 1})                      # the empty subset has sum 0
    for v in values:
        for s, ways in list(sums.items()):
            sums[s + v] += ways
    return sums


def count_subsets_any_size(nums, target):
    half = len(nums) // 2
    left = subset_sums(nums[:half])
    right = subset_sums(nums[half:])
    return sum(ways * left.get(target - s, 0) for s, ways in right.items())


assert count_subsets_any_size([1, 2, 3], 3) == 2            # {3} and {1,2}
assert count_subsets_any_size([1, 1, 1], 2) == 3
assert count_subsets_any_size([2, 4], 0) == 1               # only the empty set
```

```cpp
map<int, long long> subset_sums(const vector<int>& values) {
    map<int, long long> sums;
    sums[0] = 1;
    for (int v : values) {
        auto snapshot = sums;
        for (auto& [s, ways] : snapshot) sums[s + v] += ways;
    }
    return sums;
}

long long count_subsets_any_size(const vector<int>& nums, int target) {
    int half = nums.size() / 2;
    auto left = subset_sums(vector<int>(nums.begin(), nums.begin() + half));
    auto right = subset_sums(vector<int>(nums.begin() + half, nums.end()));
    long long total = 0;
    for (auto& [s, ways] : right) {
        auto it = left.find(target - s);
        if (it != left.end()) total += ways * it->second;
    }
    return total;
}
```

The step "for each right-half sum, look up the matching left-half sum" multiplies the counts, because any left subset can pair with any right subset. This is exactly the problem _Count Subsets With Sum_; it needs this idea with one extra piece of information: the key becomes the pair (how many items chosen, their sum), and you look up `(k - size, target - sum)` on the other side. The cost drops from about $2^n$ to about $2^{n/2}$.

For **distinct permutations** of a short string with repeated letters, a quick Python approach is to put all the permutations in a set and sort. For a string of up to 8 letters there are at most $8! = 40320$ orderings, which is small:

```python
def distinct_orderings(s):
    return sorted({"".join(p) for p in permutations(s)})


assert distinct_orderings("aab") == ["aab", "aba", "baa"]
assert distinct_orderings("") == [""]
assert len(distinct_orderings("abc")) == 6
```

```cpp
vector<string> distinct_orderings(string s) {
    sort(s.begin(), s.end());
    vector<string> out;
    do {
        out.push_back(s);
    } while (next_permutation(s.begin(), s.end()));
    return out;
}
```

C++ has a ready-made tool: `next_permutation` steps through the orderings in alphabetical order and skips repeats automatically, as long as you start from the sorted string. For longer strings, the better method is backtracking over distinct letters with their remaining counts, which you will meet in the recursion topic. This is exactly the problem _Distinct Permutations_.

## 9.4 Maths helpers and big numbers

`math` has many shortcuts. `math.gcd(a, b)` is the greatest common divisor, found by Euclid's method: repeatedly replace `(a, b)` with `(b, a % b)` until `b` is 0. The **least common multiple** follows from $\text{lcm}(a, b) = a / \gcd(a, b) \cdot b$. Dividing first keeps the numbers smaller. To get the lcm of a whole list, fold it in one number at a time, starting from 1 (which gives the right answer for an empty list).

```python
import math


def gcd_loop(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm_of(nums):
    result = 1
    for x in nums:
        result = result // gcd_loop(result, x) * x
    return result


assert gcd_loop(12, 18) == 6
assert lcm_of([4, 6, 10]) == 60
assert lcm_of([]) == 1
assert lcm_of([3, 5, 7]) == math.lcm(3, 5, 7)
```

```cpp
long long gcd_loop(long long a, long long b) {
    while (b) {
        long long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

long long lcm_of(const vector<long long>& nums) {
    long long result = 1;
    for (long long x : nums) {
        result = result / gcd_loop(result, x) * x;
    }
    return result;
}
```

This is exactly the problem _Least Common Multiple of a List_. In Python, `math.lcm(*nums)` does the same (Python 3.9 and newer). In C++ the lcm can overflow `long long` for long lists, while Python integers simply grow.

Python integers can be as large as memory allows, which is a superpower for questions about huge numbers. Two examples. First, square roots: `math.sqrt` works with floating point and loses digits, while `math.isqrt` is exact:

```python
assert int(math.sqrt(10**30 - 1)) == 10**15            # wrong: the float rounds up
assert math.isqrt(10**30 - 1) == 10**15 - 1             # right
assert math.isqrt(10**200) == 10**100
```

```cpp
// C++ has no built-in big integers: use the binary-search idea of Chapter 3
// with a big-number type, or restrict to 64-bit values.
long long exact_isqrt(long long n) {
    long long r = (long long)sqrtl((long double)n);
    while (r * r > n) r--;
    while ((r + 1) * (r + 1) <= n) r++;
    return r;
}
```

This is exactly the problem _Exact Square Root_: for a 200-digit number, never go through floats; use `math.isqrt` (or the binary search of Chapter 3, which also works on big integers).

Second, a factorial is huge: $10000!$ has about 35,000 digits. `math.factorial(n)` computes it exactly. Turning it into text to add up the digits needs one more line, because Python refuses to convert integers with more than 4300 digits to a string unless you lift the limit:

```python
import sys


def factorial_digit_sum(n):
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)           # 0 means "no limit"
    return sum(int(d) for d in str(math.factorial(n)))


assert factorial_digit_sum(10) == 27            # 10! = 3628800
assert factorial_digit_sum(0) == 1
```

```cpp
vector<int> factorial_digits(int n) {
    // C++ has no big integers: keep the digits ourselves, least significant first
    vector<int> digits = {1};
    for (int m = 2; m <= n; m++) {
        int carry = 0;
        for (int& d : digits) {
            int cur = d * m + carry;
            d = cur % 10;
            carry = cur / 10;
        }
        while (carry) {
            digits.push_back(carry % 10);
            carry /= 10;
        }
    }
    return digits;
}
```

In C++ you must multiply the digits yourself, as above. The digit sum is then the sum of that vector. This is exactly the problem _Digit Sum of a Factorial_. The lesson: before you write clever code, check whether the standard library already has the tool.

## 9.5 Check yourself

1. What does a heap give you quickly, and what does each push or pop cost?
2. For `a = [2, 4, 4, 6]`, what do `bisect_left(a, 4)` and `bisect_right(a, 4)` return?
3. Why does meet in the middle reduce $2^{22}$ work to about two lots of $2^{11}$?
4. Why is `math.isqrt` safer than `int(math.sqrt(n))` for very big `n`?
