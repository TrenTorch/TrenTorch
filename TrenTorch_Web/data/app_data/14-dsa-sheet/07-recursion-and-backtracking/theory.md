> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Recursion and backtracking)

This page teaches recursion, which is a way of solving a problem by letting a function call itself on a smaller version of the same problem, and backtracking, which is recursion used to try every possible choice and to take back the ones that do not work out. It covers the whole step: recursive thinking (towers, Gray codes, fast powers, Josephus), subsets, combinations and permutations, and the classic backtracking puzzles such as N-Queens and Sudoku.

The page is a staircase. **Chapter 1 is deliberately gentle**: one tiny idea, small numbers, no heavy maths. Chapters 2 to 6 build the habit of thinking recursively, counting what a recursion costs, splitting problems in halves and remembering answers. Chapters 7 to 11 turn that into backtracking and use it on harder and harder puzzles. Every chapter only uses what came before, so if a later chapter looks scary, just keep climbing. Every code example is shown in Python and in C++.

# Chapter 1. What recursion is

## 1.1 A function that calls itself

Imagine a set of nesting dolls. To find out how many dolls are inside, you open the biggest one, and you see that it contains a smaller set of nesting dolls. So the number of dolls is "1 (the one I just opened) plus the number of dolls in the smaller set". To answer that, you open the next doll and ask the same question again. You keep going until you open a doll that is empty inside. Then you can finally start answering.

A **recursive function** works the same way. It solves a problem by calling itself on a slightly smaller problem, and it must have a spot where it stops and gives a direct answer. Here is the smallest example we can think of: a function that returns the numbers from `n` down to 1.

```python
def count_down(n):
    if n == 0:
        return []
    return [n] + count_down(n - 1)


assert count_down(3) == [3, 2, 1]
assert count_down(0) == []
```

```cpp
vector<int> count_down(int n) {
    if (n == 0) return {};
    vector<int> rest = count_down(n - 1);
    rest.insert(rest.begin(), n);
    return rest;
}
```

Read it aloud: "the countdown from `n` is `n` followed by the countdown from `n - 1`". The line `if n == 0` is the doll that is empty inside: there is nothing left to count, so the answer is the empty list and no more calls are made.

## 1.2 Base case and smaller problem

Every recursive function has exactly two ingredients, and if you remember nothing else from this page, remember these two.

The **base case** is the input so small that you can answer it directly, without calling yourself. In `count_down` it is `n == 0`. The **recursive case** is everything else: you call the same function on a smaller input, then use that answer to build yours. In `count_down` the smaller input is `n - 1`, and "use the answer" means putting `n` in front.

The word "smaller" matters. Each call must move closer to the base case, otherwise it never stops. Let's see one more function with these two ingredients, the sum $1 + 2 + \dots + n$.

```python
def sum_to(n):
    if n == 0:
        return 0
    return n + sum_to(n - 1)


assert sum_to(4) == 10
assert sum_to(0) == 0
```

```cpp
int sum_to(int n) {
    if (n == 0) return 0;
    return n + sum_to(n - 1);
}
```

To compute `sum_to(4)` we do not need to know how the sum is computed in general. We only say: "the sum up to 4 is 4 plus the sum up to 3". We trust that the call for 3 will give the right answer, and it will, because it makes the same trusting step for 2, and so on, down to `sum_to(0)` which is 0. This trust is the hardest mental step for beginners, and also the most powerful. We will come back to it in Chapter 2.

## 1.3 The call stack by example

What does the computer actually do while it runs `sum_to(4)`? It cannot finish `4 + sum_to(3)` until `sum_to(3)` has returned, so it parks the unfinished work and starts the new call. The parking place is called the **call stack**, a pile of unfinished calls where only the top one is active, like a pile of plates where you can only touch the top plate.

```
sum_to(4) waits for sum_to(3)           the pile grows downwards
  sum_to(3) waits for sum_to(2)
    sum_to(2) waits for sum_to(1)
      sum_to(1) waits for sum_to(0)
        sum_to(0) returns 0             base case reached
      sum_to(1) returns 1 + 0 = 1       now the pile shrinks
    sum_to(2) returns 2 + 1 = 3
  sum_to(3) returns 3 + 3 = 6
sum_to(4) returns 4 + 6 = 10
```

First the calls pile up until the base case, then the answers flow back one by one. The stack is $5$ calls tall at its tallest, and in general `sum_to(n)` needs $n + 1$ calls on the stack at once. That is the reason we must always have a base case that is actually reachable: with no base case the pile would grow until the computer runs out of room, which Python reports as a `RecursionError` (by default it allows about 1000 nested calls) and C++ reports by crashing with a stack overflow.

## 1.4 Smaller does not mean one less

"Smaller" can mean many things. To add up the digits of a number we can chop off the last digit, so the number gets about ten times smaller. To check whether a word is a palindrome (reads the same forwards and backwards) we compare the two ends and then check the word that remains in the middle, which is two letters shorter.

```python
def digit_sum(n):
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)


def is_palindrome(s, lo, hi):
    if lo >= hi:
        return True
    if s[lo] != s[hi]:
        return False
    return is_palindrome(s, lo + 1, hi - 1)


assert digit_sum(1234) == 10
assert is_palindrome("level", 0, 4) is True
assert is_palindrome("leaves", 0, 5) is False
```

```cpp
int digit_sum(int n) {
    if (n < 10) return n;
    return n % 10 + digit_sum(n / 10);
}

bool is_palindrome(const string& s, int lo, int hi) {
    if (lo >= hi) return true;
    if (s[lo] != s[hi]) return false;
    return is_palindrome(s, lo + 1, hi - 1);
}
```

In the palindrome check we pass the two ends `lo` and `hi` instead of building new strings: the "smaller problem" is the piece of the word between them. Notice that `is_palindrome` has two ways to stop: a piece with at most one letter is a palindrome, and a mismatch is an immediate "no". A recursive function may have several base cases, as long as every path of calls ends in one of them.

## 1.5 Check yourself

1. What are the two ingredients every recursive function needs?
2. In `sum_to`, what would happen if we deleted the line `if n == 0`?
3. How tall is the call stack at its tallest for `sum_to(10)`?
4. In `digit_sum(907)`, what is the smaller problem that the first call makes?

# Chapter 2. Designing a recursive solution

## 2.1 Four questions to ask

In Chapter 1 the functions were so small that they almost wrote themselves. For harder problems it helps to follow the same four questions every time, in order.

First: what does my function promise? Write it in one plain sentence, for example "`reverse(s)` returns the string `s` backwards". This sentence is your contract. Second: what is the smallest input, and what is its answer? That is the base case. Third: how can I shrink the input so that the contract still applies to it? Fourth, and this is where the creativity is: if I assume the smaller call keeps the promise, how do I turn its answer into the answer for my input?

The most common mistake is to try to follow the whole chain of calls in your head. Do not. Check only two things: the base case is right, and one step is right assuming the smaller call is right. If both hold, the whole function is right, exactly like a row of falling dominoes.

## 2.2 Trusting the smaller call

Let's use the four questions to reverse a string. The promise: `reverse(s)` returns `s` backwards. The base case: a string of length 0 or 1 is its own reverse. The shrink: remove the first letter, leaving `s[1:]`. The combination: the reverse of the whole string is the reverse of the rest, followed by the first letter.

```python
def reverse(s):
    if len(s) <= 1:
        return s
    return reverse(s[1:]) + s[0]


assert reverse("abc") == "cba"
assert reverse("") == ""
```

```cpp
string reverse_str(const string& s) {
    if (s.size() <= 1) return s;
    return reverse_str(s.substr(1)) + s[0];
}
```

By hand for `"abc"`: `reverse("abc")` waits for `reverse("bc")`, which waits for `reverse("c")`, which returns `"c"`. Then `reverse("bc")` returns `"c" + "b"` which is `"cb"`, and finally `reverse("abc")` returns `"cb" + "a"` which is `"cba"`. At no point did we need to think about more than one step.

## 2.3 Moving a tower of disks

Now a classic puzzle. You have three pegs, numbered 1, 2 and 3, and `n` disks of different sizes stacked on peg 1 with the biggest at the bottom. You may move one disk at a time, and you may never put a bigger disk on a smaller one. The goal is to move the whole tower to peg 3 using as few moves as possible. This is exactly the problem _Tower of Hanoi_.

Try to solve it for 10 disks by hand and you will quickly get lost. But apply the four questions. The promise: `moves(k, a, b, c)` lists the moves that carry a tower of `k` disks from peg `a` to peg `b`, using peg `c` as a spare. The base case: zero disks need zero moves. The shrink: the biggest disk can only move when it has nothing on top of it and its destination is empty. So the `k - 1` smaller disks must first go out of the way onto the spare, then the big disk moves across in one move, and then the `k - 1` disks move on top of it. Moving a tower of `k - 1` disks is the same problem again, with the pegs playing different roles.

```python
def moves(k, a, b, c):
    if k == 0:
        return []
    return moves(k - 1, a, c, b) + [[a, b]] + moves(k - 1, c, b, a)


assert moves(1, 1, 3, 2) == [[1, 3]]
assert moves(3, 1, 3, 2) == [[1, 3], [1, 2], [3, 2], [1, 3], [2, 1], [2, 3], [1, 3]]
```

```cpp
vector<vector<int>> moves(int k, int a, int b, int c) {
    if (k == 0) return {};
    vector<vector<int>> result = moves(k - 1, a, c, b);
    result.push_back({a, b});
    vector<vector<int>> rest = moves(k - 1, c, b, a);
    result.insert(result.end(), rest.begin(), rest.end());
    return result;
}
```

For three disks the list has 7 moves, as in the assert. In the middle of that list, the move `[1, 3]` is the biggest disk travelling from peg 1 to peg 3, with the two smaller disks parked on peg 2 (the first three moves carried them there, and the last three carry them back on top). The answer for $k$ disks uses exactly $2^k - 1$ moves, and we will prove it in Chapter 3.

## 2.4 Building a list from a smaller list

Sometimes the recursion does not shrink a number but builds a whole list. A **Gray code** is a list of all the numbers with $n$ binary digits (bits) in which neighbours differ in exactly one bit. For $n = 2$ the list is `00, 01, 11, 10`: each step flips one bit. This is exactly the problem _Gray Code_.

Here is a neat way to build it. Take the code for $n - 1$ bits. Write it once with a leading `0` in front of each entry, and then write it again in reverse order with a leading `1`. The seam in the middle is fine because the two entries on either side are the same number except for the new leading bit.

```
n=1:   0   1
n=2:  00  01   |   11  10        (first copy with 0, then reversed copy with 1)
n=3: 000 001 011 010 | 110 111 101 100
```

```python
def gray_codes(n):
    if n == 0:
        return [0]
    smaller = gray_codes(n - 1)
    top = 1 << (n - 1)
    return smaller + [top + x for x in reversed(smaller)]


assert gray_codes(2) == [0, 1, 3, 2]
assert gray_codes(3) == [0, 1, 3, 2, 6, 7, 5, 4]
assert gray_codes(3) == [i ^ (i >> 1) for i in range(8)]
```

```cpp
vector<int> gray_codes(int n) {
    if (n == 0) return {0};
    vector<int> smaller = gray_codes(n - 1);
    int top = 1 << (n - 1);
    vector<int> result = smaller;
    for (int i = (int)smaller.size() - 1; i >= 0; i--) result.push_back(top + smaller[i]);
    return result;
}
```

Here `1 << (n - 1)` means "1 shifted left by $n - 1$ places", the number $2^{n-1}$, which is exactly the value of the new leading bit. The last assert shows a surprising shortcut: the $i$-th code is simply `i ^ (i >> 1)`, where `>> 1` drops the last bit of `i` and `^` keeps a bit when the two numbers differ in it. This direct formula gives each code in constant time, and the recursion explains why it works. Time and space are both $O(2^n)$, the size of the answer.

## 2.5 Check yourself

1. What are the four questions to ask when designing a recursive function?
2. In the tower puzzle, why must the `k - 1` smaller disks move to the spare peg before the biggest disk can move?
3. In the Gray code construction, why do we reverse the smaller list before adding the leading 1?
4. When checking a recursive function by hand, which two things should you check?

# Chapter 3. What a recursion costs

## 3.1 Drawing the calls as a tree

To know how fast a recursive function is, draw every call as a dot, and connect each call to the calls it makes. This picture is the **recursion tree**. The function `sum_to` makes a single call each time, so its tree is just a line. Functions that call themselves twice make a tree that spreads out. Here is the tree for the slow Fibonacci function, where $f(n) = f(n-1) + f(n-2)$ and $f(0) = 0$, $f(1) = 1$.

```
                    f(4)
                 /        \
             f(3)          f(2)
            /    \        /    \
         f(2)    f(1)  f(1)    f(0)
        /   \
     f(1)   f(0)
```

You can see that `f(2)` is computed twice and `f(1)` three times. The time of a recursion is roughly the number of dots in the tree, multiplied by the work done at each dot besides the calls themselves. The extra memory is roughly the height of the tree, because only one path from the top to the current dot sits on the call stack at any moment.

## 3.2 Counting calls with a recurrence

Let $T(n)$ be the number of calls made by `fib(n)`, counting itself. For $n \ge 2$ there is one call for the function itself, plus all calls of the two smaller problems. A formula that defines a quantity through smaller versions of itself is called a **recurrence**:

$$T(n) = 1 + T(n-1) + T(n-2), \qquad T(0) = T(1) = 1.$$

We can let a function count for us, using the same recursive shape.

```python
def fib_calls(n):
    if n < 2:
        return 1
    return 1 + fib_calls(n - 1) + fib_calls(n - 2)


assert fib_calls(4) == 9
assert fib_calls(10) == 177
assert fib_calls(20) == 21891
```

```cpp
long long fib_calls(int n) {
    if (n < 2) return 1;
    return 1 + fib_calls(n - 1) + fib_calls(n - 2);
}
```

The tree above for $n = 4$ has 9 dots, which agrees. Notice how fast it grows: 177 calls for $n = 10$, but 21891 calls for $n = 20$. The number of calls multiplies by about 1.6 each time $n$ grows by one, so it is exponential, roughly $O(1.6^n)$. By $n = 50$ no computer can wait for it. We will fix this in Chapter 6.

## 3.3 Unrolling a recurrence

A neat way to solve a recurrence is to unroll it, which means substituting it into itself until a pattern shows. Take the tower puzzle. The number of moves $M(k)$ for $k$ disks is the moves for $k - 1$ disks twice plus one move for the big disk:

$$M(k) = 2\,M(k-1) + 1, \qquad M(0) = 0.$$

Unroll it: $M(1) = 1$, $M(2) = 2 \cdot 1 + 1 = 3$, $M(3) = 2 \cdot 3 + 1 = 7$, $M(4) = 15$. Each value is one less than a power of two, and we can prove it. If $M(k-1) = 2^{k-1} - 1$, then $M(k) = 2(2^{k-1} - 1) + 1 = 2^k - 1$. The base case $M(0) = 2^0 - 1 = 0$ holds too, so the formula is true for every $k$.

```python
def hanoi_count(k):
    if k == 0:
        return 0
    return 2 * hanoi_count(k - 1) + 1


assert hanoi_count(3) == 7
assert hanoi_count(10) == 1023
assert all(hanoi_count(k) == 2**k - 1 for k in range(12))
```

```cpp
long long hanoi_count(int k) {
    if (k == 0) return 0;
    return 2 * hanoi_count(k - 1) + 1;
}
```

So the tower puzzle needs $2^n - 1$ moves, and time $O(2^n)$ is unavoidable because the answer itself has that many moves. Legend says monks move 64 golden disks, which would take $2^{64} - 1$ moves, more than 18 billion billion. Our `moves` function from Chapter 2 uses only $O(n)$ stack, because the tree is $n$ levels high, but the list it returns takes $O(2^n)$ space.

## 3.4 Time is nodes, space is height

Let's put the rule in one place. The **time** of a recursion is the number of dots in its tree times the work per dot. The **extra space** is the height of the tree (how deep the stack gets) plus whatever answer you store. A fat, short tree such as the tower tree is slow but easy on the stack. A thin, tall tree such as `sum_to(100000)` is quick but can crash the stack: Python stops at about 1000 nested calls unless you raise the limit with `sys.setrecursionlimit`, and C++ typically allows tens of thousands.

When a recursion is too deep, the usual fix is to turn it into a loop that carries its own variables, as we will do for Josephus in Chapter 5 and for fast powers in Chapter 4. A loop never grows the call stack.

## 3.5 Check yourself

1. In the recursion tree of slow Fibonacci, why does the tree contain the same `f(2)` more than once?
2. If every call makes two calls and the tree is $n$ levels high, roughly how many calls are there?
3. Why is the number of moves for $k$ disks exactly $2^k - 1$ and not $2^k$?
4. What determines the extra memory used by a recursive function?

# Chapter 4. Divide and conquer

## 4.1 Halve the problem

In Chapter 1 every call made the problem one step smaller. A much stronger move is to make it **half** as big. Think about a phone book: to find a name you do not read page by page, you open the middle, decide which half holds the name, and throw the other half away. After about 10 halvings a book of 1000 pages is down to one page.

This style is called **divide and conquer**: divide the problem into smaller pieces of the same kind, solve each piece recursively, then combine the answers. Let's use it to compute a power $x^n$. The slow way multiplies $x$ by itself $n$ times. The quick way notices that

$$x^n = \left(x^{n/2}\right)^2 \text{ when } n \text{ is even}, \qquad x^n = \left(x^{(n-1)/2}\right)^2 \cdot x \text{ when } n \text{ is odd.}$$

So one recursive call on half the exponent does the work of many multiplications.

```python
def power(x, n):
    if n == 0:
        return 1
    half = power(x, n // 2)
    if n % 2 == 0:
        return half * half
    return half * half * x


assert power(2, 10) == 1024
assert power(3, 13) == 1594323
assert power(7, 0) == 1
```

```cpp
long long power(long long x, int n) {
    if (n == 0) return 1;
    long long half = power(x, n / 2);
    if (n % 2 == 0) return half * half;
    return half * half * x;
}
```

For $n = 13$ the exponents visited are 13, 6, 3, 1, 0, only 5 calls instead of 13 multiplications. The exponent halves every time, so there are about $\log_2 n$ calls. A **logarithm** $\log_2 n$ is simply "how many times can you halve $n$ before reaching 1". For $n = 10^{18}$ that is only about 60 calls.

## 4.2 Fast power with a remainder

Real tests ask for $x^n$ with a huge $n$ and want only the **remainder** after dividing by some number `mod`. Raising $3$ to the power $10^{18}$ would have more digits than there are atoms in the universe, so we must never build the whole number. Luckily remainders play nicely with multiplication: the remainder of a product equals the remainder of the product of the remainders. In symbols,

$$(a \cdot b) \bmod m = \big((a \bmod m)\cdot(b \bmod m)\big) \bmod m.$$

So we can take the remainder after every multiplication, and numbers never grow beyond `mod` squared. This is exactly the problem _Fast Power With a Remainder_.

```python
def power_mod(base, exp, mod):
    if exp == 0:
        return 1 % mod
    half = power_mod(base, exp // 2, mod)
    result = half * half % mod
    if exp % 2 == 1:
        result = result * (base % mod) % mod
    return result


assert power_mod(3, 13, 1000) == 323
assert power_mod(2, 10, 1) == 0
assert power_mod(5, 0, 7) == 1
```

```cpp
long long power_mod(long long base, long long exp, long long mod) {
    if (exp == 0) return 1 % mod;
    long long half = power_mod(base, exp / 2, mod);
    long long result = half * half % mod;
    if (exp % 2 == 1) result = result * (base % mod) % mod;
    return result;
}
```

The `1 % mod` in the base case matters when `mod` is 1, because then every remainder is 0, including the empty product. In C++ the product `half * half` must fit in 64 bits, which is safe when `mod` is below about $3 \cdot 10^9$. Time is $O(\log \text{exp})$ and the stack is the same height, $O(\log \text{exp})$.

## 4.3 Reading the exponent in binary

There is a second way to see the same algorithm, with no recursion at all. Write the exponent in binary (base 2). For example $13 = 1101_2$, which means $13 = 8 + 4 + 1$, so $3^{13} = 3^8 \cdot 3^4 \cdot 3^1$. We can get $3^1, 3^2, 3^4, 3^8, \dots$ by squaring again and again, and we multiply into the answer only the ones whose binary digit is 1. A loop does it: look at the last bit of the exponent, multiply it in when it is 1, square the base, and drop the last bit by halving.

```python
def power_mod_loop(base, exp, mod):
    result = 1 % mod
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = result * base % mod
        base = base * base % mod
        exp //= 2
    return result


assert power_mod_loop(3, 13, 1000) == 323
assert power_mod_loop(2, 10, 1) == 0
assert power_mod_loop(10, 18, 10**9 + 7) == power_mod(10, 18, 10**9 + 7)
```

```cpp
long long power_mod_loop(long long base, long long exp, long long mod) {
    long long result = 1 % mod;
    base %= mod;
    while (exp > 0) {
        if (exp % 2 == 1) result = result * base % mod;
        base = base * base % mod;
        exp /= 2;
    }
    return result;
}
```

Here is the hand trace for $3^{13} \bmod 1000$, with every number checked by running the code.

| exponent | last bit | result after step | base after squaring |
| -------- | -------- | ----------------- | ------------------- |
| 13       | 1        | 3                 | 9                   |
| 6        | 0        | 3                 | 81                  |
| 3        | 1        | 243               | 561                 |
| 1        | 1        | 323               | 721                 |

When the exponent reaches 0 the answer is 323. This loop uses $O(1)$ extra space, which is why it is the version people write in contests. The recursive version is easier to see; the loop is the same idea with the stack removed.

## 4.4 Splitting a list in two

Halving also helps with lists. To sort a list: cut it into a left half and a right half, sort each half recursively, and then **merge** the two sorted halves, which means repeatedly taking the smaller of the two front items. The base case is a list of 0 or 1 items, which is already sorted.

```python
def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


assert merge_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9]
assert merge_sort([]) == []
```

```cpp
vector<int> merge_sort(vector<int> a) {
    if (a.size() <= 1) return a;
    int mid = a.size() / 2;
    vector<int> left = merge_sort(vector<int>(a.begin(), a.begin() + mid));
    vector<int> right = merge_sort(vector<int>(a.begin() + mid, a.end()));
    vector<int> out;
    size_t i = 0, j = 0;
    while (i < left.size() && j < right.size()) {
        if (left[i] <= right[j]) out.push_back(left[i++]);
        else out.push_back(right[j++]);
    }
    while (i < left.size()) out.push_back(left[i++]);
    while (j < right.size()) out.push_back(right[j++]);
    return out;
}
```

The cost is easy to read from the recursion tree. Each level of the tree handles all $n$ items once while merging, and halving $n$ gives about $\log_2 n$ levels, so the total is

$$T(n) = 2\,T(n/2) + O(n) \;\Rightarrow\; O(n \log n).$$

Compare this with the fast power: there one half was enough, giving $T(n) = T(n/2) + O(1) = O(\log n)$. The general rule is: count the levels, then count the work on each level.

## 4.5 Check yourself

1. How many recursive calls does `power(x, 64)` make before reaching the base case?
2. Why can we take the remainder after every multiplication in `power_mod`?
3. In the binary view of $3^{13}$, which powers of 3 are multiplied into the answer?
4. Why does merge sort take $O(n \log n)$ time and not $O(n^2)$?

# Chapter 5. Building on smaller answers

## 5.1 Take it or leave it

The next kind of recursion handles a list one item at a time. For each item there are two options: take it or leave it. Suppose we want the sum of every subset of a list (a subset is any selection of items, including none and all). The subsets of `[1, 2, 3]` are `{}`, `{1}`, `{2}`, `{3}`, `{1,2}`, `{1,3}`, `{2,3}`, `{1,2,3}` with sums 0, 1, 2, 3, 3, 4, 5, 6.

Here is the recursive thought. Suppose we already know the sums of all subsets of the list without its first item. Every subset of the whole list either leaves the first item out (its sum is one of the known sums) or takes it (its sum is a known sum plus the first item). So the answer is the known list, together with the known list shifted by the first item. This is exactly the problem _All Subset Sums_.

```python
def subset_sums(nums, start=0):
    if start == len(nums):
        return [0]
    rest = subset_sums(nums, start + 1)
    return sorted(rest + [s + nums[start] for s in rest])


assert subset_sums([1, 2, 3]) == [0, 1, 2, 3, 3, 4, 5, 6]
assert subset_sums([]) == [0]
assert subset_sums([5, 5]) == [0, 5, 5, 10]
```

```cpp
vector<int> subset_sums(const vector<int>& nums, int start = 0) {
    if (start == (int)nums.size()) return {0};
    vector<int> result = subset_sums(nums, start + 1);
    size_t old = result.size();
    for (size_t i = 0; i < old; i++) result.push_back(result[i] + nums[start]);
    sort(result.begin(), result.end());
    return result;
}
```

The empty list has one subset, the empty one, with sum 0: that is the base case. Each new item doubles the length of the list, so the answer has $2^n$ numbers and the work is $O(n \cdot 2^n)$ with the sorting included (it can be made $O(2^n)$ by merging the two sorted halves). Keep this "take it or leave it" picture in mind: it is exactly the decision tree of backtracking in Chapter 7.

## 5.2 The Josephus circle

A famous puzzle from history. `n` people stand in a circle, numbered 1 to `n`. Starting at person 1 you count `k` people (person 1 counts as the first) and remove the person you land on. Then you start counting again from the next person still standing. The last person left is the survivor. For $n = 5$ and $k = 2$ the people go in the order 2, 4, 1, 5, and person 3 survives. This is exactly the problem _The Josephus Problem_.

The honest way is to act it out with a list and remove people one by one.

```python
def josephus_removal(n, k):
    circle = list(range(1, n + 1))
    i = 0
    while len(circle) > 1:
        i = (i + k - 1) % len(circle)
        circle.pop(i)
    return circle[0]


assert josephus_removal(5, 2) == 3
assert josephus_removal(7, 3) == 4
```

```cpp
int josephus_removal(int n, int k) {
    vector<int> circle(n);
    for (int i = 0; i < n; i++) circle[i] = i + 1;
    int i = 0;
    while (circle.size() > 1) {
        i = (i + k - 1) % circle.size();
        circle.erase(circle.begin() + i);
    }
    return circle[0];
}
```

This works but costs $O(n^2)$ because removing from the middle of a list is slow, and a huge `n` makes it unusable. Here is the clever recursive thought. Number the people $0, 1, \dots, m-1$ and count from the start. The first person removed is number $(k-1) \bmod m$. After that, the circle has $m - 1$ people and counting resumes at the person numbered $k \bmod m$. If we relabel the survivors so that this person is the new number 0, we get an ordinary Josephus circle of $m-1$ people! A survivor labelled $p$ in the small circle was labelled $(p + k) \bmod m$ in the big one. So if $J(m)$ is the survivor's number among $m$ people (counting from 0):

$$J(1) = 0, \qquad J(m) = \big(J(m-1) + k\big) \bmod m.$$

For $k = 2$ the values are $J(1) = 0$, $J(2) = (0+2) \bmod 2 = 0$, $J(3) = (0+2) \bmod 3 = 2$, $J(4) = (2+2) \bmod 4 = 0$, $J(5) = (0+2) \bmod 5 = 2$. The survivor of 5 people is number 2 counting from 0, which is person 3 when counting from 1. It matches the story above.

```python
def survivor_index(m, k):
    if m == 1:
        return 0
    return (survivor_index(m - 1, k) + k) % m


def josephus(n, k):
    return survivor_index(n, k) + 1


def josephus_loop(n, k):
    position = 0
    for m in range(2, n + 1):
        position = (position + k) % m
    return position + 1


assert josephus(5, 2) == 3
assert josephus_loop(5, 2) == 3
assert all(josephus(n, k) == josephus_removal(n, k) == josephus_loop(n, k) for n in range(1, 30) for k in range(1, 8))
```

```cpp
int survivor_index(int m, int k) {
    if (m == 1) return 0;
    return (survivor_index(m - 1, k) + k) % m;
}

int josephus(int n, int k) {
    return survivor_index(n, k) + 1;
}

int josephus_loop(int n, int k) {
    int position = 0;
    for (int m = 2; m <= n; m++) position = (position + k) % m;
    return position + 1;
}
```

The recursion goes $n$ levels deep, which is too much for a very large $n$, so we flip it into the loop: start from the base case and walk up through $m = 2, 3, \dots, n$. Time is $O(n)$ and the loop uses $O(1)$ space. This is a very common move: when each call depends on only one smaller call, the recursion can be rewritten as a loop that builds answers from the small case upwards.

## 5.3 Check yourself

1. In the subset sums recursion, what is the answer for the empty list, and why?
2. If a list has 10 items, how many subset sums are there?
3. After the first person is removed from a circle of $m$ people, who becomes the new number 0 in the smaller circle?
4. Why does the Josephus loop start at $m = 2$ and not $m = 1$?

# Chapter 6. Remembering answers: memoization

## 6.1 Asking the same question twice

Back in Chapter 3 we saw that the slow Fibonacci function asks for `f(2)` again and again. The cure is to keep a notebook, usually a dictionary, from the input to the answer. Before doing any work we look in the notebook, and after finishing we write the answer in it. This technique is called **memoization** (from "memo", a written note).

```python
def fib_memo(n, memo):
    if n in memo:
        return memo[n]
    if n < 2:
        memo[n] = n
    else:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


assert fib_memo(10, {}) == 55
assert fib_memo(50, {}) == 12586269025
```

```cpp
long long fib_memo(int n, unordered_map<int, long long>& memo) {
    if (memo.count(n)) return memo[n];
    if (n < 2) return memo[n] = n;
    return memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo);
}
```

Each value from 0 to $n$ is computed once, and every later request is answered from the notebook. For $n = 10$ the whole run makes 19 calls (instead of 177), for $n = 30$ only 59 calls. In general it is $2n - 1$ calls, so time falls from exponential to $O(n)$. The only requirement is that the answer depends only on the inputs we use as the notebook key.

## 6.2 Counting routes in a grid

A **state** is the set of numbers that completely describe one subproblem. For Fibonacci the state is just $n$. Here is a problem with two numbers in the state. A robot stands in the top-left corner of a grid and may only move right or down. How many different routes lead to the cell in row `r` and column `c` (counting from 0)? Every route arrives from the cell above or from the cell to the left, so

$$\text{ways}(r, c) = \text{ways}(r-1, c) + \text{ways}(r, c-1),$$

and along the top row and left column there is exactly one route.

```python
def ways(r, c, memo):
    if r == 0 or c == 0:
        return 1
    if (r, c) in memo:
        return memo[(r, c)]
    memo[(r, c)] = ways(r - 1, c, memo) + ways(r, c - 1, memo)
    return memo[(r, c)]


assert ways(2, 2, {}) == 6
assert ways(16, 16, {}) == 601080390
```

```cpp
long long ways(int r, int c, map<pair<int, int>, long long>& memo) {
    if (r == 0 || c == 0) return 1;
    auto key = make_pair(r, c);
    if (memo.count(key)) return memo[key];
    return memo[key] = ways(r - 1, c, memo) + ways(r, c - 1, memo);
}
```

Without the notebook the number of calls would be as large as the answer itself, over 600 million for the cell $(16, 16)$. With it, each of the $r \cdot c$ cells is solved once, so the time is $O(r \cdot c)$.

## 6.3 Can some items add up to a target

One more state with two numbers, and this one is the bridge to the next big topic. Given positive numbers and a target, can some of them add up exactly to the target? For each item we can take it or leave it (the picture from Chapter 5), and the state is "which item am I looking at, and how much do I still need".

```python
def can_make(nums, i, remaining, memo):
    if remaining == 0:
        return True
    if remaining < 0 or i == len(nums):
        return False
    if (i, remaining) in memo:
        return memo[(i, remaining)]
    answer = can_make(nums, i + 1, remaining - nums[i], memo) or can_make(nums, i + 1, remaining, memo)
    memo[(i, remaining)] = answer
    return answer


assert can_make([3, 34, 4, 12, 5, 2], 0, 9, {}) is True
assert can_make([3, 34, 4, 12, 5, 2], 0, 30, {}) is False
```

```cpp
bool can_make(const vector<int>& nums, int i, int remaining, map<pair<int, int>, bool>& memo) {
    if (remaining == 0) return true;
    if (remaining < 0 || i == (int)nums.size()) return false;
    auto key = make_pair(i, remaining);
    if (memo.count(key)) return memo[key];
    bool answer = can_make(nums, i + 1, remaining - nums[i], memo) || can_make(nums, i + 1, remaining, memo);
    return memo[key] = answer;
}
```

Without the notebook this tries up to $2^n$ combinations. With it there are at most $n \cdot (\text{target} + 1)$ different states, each solved once, so the time is $O(n \cdot \text{target})$. A recursion with a notebook is called **top-down dynamic programming**, and the step on dynamic programming later in this course builds on exactly this idea.

## 6.4 When a notebook does not help

Memoization pays off only when the same state shows up many times and the answer is a small thing, like a number or a yes/no. It does not help when you must **list every answer**, as in "print all subsets" or "all arrangements". There, every path of choices is a different answer and nothing repeats, so there is nothing to look up. That family of problems is solved by **backtracking**, our topic from the next chapter on. A short rule: counting or yes/no with repeated states means memoize; listing everything or searching through choices means backtrack.

## 6.5 Check yourself

1. What two things does a memoized function do around its real work?
2. What is the state in the grid-routes problem?
3. Why is the table of `can_make` at most $n \cdot (\text{target} + 1)$ in size?
4. Why is memoization of no use for printing all subsets of a list?

# Chapter 7. Backtracking: choose, explore, undo

## 7.1 Trying every choice

So far each recursion computed one answer. Now we want something different: to **list** many answers, or to search for one among a huge number of possibilities. Think of walking through a maze with a ball of thread. At every fork you choose a corridor and walk down it. If it leads to a dead end, you walk back to the fork, wind the thread up a little, and try the next corridor. You never forget which corridors you have tried, and you never leave a trail that belongs to a path you gave up.

That is **backtracking**. In code, every step of the walk has three parts: **choose** (add one decision to the path built so far), **explore** (recurse to make the next decision), and **undo** (remove the decision again so that the next sibling choice starts from a clean path). Here is the smallest example: list every binary string of length `n`.

```python
def binary_strings(n):
    out = []
    current = []

    def go():
        if len(current) == n:
            out.append("".join(current))
            return
        for digit in "01":
            current.append(digit)
            go()
            current.pop()

    go()
    return out


assert binary_strings(2) == ["00", "01", "10", "11"]
assert binary_strings(0) == [""]
```

```cpp
void binary_strings_go(int n, string& current, vector<string>& out) {
    if ((int)current.size() == n) {
        out.push_back(current);
        return;
    }
    for (char digit : string("01")) {
        current.push_back(digit);
        binary_strings_go(n, current, out);
        current.pop_back();
    }
}

vector<string> binary_strings(int n) {
    vector<string> out;
    string current;
    binary_strings_go(n, current, out);
    return out;
}
```

The `current` list is shared by all the calls: there is only one path, and it grows and shrinks as we walk. The `append` is the choose, the `go()` is the explore and the `pop` is the undo. If we forgot the `pop`, the path would keep growing and the second digit of the first string would stay in place for all the others.

## 7.2 The tree of decisions

Backtracking is a walk over a **decision tree**: each node is a partial path, and each branch is one choice. For the strings above, the root is the empty path, it has two children `0` and `1`, each of those has two children, and so on. The leaves at depth `n` are the answers. The walk visits the tree depth first: go down as far as possible, record the answer if you reach the end, climb back up one step by undoing, and take the next branch.

A different way to shape the tree is "take it or leave it" from Chapter 5. For every item of a list, one branch takes it and the other leaves it. After deciding about all items we have one subset.

```python
def subsets_take_skip(nums):
    out = []
    current = []

    def go(i):
        if i == len(nums):
            out.append(list(current))
            return
        current.append(nums[i])
        go(i + 1)
        current.pop()
        go(i + 1)

    go(0)
    return out


assert subsets_take_skip([1, 2]) == [[1, 2], [1], [2], []]
assert len(subsets_take_skip([1, 2, 3, 4])) == 16
```

```cpp
void subsets_take_skip_go(const vector<int>& nums, int i, vector<int>& current, vector<vector<int>>& out) {
    if (i == (int)nums.size()) {
        out.push_back(current);
        return;
    }
    current.push_back(nums[i]);
    subsets_take_skip_go(nums, i + 1, current, out);
    current.pop_back();
    subsets_take_skip_go(nums, i + 1, current, out);
}

vector<vector<int>> subsets_take_skip(const vector<int>& nums) {
    vector<vector<int>> out;
    vector<int> current;
    subsets_take_skip_go(nums, 0, current, out);
    return out;
}
```

Look carefully at `out.append(list(current))`. We store a **copy** of the path, not the path itself. If we stored `current` directly, every entry in `out` would point to the same list, and when the walk finishes and undoes everything, all entries would turn into empty lists. This copy is the most common beginner bug in backtracking. The tree has $2^n$ leaves, each copy costs up to $n$, so time and space are $O(n \cdot 2^n)$ plus a recursion that is only $n$ levels deep.

## 7.3 Subsets in dictionary order

The take/skip tree gives all subsets, but not in a nice order. Another view of the same thing is often better: every subset is built by repeatedly adding an item that sits **after** the last one chosen. Then each subset is a path in a different tree, in which a node is a subset and the children are the ways to extend it by one more item. A parameter `start` remembers where the next item may come from, so we never go backwards and never produce the same subset in two orders. Every node of this tree is itself an answer, so we record it as soon as we arrive. This is exactly the problem _All Subsets_.

```python
def all_subsets(nums):
    a = sorted(nums)
    out = []

    def go(start, current):
        out.append(list(current))
        for j in range(start, len(a)):
            current.append(a[j])
            go(j + 1, current)
            current.pop()

    go(0, [])
    return out


assert all_subsets([1, 2, 3]) == [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
assert all_subsets([3, 1]) == [[], [1], [1, 3], [3]]
```

```cpp
void all_subsets_go(const vector<int>& a, int start, vector<int>& current, vector<vector<int>>& out) {
    out.push_back(current);
    for (int j = start; j < (int)a.size(); j++) {
        current.push_back(a[j]);
        all_subsets_go(a, j + 1, current, out);
        current.pop_back();
    }
}

vector<vector<int>> all_subsets(vector<int> nums) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> out;
    vector<int> current;
    all_subsets_go(nums, 0, current, out);
    return out;
}
```

For `[1, 2, 3]` the walk goes: record `[]`; add 1 and record `[1]`; add 2 and record `[1,2]`; add 3 and record `[1,2,3]`; undo 3 (nothing else to add after 3), undo 2, add 3 instead and record `[1,3]`; undo, undo, add 2 and record `[2]`; and so on. Because we sort first and always try the smaller items first, the answers come out in dictionary order for free. Time is $O(n \cdot 2^n)$ again.

## 7.4 Combinations and cutting dead branches

A **combination** is a selection where order does not matter. We want every way to choose $k$ numbers out of $1, 2, \dots, n$; for $n = 4$ and $k = 2$ these are $[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]$. The number of them is the binomial coefficient $\binom{n}{k}$. This is exactly the problem _All Combinations of K Numbers_.

The walk is the same as in the last section, but we only record when the path has exactly $k$ numbers, and now there is a chance to be clever. If we need `need` more numbers, then the next number cannot be larger than $n - \text{need} + 1$: otherwise there are not enough numbers left to the right. Starting a branch that can never reach size $k$ is wasted work. Stopping it early is called **pruning**, like cutting dead branches off a tree.

```python
def all_combinations(n, k):
    out = []

    def go(start, current):
        need = k - len(current)
        if need == 0:
            out.append(list(current))
            return
        for j in range(start, n - need + 2):
            current.append(j)
            go(j + 1, current)
            current.pop()

    go(1, [])
    return out


assert all_combinations(4, 2) == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
assert all_combinations(3, 3) == [[1, 2, 3]]
assert len(all_combinations(8, 4)) == 70
```

```cpp
void all_combinations_go(int n, int k, int start, vector<int>& current, vector<vector<int>>& out) {
    int need = k - (int)current.size();
    if (need == 0) {
        out.push_back(current);
        return;
    }
    for (int j = start; j <= n - need + 1; j++) {
        current.push_back(j);
        all_combinations_go(n, k, j + 1, current, out);
        current.pop_back();
    }
}

vector<vector<int>> all_combinations(int n, int k) {
    vector<vector<int>> out;
    vector<int> current;
    all_combinations_go(n, k, 1, current, out);
    return out;
}
```

How much does pruning help? For $n = 6$ and $k = 5$ the function makes 21 calls with the bound, but 63 calls if the loop runs all the way to $n$ (counting every call, checked by running both). The answer has $\binom{n}{k}$ lists of length $k$, so the time is $O(k \cdot \binom{n}{k})$.

## 7.5 Check yourself

1. What are the three parts of every backtracking step?
2. Why do we store `list(current)` and not `current` when we record an answer?
3. In the subsets walk, what does the parameter `start` prevent?
4. What does the bound $n - \text{need} + 1$ in the combinations loop prevent?

# Chapter 8. Orderings, duplicates and sums

## 8.1 All orderings

A **permutation** is an ordering of all the items, such as `[2, 3, 1]`. For three different items there are $3 \cdot 2 \cdot 1 = 6$ of them, and for $n$ items $n! = n \cdot (n-1) \cdots 1$ (read "n factorial"). Now the next item is not restricted to come after the last one: any item not yet used may come next. So we keep a `used` flag for each item. This is exactly the problem _All Permutations_.

```python
def all_permutations(nums):
    a = sorted(nums)
    used = [False] * len(a)
    out = []
    current = []

    def go():
        if len(current) == len(a):
            out.append(list(current))
            return
        for j in range(len(a)):
            if used[j]:
                continue
            used[j] = True
            current.append(a[j])
            go()
            current.pop()
            used[j] = False

    go()
    return out


assert all_permutations([1, 2, 3]) == [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
assert len(all_permutations([4, 1, 3, 2])) == 24
```

```cpp
void all_permutations_go(const vector<int>& a, vector<bool>& used, vector<int>& current, vector<vector<int>>& out) {
    if (current.size() == a.size()) {
        out.push_back(current);
        return;
    }
    for (int j = 0; j < (int)a.size(); j++) {
        if (used[j]) continue;
        used[j] = true;
        current.push_back(a[j]);
        all_permutations_go(a, used, current, out);
        current.pop_back();
        used[j] = false;
    }
}

vector<vector<int>> all_permutations(vector<int> nums) {
    sort(nums.begin(), nums.end());
    vector<bool> used(nums.size(), false);
    vector<int> current;
    vector<vector<int>> out;
    all_permutations_go(nums, used, current, out);
    return out;
}
```

Notice that the undo has **two** parts now: remove the item from the path and clear its `used` flag. Any extra state you change when choosing must be restored when undoing, otherwise the next branch starts from a wrong picture. The tree has $n$ children at the top, $n - 1$ below, and so on, so $n!$ leaves, and the time is $O(n \cdot n!)$.

## 8.2 Repeated values in subsets

What if the list has equal values, like `[1, 2, 2]`? The earlier subsets walk would produce `[1,2]` twice (once with the first 2 and once with the second) and `[2]` twice. We want each different subset once: `[], [1], [1,2], [1,2,2], [2], [2,2]`. This is exactly the problem _Subsets With Repeated Values_.

The fix is a rule about each loop. Sort the list so equal values sit next to each other. Inside one loop of choices, choosing the second 2 is pointless if we have just tried the first 2: any subset built from the second would be built from the first, too. But **deeper in the recursion** a new loop begins, and there a 2 after another 2 is fine, because it makes `[2,2]`. So we skip a value only when it equals the previous value and the previous value was a choice in this very same loop, which means `j > start`.

```python
def subsets_with_duplicates(nums):
    a = sorted(nums)
    out = []

    def go(start, current):
        out.append(list(current))
        for j in range(start, len(a)):
            if j > start and a[j] == a[j - 1]:
                continue
            current.append(a[j])
            go(j + 1, current)
            current.pop()

    go(0, [])
    return out


assert subsets_with_duplicates([1, 2, 2]) == [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
assert subsets_with_duplicates([2, 2, 2]) == [[], [2], [2, 2], [2, 2, 2]]
```

```cpp
void subsets_with_duplicates_go(const vector<int>& a, int start, vector<int>& current, vector<vector<int>>& out) {
    out.push_back(current);
    for (int j = start; j < (int)a.size(); j++) {
        if (j > start && a[j] == a[j - 1]) continue;
        current.push_back(a[j]);
        subsets_with_duplicates_go(a, j + 1, current, out);
        current.pop_back();
    }
}

vector<vector<int>> subsets_with_duplicates(vector<int> nums) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> out;
    vector<int> current;
    subsets_with_duplicates_go(nums, 0, current, out);
    return out;
}
```

Trace for `[1, 2, 2]`: at the top we take 1 or the first 2, and the second 2 is skipped (`j = 2 > start = 0` and it equals its neighbour). Inside the branch that took the first 2, a new loop starts at `start = 2`, where `j == start`, so the second 2 is allowed and gives `[2, 2]`. The skipping never builds a duplicate in the first place, so there is no wasted work and no need to compare lists afterwards.

## 8.3 Repeated values in permutations

For permutations of `[1, 1, 2]` we want the three different orderings `[1,1,2], [1,2,1], [2,1,1]`, not six. The two 1s are twins: swapping them gives the same list. The trick is to force twins to be used in a fixed order, always left to right in the sorted list. In code: an item `a[j]` is skipped if its twin `a[j-1]` to the left is **not yet used**, because that means we are trying to place the right twin before the left twin. This is exactly the problem _Permutations With Repeated Values_.

```python
def unique_permutations(nums):
    a = sorted(nums)
    used = [False] * len(a)
    out = []
    current = []

    def go():
        if len(current) == len(a):
            out.append(list(current))
            return
        for j in range(len(a)):
            if used[j]:
                continue
            if j > 0 and a[j] == a[j - 1] and not used[j - 1]:
                continue
            used[j] = True
            current.append(a[j])
            go()
            current.pop()
            used[j] = False

    go()
    return out


assert unique_permutations([1, 1, 2]) == [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
assert len(unique_permutations([1, 1, 2, 2])) == 6
```

```cpp
void unique_permutations_go(const vector<int>& a, vector<bool>& used, vector<int>& current, vector<vector<int>>& out) {
    if (current.size() == a.size()) {
        out.push_back(current);
        return;
    }
    for (int j = 0; j < (int)a.size(); j++) {
        if (used[j]) continue;
        if (j > 0 && a[j] == a[j - 1] && !used[j - 1]) continue;
        used[j] = true;
        current.push_back(a[j]);
        unique_permutations_go(a, used, current, out);
        current.pop_back();
        used[j] = false;
    }
}

vector<vector<int>> unique_permutations(vector<int> nums) {
    sort(nums.begin(), nums.end());
    vector<bool> used(nums.size(), false);
    vector<int> current;
    vector<vector<int>> out;
    unique_permutations_go(nums, used, current, out);
    return out;
}
```

The count of different orderings of `[1,1,2,2]` is $\dfrac{4!}{2!\,2!} = 6$, which the last assert confirms: divide $n!$ by the factorial of the size of each group of twins.

## 8.4 Sums where items repeat

Now we pick numbers that add up to a target. Given different positive numbers `[2, 3, 6, 7]` and target 7, which selections add to 7 if each number may be used **any number of times**? The answers are `[2, 2, 3]` and `[7]`. This is exactly the problem _Combination Sum_.

We build the path in non-decreasing order, so `[2,3,2]` and `[2,2,3]` are never both produced. The item chosen may be chosen again, so we recurse with the **same** index `j` instead of `j + 1`. We carry `remaining` (the target minus the path sum). If it hits 0, record. And because the list is sorted, as soon as a candidate is bigger than `remaining`, all later candidates are too, so we can stop the loop: another pruning.

```python
def combination_sum(candidates, target):
    a = sorted(candidates)
    out = []

    def go(start, remaining, current):
        if remaining == 0:
            out.append(list(current))
            return
        for j in range(start, len(a)):
            if a[j] > remaining:
                break
            current.append(a[j])
            go(j, remaining - a[j], current)
            current.pop()

    go(0, target, [])
    return out


assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
assert combination_sum([2, 4], 3) == []
```

```cpp
void combination_sum_go(const vector<int>& a, int start, int remaining, vector<int>& current, vector<vector<int>>& out) {
    if (remaining == 0) {
        out.push_back(current);
        return;
    }
    for (int j = start; j < (int)a.size(); j++) {
        if (a[j] > remaining) break;
        current.push_back(a[j]);
        combination_sum_go(a, j, remaining - a[j], current, out);
        current.pop_back();
    }
}

vector<vector<int>> combination_sum(vector<int> candidates, int target) {
    sort(candidates.begin(), candidates.end());
    vector<vector<int>> out;
    vector<int> current;
    combination_sum_go(candidates, 0, target, current, out);
    return out;
}
```

The walk for the example: choose 2 (remaining 5), 2 again (3), 2 again (1): now every candidate exceeds 1, so the loop ends and we back up. Then 3 gives remaining 0 and `[2,2,3]` is recorded. Later the top loop tries 7 and records `[7]`. The depth is at most target divided by the smallest candidate.

## 8.5 Sums where each item is used once

When the list may contain repeated values and each **position** may be used at most once, we combine two earlier ideas: recurse with `j + 1` (as in subsets) and skip a value equal to the previous one in the same loop (as in Section 8.2). For `[10, 1, 2, 7, 6, 1, 5]` and target 8 the answers are `[1,1,6], [1,2,5], [1,7], [2,6]`. This is exactly the problem _Combination Sum, Each Number Once_.

```python
def combination_sum_ii(candidates, target):
    a = sorted(candidates)
    out = []

    def go(start, remaining, current):
        if remaining == 0:
            out.append(list(current))
            return
        for j in range(start, len(a)):
            if j > start and a[j] == a[j - 1]:
                continue
            if a[j] > remaining:
                break
            current.append(a[j])
            go(j + 1, remaining - a[j], current)
            current.pop()

    go(0, target, [])
    return out


assert combination_sum_ii([10, 1, 2, 7, 6, 1, 5], 8) == [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
assert combination_sum_ii([2, 5, 2, 1, 2], 5) == [[1, 2, 2], [5]]
```

```cpp
void combination_sum_ii_go(const vector<int>& a, int start, int remaining, vector<int>& current, vector<vector<int>>& out) {
    if (remaining == 0) {
        out.push_back(current);
        return;
    }
    for (int j = start; j < (int)a.size(); j++) {
        if (j > start && a[j] == a[j - 1]) continue;
        if (a[j] > remaining) break;
        current.push_back(a[j]);
        combination_sum_ii_go(a, j + 1, remaining - a[j], current, out);
        current.pop_back();
    }
}

vector<vector<int>> combination_sum_ii(vector<int> candidates, int target) {
    sort(candidates.begin(), candidates.end());
    vector<vector<int>> out;
    vector<int> current;
    combination_sum_ii_go(candidates, 0, target, current, out);
    return out;
}
```

In the sorted list `[1, 1, 2, 5, 6, 7, 10]` the first loop skips the second 1 (it would only repeat what the first 1 already explored), yet inside the branch that chose the first 1, the second 1 is allowed and produces `[1,1,6]`. The worst case is still the $2^n$ take-or-leave choices, but sorting, the skip and the early `break` prune almost everything in practice.

## 8.6 Jumping straight to the kth permutation

Sometimes we do not want all the answers but only one specific one. The numbers $1, \dots, n$ have $n!$ orderings in dictionary order. The 9th of the 24 orderings of $1,2,3,4$ is the ordering we want; listing all 24 would work for $n = 4$ but not for $n = 20$, which has more than $10^{18}$ orderings. This is exactly the problem _The Kth Permutation_.

Look at the structure of the sorted list. The first $(n-1)!$ orderings all start with 1, the next $(n-1)!$ with 2, and so on. For $n = 4$ that is blocks of $3! = 6$. So the position tells us the first number directly: use zero-based position $k - 1 = 8$, and $8 \div 6$ gives block 1, meaning the second smallest number, 2. The leftover position inside the block is $8 \bmod 6 = 2$, and now we repeat for the remaining numbers $\{1, 3, 4\}$ with blocks of $2! = 2$: $2 \div 2 = 1$, so we take the second smallest remaining number, 3, with leftover 0. Next blocks of $1! = 1$ and $0 \div 1 = 0$, so we take the smallest remaining, 1, and 4 is last. The answer is `2314`.

```python
def kth_permutation(n, k):
    fact = [1] * n
    for i in range(1, n):
        fact[i] = fact[i - 1] * i
    pool = list(range(1, n + 1))
    k -= 1
    digits = []
    for pos in range(n - 1, -1, -1):
        index = k // fact[pos]
        k %= fact[pos]
        digits.append(str(pool.pop(index)))
    return "".join(digits)


assert kth_permutation(4, 9) == "2314"
assert kth_permutation(3, 1) == "123"
assert kth_permutation(3, 6) == "321"
```

```cpp
string kth_permutation(int n, long long k) {
    vector<long long> fact(n, 1);
    for (int i = 1; i < n; i++) fact[i] = fact[i - 1] * i;
    vector<int> pool;
    for (int i = 1; i <= n; i++) pool.push_back(i);
    k -= 1;
    string digits;
    for (int pos = n - 1; pos >= 0; pos--) {
        int index = k / fact[pos];
        k %= fact[pos];
        digits += to_string(pool[index]);
        pool.erase(pool.begin() + index);
    }
    return digits;
}
```

There is no backtracking here at all: we skip over whole blocks of answers by counting them. Time is $O(n^2)$ because removing from the list costs up to $n$ per step, and the space is $O(n)$. In C++ the factorials fit in 64 bits up to $n = 20$.

## 8.7 Check yourself

1. How many leaves does the permutation tree for 4 different items have?
2. In the loop for subsets with repeated values, why does the condition use `j > start` and not `j > 0`?
3. In combination sum, what changes in the recursive call when an item may be reused?
4. For $n = 4$ and $k = 9$, why is the first number 2?

# Chapter 9. Building strings with rules

## 9.1 A menu for every position

Many backtracking puzzles build a string one character at a time. The simplest case is when each position has its own menu of allowed letters, and any combination of one letter per menu is fine. With menus `"ab"` and `"xyz"` the strings are `ax, ay, az, bx, by, bz`: two choices times three choices.

Notice something pleasant. In Python a string cannot be changed, so `prefix + letter` creates a new string and the old prefix stays untouched. That means the "undo" happens by itself: after the recursive call returns, `prefix` is still the same. We only need an explicit undo when we change a shared list.

```python
def menu_strings(menus, i=0, prefix=""):
    if i == len(menus):
        return [prefix]
    out = []
    for letter in menus[i]:
        out += menu_strings(menus, i + 1, prefix + letter)
    return out


assert menu_strings(["ab", "xyz"]) == ["ax", "ay", "az", "bx", "by", "bz"]
assert menu_strings([]) == [""]
```

```cpp
vector<string> menu_strings(const vector<string>& menus, int i = 0, string prefix = "") {
    if (i == (int)menus.size()) return {prefix};
    vector<string> out;
    for (char letter : menus[i]) {
        vector<string> more = menu_strings(menus, i + 1, prefix + letter);
        out.insert(out.end(), more.begin(), more.end());
    }
    return out;
}
```

A phone keypad is exactly this: the digit `2` stands for the menu `"abc"`, `3` for `"def"`, and so on up to `9` for `"wxyz"`. So for a string of digits we look up one menu per digit and call the function above. This is exactly the problem _Phone Keypad Letters_. Be careful with the empty input: for no digits the question wants an empty list, not a list holding the empty string.

```python
def letter_combinations(digits):
    keys = ["abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]
    if not digits:
        return []
    menus = [keys[int(d) - 2] for d in digits]
    return menu_strings(menus)


assert letter_combinations("23") == ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
assert letter_combinations("") == []
assert len(letter_combinations("79")) == 16
```

```cpp
vector<string> letter_combinations(const string& digits) {
    vector<string> keys = {"abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
    if (digits.empty()) return {};
    vector<string> menus;
    for (char d : digits) menus.push_back(keys[d - '2']);
    return menu_strings(menus);
}
```

The digits 7 and 9 have four letters each, so at most $4^n$ strings come out for $n$ digits, each $n$ letters long: the time is $O(n \cdot 4^n)$.

## 9.2 A rule on the next choice

Often the menu changes depending on what we have already built. Take all binary strings of length $n$ in which no two `1`s sit next to each other. At each position we may always write `0`, but we may write `1` only if the previous character is not `1`. This is exactly the problem _Binary Strings Without Two Ones in a Row_.

```python
def no_adjacent_ones(n):
    out = []

    def go(prefix):
        if len(prefix) == n:
            out.append(prefix)
            return
        go(prefix + "0")
        if not prefix.endswith("1"):
            go(prefix + "1")

    go("")
    return out


assert no_adjacent_ones(3) == ["000", "001", "010", "100", "101"]
assert no_adjacent_ones(0) == [""]
assert [len(no_adjacent_ones(n)) for n in range(6)] == [1, 2, 3, 5, 8, 13]
```

```cpp
void no_adjacent_ones_go(int n, string prefix, vector<string>& out) {
    if ((int)prefix.size() == n) {
        out.push_back(prefix);
        return;
    }
    no_adjacent_ones_go(n, prefix + "0", out);
    if (prefix.empty() || prefix.back() != '1') no_adjacent_ones_go(n, prefix + "1", out);
}

vector<string> no_adjacent_ones(int n) {
    vector<string> out;
    no_adjacent_ones_go(n, "", out);
    return out;
}
```

The rule is checked **before** the choice is made, so a bad prefix is never created. This is pruning in its cleanest form. The counts 1, 2, 3, 5, 8, 13 are Fibonacci numbers: a good string of length $n$ either ends in `0` (any good string of length $n-1$ before it) or ends in `01` (any good string of length $n-2$ before it), so $F(n) = F(n-1) + F(n-2)$. The time is $O(n \cdot F(n))$, which is about $O(n \cdot 1.62^n)$.

## 9.3 Balanced brackets

A string of round brackets is **balanced** when every `(` is closed by a later `)`, such as `(()())`. The strings `())(` and `((` are not. We want all balanced strings made of exactly $n$ pairs. This is exactly the problem _Generate Parentheses_.

The two rules are easy to state. We may add `(` while we have used fewer than $n$ of them. We may add `)` only while the number of `)` used so far is smaller than the number of `(` used so far, because a `)` with nothing to close would break the balance forever. With these two rules every prefix we build can still be finished into a balanced string, so no branch is wasted.

```python
def generate_parentheses(n):
    out = []

    def go(prefix, opens, closes):
        if len(prefix) == 2 * n:
            out.append(prefix)
            return
        if opens < n:
            go(prefix + "(", opens + 1, closes)
        if closes < opens:
            go(prefix + ")", opens, closes + 1)

    go("", 0, 0)
    return out


assert generate_parentheses(1) == ["()"]
assert generate_parentheses(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
assert [len(generate_parentheses(n)) for n in range(1, 7)] == [1, 2, 5, 14, 42, 132]
```

```cpp
void generate_parentheses_go(int n, string prefix, int opens, int closes, vector<string>& out) {
    if ((int)prefix.size() == 2 * n) {
        out.push_back(prefix);
        return;
    }
    if (opens < n) generate_parentheses_go(n, prefix + "(", opens + 1, closes, out);
    if (closes < opens) generate_parentheses_go(n, prefix + ")", opens, closes + 1, out);
}

vector<string> generate_parentheses(int n) {
    vector<string> out;
    generate_parentheses_go(n, "", 0, 0, out);
    return out;
}
```

The number of balanced strings is the Catalan number $C_n = \frac{1}{n+1}\binom{2n}{n}$, which is 1, 2, 5, 14, 42, 132 for $n = 1, \dots, 6$. It grows like $4^n / n^{1.5}$. Since `(` is tried before `)`, the output is already in dictionary order.

## 9.4 Cutting a string into valid pieces

A new shape: instead of choosing a letter, we choose where to cut. From the current position we try piece lengths 1, 2, ..., check that the piece is allowed, and continue after it. Here is a warm-up: a digit string such as `"226"` can be read as letters if `1 = A, 2 = B, ..., 26 = Z`, and each piece is one or two digits, without a leading zero, with a value at most 26. The readings of `"226"` are `BBF` (2, 2, 6), `BZ` (2, 26) and `VF` (22, 6).

```python
def decodings(s):
    out = []

    def go(start, letters):
        if start == len(s):
            out.append(letters)
            return
        for length in (1, 2):
            piece = s[start:start + length]
            if len(piece) < length or piece[0] == "0" or int(piece) > 26:
                continue
            go(start + length, letters + chr(ord("A") + int(piece) - 1))

    go(0, "")
    return out


assert decodings("226") == ["BBF", "BZ", "VF"]
assert decodings("10") == ["J"]
assert decodings("0") == []
```

```cpp
void decodings_go(const string& s, int start, string letters, vector<string>& out) {
    if (start == (int)s.size()) {
        out.push_back(letters);
        return;
    }
    for (int length = 1; length <= 2; length++) {
        if (start + length > (int)s.size()) continue;
        string piece = s.substr(start, length);
        if (piece[0] == '0' || stoi(piece) > 26) continue;
        decodings_go(s, start + length, letters + char('A' + stoi(piece) - 1), out);
    }
}

vector<string> decodings(const string& s) {
    vector<string> out;
    decodings_go(s, 0, "", out);
    return out;
}
```

The only things that change from one cutting puzzle to the next are the allowed piece lengths, the test that a piece is valid, and what counts as finished. For an IP address we need exactly four pieces of 1 to 3 digits, each a number from 0 to 255 without a leading zero (the single digit `0` is fine, `01` is not), and the last piece must end exactly at the end of the string. This is exactly the problem _Restore IP Addresses_.

```python
def restore_ip_addresses(s):
    out = []

    def valid(part):
        return (part == "0" or part[0] != "0") and int(part) <= 255

    def go(start, parts):
        if len(parts) == 4:
            if start == len(s):
                out.append(".".join(parts))
            return
        for length in (1, 2, 3):
            part = s[start:start + length]
            if len(part) == length and valid(part):
                go(start + length, parts + [part])

    go(0, [])
    return sorted(out)


assert restore_ip_addresses("25525511135") == ["255.255.11.135", "255.255.111.35"]
assert restore_ip_addresses("0000") == ["0.0.0.0"]
assert restore_ip_addresses("1") == []
```

```cpp
void restore_ip_addresses_go(const string& s, int start, vector<string>& parts, vector<string>& out) {
    if (parts.size() == 4) {
        if (start == (int)s.size()) out.push_back(parts[0] + "." + parts[1] + "." + parts[2] + "." + parts[3]);
        return;
    }
    for (int length = 1; length <= 3; length++) {
        if (start + length > (int)s.size()) break;
        string part = s.substr(start, length);
        if (part.size() > 1 && part[0] == '0') continue;
        if (stoi(part) > 255) continue;
        parts.push_back(part);
        restore_ip_addresses_go(s, start + length, parts, out);
        parts.pop_back();
    }
}

vector<string> restore_ip_addresses(const string& s) {
    vector<string> out;
    vector<string> parts;
    restore_ip_addresses_go(s, 0, parts, out);
    sort(out.begin(), out.end());
    return out;
}
```

There are at most 3 choices for each of 4 pieces, so at most $3^4 = 81$ branches: constant time. (In Python we build `parts + [part]`, a fresh list, so no undo is needed; in C++ we push and pop the shared vector.)

## 9.5 Cutting into palindromes

The same shape works when a piece is valid if it is a palindrome. We want every way to cut `"aab"` into pieces that are all palindromes: `["a","a","b"]` and `["aa","b"]`. Checking each candidate piece letter by letter would repeat work, so first build a table `pal[i][j]` that says whether `s[i..j]` is a palindrome. A piece is a palindrome when its two ends match and the inside is a palindrome (or has at most one letter). We fill the table from short pieces to long ones, so the inside is always ready when we need it.

```python
def palindrome_table(s):
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            pal[i][j] = s[i] == s[j] and (length <= 2 or pal[i + 1][j - 1])
    return pal


table = palindrome_table("aab")
assert table[0][1] is True
assert table[0][2] is False
assert table[1][2] is False
```

```cpp
vector<vector<bool>> palindrome_table(const string& s) {
    int n = s.size();
    vector<vector<bool>> pal(n, vector<bool>(n, false));
    for (int length = 1; length <= n; length++) {
        for (int i = 0; i + length <= n; i++) {
            int j = i + length - 1;
            pal[i][j] = s[i] == s[j] && (length <= 2 || pal[i + 1][j - 1]);
        }
    }
    return pal;
}
```

Now the cutting walk is just like before, with `pal[start][j]` as the validity test. Trying shorter pieces first gives the answers in sorted order. This is exactly the problem _Palindrome Partitioning_.

```python
def palindrome_partitions(s):
    n = len(s)
    pal = palindrome_table(s)
    out = []
    pieces = []

    def go(start):
        if start == n:
            out.append(list(pieces))
            return
        for j in range(start, n):
            if pal[start][j]:
                pieces.append(s[start:j + 1])
                go(j + 1)
                pieces.pop()

    go(0)
    return out


assert palindrome_partitions("aab") == [["a", "a", "b"], ["aa", "b"]]
assert palindrome_partitions("aaa") == [["a", "a", "a"], ["a", "aa"], ["aa", "a"], ["aaa"]]
```

```cpp
void palindrome_partitions_go(const string& s, const vector<vector<bool>>& pal, int start, vector<string>& pieces, vector<vector<string>>& out) {
    if (start == (int)s.size()) {
        out.push_back(pieces);
        return;
    }
    for (int j = start; j < (int)s.size(); j++) {
        if (pal[start][j]) {
            pieces.push_back(s.substr(start, j - start + 1));
            palindrome_partitions_go(s, pal, j + 1, pieces, out);
            pieces.pop_back();
        }
    }
}

vector<vector<string>> palindrome_partitions(const string& s) {
    vector<vector<string>> out;
    vector<string> pieces;
    palindrome_partitions_go(s, palindrome_table(s), 0, pieces, out);
    return out;
}
```

The table costs $O(n^2)$ to build. A string of $n$ equal letters has $2^{n-1}$ ways to be cut (a cut or no cut in each of the $n - 1$ gaps), so the walk costs $O(n \cdot 2^n)$ in the worst case.

## 9.6 Check yourself

1. Why does a Python string prefix need no explicit undo step?
2. In the brackets walk, why may a `)` be added only when `closes < opens`?
3. Why is the number of binary strings without two adjacent ones a Fibonacci number?
4. In a cutting puzzle, what three things change from one problem to the next?

# Chapter 10. Walking through grids

## 10.1 Marking the cells of the current path

On a grid we walk from cell to cell: up, down, left or right. If we may step on a cell only once per path, we need to remember which cells are on the **current** path. We keep a grid of flags `on_path`. When we enter a cell we set its flag, and when we leave it for good we clear the flag. This is the choose-explore-undo rhythm with the cell as the choice.

This differs from the visited marks in a graph search such as BFS (breadth first search). There a cell is marked once and for all because we only ask whether it can be reached. Here the same cell can be used by many different paths, so the mark must be taken off when we back out. Let's first just count the routes. The maze has `1` for an open cell and `0` for a wall, and we walk from the top-left corner to the bottom-right corner without stepping on any cell twice.

```python
def count_routes(maze):
    rows, cols = len(maze), len(maze[0])
    if maze[0][0] == 0 or maze[rows - 1][cols - 1] == 0:
        return 0
    on_path = [[False] * cols for _ in range(rows)]

    def go(r, c):
        if r == rows - 1 and c == cols - 1:
            return 1
        on_path[r][c] = True
        total = 0
        for dr, dc in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 1 and not on_path[nr][nc]:
                total += go(nr, nc)
        on_path[r][c] = False
        return total

    return go(0, 0)


assert count_routes([[1, 1], [1, 1]]) == 2
assert count_routes([[1, 0], [1, 1]]) == 1
assert count_routes([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) == 12
```

```cpp
int count_routes_go(const vector<vector<int>>& maze, vector<vector<bool>>& on_path, int r, int c) {
    int rows = maze.size(), cols = maze[0].size();
    if (r == rows - 1 && c == cols - 1) return 1;
    on_path[r][c] = true;
    int total = 0;
    int dr[4] = {1, 0, -1, 0};
    int dc[4] = {0, 1, 0, -1};
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && maze[nr][nc] == 1 && !on_path[nr][nc]) {
            total += count_routes_go(maze, on_path, nr, nc);
        }
    }
    on_path[r][c] = false;
    return total;
}

int count_routes(const vector<vector<int>>& maze) {
    int rows = maze.size(), cols = maze[0].size();
    if (maze[0][0] == 0 || maze[rows - 1][cols - 1] == 0) return 0;
    vector<vector<bool>> on_path(rows, vector<bool>(cols, false));
    return count_routes_go(maze, on_path, 0, 0);
}
```

In a 3 by 3 grid with no walls there are 12 such routes. The number grows very quickly for bigger grids, so the worst-case time is exponential in the number of cells, and the extra space is $O(\text{rows} \cdot \text{cols})$ for the flags and the stack.

## 10.2 Recording the moves of the rat

A rat starts at the top-left cell of a maze and must reach the bottom-right cell. We want every path written as a string of moves `D` (down), `L` (left), `R` (right), `U` (up), listed in dictionary order. If the start or the goal is a wall, or no path exists, the answer is an empty list; for a grid with one open cell the only path is the empty string. This is exactly the problem _Rat in a Maze_.

It is the previous function with one more shared list, `path`, of the letters so far. We push a letter before stepping into a neighbour and pop it afterwards. The directions are tried in the order `D, L, R, U`, which is alphabetical, so the paths come out sorted with no extra work.

```python
def rat_in_a_maze(maze):
    rows, cols = len(maze), len(maze[0])
    if maze[0][0] == 0 or maze[rows - 1][cols - 1] == 0:
        return []
    out = []
    path = []
    on_path = [[False] * cols for _ in range(rows)]
    steps = (("D", 1, 0), ("L", 0, -1), ("R", 0, 1), ("U", -1, 0))

    def go(r, c):
        if r == rows - 1 and c == cols - 1:
            out.append("".join(path))
            return
        on_path[r][c] = True
        for letter, dr, dc in steps:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 1 and not on_path[nr][nc]:
                path.append(letter)
                go(nr, nc)
                path.pop()
        on_path[r][c] = False

    go(0, 0)
    return out


assert rat_in_a_maze([[1, 1, 0], [1, 1, 1], [0, 1, 1]]) == ["DRDR", "DRRD", "RDDR", "RDRD"]
assert rat_in_a_maze([[1, 0], [1, 1]]) == ["DR"]
assert rat_in_a_maze([[1]]) == [""]
assert rat_in_a_maze([[1, 0], [0, 1]]) == []
```

```cpp
void rat_in_a_maze_go(const vector<vector<int>>& maze, vector<vector<bool>>& on_path, int r, int c, string& path, vector<string>& out) {
    int rows = maze.size(), cols = maze[0].size();
    if (r == rows - 1 && c == cols - 1) {
        out.push_back(path);
        return;
    }
    on_path[r][c] = true;
    const char letters[4] = {'D', 'L', 'R', 'U'};
    const int dr[4] = {1, 0, 0, -1};
    const int dc[4] = {0, -1, 1, 0};
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && maze[nr][nc] == 1 && !on_path[nr][nc]) {
            path.push_back(letters[d]);
            rat_in_a_maze_go(maze, on_path, nr, nc, path, out);
            path.pop_back();
        }
    }
    on_path[r][c] = false;
}

vector<string> rat_in_a_maze(const vector<vector<int>>& maze) {
    int rows = maze.size(), cols = maze[0].size();
    vector<string> out;
    if (maze[0][0] == 0 || maze[rows - 1][cols - 1] == 0) return out;
    vector<vector<bool>> on_path(rows, vector<bool>(cols, false));
    string path;
    rat_in_a_maze_go(maze, on_path, 0, 0, path, out);
    return out;
}
```

By hand for the 3 by 3 maze in the first assert: from the top-left cell going `D` reaches the middle-left cell, then `R` the centre, then either `D` then `R`, or `R` then `D`. Going `R` first from the start gives the other two. The cell at the top right and the bottom left are walls, so those are the four paths. The worst case is exponential, $O(4^{\text{rows} \cdot \text{cols}})$ at the very most, since the flags stop a path from crossing itself.

## 10.3 Hunting for a word in a grid

In a grid of letters we want to know whether a word can be spelled by walking from cell to neighbouring cell (up, down, left, right) without using any cell twice. The path is the word itself: at step `i` we must stand on a cell holding `word[i]`. So we try every cell as a start and ask `go(r, c, i)`: can the word from index `i` onwards be spelled starting at this cell?

A neat trick avoids a second grid. While a cell is on the current path we overwrite its letter with `#`, which matches no letter, so the walk cannot step there again. After exploring we write the original letter back. That is the undo. Note also that we stop as soon as one path works, because we only need yes or no. This is exactly the problem _Word Search_.

```python
def word_search(board, word):
    rows, cols = len(board), len(board[0])
    grid = [list(row) for row in board]

    def go(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != word[i]:
            return False
        saved = grid[r][c]
        grid[r][c] = "#"
        found = go(r + 1, c, i + 1) or go(r - 1, c, i + 1) or go(r, c + 1, i + 1) or go(r, c - 1, i + 1)
        grid[r][c] = saved
        return found

    return any(go(r, c, 0) for r in range(rows) for c in range(cols))


board = ["ABCE", "SFCS", "ADEE"]
assert word_search(board, "ABCCED") is True
assert word_search(board, "SEE") is True
assert word_search(board, "ABCB") is False
```

```cpp
bool word_search_go(vector<string>& grid, const string& word, int r, int c, int i) {
    if (i == (int)word.size()) return true;
    if (r < 0 || r >= (int)grid.size() || c < 0 || c >= (int)grid[0].size() || grid[r][c] != word[i]) return false;
    char saved = grid[r][c];
    grid[r][c] = '#';
    bool found = word_search_go(grid, word, r + 1, c, i + 1) || word_search_go(grid, word, r - 1, c, i + 1) ||
                 word_search_go(grid, word, r, c + 1, i + 1) || word_search_go(grid, word, r, c - 1, i + 1);
    grid[r][c] = saved;
    return found;
}

bool word_search(vector<string> board, const string& word) {
    for (int r = 0; r < (int)board.size(); r++) {
        for (int c = 0; c < (int)board[0].size(); c++) {
            if (word_search_go(board, word, r, c, 0)) return true;
        }
    }
    return false;
}
```

The word `ABCB` fails because the only `B` is used by the first step, and it cannot be used again. After the first letter each step has at most 3 new directions (one is where we came from), so a word of length $L$ costs about $O(\text{rows} \cdot \text{cols} \cdot 3^L)$ in the worst case. In practice it is much faster, because a wrong letter ends a branch at once.

## 10.4 Check yourself

1. Why must the flag of a cell be cleared when we leave it, unlike the visited mark in BFS?
2. In the rat maze, why does trying the directions as `D, L, R, U` make the list come out sorted?
3. In word search, what does overwriting the cell with `#` achieve?
4. Why is a word search branch cheap when the next letter does not match?

# Chapter 11. Constraint puzzles

## 11.1 Queens that do not attack

A queen in chess attacks every square in her row, her column and along both diagonals. The puzzle: place $n$ queens on an $n \times n$ board so that none attacks another. Because no two queens share a row, there is exactly one queen in each row, so we place them row by row, and the only choice in row `r` is the column. This is exactly the problem _N Queens: Count the Solutions_.

To test a square quickly we need names for the lines through it. Two squares are on the same "down-right" diagonal exactly when `r - c` is equal, and on the same "down-left" diagonal exactly when `r + c` is equal. So we keep three sets: used columns, used values of `r - c`, and used values of `r + c`. Placing a queen adds one value to each set, and undoing removes it.

```
n = 4, one of the two solutions (Q = queen):

  . Q . .      row 0 -> column 1
  . . . Q      row 1 -> column 3
  Q . . .      row 2 -> column 0
  . . Q .      row 3 -> column 2
```

```python
def count_queens(n):
    cols, diag1, diag2 = set(), set(), set()

    def go(r):
        if r == n:
            return 1
        total = 0
        for c in range(n):
            if c in cols or r - c in diag1 or r + c in diag2:
                continue
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            total += go(r + 1)
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
        return total

    return go(0)


assert [count_queens(n) for n in range(1, 7)] == [1, 0, 0, 2, 10, 4]
assert count_queens(8) == 92
```

```cpp
int count_queens_go(int n, int r, set<int>& cols, set<int>& diag1, set<int>& diag2) {
    if (r == n) return 1;
    int total = 0;
    for (int c = 0; c < n; c++) {
        if (cols.count(c) || diag1.count(r - c) || diag2.count(r + c)) continue;
        cols.insert(c);
        diag1.insert(r - c);
        diag2.insert(r + c);
        total += count_queens_go(n, r + 1, cols, diag1, diag2);
        cols.erase(c);
        diag1.erase(r - c);
        diag2.erase(r + c);
    }
    return total;
}

int count_queens(int n) {
    set<int> cols, diag1, diag2;
    return count_queens_go(n, 0, cols, diag1, diag2);
}
```

Pruning makes a huge difference. Putting 8 queens anywhere on 64 squares has billions of arrangements, and even one queen per row gives $8^8 = 16{,}777{,}216$. The walk above makes only 2057 calls for $n = 8$ and finds all 92 solutions (the call counts were measured by running the code). In general it is at most $n!$ placements, so the time is $O(n!)$ and the extra space is $O(n)$.

## 11.2 Sets of squares as bits

Sets are easy to read but slowish. A faster trick stores a set of columns in a single integer: **bit** number $c$ of the integer (counting from the right, from 0) is 1 when column $c$ is in the set. Three operations are enough. `a | b` is the union of two sets, `a & b` is the intersection, and `x & -x` isolates the lowest 1-bit of `x`, which lets us pick one free column at a time.

We keep three integers: `cols` (columns already used), `d1` and `d2` (columns attacked diagonally in the current row). When we go down one row, the attacks along one diagonal move one column to the left, and the other move one column to the right, so we shift `d1` left by one and `d2` right by one. A mask `full = 2^n - 1` keeps only the $n$ columns of the board.

```python
def count_queens_bits(n):
    full = (1 << n) - 1

    def go(cols, d1, d2):
        if cols == full:
            return 1
        total = 0
        free = full & ~(cols | d1 | d2)
        while free:
            bit = free & -free
            free ^= bit
            total += go(cols | bit, ((d1 | bit) << 1) & full, (d2 | bit) >> 1)
        return total

    return go(0, 0, 0)


assert [count_queens_bits(n) for n in range(1, 7)] == [1, 0, 0, 2, 10, 4]
assert count_queens_bits(8) == 92
```

```cpp
int count_queens_bits_go(int full, int cols, int d1, int d2) {
    if (cols == full) return 1;
    int total = 0;
    int free_cols = full & ~(cols | d1 | d2);
    while (free_cols) {
        int bit = free_cols & -free_cols;
        free_cols ^= bit;
        total += count_queens_bits_go(full, cols | bit, ((d1 | bit) << 1) & full, (d2 | bit) >> 1);
    }
    return total;
}

int count_queens_bits(int n) {
    int full = (1 << n) - 1;
    return count_queens_bits_go(full, 0, 0, 0);
}
```

The line `free = full & ~(cols | d1 | d2)` reads "all columns, minus everything that is attacked". Every free column is then tried in turn, and `free ^= bit` removes it from the loop. There is no explicit undo because `cols`, `d1` and `d2` are passed by value: each call gets its own copies. Bit tricks are not needed for correctness, but they make the same search many times faster.

## 11.3 Colouring a graph

A **graph** is a set of points (nodes) joined by lines (edges). We want to colour every node with one of `colors` colours so that the two ends of every edge get different colours. Think of colouring a map so that neighbouring countries differ. This is exactly the problem _Can the Graph Be Coloured?_.

We colour the nodes one by one in order. For node `i` we try every colour that none of its already coloured neighbours uses. If a colour leads to a full colouring, we are done and return `True` straight away. If not, we reset the node to "uncoloured" (`-1`, the undo) and try the next colour. If every colour fails, the previous node must change its colour: that is the backtrack. An edge from a node to itself can never be satisfied, so the answer is `False` immediately.

```python
def can_colour(n, edges, colours):
    if any(u == v for u, v in edges):
        return False
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    colour = [-1] * n

    def go(i):
        if i == n:
            return True
        for c in range(colours):
            if all(colour[j] != c for j in adj[i]):
                colour[i] = c
                if go(i + 1):
                    return True
                colour[i] = -1
        return False

    return go(0)


triangle = [[0, 1], [1, 2], [0, 2]]
assert can_colour(3, triangle, 2) is False
assert can_colour(3, triangle, 3) is True
assert can_colour(4, [[0, 1], [1, 2], [2, 3], [3, 0]], 2) is True
assert can_colour(2, [[1, 1]], 5) is False
```

```cpp
bool can_colour_go(int i, int n, const vector<vector<int>>& adj, vector<int>& colour, int colours) {
    if (i == n) return true;
    for (int c = 0; c < colours; c++) {
        bool ok = true;
        for (int j : adj[i]) {
            if (colour[j] == c) ok = false;
        }
        if (ok) {
            colour[i] = c;
            if (can_colour_go(i + 1, n, adj, colour, colours)) return true;
            colour[i] = -1;
        }
    }
    return false;
}

bool can_colour(int n, const vector<vector<int>>& edges, int colours) {
    vector<vector<int>> adj(n);
    for (const auto& e : edges) {
        if (e[0] == e[1]) return false;
        adj[e[0]].push_back(e[1]);
        adj[e[1]].push_back(e[0]);
    }
    vector<int> colour(n, -1);
    return can_colour_go(0, n, adj, colour, colours);
}
```

A triangle needs 3 colours because all three nodes touch each other, while a square (4-cycle) is fine with 2 colours alternating around it. In the worst case there are $k^n$ colourings to try ($k$ colours), each check costing the node's degree. This is not a flaw of our code: no fast method is known for this problem in general, and it is one of the famous hard ("NP-complete") problems.

## 11.4 Sudoku

Sudoku is the same game with more rules. In the full puzzle a $9 \times 9$ grid must hold the digits 1 to 9 so that every row, every column and every $3 \times 3$ box contains each digit once. To learn the method without drowning in cells we use a mini version: a $4 \times 4$ grid with digits 1 to 4 and $2 \times 2$ boxes. Zero marks an empty cell.

The plain way is to fill empty cells in reading order, trying each digit that does not break a rule. A smarter way is to always fill the **most constrained** cell next, the empty cell with the fewest possible digits. A cell with one candidate is forced, and a cell with zero candidates proves that an earlier guess was wrong, so we backtrack at once without exploring a thing. Choosing the most constrained cell is a small change with a big effect.

```python
def solve_mini(grid):
    g = [row[:] for row in grid]

    def options(r, c):
        used = set(g[r]) | {g[i][c] for i in range(4)}
        br, bc = r // 2 * 2, c // 2 * 2
        used |= {g[i][j] for i in range(br, br + 2) for j in range(bc, bc + 2)}
        return [v for v in range(1, 5) if v not in used]

    def go():
        best = None
        for r in range(4):
            for c in range(4):
                if g[r][c] == 0:
                    opts = options(r, c)
                    if best is None or len(opts) < len(best[2]):
                        best = (r, c, opts)
        if best is None:
            return True
        r, c, opts = best
        for v in opts:
            g[r][c] = v
            if go():
                return True
            g[r][c] = 0
        return False

    go()
    return g


puzzle = [[1, 0, 0, 0], [0, 0, 3, 0], [0, 4, 0, 0], [0, 0, 0, 2]]
solved = solve_mini(puzzle)
assert solved == [[1, 3, 2, 4], [4, 2, 3, 1], [2, 4, 1, 3], [3, 1, 4, 2]]
assert all(sorted(row) == [1, 2, 3, 4] for row in solved)
assert all(sorted(solved[r][c] for r in range(4)) == [1, 2, 3, 4] for c in range(4))
```

```cpp
vector<int> mini_options(const vector<vector<int>>& g, int r, int c) {
    bool used[5] = {false, false, false, false, false};
    for (int i = 0; i < 4; i++) {
        used[g[r][i]] = true;
        used[g[i][c]] = true;
    }
    int br = r / 2 * 2, bc = c / 2 * 2;
    for (int i = br; i < br + 2; i++) {
        for (int j = bc; j < bc + 2; j++) used[g[i][j]] = true;
    }
    vector<int> opts;
    for (int v = 1; v <= 4; v++) {
        if (!used[v]) opts.push_back(v);
    }
    return opts;
}

bool solve_mini_go(vector<vector<int>>& g) {
    int bestR = -1, bestC = -1;
    vector<int> best;
    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < 4; c++) {
            if (g[r][c] == 0) {
                vector<int> opts = mini_options(g, r, c);
                if (bestR == -1 || opts.size() < best.size()) {
                    bestR = r;
                    bestC = c;
                    best = opts;
                }
            }
        }
    }
    if (bestR == -1) return true;
    for (int v : best) {
        g[bestR][bestC] = v;
        if (solve_mini_go(g)) return true;
        g[bestR][bestC] = 0;
    }
    return false;
}

vector<vector<int>> solve_mini(vector<vector<int>> grid) {
    solve_mini_go(grid);
    return grid;
}
```

(The digit 0 for an empty cell also gets marked as "used" in the arrays, which is harmless because we only read digits 1 to 4.) The full $9 \times 9$ puzzle is the same program with 9 digits and $3 \times 3$ boxes: the box number of cell $(r, c)$ is `r // 3 * 3 + c // 3`. For speed one keeps a set of used digits for each row, column and box, adds to them when placing a digit and removes from them when undoing, instead of scanning the grid every time. This is exactly the problem _Sudoku Solver_.

Backtracking on $m$ empty cells could try $9^m$ fillings in the worst case, but the "fewest candidates first" rule makes real puzzles take a tiny fraction of that. The space is constant for a fixed $9 \times 9$ grid, since the recursion is at most 81 levels deep.

## 11.5 The whole method in one place

Every problem in this chapter and the last two follows one recipe. Decide what a single step chooses (a column, a colour, a digit, a direction). Write the rule that says whether a choice is allowed, and check it **before** choosing, so that bad branches die early. Choose, explore, undo, restoring every piece of state that you changed. Record or return when the path is complete.

To make a search faster, never explore a branch that is already doomed (stop early), look at the most constrained decision first (as in Sudoku), and make the rule check cheap (sets or bits instead of scanning). Finally, if the same sub-state keeps coming back and only a number or a yes/no is needed, use the notebook of Chapter 6 instead.

## 11.6 Check yourself

1. In N-Queens, how do we recognise two squares on the same diagonal using `r` and `c`?
2. In the bit version, what does `free & -free` give?
3. In graph colouring, what is the undo step, and when is it reached?
4. In Sudoku, why is it a good idea to fill the cell with the fewest candidates first?
