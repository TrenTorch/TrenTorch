> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Dynamic programming)

This course teaches dynamic programming, often shortened to DP, from the very first idea to some of the tricks used in contests. It assumes only that you can write a loop and a simple function. Nothing else is needed.

The course is a staircase. **Chapter 1 is deliberately gentle**: one small problem, one simple idea, no heavy math. Each chapter after it adds one new family of problems, and the math grows slowly. By the last chapters you will know how to speed up a slow DP and how to test your own solutions. If a later chapter looks hard, do not worry. Every chapter only uses what came before.

Every code example is shown in Python and in C++, so pick whichever language you like.

# Chapter 1. What dynamic programming is

## 1.1 A recursion that is far too slow

Let's start with a simple sequence: Fibonacci numbers. The rule is easy: the first two numbers are 0 and 1, and every number after that is the sum of the two before it. So 0, 1, 1, 2, 3, 5, 8, 13, and so on. In math notation:

$$f(0) = 0,\quad f(1) = 1,\quad f(n) = f(n-1) + f(n-2)\text{ for }n \ge 2$$

If we write this directly as a recursive function, a function that calls itself, it looks clean and short.

```python
def fib_recursive(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib_recursive(n - 1) + fib_recursive(n - 2)


assert fib_recursive(0) == 0
assert fib_recursive(1) == 1
assert fib_recursive(6) == 8
```

```cpp
int fib_recursive(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    return fib_recursive(n - 1) + fib_recursive(n - 2);
}
```

But this clean code hides a problem. To compute `fib_recursive(5)`, the function calls itself for 4 and 3. The call for 4 then calls 3 and 2. The call for 3 calls 2 and 1. Notice that `fib_recursive(3)` and `fib_recursive(2)` are computed multiple times. As `n` grows, the same subproblems, a **subproblem** is a smaller instance of the same question, are solved again and again. The call tree doubles in size roughly every step, so the running time is about $O(2^n)$. For `n = 29` the program makes over one million calls. For `n = 50` it would take hours.

## 1.2 Memoization (top-down)

The fix is simple: remember every answer the first time we compute it. This technique is called **memoization**, like writing notes on a memo pad so you don't redo work. We keep a table (an array or dictionary) where `memo[k]` stores `f(k)` once it is known. When the function is called, it checks the table first. If the value is there, it returns immediately. Otherwise it computes, saves, and returns.

```python
def fib_memo(n: int, memo: dict[int, int] | None = None) -> int:
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n == 0:
        return 0
    if n == 1:
        return 1
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


assert fib_memo(0) == 0
assert fib_memo(1) == 1
assert fib_memo(6) == 8
assert fib_memo(10) == 55
```

```cpp
int fib_memo(int n, unordered_map<int, int>& memo) {
    if (memo.count(n)) return memo[n];
    if (n == 0) return 0;
    if (n == 1) return 1;
    return memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo);
}
```

Now each value from 0 up to `n` is computed exactly once. The work per subproblem is $O(1)$, and there are $n+1$ subproblems, so total time is $O(n)$. Space is also $O(n)$ for the table plus the recursion call stack. This style, starting from the target and recursing down to base cases, is called **top-down dynamic programming**.

## 1.3 Tables (bottom-up)

We can also fill the table in the opposite direction: start from the base cases and build up step by step to the answer we want. This is **bottom-up dynamic programming**. For Fibonacci we only need the two previous numbers, so we can even throw away older values and keep just two variables.

```python
def fib_bottom_up(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


assert fib_bottom_up(0) == 0
assert fib_bottom_up(1) == 1
assert fib_bottom_up(6) == 8
assert fib_bottom_up(10) == 55
```

```cpp
int fib_bottom_up(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    int a = 0, b = 1;
    for (int i = 2; i <= n; ++i) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}
```

Time is still $O(n)$, but space drops to $O(1)$ because we only store the last two numbers. Both top-down and bottom-up are dynamic programming; they just fill the table in different orders.

## 1.4 Three questions for every DP

When you see a new problem, ask these three questions to find the dynamic programming structure:

1. **What is the state?** A state is a compact description of a subproblem. For Fibonacci the state is just the integer `n`. For a problem on a string it might be an index `i`; for a grid it might be a cell `(i, j)`. The set of all states must be finite and each state must correspond to a well-defined answer.
2. **What is the transition?** The transition tells how to compute the answer for one state using answers of smaller states. For Fibonacci the transition is `f(n) = f(n-1) + f(n-2)`. A transition is simply a formula or rule that connects states.
3. **Where do we start?** These are the base cases, states whose answers are known without recursion. For Fibonacci the base cases are `f(0) = 0` and `f(1) = 1`.

If you can answer these three questions clearly, you have a dynamic programming solution. The rest is just filling the table (bottom-up) or writing the memoized recursion (top-down).

## 1.5 Climbing stairs

This is exactly the problem **Climbing Stairs**. You stand at step 0 and want to reach step `n`. Each move you may climb 1 or 2 steps. How many distinct ways can you reach the top? Let `ways[i]` be the number of ways to reach step `i`. From step `i-1` you can take a single step; from step `i-2` you can take a double step. So `ways[i] = ways[i-1] + ways[i-2]`. The base cases: `ways[0] = 1` (one way to stay at the ground), `ways[1] = 1` (only a single step). This is the Fibonacci recurrence shifted by one.

Let's trace `n = 4` by hand:

- `ways[0] = 1`
- `ways[1] = 1`
- `ways[2] = 1 + 1 = 2`
- `ways[3] = 2 + 1 = 3`
- `ways[4] = 3 + 2 = 5`

The five sequences for `n=4` are: (1,1,1,1), (1,1,2), (1,2,1), (2,1,1), (2,2).

```python
def climb_stairs(n: int) -> int:
    if n <= 1:
        return 1
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


assert climb_stairs(1) == 1
assert climb_stairs(2) == 2
assert climb_stairs(4) == 5
```

```cpp
int climb_stairs(int n) {
    if (n <= 1) return 1;
    int a = 1, b = 1;
    for (int i = 2; i <= n; ++i) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}
```

Time $O(n)$, space $O(1)$.

Now a twist: **Min Cost Climbing Stairs**. Each step `i` has a non-negative cost `cost[i]`. You start at step 0 or step 1 (your choice) and want to reach the floor just past the last step (step `n`). When you land on a step you pay its cost. Find the minimum total cost. Let `dp[i]` be the minimum cost to reach step `i`. The transition: to stand on step `i` you must have come from `i-1` or `i-2`, so `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`. Base cases: `dp[0] = cost[0]`, `dp[1] = cost[1]`. The answer is `min(dp[n-1], dp[n-2])` because you can finish from either of the last two steps.

Example: `cost = [10, 15, 20]`.

- `dp[0] = 10`
- `dp[1] = 15`
- `dp[2] = 20 + min(15, 10) = 30`
  Answer `min(15, 30) = 15` (start at step 1, jump two steps to the floor).

```python
def min_cost_climbing_stairs(cost: list[int]) -> int:
    n = len(cost)
    if n == 2:
        return min(cost[0], cost[1])
    dp0, dp1 = cost[0], cost[1]
    for i in range(2, n):
        dp0, dp1 = dp1, cost[i] + min(dp0, dp1)
    return min(dp0, dp1)


assert min_cost_climbing_stairs([10, 15, 20]) == 15
assert min_cost_climbing_stairs([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]) == 6
```

```cpp
int min_cost_climbing_stairs(vector<int>& cost) {
    int n = cost.size();
    if (n == 2) return min(cost[0], cost[1]);
    int dp0 = cost[0], dp1 = cost[1];
    for (int i = 2; i < n; ++i) {
        int dpi = cost[i] + min(dp0, dp1);
        dp0 = dp1;
        dp1 = dpi;
    }
    return min(dp0, dp1);
}
```

Time $O(n)$, space $O(1)$. Notice how the same three questions guided us: state is the step index, transition picks the cheaper previous step, base cases are the first two steps.

## 1.6 Check yourself

1. Why does the plain recursive Fibonacci function repeat work, and roughly how many calls does it make for input `n`?
2. What is the difference between top-down and bottom-up dynamic programming in terms of the order subproblems are solved?
3. For the climbing stairs problem, what are the state, the transition, and the base cases?
4. In min cost climbing stairs, why is the final answer `min(dp[n-1], dp[n-2])` instead of `dp[n]`?

# Chapter 2. Counting and choosing along a line

## 2.1 House robber

Imagine a row of houses, each with some cash inside. You want to take as much money as possible, but you cannot rob two houses that sit next to each other; the alarm would go off. This is exactly the problem _House Robber_.

Let's think about the last house in the row. You have two choices: rob it, or skip it. If you rob it, you cannot rob the previous house, so the best you can do is the money in this house plus the best amount from all houses before the previous one. If you skip it, the best amount is simply whatever you could get from all houses before this one.

We can write this idea as a recurrence. Let `best[i]` be the maximum money you can collect from the first `i` houses (using 1-based indexing for the houses, so house 1 is the first). Then:

$$
\text{best}[i] = \max(\text{best}[i-1],\; \text{money}[i] + \text{best}[i-2])
$$

The base cases are `best[0] = 0` (no houses, no money) and `best[1] = money[1]` (only the first house). We fill the table from left to right. This bottom-up approach visits each house once, so the time cost is $O(n)$ and the space cost is $O(n)$, where $n$ is the number of houses. We can even reduce space to $O(1)$ by keeping only the last two values.

Let's trace a tiny example by hand: `money = [3, 2, 7, 10]`.

- `best[0] = 0`
- `best[1] = 3`
- `best[2] = max(best[1], money[2] + best[0]) = max(3, 2 + 0) = 3`
- `best[3] = max(best[2], money[3] + best[1]) = max(3, 7 + 3) = 10`
- `best[4] = max(best[3], money[4] + best[2]) = max(10, 10 + 3) = 13`

The answer is 13 (rob houses 1 and 4).

```python
def house_robber(money: list[int]) -> int:
    """Return the maximum amount that can be robbed without adjacent houses."""
    n = len(money)
    if n == 0:
        return 0
    if n == 1:
        return money[0]
    # dp[i] = best for first i houses (1-based)
    dp = [0] * (n + 1)
    dp[1] = money[0]
    for i in range(2, n + 1):
        dp[i] = max(dp[i - 1], money[i - 1] + dp[i - 2])
    return dp[n]

# Quick checks
assert house_robber([3, 2, 7, 10]) == 13
assert house_robber([3, 2, 5, 10, 7]) == 15  # 3 + 5 + 7
assert house_robber([]) == 0
assert house_robber([5]) == 5
```

```cpp
int houseRobber(const vector<int>& money) {
    int n = money.size();
    if (n == 0) return 0;
    if (n == 1) return money[0];
    vector<int> dp(n + 1);
    dp[1] = money[0];
    for (int i = 2; i <= n; ++i) {
        dp[i] = max(dp[i - 1], money[i - 1] + dp[i - 2]);
    }
    return dp[n];
}
```

## 2.2 House robber on a circle

Now suppose the houses form a circle; the first and last houses are also neighbors. This is exactly the problem _House Robber II_. You cannot simply run the same linear algorithm because the first and last houses are now adjacent.

The trick is to break the circle into two linear cases: either you rob the first house (and therefore cannot rob the last), or you skip the first house (and the last house is free to choose). Compute the best for each case using the linear algorithm from before, then take the larger of the two.

If there is only one house, the answer is just that house's money. For two houses, the answer is the maximum of the two. For three or more, we run the linear solver on `money[0..n-2]` (exclude last) and on `money[1..n-1]` (exclude first). The time cost is still $O(n)$ and space is $O(n)$ (or $O(1)$ with the optimized version).

Example: `money = [2, 3, 2]`. Case A (rob first, exclude last): houses `[2, 3]` → best is 3. Case B (exclude first): houses `[3, 2]` → best is 3. Answer is 3.

```python
def house_robber_linear(money: list[int]) -> int:
    """Helper for the linear version (same as before)."""
    n = len(money)
    if n == 0:
        return 0
    if n == 1:
        return money[0]
    dp = [0] * (n + 1)
    dp[1] = money[0]
    for i in range(2, n + 1):
        dp[i] = max(dp[i - 1], money[i - 1] + dp[i - 2])
    return dp[n]

def house_robber_ii(money: list[int]) -> int:
    """Circular version: first and last are adjacent."""
    n = len(money)
    if n == 0:
        return 0
    if n == 1:
        return money[0]
    if n == 2:
        return max(money[0], money[1])
    # Case 1: rob first, skip last
    case1 = house_robber_linear(money[:-1])
    # Case 2: skip first, last is available
    case2 = house_robber_linear(money[1:])
    return max(case1, case2)

assert house_robber_ii([2, 3, 2]) == 3
assert house_robber_ii([1, 2, 3, 1]) == 4  # 1 + 3
assert house_robber_ii([1, 2, 3]) == 3
assert house_robber_ii([5]) == 5
```

```cpp
int houseRobberLinear(const vector<int>& money) {
    int n = money.size();
    if (n == 0) return 0;
    if (n == 1) return money[0];
    vector<int> dp(n + 1);
    dp[1] = money[0];
    for (int i = 2; i <= n; ++i) {
        dp[i] = max(dp[i - 1], money[i - 1] + dp[i - 2]);
    }
    return dp[n];
}

int houseRobberII(const vector<int>& money) {
    int n = money.size();
    if (n == 0) return 0;
    if (n == 1) return money[0];
    if (n == 2) return max(money[0], money[1]);
    vector<int> first(money.begin(), money.end() - 1);
    vector<int> second(money.begin() + 1, money.end());
    return max(houseRobberLinear(first), houseRobberLinear(second));
}
```

## 2.3 Decode ways

A message containing digits can be decoded into letters where `'1' -> 'A'`, `'2' -> 'B'`, ..., `'26' -> 'Z'`. Given a string of digits, count how many ways it can be decoded. This is exactly the problem _Decode Ways_.

Let `ways[i]` be the number of decodings for the prefix of length `i` (first `i` characters). Look at the last one or two digits of that prefix. If the last digit is not `'0'`, it can stand alone as a letter, so we add `ways[i-1]`. If the last two digits form a number between 10 and 26 inclusive, they can be decoded together as one letter, so we add `ways[i-2]`. Base case: `ways[0] = 1` (empty string has one decoding, do nothing).

Example: `s = "12"`. `ways[0] = 1`. `ways[1]`: last digit `'2'` is valid → `ways[0] = 1`. `ways[2]`: last digit `'2'` valid → add `ways[1] = 1`; last two digits `"12"` valid → add `ways[0] = 1`. Total `ways[2] = 2` (decodings: "AB" and "L").

Time cost is $O(n)$, space is $O(n)$ (reducible to $O(1)$).

```python
def num_decodings(s: str) -> int:
    """Return the number of ways to decode the digit string s."""
    n = len(s)
    if n == 0:
        return 0
    dp = [0] * (n + 1)
    dp[0] = 1
    # first character
    dp[1] = 0 if s[0] == '0' else 1
    for i in range(2, n + 1):
        # single digit
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
        # two digits
        two = int(s[i - 2:i])
        if 10 <= two <= 26:
            dp[i] += dp[i - 2]
    return dp[n]

assert num_decodings("12") == 2
assert num_decodings("226") == 3  # BBF, BZ, VF
assert num_decodings("06") == 0
assert num_decodings("10") == 1
assert num_decodings("") == 0
```

```cpp
int numDecodings(const string& s) {
    int n = s.size();
    if (n == 0) return 0;
    vector<int> dp(n + 1);
    dp[0] = 1;
    dp[1] = (s[0] == '0') ? 0 : 1;
    for (int i = 2; i <= n; ++i) {
        if (s[i - 1] != '0') dp[i] += dp[i - 1];
        int two = (s[i - 2] - '0') * 10 + (s[i - 1] - '0');
        if (10 <= two && two <= 26) dp[i] += dp[i - 2];
    }
    return dp[n];
}
```

## 2.4 Coin change

You have coins of different denominations and want to make a target amount. Two classic questions: what is the _fewest_ coins needed (problem _Coin Change_), and how many _different combinations_ of coins make the amount (problem _Coin Change II_). The loop order in the inner loop changes the meaning of the answer.

### Fewest coins

Let `dp[x]` be the minimum coins to make amount `x`. Initialize `dp[0] = 0` and all others to a large number (infinity). For each coin `c`, we try to improve every amount `x` from `c` up to `target`: `dp[x] = min(dp[x], dp[x - c] + 1)`. The outer loop goes over coins, the inner loop goes over amounts **increasing**. This allows using the same coin many times. At the end, if `dp[target]` is still infinity, the amount cannot be made.

Example: `coins = [1, 3, 4]`, `target = 6`. Table after all coins:

- `dp[0]=0`
- `dp[1]=1` (1)
- `dp[2]=2` (1+1)
- `dp[3]=1` (3)
- `dp[4]=1` (4)
- `dp[5]=2` (4+1)
- `dp[6]=2` (3+3)

Time cost is $O(n \cdot \text{target})$, space is $O(\text{target})$.

### Number of combinations (order of coins does not matter)

Now let `ways[x]` be the number of combinations to make amount `x`. Initialize `ways[0] = 1`. For each coin `c`, for `x` from `c` to `target`: `ways[x] += ways[x - c]`. The outer loop over coins and inner loop **increasing** over amounts ensures each combination is counted once regardless of coin order. If we swapped the loops (amounts outer, coins inner), we would count permutations instead of combinations.

Example: `coins = [1, 2]`, `target = 3`. Combinations: `1+1+1`, `1+2` → 2 ways. With loops swapped we would get `1+1+1`, `1+2`, `2+1` → 3 ways.

```python
def coin_change_min(coins: list[int], target: int) -> int:
    """Fewest coins to make target, or -1 if impossible."""
    INF = target + 1
    dp = [INF] * (target + 1)
    dp[0] = 0
    for c in coins:
        for x in range(c, target + 1):
            dp[x] = min(dp[x], dp[x - c] + 1)
    return -1 if dp[target] == INF else dp[target]

def coin_change_ways(coins: list[int], target: int) -> int:
    """Number of combinations to make target (order of coins ignored)."""
    dp = [0] * (target + 1)
    dp[0] = 1
    for c in coins:
        for x in range(c, target + 1):
            dp[x] += dp[x - c]
    return dp[target]

assert coin_change_min([1, 3, 4], 6) == 2
assert coin_change_min([2], 3) == -1
assert coin_change_ways([1, 2], 3) == 2
assert coin_change_ways([2, 5], 3) == 0
```

```cpp
int coinChangeMin(const vector<int>& coins, int target) {
    const int INF = target + 1;
    vector<int> dp(target + 1, INF);
    dp[0] = 0;
    for (int c : coins) {
        for (int x = c; x <= target; ++x) {
            dp[x] = min(dp[x], dp[x - c] + 1);
        }
    }
    return dp[target] == INF ? -1 : dp[target];
}

int coinChangeWays(const vector<int>& coins, int target) {
    vector<int> dp(target + 1);
    dp[0] = 1;
    for (int c : coins) {
        for (int x = c; x <= target; ++x) {
            dp[x] += dp[x - c];
        }
    }
    return dp[target];
}
```

## 2.5 Perfect squares and word break

Some problems ask whether a thing can be split into valid pieces, or what is the minimum number of pieces. The idea is the same: try every possible last piece.

### Perfect squares

Given an integer `n`, find the least number of perfect square numbers (1, 4, 9, 16, ...) that sum to `n`. This is exactly the problem _Perfect Squares_. Let `dp[x]` be the minimum squares for `x`. For each `x` from 1 to `n`, try every square `s = k*k <= x` and take `dp[x] = min(dp[x], dp[x - s] + 1)`. Base `dp[0] = 0`.

Example: `n = 12`. Squares ≤ 12: 1, 4, 9.

- `dp[1]=1`, `dp[2]=2`, `dp[3]=3`, `dp[4]=1`, `dp[5]=2`, `dp[6]=3`, `dp[7]=4`, `dp[8]=2` (4+4), `dp[9]=1`, `dp[10]=2` (9+1), `dp[11]=3`, `dp[12]=3` (4+4+4).

Time cost is $O(n \sqrt{n})$, space is $O(n)$.

### Word break

Given a string `s` and a list of words `dict`, decide if `s` can be segmented into a sequence of dictionary words. This is exactly the problem _Word Break_. Let `can[i]` be true if the prefix of length `i` can be segmented. `can[0] = true`. For each `i` from 1 to `n`, check every `j < i`: if `can[j]` is true and `s[j:i]` is in the dictionary, set `can[i] = true`.

Example: `s = "leetcode"`, `dict = ["leet", "code"]`.

- `can[0]=true`
- `i=4`: `j=0`, `can[0]=true`, `s[0:4]="leet"` in dict → `can[4]=true`
- `i=8`: `j=4`, `can[4]=true`, `s[4:8]="code"` in dict → `can[8]=true`

Time cost is $O(n^2)$ for the nested loops (substring lookup is $O(1)$ with a hash set), space is $O(n)$.

```python
def num_squares(n: int) -> int:
    """Least number of perfect squares that sum to n."""
    dp = [n] * (n + 1)  # worst case: n = 1+1+...
    dp[0] = 0
    for x in range(1, n + 1):
        k = 1
        while k * k <= x:
            s = k * k
            dp[x] = min(dp[x], dp[x - s] + 1)
            k += 1
    return dp[n]

def word_break(s: str, word_dict: list[str]) -> bool:
    """Return True if s can be segmented into words from word_dict."""
    word_set = set(word_dict)
    n = len(s)
    can = [False] * (n + 1)
    can[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if can[j] and s[j:i] in word_set:
                can[i] = True
                break
    return can[n]

assert num_squares(12) == 3
assert num_squares(13) == 2  # 9 + 4
assert word_break("leetcode", ["leet", "code"]) == True
assert word_break("applepenapple", ["apple", "pen"]) == True
assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False
```

```cpp
int numSquares(int n) {
    vector<int> dp(n + 1, n);
    dp[0] = 0;
    for (int x = 1; x <= n; ++x) {
        for (int k = 1; k * k <= x; ++k) {
            dp[x] = min(dp[x], dp[x - k * k] + 1);
        }
    }
    return dp[n];
}

bool wordBreak(const string& s, const vector<string>& wordDict) {
    unordered_set<string> dict(wordDict.begin(), wordDict.end());
    int n = s.size();
    vector<bool> can(n + 1);
    can[0] = true;
    for (int i = 1; i <= n; ++i) {
        for (int j = 0; j < i; ++j) {
            if (can[j] && dict.count(s.substr(j, i - j))) {
                can[i] = true;
                break;
            }
        }
    }
    return can[n];
}
```

## 2.6 Dice roll sum

You have `d` dice, each with `f` faces numbered 1 to `f`. How many ways can the dice sum to a target `t`? This is exactly the problem _Dice Roll Sum_.

Let `dp[i][s]` be the number of ways to get sum `s` using the first `i` dice. Base: `dp[0][0] = 1`. For each die `i` from 1 to `d`, for each possible sum `s` from `i` to `i*f`, we add the ways from the previous die with each face value: `dp[i][s] = sum(dp[i-1][s - face] for face in 1..f if s - face >= 0)`.

We can compress this to a 1D array by iterating sums **backwards** (from high to low) for each die, or we can keep a 2D table for clarity. The 2D version uses $O(d \cdot t)$ time and space. The 1D version uses $O(t)$ space.

Example: `d = 2`, `f = 6`, `t = 7`. Ways: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) → 6 ways.

```python
def dice_roll_sum(d: int, f: int, target: int) -> int:
    """Number of ways to roll d f-faced dice to get sum target."""
    dp = [0] * (target + 1)
    dp[0] = 1
    for _ in range(d):
        new_dp = [0] * (target + 1)
        for s in range(1, target + 1):
            for face in range(1, f + 1):
                if s - face >= 0:
                    new_dp[s] += dp[s - face]
        dp = new_dp
    return dp[target]

assert dice_roll_sum(2, 6, 7) == 6
assert dice_roll_sum(1, 6, 3) == 1
assert dice_roll_sum(2, 6, 12) == 1  # 6+6
assert dice_roll_sum(3, 6, 7) == 15
```

```cpp
int diceRollSum(int d, int f, int target) {
    vector<int> dp(target + 1);
    dp[0] = 1;
    for (int i = 0; i < d; ++i) {
        vector<int> ndp(target + 1);
        for (int s = 1; s <= target; ++s) {
            for (int face = 1; face <= f; ++face) {
                if (s - face >= 0) ndp[s] += dp[s - face];
            }
        }
        dp.swap(ndp);
    }
    return dp[target];
}
```

## 2.7 Check yourself

1. In the house robber recurrence, why do we use `best[i-2]` when we choose to rob house `i`?
2. For coin change (fewest coins), what happens if the inner loop goes over amounts in decreasing order instead of increasing?
3. In word break, why do we check `can[j]` before looking up `s[j:i]` in the dictionary?
4. For dice roll sum with 2 dice and 6 faces, how many ways are there to get a sum of 2, and how many for a sum of 7?

# Chapter 3. Dynamic programming on grids

## 3.1 Counting paths in a grid

Imagine a robot sitting in the top-left corner of a rectangular board. The robot can only move right or down, one cell at a time. We want to know how many different ways the robot can reach the bottom-right corner. This is exactly the problem _Unique Paths_.

Let the board have $m$ rows and $n$ columns. Number the rows $0$ to $m-1$ from top to bottom, and columns $0$ to $n-1$ from left to right. The robot starts at $(0,0)$ and must finish at $(m-1,n-1)$.

If we write the number of ways to reach each cell in a table, a simple pattern appears. The first row and the first column can only be reached in one way: by moving straight right or straight down. For any other cell $(i,j)$, the robot must have come from the cell above $(i-1,j)$ or from the cell to the left $(i,j-1)$. So the number of ways to reach $(i,j)$ is the sum of the ways to reach those two neighbours.

Let us work through a $3 \times 3$ board by hand. The table of ways looks like this:

|     | 0   | 1   | 2   |
| --- | --- | --- | --- |
| 0   | 1   | 1   | 1   |
| 1   | 1   | 2   | 3   |
| 2   | 1   | 3   | 6   |

The answer is $6$. Notice how we filled the table row by row, left to right. We always used values that were already computed. This order works because every cell depends only on its top and left neighbours, which live in earlier rows or earlier columns.

The algorithm runs in $O(mn)$ time and uses $O(mn)$ space if we keep the whole table. We can reduce space to $O(n)$ by keeping only the current row, because each new cell only needs the value to its left (already in the current row) and the value above (stored in the same column from the previous row).

```python
def unique_paths(m: int, n: int) -> int:
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    return dp[-1]

assert unique_paths(3, 3) == 6
assert unique_paths(2, 2) == 2
```

```cpp
int uniquePaths(int m, int n) {
    vector<int> dp(n, 1);
    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j) {
            dp[j] += dp[j - 1];
        }
    }
    return dp[n - 1];
}
```

## 3.2 Blocked cells and cheapest paths

Now suppose some cells are blocked and the robot cannot step on them. This is the problem _Unique Paths with Obstacles_. We use the same table idea, but a blocked cell gets a value of $0$ ways. The start cell is $1$ if it is free, otherwise $0$. Every other free cell adds the ways from top and left, treating blocked neighbours as $0$.

Next, imagine each cell has a cost (a non-negative number) and we want the cheapest total cost from start to finish. This is _Minimum Path Sum_. The recurrence changes from counting to minimizing: the cheapest cost to reach $(i,j)$ is the cell's own cost plus the smaller of the cheapest costs to reach $(i-1,j)$ and $(i,j-1)$. The first row and first column are just cumulative sums because there is only one way to reach them.

Let us trace a tiny $2 \times 3$ grid with costs:

```
1 2 3
4 5 6
```

The table of minimum costs:

|     | 0   | 1   | 2   |
| --- | --- | --- | --- |
| 0   | 1   | 3   | 6   |
| 1   | 5   | 8   | 12  |

The answer is $12$. We fill the table in the same top-left to bottom-right order. Time $O(mn)$, space $O(n)$ with a rolling row.

```python
def min_path_sum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [float('inf')] * n
    dp[0] = grid[0][0]
    for j in range(1, n):
        dp[j] = dp[j - 1] + grid[0][j]
    for i in range(1, m):
        dp[0] += grid[i][0]
        for j in range(1, n):
            dp[j] = grid[i][j] + min(dp[j], dp[j - 1])
    return dp[-1]

assert min_path_sum([[1,2,3],[4,5,6]]) == 12
assert min_path_sum([[1]]) == 1
```

```cpp
int minPathSum(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    vector<int> dp(n, INT_MAX);
    dp[0] = grid[0][0];
    for (int j = 1; j < n; ++j) dp[j] = dp[j - 1] + grid[0][j];
    for (int i = 1; i < m; ++i) {
        dp[0] += grid[i][0];
        for (int j = 1; j < n; ++j) {
            dp[j] = grid[i][j] + min(dp[j], dp[j - 1]);
        }
    }
    return dp[n - 1];
}
```

For _Unique Paths with Obstacles_ we only need to zero out blocked cells:

```python
def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = 1 if grid[0][0] == 0 else 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]
    return dp[-1]

assert unique_paths_with_obstacles([[0,0,0],[0,1,0],[0,0,0]]) == 2
assert unique_paths_with_obstacles([[1]]) == 0
```

```cpp
int uniquePathsWithObstacles(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    vector<int> dp(n, 0);
    dp[0] = grid[0][0] == 0 ? 1 : 0;
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (grid[i][j] == 1) dp[j] = 0;
            else if (j > 0) dp[j] += dp[j - 1];
        }
    }
    return dp[n - 1];
}
```

## 3.3 Triangles and falling paths

A triangle of numbers looks like this:

```
   2
  3 4
 6 5 7
4 1 8 3
```

We start at the top and move down to adjacent numbers on the next row. The goal is to find the path with the smallest sum. This is _Triangle Minimum Path_. The triangle has $n$ rows. Row $i$ has $i+1$ numbers, indexed $0$ to $i$. From position $(i,j)$ we can go to $(i+1,j)$ or $(i+1,j+1)$.

It is natural to fill a DP table from the bottom up. The bottom row's best sums are just the numbers themselves. For each cell above, its best sum is its own value plus the smaller of the two cells directly below it. Working upward, the top cell finally holds the answer.

Let us compute the example by hand. Bottom row: $4, 1, 8, 3$. Row above: $6+\min(4,1)=7$, $5+\min(1,8)=6$, $7+\min(8,3)=10$. Next: $3+\min(7,6)=9$, $4+\min(6,10)=10$. Top: $2+\min(9,10)=11$. The answer is $11$.

We can do this in place on a copy of the last row, updating from left to right: the new value at position $j$ needs the old values at positions $j$ and $j+1$, and position $j+1$ has not been changed yet. Time $O(n^2)$, space $O(n)$.

```python
def minimum_total(triangle: list[list[int]]) -> int:
    dp = triangle[-1][:]
    for i in range(len(triangle) - 2, -1, -1):
        for j in range(i + 1):
            dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])
    return dp[0]

assert minimum_total([[2],[3,4],[6,5,7],[4,1,8,3]]) == 11
assert minimum_total([[-10]]) == -10
```

```cpp
int minimumTotal(vector<vector<int>>& triangle) {
    int n = triangle.size();
    vector<int> dp = triangle.back();
    for (int i = n - 2; i >= 0; --i) {
        for (int j = 0; j <= i; ++j) {
            dp[j] = triangle[i][j] + min(dp[j], dp[j + 1]);
        }
    }
    return dp[0];
}
```

A close cousin is _Minimum Falling Path Sum_. Here we have a square $n \times n$ matrix. We start at any cell in the top row and move down to the next row, choosing the same column or one step left or right. We want the smallest sum reaching the bottom row. The recurrence is similar: $dp[i][j] = grid[i][j] + \min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1])$ with boundary checks. We fill top to bottom. Time $O(n^2)$, space $O(n)$ with two rows.

```python
def min_falling_path_sum(grid: list[list[int]]) -> int:
    n = len(grid)
    prev = grid[0][:]
    for i in range(1, n):
        cur = [0] * n
        for j in range(n):
            best = prev[j]
            if j > 0: best = min(best, prev[j - 1])
            if j + 1 < n: best = min(best, prev[j + 1])
            cur[j] = grid[i][j] + best
        prev = cur
    return min(prev)

assert min_falling_path_sum([[2,1,3],[6,5,4],[7,8,9]]) == 13
assert min_falling_path_sum([[-19,57],[-40,-5]]) == -59
```

```cpp
int minFallingPathSum(vector<vector<int>>& grid) {
    int n = grid.size();
    vector<int> prev = grid[0];
    for (int i = 1; i < n; ++i) {
        vector<int> cur(n);
        for (int j = 0; j < n; ++j) {
            int best = prev[j];
            if (j > 0) best = min(best, prev[j - 1]);
            if (j + 1 < n) best = min(best, prev[j + 1]);
            cur[j] = grid[i][j] + best;
        }
        prev = move(cur);
    }
    return *min_element(prev.begin(), prev.end());
}
```

## 3.4 Squares inside a grid

Two problems ask about squares made of $1$s in a binary matrix. _Maximal Square_ wants the area of the largest all-$1$ square. _Count Square Submatrices_ wants the total number of square submatrices that are all $1$s.

Let $dp[i][j]$ be the side length of the largest all-$1$ square whose bottom-right corner is at $(i,j)$. If $grid[i][j] = 0$, then $dp[i][j] = 0$. Otherwise, the square can extend only as far as the smallest of its three neighbours: top, left, and top-left. So $dp[i][j] = 1 + \min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])$.

Why does this work? A square of side $k$ ending at $(i,j)$ needs a square of side $k-1$ ending at each of those three neighbours. The smallest neighbour limits how large we can go.

For a $3 \times 3$ all-$1$ matrix, the $dp$ table becomes:

|     | 0   | 1   | 2   |
| --- | --- | --- | --- |
| 0   | 1   | 1   | 1   |
| 1   | 1   | 2   | 2   |
| 2   | 1   | 2   | 3   |

The maximal square has side $3$, area $9$. The sum of all entries is $1+1+1+1+2+2+1+2+3 = 14$, which is exactly the count of all square submatrices (each cell contributes the number of squares ending there).

We can compute row by row with a single array of length $n$, keeping the previous row's values in a variable for the top-left neighbour. Time $O(mn)$, space $O(n)$.

```python
def maximal_square(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [0] * (n + 1)
    max_side = 0
    prev = 0
    for i in range(m):
        for j in range(n):
            temp = dp[j + 1]
            if grid[i][j] == 1:
                dp[j + 1] = 1 + min(dp[j], dp[j + 1], prev)
                max_side = max(max_side, dp[j + 1])
            else:
                dp[j + 1] = 0
            prev = temp
        prev = 0
    return max_side * max_side

def count_squares(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [0] * (n + 1)
    total = 0
    prev = 0
    for i in range(m):
        for j in range(n):
            temp = dp[j + 1]
            if grid[i][j] == 1:
                dp[j + 1] = 1 + min(dp[j], dp[j + 1], prev)
                total += dp[j + 1]
            else:
                dp[j + 1] = 0
            prev = temp
        prev = 0
    return total

assert maximal_square([[1,1,1],[1,1,1],[1,1,1]]) == 9
assert count_squares([[1,1,1],[1,1,1],[1,1,1]]) == 14
assert maximal_square([[0]]) == 0
```

```cpp
int maximalSquare(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    vector<int> dp(n + 1, 0);
    int maxSide = 0, prev = 0;
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            int temp = dp[j + 1];
            if (grid[i][j] == 1) {
                dp[j + 1] = 1 + min({dp[j], dp[j + 1], prev});
                maxSide = max(maxSide, dp[j + 1]);
            } else {
                dp[j + 1] = 0;
            }
            prev = temp;
        }
        prev = 0;
    }
    return maxSide * maxSide;
}

int countSquares(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    vector<int> dp(n + 1, 0);
    int total = 0, prev = 0;
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            int temp = dp[j + 1];
            if (grid[i][j] == 1) {
                dp[j + 1] = 1 + min({dp[j], dp[j + 1], prev});
                total += dp[j + 1];
            } else {
                dp[j + 1] = 0;
            }
            prev = temp;
        }
        prev = 0;
    }
    return total;
}
```

## 3.5 Filling the table backwards: dungeon game

In _Dungeon Game_ a knight starts at the top-left of a grid and must reach the bottom-right. Each cell changes the knight's health (positive heals, negative damages). The knight can only move right or down. We need the minimum initial health so the knight never drops to $0$ or below.

If we try to go forward, we don't know how much health we will need later. The trick is to go backward from the destination. Let $dp[i][j]$ be the minimum health needed to _enter_ cell $(i,j)$ and survive to the end. At the bottom-right, we need at least $1$ health after the cell's effect, so $dp[m-1][n-1] = \max(1, 1 - grid[m-1][n-1])$.

For other cells, the knight will choose the easier of the two next steps (right or down). If we go right, we need $dp[i][j+1]$ health entering the next cell. So we need $dp[i][j+1] - grid[i][j]$ health entering the current cell. But health can never be less than $1$. So $dp[i][j] = \max(1, \min(dp[i+1][j], dp[i][j+1]) - grid[i][j])$.

We fill the table from bottom-right to top-left. Time $O(mn)$, space $O(n)$ with a rolling row from right to left.

Let us trace a tiny $2 \times 2$ grid:

```
-2  -3
-5 -10
```

Destination $(1,1)$: need $\max(1, 1 - (-10)) = 11$.
$(1,0)$: only right, need $\max(1, 11 - (-5)) = 16$.
$(0,1)$: only down, need $\max(1, 11 - (-3)) = 14$.
$(0,0)$: choose min of right ($14$) and down ($16$), so $\max(1, 14 - (-2)) = 16$.

Answer is $16$.

```python
def calculate_minimum_hp(dungeon: list[list[int]]) -> int:
    m, n = len(dungeon), len(dungeon[0])
    dp = [float('inf')] * (n + 1)
    dp[n - 1] = 1
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            need = min(dp[j], dp[j + 1]) - dungeon[i][j]
            dp[j] = max(1, need)
    return dp[0]

assert calculate_minimum_hp([[-2,-3],[-5,-10]]) == 16
assert calculate_minimum_hp([[0]]) == 1
assert calculate_minimum_hp([[100]]) == 1
```

```cpp
int calculateMinimumHP(vector<vector<int>>& dungeon) {
    int m = dungeon.size(), n = dungeon[0].size();
    vector<int> dp(n + 1, INT_MAX);
    dp[n - 1] = 1;
    for (int i = m - 1; i >= 0; --i) {
        for (int j = n - 1; j >= 0; --j) {
            int need = min(dp[j], dp[j + 1]) - dungeon[i][j];
            dp[j] = max(1, need);
        }
    }
    return dp[0];
}
```

## 3.6 The largest all-zero rectangle

Now we look for the largest rectangle containing only zeros in a binary matrix. This is sometimes called the _maximal rectangle of zeros_. We can solve it in $O(mn)$ time using a stack, similar to the largest rectangle in a histogram.

First, for each cell we compute how many consecutive zeros are directly above it (including itself). Call this $height[i][j]$. If $grid[i][j] = 1$, then $height[i][j] = 0$. Otherwise $height[i][j] = 1 + height[i-1][j]$. This turns each row into a histogram where the bar heights are the number of continuous zeros upward.

For a fixed row, we want the largest rectangle in this histogram. The classic stack algorithm finds it in $O(n)$: scan left to right, maintain a stack of column indices with increasing heights. When the current height is lower than the stack top, we pop and compute the area of the rectangle that uses the popped height as the limiting bar. The width extends from the new stack top (or left border) to the current column minus one.

We do this for every row and keep the maximum area. Total time $O(mn)$, space $O(n)$.

Let us trace a small example:

```
0 0 1
0 0 0
1 0 0
```

Heights row by row:
Row 0: $1, 1, 0$
Row 1: $2, 2, 1$
Row 2: $0, 3, 2$

For row 1 histogram $[2,2,1]$, the largest rectangle has area $4$ (columns $0$ and $1$, height $2$). For row 2 histogram $[0,3,2]$, the largest is $4$ (columns $1$ and $2$, height $2$). Overall answer $4$.

```python
def maximal_rectangle_of_zeros(grid: list[list[int]]) -> int:
    if not grid: return 0
    m, n = len(grid), len(grid[0])
    height = [0] * n
    best = 0
    for i in range(m):
        for j in range(n):
            height[j] = height[j] + 1 if grid[i][j] == 0 else 0
        stack = []
        for j in range(n + 1):
            cur_h = height[j] if j < n else 0
            while stack and cur_h < height[stack[-1]]:
                h = height[stack.pop()]
                left = stack[-1] if stack else -1
                area = h * (j - left - 1)
                best = max(best, area)
            stack.append(j)
    return best

assert maximal_rectangle_of_zeros([[0,0,1],[0,0,0],[1,0,0]]) == 4
assert maximal_rectangle_of_zeros([[1,1],[1,1]]) == 0
assert maximal_rectangle_of_zeros([[0]]) == 1
```

```cpp
int maximalRectangleOfZeros(vector<vector<int>>& grid) {
    if (grid.empty()) return 0;
    int m = grid.size(), n = grid[0].size();
    vector<int> height(n, 0);
    int best = 0;
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            height[j] = grid[i][j] == 0 ? height[j] + 1 : 0;
        }
        vector<int> st;
        for (int j = 0; j <= n; ++j) {
            int cur = (j < n) ? height[j] : 0;
            while (!st.empty() && cur < height[st.back()]) {
                int h = height[st.back()];
                st.pop_back();
                int left = st.empty() ? -1 : st.back();
                best = max(best, h * (j - left - 1));
            }
            st.push_back(j);
        }
    }
    return best;
}
```

## 3.7 Check yourself

1. In the unique paths problem, why can we fill the DP table row by row from top-left to bottom-right?
2. For minimum path sum, what changes in the recurrence compared to counting paths?
3. When solving the triangle minimum path bottom-up, why do we update the DP array from left to right?
4. In the maximal square problem, what does $dp[i][j]$ represent, and why do we take the minimum of three neighbours?
5. For the dungeon game, why must we fill the DP table backwards from the destination?

# Chapter 4. Sequences: longest increasing subsequence

## 4.1 Subsequences and the LIS problem

A subsequence keeps the order of elements but may skip some of them. From 2,4,1,3 the subsequence 2,1,3 is valid because the indices increase, while 3,1 is not because the order flips.

The longest increasing subsequence problem asks for the longest subsequence whose values also increase. Formally we want indices
$$i_1 < i_2 < \dots < i_k$$
with
$$a[i_1] < a[i_2] < \dots < a[i_k]$$
and $k$ as large as possible. This is exactly the problem _Longest Increasing Subsequence_ from the sheet.

## 4.2 The quadratic DP

Dynamic programming builds a solution from smaller answers. Let $d[i]$ be the length of the longest increasing subsequence that ends exactly at position $i$.
Then $d[i]$ is 1 by itself, or it can be extended from an earlier $j<i$ with $a[j]<a[i]$.

$$d[i]=\max\Bigl(1,\max_{\substack{j<i\\a[j]<a[i]}} d[j]+1\Bigr)$$

The answer is $\max_i d[i]$.

For $a = \{8,3,4,6,5,2,0,7,9,1\}$ we get
$d = \{1,1,2,3,3,1,1,4,5,2\}$.
The longest length is 5, e.g. 3,4,5,7,9. This method uses $O(n^2)$ time and $O(n)$ space.

```python
def lis_length(a):
    n = len(a)
    d = [1]*n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i]:
                if d[j] + 1 > d[i]:
                    d[i] = d[j] + 1
    return max(d) if d else 0

assert lis_length([8,3,4,6,5,2,0,7,9,1]) == 5
assert lis_length([1,2,3,4]) == 4
```

```cpp
int lis_length(vector<int> const& a){
    int n = (int)a.size();
    vector<int> d(n,1);
    for(int i=0;i<n;i++){
        for(int j=0;j<i;j++){
            if(a[j] < a[i]) d[i] = max(d[i], d[j]+1);
        }
    }
    int ans = 0;
    for(int v:d) ans = max(ans,v);
    return ans;
}
```

## 4.3 The faster tails idea

Binary search finds a position in a sorted list in logarithmic time.

Keep `tails[l]` as the smallest possible last value of an increasing subsequence of length $l+1$ seen so far. The array stays sorted.

Processing 8,3,4,6,5,2,0,7,9,1:

```
step   tails
8      [8]
3      [3]
4      [3,4]
6      [3,4,6]
5      [3,4,5]
2      [2,4,5]
0      [0,4,5]
7      [0,4,5,7]
9      [0,4,5,7,9]
1      [0,1,5,7,9]
```

For each $x$ we binary search the first $tails$ entry $\ge x$ and replace it, or append if $x$ is larger than all. The length of `tails` is the LIS length. This is $O(n\log n)$ time and $O(n)$ space.

```python
import bisect
def lis_len_nlogn(a):
    d = []
    for x in a:
        i = bisect.bisect_left(d, x)
        if i == len(d):
            d.append(x)
        else:
            d[i] = x
    return len(d)

assert lis_len_nlogn([8,3,4,6,5,2,0,7,9,1]) == 5
assert lis_len_nlogn([3,4,2,5,1]) == 3
```

```cpp
int lis_len_nlogn(vector<int> const& a){
    vector<int> d;
    for(int x:a){
        auto it = lower_bound(d.begin(), d.end(), x);
        if(it == d.end()) d.push_back(x);
        else *it = x;
    }
    return (int)d.size();
}
```

## 4.4 Getting the subsequence back

With the tails idea we can also recover a subsequence. Store for each element the position $p[i]$ where it would be placed in `tails`. Then scan the array backwards, picking the last occurrence with position $L-1$, then $L-2$, etc. The picked values are increasing by construction.

```python
import bisect
def lis_seq(a):
    n = len(a)
    d = []
    p = [0]*n
    for i,x in enumerate(a):
        pos = bisect.bisect_left(d, x)
        p[i] = pos
        if pos == len(d):
            d.append(x)
        else:
            d[pos] = x
    l = len(d)-1
    res = []
    for i in range(n-1,-1,-1):
        if p[i] == l:
            res.append(a[i])
            l -= 1
            if l < 0:
                break
    res.reverse()
    return res

assert lis_seq([8,3,4,6,5,2,0,7,9,1]) == [3,4,5,7,9]
assert len(lis_seq([1,2,3])) == 3
```

```cpp
vector<int> lis_seq(vector<int> const& a){
    int n = (int)a.size();
    vector<int> d;
    vector<int> p(n);
    for(int i=0;i<n;i++){
        auto it = lower_bound(d.begin(), d.end(), a[i]);
        p[i] = int(it - d.begin());
        if(it == d.end()) d.push_back(a[i]);
        else *it = a[i];
    }
    int l = (int)d.size()-1;
    vector<int> subseq;
    for(int i=n-1;i>=0 && l>=0;i--){
        if(p[i]==l){
            subseq.push_back(a[i]);
            l--;
        }
    }
    reverse(subseq.begin(), subseq.end());
    return subseq;
}
```

## 4.5 Check yourself

What is a subsequence of 5,1,4,2,3 that is increasing and has length three?
Why does the tails array stay sorted after each update?
What does `bisect_left` return for a value smaller than all elements in tails?
If you run the reconstruction backwards from the last element, why must the chosen values be strictly increasing?

# Chapter 5. Two strings at a time

## 5.1 Longest common subsequence

A **subsequence** of a string is a sequence of characters that appears in the same order, but not necessarily consecutively. For example, "ace" is a subsequence of "abcde". A **common subsequence** of two strings is a subsequence of both. The **longest common subsequence** (LCS) problem asks for the length of the longest such sequence. This is exactly the problem _Longest Common Subsequence_.

We solve it with dynamic programming. Let the two strings be `A` of length `n` and `B` of length `m`. We build a table `dp` where `dp[i][j]` is the length of the LCS of the first `i` characters of `A` and the first `j` characters of `B`. The table has `(n+1)` rows and `(m+1)` columns, with row 0 and column 0 initialized to 0 because an empty string has no common subsequence with anything.

The recurrence is simple:

- If `A[i-1] == B[j-1]`, the last characters match, so we can extend the LCS of the prefixes without these characters: `dp[i][j] = dp[i-1][j-1] + 1`.
- Otherwise, we cannot use both last characters together, so we take the best of dropping one: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.

Let's work through a tiny example by hand. Let `A = "ABC"` and `B = "AC"`. We create a 4×3 table (rows 0..3, columns 0..2).

|     |     | 0   | 1   | 2   |
| --- | --- | --- | --- | --- |
|     |     |     | A   | C   |
| 0   |     | 0   | 0   | 0   |
| 1   | A   | 0   | 1   | 1   |
| 2   | B   | 0   | 1   | 1   |
| 3   | C   | 0   | 1   | 2   |

We fill row by row. Row 1, column 1: `A[0]=='A'` matches `B[0]=='A'`, so `dp[1][1] = dp[0][0]+1 = 1`. Row 1, column 2: `A[0]=='A'` vs `B[1]=='C'` no match, so `max(dp[0][2], dp[1][1]) = 1`. Row 2, column 1: `B` vs `A` no match, `max(dp[1][1], dp[2][0]) = 1`. Row 2, column 2: `B` vs `C` no match, `max(1,1)=1`. Row 3, column 1: `C` vs `A` no match, `max(1,0)=1`. Row 3, column 2: `C` matches `C`, so `dp[3][2] = dp[2][1]+1 = 2`. The answer is `dp[3][2] = 2`, and the LCS is "AC".

To recover the actual subsequence, we walk backwards from `dp[n][m]`. If the characters at the current position match, that character is part of the LCS and we move diagonally up-left. Otherwise we move towards the larger of the left or top cell (if equal, either works). This reconstruction takes $O(n+m)$ time.

The time complexity is $O(nm)$ and the space complexity is $O(nm)$ for the full table. If only the length is needed, we can reduce space to $O(\min(n,m))$ by keeping only two rows.

```python
def lcs_length(a: str, b: str) -> int:
    n, m = len(a), len(b)
    if n < m:
        a, b = b, a
        n, m = m, n
    prev = [0] * (m + 1)
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[m]

def lcs_string(a: str, b: str) -> str:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # reconstruct
    i, j = n, m
    res = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            res.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(res))

assert lcs_length("ABC", "AC") == 2
assert lcs_string("ABC", "AC") == "AC"
assert lcs_length("AGGTAB", "GXTXAYB") == 4
assert lcs_string("AGGTAB", "GXTXAYB") == "GTAB"
```

```cpp
int lcs_length(const string& a, const string& b) {
    int n = a.size(), m = b.size();
    if (n < m) return lcs_length(b, a);
    vector<int> prev(m + 1), cur(m + 1);
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (a[i - 1] == b[j - 1]) cur[j] = prev[j - 1] + 1;
            else cur[j] = max(prev[j], cur[j - 1]);
        }
        swap(prev, cur);
    }
    return prev[m];
}

string lcs_string(const string& a, const string& b) {
    int n = a.size(), m = b.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1));
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (a[i - 1] == b[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
            else dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
        }
    }
    string res;
    int i = n, j = m;
    while (i > 0 && j > 0) {
        if (a[i - 1] == b[j - 1]) {
            res.push_back(a[i - 1]);
            --i; --j;
        } else if (dp[i - 1][j] >= dp[i][j - 1]) --i;
        else --j;
    }
    reverse(res.begin(), res.end());
    return res;
}
```

## 5.2 Edit distance

The **edit distance** (also called Levenshtein distance) between two strings is the minimum number of operations required to transform one string into the other. The allowed operations are:

- Insert a character.
- Delete a character.
- Replace a character with another.

This is exactly the problem _Edit Distance_.

We again use a DP table `dp[i][j]` representing the minimum edit distance between the first `i` characters of string `A` and the first `j` characters of string `B`. The base cases: `dp[i][0] = i` (delete all `i` characters) and `dp[0][j] = j` (insert `j` characters).

The recurrence for `i>0, j>0`:

- If `A[i-1] == B[j-1]`, no operation is needed for the last character: `dp[i][j] = dp[i-1][j-1]`.
- Otherwise, we consider three possibilities:
  1. Replace `A[i-1]` with `B[j-1]`: cost `1 + dp[i-1][j-1]`.
  2. Delete `A[i-1]`: cost `1 + dp[i-1][j]`.
  3. Insert `B[j-1]` into `A`: cost `1 + dp[i][j-1]`.
     We take the minimum of these three.

Let's compute the edit distance between `"cat"` and `"cut"`. Table size 4×4.

|     |     | 0   | 1   | 2   | 3   |
| --- | --- | --- | --- | --- | --- |
|     |     |     | c   | u   | t   |
| 0   |     | 0   | 1   | 2   | 3   |
| 1   | c   | 1   | 0   | 1   | 2   |
| 2   | a   | 2   | 1   | 1   | 2   |
| 3   | t   | 3   | 2   | 2   | 1   |

Row 0 and column 0 are 0,1,2,3. Row 1, col 1: `c==c` -> `dp[0][0]=0`. Row 1, col 2: `c!=u` -> min(1+dp[0][1]=2, 1+dp[1][1]=1, 1+dp[0][2]=3) = 1. Row 1, col 3: `c!=t` -> min(1+dp[0][2]=3, 1+dp[1][2]=2, 1+dp[0][3]=4) = 2. Row 2, col 1: `a!=c` -> min(1+dp[1][0]=2, 1+dp[2][0]=3, 1+dp[1][1]=1) = 1. Row 2, col 2: `a!=u` -> min(1+dp[1][1]=1, 1+dp[2][1]=2, 1+dp[1][2]=2) = 1. Row 2, col 3: `a!=t` -> min(1+dp[1][2]=2, 1+dp[2][2]=2, 1+dp[1][3]=3) = 2. Row 3, col 1: `t!=c` -> min(1+dp[2][0]=3, 1+dp[3][0]=4, 1+dp[2][1]=2) = 2. Row 3, col 2: `t!=u` -> min(1+dp[2][1]=2, 1+dp[3][1]=3, 1+dp[2][2]=2) = 2. Row 3, col 3: `t==t` -> `dp[2][2]=1`. Final answer 1.

Time complexity is $O(nm)$, space complexity is $O(nm)$ (or $O(\min(n,m))$ with two rows).

```python
def edit_distance(a: str, b: str) -> int:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # replace
                    dp[i - 1][j],      # delete
                    dp[i][j - 1]       # insert
                )
    return dp[n][m]

assert edit_distance("cat", "cut") == 1
assert edit_distance("kitten", "sitting") == 3
assert edit_distance("", "abc") == 3
```

```cpp
int edit_distance(const string& a, const string& b) {
    int n = a.size(), m = b.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1));
    for (int i = 0; i <= n; ++i) dp[i][0] = i;
    for (int j = 0; j <= m; ++j) dp[0][j] = j;
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (a[i - 1] == b[j - 1]) dp[i][j] = dp[i - 1][j - 1];
            else dp[i][j] = 1 + min({dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]});
        }
    }
    return dp[n][m];
}
```

## 5.3 Palindromes inside strings

A **palindrome** reads the same forward and backward. The **longest palindromic subsequence** (LPS) of a string is the longest subsequence that is a palindrome. This is exactly the problem _Longest Palindromic Subsequence_. A beautiful observation: the LPS of a string `S` is exactly the LCS of `S` and its reverse `S_rev`. Because a palindrome equals its reverse, any common subsequence of `S` and `S_rev` reads the same forward in `S` and backward in `S_rev`, hence it is a palindrome.

The **minimum insertions to make a string a palindrome** is the number of characters we need to insert anywhere to turn the string into a palindrome. This is exactly the problem _Minimum Insertions for Palindrome_. The answer is `len(S) - LPS(S)`. Why? The LPS already forms a palindrome skeleton; we only need to insert the missing characters to pair up the rest.

Let's test on `S = "bbbab"`. Its reverse is `"babbb"`, and the longest common subsequence of the two is `"bbbb"`, so the longest palindromic subsequence has length 4 and the minimum number of insertions is $5 - 4 = 1$. Concretely, the four `b` letters already pair up. Only the `a` is left without a partner, so we insert a second `a` right after the first `b` and get `"babbab"`, which reads the same forwards and backwards.

For LPS directly: let `dp[i][j]` be the length of the longest palindromic subsequence in substring `S[i..j]` (inclusive). Base: `dp[i][i] = 1`. For `i < j`: if `S[i] == S[j]`, then `dp[i][j] = dp[i+1][j-1] + 2`; else `dp[i][j] = max(dp[i+1][j], dp[i][j-1])`. We fill by increasing length.

Time complexity $O(n^2)$, space $O(n^2)$ (or $O(n)$ with clever ordering).

```python
def longest_palindromic_subsequence(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2 if length > 2 else 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]

def min_insertions_palindrome(s: str) -> int:
    return len(s) - longest_palindromic_subsequence(s)

assert longest_palindromic_subsequence("bbbab") == 4
assert min_insertions_palindrome("bbbab") == 1
assert longest_palindromic_subsequence("cbbd") == 2
assert min_insertions_palindrome("cbbd") == 2
```

```cpp
int longest_palindromic_subsequence(const string& s) {
    int n = s.size();
    vector<vector<int>> dp(n, vector<int>(n));
    for (int i = 0; i < n; ++i) dp[i][i] = 1;
    for (int len = 2; len <= n; ++len) {
        for (int i = 0; i + len <= n; ++i) {
            int j = i + len - 1;
            if (s[i] == s[j]) dp[i][j] = (len > 2 ? dp[i + 1][j - 1] : 0) + 2;
            else dp[i][j] = max(dp[i + 1][j], dp[i][j - 1]);
        }
    }
    return dp[0][n - 1];
}

int min_insertions_palindrome(const string& s) {
    return s.size() - longest_palindromic_subsequence(s);
}
```

## 5.4 Counting subsequences

Sometimes we need to count how many ways a string `T` appears as a subsequence of `S`. This is the **distinct subsequences** problem (exactly the problem _Distinct Subsequences_). We use DP where `dp[i][j]` is the number of ways the first `j` characters of `T` appear as a subsequence in the first `i` characters of `S`. Base: `dp[i][0] = 1` for all `i` (empty string is a subsequence exactly once). `dp[0][j] = 0` for `j>0`. Recurrence: if `S[i-1] == T[j-1]`, we can either use this match (`dp[i-1][j-1]`) or skip it (`dp[i-1][j]`), so `dp[i][j] = dp[i-1][j-1] + dp[i-1][j]`. Otherwise, we must skip: `dp[i][j] = dp[i-1][j]`.

Example: `S = "rabbbit"`, `T = "rabbit"`. The answer is 3.

Another problem is **interleaving string** (exactly the problem _Interleaving String_). Given strings `A`, `B`, `C`, we want to know if `C` is formed by interleaving `A` and `B` (keeping the order of characters within each). DP: `dp[i][j]` is true if `C[:i+j]` can be formed by interleaving `A[:i]` and `B[:j]`. Base: `dp[0][0] = true`. Transition: `dp[i][j] = (dp[i-1][j] and A[i-1]==C[i+j-1]) or (dp[i][j-1] and B[j-1]==C[i+j-1])`.

Both run in $O(nm)$ time and space.

```python
def num_distinct_subsequences(s: str, t: str) -> int:
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 1
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j]
    return dp[n][m]

def is_interleave(a: str, b: str, c: str) -> bool:
    n, m = len(a), len(b)
    if n + m != len(c):
        return False
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] and a[i - 1] == c[i - 1]
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] and b[j - 1] == c[j - 1]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = (dp[i - 1][j] and a[i - 1] == c[i + j - 1]) or \
                       (dp[i][j - 1] and b[j - 1] == c[i + j - 1])
    return dp[n][m]

assert num_distinct_subsequences("rabbbit", "rabbit") == 3
assert is_interleave("aab", "axy", "aaxaby") == True
assert is_interleave("aab", "axy", "aaxbay") == False
```

```cpp
int num_distinct_subsequences(const string& s, const string& t) {
    int n = s.size(), m = t.size();
    vector<vector<long long>> dp(n + 1, vector<long long>(m + 1));
    for (int i = 0; i <= n; ++i) dp[i][0] = 1;
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (s[i - 1] == t[j - 1]) dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j];
            else dp[i][j] = dp[i - 1][j];
        }
    }
    return dp[n][m];
}

bool is_interleave(const string& a, const string& b, const string& c) {
    int n = a.size(), m = b.size();
    if (n + m != (int)c.size()) return false;
    vector<vector<bool>> dp(n + 1, vector<bool>(m + 1));
    dp[0][0] = true;
    for (int i = 1; i <= n; ++i) dp[i][0] = dp[i - 1][0] && a[i - 1] == c[i - 1];
    for (int j = 1; j <= m; ++j) dp[0][j] = dp[0][j - 1] && b[j - 1] == c[j - 1];
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            dp[i][j] = (dp[i - 1][j] && a[i - 1] == c[i + j - 1]) ||
                       (dp[i][j - 1] && b[j - 1] == c[i + j - 1]);
        }
    }
    return dp[n][m];
}
```

## 5.5 Wildcard and regular expression matching

**Wildcard matching** (problem _Wildcard Matching_) asks if a pattern containing `?` (matches any single character) and `*` (matches any sequence of characters, including empty) matches a given string. **Regular expression matching** (problem _Regular Expression Matching_) uses `.` (any single character) and `*` (zero or more of the preceding element). Both are solved with DP where `dp[i][j]` indicates whether the first `i` characters of the string match the first `j` characters of the pattern.

For wildcard matching, the star `*` can match zero or more characters. The recurrence:

- If pattern[j-1] is a letter or `?`, then `dp[i][j] = dp[i-1][j-1]` provided the character matches (or `?`).
- If pattern[j-1] is `*`, then `dp[i][j] = dp[i][j-1]` (star matches empty) or `dp[i-1][j]` (star matches one more character).

For regular expression matching, the star applies to the preceding character. We typically process the pattern and handle `*` by looking two steps back. Let `dp[i][j]` be match for string prefix `i` and pattern prefix `j`. If pattern[j-1] is not `*` (or it's the first character), we check direct match. If pattern[j-1] is `*`, we consider zero occurrences of the preceding element (`dp[i][j-2]`) or, if the preceding element matches the current string character, we can consume the string character (`dp[i-1][j]`).

Both run in $O(nm)$ time and space.

```python
def is_match_wildcard(s: str, p: str) -> bool:
    n, m = len(s), len(p)
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for j in range(1, m + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif p[j - 1] == '?' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[n][m]

def is_match_regex(s: str, p: str) -> bool:
    n, m = len(s), len(p)
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for j in range(2, m + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i][j - 2]  # zero occurrence
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]  # one more occurrence
            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[n][m]

assert is_match_wildcard("acb", "a*b") == True
assert is_match_wildcard("acb", "a?b") == True
assert is_match_wildcard("acb", "a*c") == False
assert is_match_regex("aaab", "a*b") == True
assert is_match_regex("ab", ".*") == True
assert is_match_regex("aab", "c*a*b") == True
```

```cpp
bool is_match_wildcard(const string& s, const string& p) {
    int n = s.size(), m = p.size();
    vector<vector<bool>> dp(n + 1, vector<bool>(m + 1));
    dp[0][0] = true;
    for (int j = 1; j <= m; ++j)
        if (p[j - 1] == '*') dp[0][j] = dp[0][j - 1];
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (p[j - 1] == '*') dp[i][j] = dp[i][j - 1] || dp[i - 1][j];
            else if (p[j - 1] == '?' || p[j - 1] == s[i - 1]) dp[i][j] = dp[i - 1][j - 1];
        }
    }
    return dp[n][m];
}

bool is_match_regex(const string& s, const string& p) {
    int n = s.size(), m = p.size();
    vector<vector<bool>> dp(n + 1, vector<bool>(m + 1));
    dp[0][0] = true;
    for (int j = 2; j <= m; ++j)
        if (p[j - 1] == '*') dp[0][j] = dp[0][j - 2];
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (p[j - 1] == '*') {
                dp[i][j] = dp[i][j - 2];
                if (p[j - 2] == '.' || p[j - 2] == s[i - 1])
                    dp[i][j] = dp[i][j] || dp[i - 1][j];
            } else if (p[j - 1] == '.' || p[j - 1] == s[i - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            }
        }
    }
    return dp[n][m];
}
```

## 5.6 Longest common substring

A **substring** is a contiguous block of characters, unlike a subsequence which can skip characters. The **longest common substring** problem (exactly the problem _Longest Common Substring_) asks for the longest string that appears as a substring in both input strings.

The DP is similar to LCS but with a crucial difference: because the substring must be contiguous, if the current characters don't match, the length of the common suffix ending here is zero. Let `dp[i][j]` be the length of the longest common suffix of `A[:i]` and `B[:j]` (i.e., ending exactly at `A[i-1]` and `B[j-1]`). Then:

- If `A[i-1] == B[j-1]`, `dp[i][j] = dp[i-1][j-1] + 1`.
- Else `dp[i][j] = 0`.

The answer is the maximum value in the whole table.

Example: `A = "abcde"`, `B = "abfce"`. Table 6×6.

|     |     | 0   | 1   | 2   | 3   | 4   | 5   |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | a   | b   | f   | c   | e   |
| 0   |     | 0   | 0   | 0   | 0   | 0   | 0   |
| 1   | a   | 0   | 1   | 0   | 0   | 0   | 0   |
| 2   | b   | 0   | 0   | 2   | 0   | 0   | 0   |
| 3   | c   | 0   | 0   | 0   | 0   | 1   | 0   |
| 4   | d   | 0   | 0   | 0   | 0   | 0   | 0   |
| 5   | e   | 0   | 0   | 0   | 0   | 0   | 1   |

Maximum is 2, corresponding to "ab".

Time complexity $O(nm)$, space $O(nm)$ (or $O(\min(n,m))$ with two rows).

```python
def longest_common_substring(a: str, b: str) -> int:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    best = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > best:
                    best = dp[i][j]
            else:
                dp[i][j] = 0
    return best

assert longest_common_substring("abcde", "abfce") == 2
assert longest_common_substring("abc", "def") == 0
assert longest_common_substring("abab", "baba") == 3  # "aba" or "bab"
```

```cpp
int longest_common_substring(const string& a, const string& b) {
    int n = a.size(), m = b.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1));
    int best = 0;
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (a[i - 1] == b[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                best = max(best, dp[i][j]);
            } else {
                dp[i][j] = 0;
            }
        }
    }
    return best;
}
```

## 5.7 Check yourself

1. In the LCS table, what does a diagonal step during reconstruction indicate?
2. Why does the edit distance recurrence have three options when characters differ, but the LCS recurrence only has two?
3. For the string "character", what is the length of its longest palindromic subsequence? (Hint: use the reverse trick.)
4. In wildcard matching, if the pattern is "a*b" and the string is "acccb", which DP cell represents the star matching "ccc"?

# Chapter 6. The knapsack family

## 6.1 The 0/1 knapsack

Imagine you have a knapsack that can hold at most _W_ kilograms. You also have _n_ items, each with a weight and a value. You may either take an item or leave it; you cannot break it and you cannot take it more than once. Your goal is to maximize the total value inside the knapsack without exceeding the weight limit. This is exactly the problem _Zero One Knapsack_.

To solve it we build a table. Let `dp[i][w]` be the best value we can get using only the first _i_ items when the knapsack capacity is _w_. The table has _n_+1 rows (including a row for zero items) and _W_+1 columns (capacities from 0 to _W_). Row 0 is all zeros because with no items we carry no value.

Now consider item _i_ (1‑based). Its weight is `wt[i]` and its value is `val[i]`. For a given capacity _w_ we have two choices:

- Skip the item: the value stays `dp[i-1][w]`.
- Take the item (only possible if `wt[i] ≤ w`): we gain `val[i]` and the remaining capacity becomes `w - wt[i]`, so the value is `dp[i-1][w-wt[i]] + val[i]`.

We pick the larger of the two. In formula form:

$$ dp[i][w] = \max\bigl(dp[i-1][w],\; dp[i-1][w-wt[i]] + val[i]\bigr) \quad\text{(if } wt[i] \le w\text{)} $$

If the item is too heavy we simply copy `dp[i-1][w]`.

Let's walk through a tiny example by hand. Three items: weights `[2, 3, 4]`, values `[3, 4, 5]`. Capacity `W = 5`.

| i \ w   | 0   | 1   | 2   | 3   | 4   | 5   |
| ------- | --- | --- | --- | --- | --- | --- |
| 0       | 0   | 0   | 0   | 0   | 0   | 0   |
| 1 (2,3) | 0   | 0   | 3   | 3   | 3   | 3   |
| 2 (3,4) | 0   | 0   | 3   | 4   | 4   | 7   |
| 3 (4,5) | 0   | 0   | 3   | 4   | 5   | 7   |

Row 1: item 1 weighs 2, value 3. For w=2..5 we can take it, so value 3.
Row 2: item 2 weighs 3, value 4. At w=3 we compare skip (3) vs take (0+4)=4 → 4. At w=5 we compare skip (3) vs take (dp[1][2]+4=3+4=7) → 7.
Row 3: item 3 weighs 4, value 5. At w=4 we compare skip (4) vs take (0+5)=5 → 5. At w=5 we compare skip (7) vs take (dp[2][1]+5=0+5=5) → 7.

The answer is `dp[3][5] = 7`. This table takes $O(nW)$ time and $O(nW)$ space because we fill every cell once.

## 6.2 Saving memory with one row

Notice that row _i_ only uses row _i-1_. We can therefore keep just one array `dp[w]` and update it in place for each item. But the order of the inner loop matters. If we iterate _w_ from 0 up to _W_, then when we compute `dp[w]` the entry `dp[w-wt[i]]` has already been updated for the current item; that would mean we are using the same item more than once. To enforce the 0/1 rule we must iterate _w_ **downwards** from _W_ to `wt[i]`. Then `dp[w-wt[i]]` still holds the value from the previous item (the old row), so each item is used at most once.

The 1D transition becomes:

$$ dp[w] = \max\bigl(dp[w],\; dp[w-wt[i]] + val[i]\bigr) \quad\text{for } w = W \dots wt[i] $$

Time stays $O(nW)$, space drops to $O(W)$.

```python
def knapsack_01(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for wt, val in zip(weights, values):
        for w in range(capacity, wt - 1, -1):
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[capacity]

# Example from section 6.1: weights [2,3,4], values [3,4,5], capacity 5 -> 7
assert knapsack_01([2, 3, 4], [3, 4, 5], 5) == 7
# Another tiny check: one item weight 3 value 10, capacity 2 -> 0
assert knapsack_01([3], [10], 2) == 0
# One item fits exactly
assert knapsack_01([3], [10], 3) == 10
```

```cpp
int knapsack_01(const vector<int>& weights, const vector<int>& values, int capacity) {
    vector<int> dp(capacity + 1, 0);
    for (size_t i = 0; i < weights.size(); ++i) {
        int wt = weights[i], val = values[i];
        for (int w = capacity; w >= wt; --w) {
            dp[w] = max(dp[w], dp[w - wt] + val);
        }
    }
    return dp[capacity];
}
```

## 6.3 The unbounded knapsack

Sometimes you may take as many copies of each item as you like. This is the _Unbounded Knapsack_ problem. The state definition is the same, but the transition changes: after taking an item we may take it again, so we want `dp[w-wt[i]]` to already include the current item. That happens automatically if we iterate _w_ **upwards** from `wt[i]` to _W_.

The transition:

$$ dp[w] = \max\bigl(dp[w],\; dp[w-wt[i]] + val[i]\bigr) \quad\text{for } w = wt[i] \dots W $$

Time $O(nW)$, space $O(W)$.

Let's test the same three items (weights 2, 3, 4 and values 3, 4, 5) with capacity 5, now with unlimited copies. Two copies of item 1 weigh 4 and are worth 6. Item 1 together with item 2 weighs 5 and is worth 7. Nothing better fits, so the answer is still 7. With capacity 6 things change: three copies of item 1 weigh 6 and are worth 9, which beats any mix with the other items.

```python
def unbounded_knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for wt, val in zip(weights, values):
        for w in range(wt, capacity + 1):
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[capacity]

# Same items, capacity 5 -> 7 (item1+item2)
assert unbounded_knapsack([2, 3, 4], [3, 4, 5], 5) == 7
# Capacity 6 -> three copies of item1: 3*3=9
assert unbounded_knapsack([2, 3, 4], [3, 4, 5], 6) == 9
# One item weight 3 value 10, capacity 7 -> two copies (6) value 20
assert unbounded_knapsack([3], [10], 7) == 20
```

```cpp
int unbounded_knapsack(const vector<int>& weights, const vector<int>& values, int capacity) {
    vector<int> dp(capacity + 1, 0);
    for (size_t i = 0; i < weights.size(); ++i) {
        int wt = weights[i], val = values[i];
        for (int w = wt; w <= capacity; ++w) {
            dp[w] = max(dp[w], dp[w - wt] + val);
        }
    }
    return dp[capacity];
}
```

## 6.4 Subset sum and its cousins

Many problems that don't look like knapsack at first can be modeled as one.

**Subset Sum** (problem _Subset Sum_) asks: given a list of positive integers, can we pick some of them that add up exactly to a target _T_? This is a 0/1 knapsack where every item's weight equals its value, and we only care whether a sum is reachable. We use a boolean array `dp[w]` (true if sum _w_ is possible). The update is `dp[w] = dp[w] or dp[w - x]` for each number _x_, iterating downwards.

**Partition Equal Subset Sum** (problem _Partition Equal Subset Sum_) gives an array and asks if it can be split into two subsets with equal sum. If the total sum is odd, answer is no. Otherwise we just need to know whether a subset sums to `total/2`, exactly Subset Sum.

**Minimum Subset Sum Difference** (problem _Minimum Subset Sum Difference_) asks for the smallest possible absolute difference between the sums of two partitions. We compute all reachable sums up to `total/2` using the same boolean DP, then scan for the largest reachable sum `s`; the difference is `total - 2*s`.

Let's illustrate Subset Sum with numbers `[2, 3, 7]` and target `5`. Boolean table (rows = items, columns = sums 0..5):

| i \ w | 0   | 1   | 2   | 3   | 4   | 5   |
| ----- | --- | --- | --- | --- | --- | --- |
| 0     | T   | F   | F   | F   | F   | F   |
| 2     | T   | F   | T   | F   | F   | F   |
| 3     | T   | F   | T   | T   | F   | T   |
| 7     | T   | F   | T   | T   | F   | T   |

We see sum 5 is reachable (2+3). For Partition Equal Subset Sum with `[1, 5, 11, 5]`, total = 22, half = 11. Subset Sum for 11 succeeds (1+5+5). For Minimum Subset Sum Difference with `[3, 1, 4, 2, 2, 1]`, total = 13, half = 6. Reachable sums up to 6: 0,1,2,3,4,5,6 all reachable? Let's check: 3+1+2=6, so difference = 13-12=1.

```python
def can_partition_equal(nums):
    total = sum(nums)
    if total % 2: return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for w in range(target, x - 1, -1):
            dp[w] = dp[w] or dp[w - x]
    return dp[target]

def min_subset_diff(nums):
    total = sum(nums)
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for w in range(target, x - 1, -1):
            dp[w] = dp[w] or dp[w - x]
    for s in range(target, -1, -1):
        if dp[s]:
            return total - 2 * s
    return total

# Subset sum [2,3,7] target 5 -> True
assert can_partition_equal([2, 3, 7]) == False  # total 12, half 6 -> 2+? actually 2+3+7=12, half 6, can we make 6? 2+3+? no 7>6, so False. Wait 2+3+7=12, half 6, subset {2,?} no. So False.
# Let's test a true case
assert can_partition_equal([1, 5, 11, 5]) == True
# Min diff [3,1,4,2,2,1] -> 1
assert min_subset_diff([3, 1, 4, 2, 2, 1]) == 1
```

```cpp
bool can_partition_equal(const vector<int>& nums) {
    int total = 0;
    for (int x : nums) total += x;
    if (total % 2) return false;
    int target = total / 2;
    vector<bool> dp(target + 1, false);
    dp[0] = true;
    for (int x : nums) {
        for (int w = target; w >= x; --w) {
            dp[w] = dp[w] || dp[w - x];
        }
    }
    return dp[target];
}

int min_subset_diff(const vector<int>& nums) {
    int total = 0;
    for (int x : nums) total += x;
    int target = total / 2;
    vector<bool> dp(target + 1, false);
    dp[0] = true;
    for (int x : nums) {
        for (int w = target; w >= x; --w) {
            dp[w] = dp[w] || dp[w - x];
        }
    }
    for (int s = target; s >= 0; --s) {
        if (dp[s]) return total - 2 * s;
    }
    return total;
}
```

## 6.5 Counting versions and two budgets

Some knapsack variants ask for the number of ways to achieve a goal, or they add extra constraints.

**Target Sum** (problem _Target Sum_): you have an array of non‑negative integers and a target _S_. You must put a `+` or `-` sign in front of each number so that the total equals _S_. Let the sum of numbers with `+` be `P` and with `-` be `N`. Then `P - N = S` and `P + N = total`. So `P = (total + S) / 2`. The problem reduces to counting subsets that sum to `P`, a 0/1 knapsack where `dp[w]` stores the number of ways to reach sum `w`. Initialize `dp[0] = 1` and iterate numbers downwards: `dp[w] += dp[w - x]`.

**Ones and Zeroes** (problem _Ones and Zeroes_): you are given binary strings and limits `m` (max zeros) and `n` (max ones). Pick the maximum number of strings such that total zeros ≤ `m` and total ones ≤ `n`. This is a 0/1 knapsack with two weight dimensions. State `dp[i][j]` = max strings using _i_ zeros and _j_ ones. For each string with `z` zeros and `o` ones, update backwards: `dp[i][j] = max(dp[i][j], dp[i-z][j-o] + 1)`.

**Rod Cutting** (problem _Rod Cutting_): a rod of length _L_ can be cut into pieces. Each piece of length `i` has price `p[i]`. You may cut as many pieces of each length as you want. This is exactly Unbounded Knapsack where items are lengths 1..L, weight = length, value = price, capacity = L. The answer is `dp[L]` with the upward loop.

```python
def target_sum_ways(nums, target):
    total = sum(nums)
    if (total + target) % 2 != 0:
        return 0
    P = (total + target) // 2
    if P < 0:
        return 0
    dp = [0] * (P + 1)
    dp[0] = 1
    for x in nums:
        for w in range(P, x - 1, -1):
            dp[w] += dp[w - x]
    return dp[P]

def max_strings_on_zero(strs, m, n):
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        zeros = s.count('0')
        ones = len(s) - zeros
        for i in range(m, zeros - 1, -1):
            for j in range(n, ones - 1, -1):
                dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)
    return dp[m][n]

def rod_cutting(prices, length):
    # prices is 1-indexed list or 0-indexed with prices[i] for length i+1
    dp = [0] * (length + 1)
    for l in range(1, length + 1):
        price = prices[l - 1] if l - 1 < len(prices) else 0
        for w in range(l, length + 1):
            dp[w] = max(dp[w], dp[w - l] + price)
    return dp[length]

# Target sum: nums [1,1,1,1,1], target 3 -> 5 ways (choose 4 plus, 1 minus? Actually P=(5+3)/2=4, subsets of size 4: 5 ways)
assert target_sum_ways([1,1,1,1,1], 3) == 5
# Ones and zeroes: strs ["10","0001","111001","1","0"], m=5, n=3 -> 4
assert max_strings_on_zero(["10","0001","111001","1","0"], 5, 3) == 4
# Rod cutting: prices [1,5,8,9,10,17,17,20] for lengths 1..8, length 4 -> max price 10 (2+2 or 4)
assert rod_cutting([1,5,8,9,10,17,17,20], 4) == 10
```

```cpp
int target_sum_ways(const vector<int>& nums, int target) {
    int total = 0;
    for (int x : nums) total += x;
    if ((total + target) % 2 != 0) return 0;
    int P = (total + target) / 2;
    if (P < 0) return 0;
    vector<int> dp(P + 1, 0);
    dp[0] = 1;
    for (int x : nums) {
        for (int w = P; w >= x; --w) {
            dp[w] += dp[w - x];
        }
    }
    return dp[P];
}

int max_strings_on_zero(const vector<string>& strs, int m, int n) {
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    for (const string& s : strs) {
        int zeros = 0, ones = 0;
        for (char c : s) {
            if (c == '0') zeros++;
            else ones++;
        }
        for (int i = m; i >= zeros; --i) {
            for (int j = n; j >= ones; --j) {
                dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1);
            }
        }
    }
    return dp[m][n];
}

int rod_cutting(const vector<int>& prices, int length) {
    vector<int> dp(length + 1, 0);
    for (int l = 1; l <= length; ++l) {
        int price = (l - 1 < (int)prices.size()) ? prices[l - 1] : 0;
        for (int w = l; w <= length; ++w) {
            dp[w] = max(dp[w], dp[w - l] + price);
        }
    }
    return dp[length];
}
```

## 6.6 Check yourself

1. In the 0/1 knapsack 1D array, why must the inner loop run from high capacity down to the item's weight?
2. What changes in the loop direction when we switch from 0/1 knapsack to unbounded knapsack, and why?
3. How can you turn the Partition Equal Subset Sum problem into a Subset Sum problem?
4. In the Target Sum problem, why do we compute `P = (total + target) / 2` and then count subsets that sum to `P`?

# Chapter 7. Intervals and state machines

## 7.1 Interval DP: matrix chain

Many problems ask us to combine a sequence of items in some order, and the cost of combining two adjacent pieces depends only on the pieces themselves. A classic example is _Matrix Chain Multiplication_: we have a chain of matrices $A_1, A_2, \dots, A_n$ where matrix $A_i$ has dimensions $p_{i-1} \times p_i$. We want to parenthesize the product to minimize the total number of scalar multiplications. The order matters: multiplying a $10 \times 100$ matrix by a $100 \times 5$ matrix takes $10 \times 100 \times 5 = 5000$ multiplications, but if we have three matrices the grouping changes the total.

The key idea is to let the DP state be an interval. Define $dp[l][r]$ as the minimum cost to multiply matrices $l$ through $r$ (inclusive). For a single matrix the cost is zero. For a longer interval we try every possible split point $k$ between $l$ and $r-1$: first multiply $l..k$, then multiply $k+1..r$, then multiply the two results. The cost of the final multiplication is $p_{l-1} \times p_k \times p_r$. So

$$
dp[l][r] = \min_{l \le k < r} \bigl( dp[l][k] + dp[k+1][r] + p_{l-1} p_k p_r \bigr).
$$

We fill the table by increasing interval length. For dimensions $[10, 20, 30, 40]$ (three matrices: $10\times20$, $20\times30$, $30\times40$) we compute:

- length 1: $dp[1][1]=dp[2][2]=dp[3][3]=0$
- length 2: $dp[1][2] = 10\cdot20\cdot30 = 6000$, $dp[2][3] = 20\cdot30\cdot40 = 24000$
- length 3: $dp[1][3] = \min( dp[1][1]+dp[2][3]+10\cdot20\cdot40,\; dp[1][2]+dp[3][3]+10\cdot30\cdot40 ) = \min(0+24000+8000,\; 6000+0+12000) = 18000$.

The optimal grouping is $(A_1 A_2) A_3$ with 18000 multiplications. This is exactly the problem _Matrix Chain Multiplication_. Time and space are $O(n^3)$ and $O(n^2)$.

```python
def matrix_chain_order(p):
    """p is list of dimensions, length n+1 for n matrices. Returns min cost."""
    n = len(p) - 1
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):
        for l in range(1, n - length + 2):
            r = l + length - 1
            dp[l][r] = float('inf')
            for k in range(l, r):
                cost = dp[l][k] + dp[k+1][r] + p[l-1] * p[k] * p[r]
                if cost < dp[l][r]:
                    dp[l][r] = cost
    return dp[1][n]

# dimensions: 10x20, 20x30, 30x40
assert matrix_chain_order([10, 20, 30, 40]) == 18000
```

```cpp
long long matrix_chain_order(vector<long long> p) {
    int n = (int)p.size() - 1;
    vector<vector<long long>> dp(n + 1, vector<long long>(n + 1, 0));
    for (int len = 2; len <= n; ++len) {
        for (int l = 1; l + len - 1 <= n; ++l) {
            int r = l + len - 1;
            dp[l][r] = LLONG_MAX;
            for (int k = l; k < r; ++k) {
                long long cost = dp[l][k] + dp[k+1][r] + p[l-1] * p[k] * p[r];
                if (cost < dp[l][r]) dp[l][r] = cost;
            }
        }
    }
    return dp[1][n];
}
```

## 7.2 Burst balloons and cutting a stick

Two problems that look different share the same interval DP skeleton: _Burst Balloons_ and _Minimum Cost to Cut a Stick_. In both, the natural first thought is to pick the first balloon to burst or the first cut to make. That leads to messy dependencies because the remaining pieces change shape. The trick is to think backwards: pick the **last** operation in the interval. When the last balloon in $(l, r)$ is burst, its left and right neighbors are fixed as the boundaries $l$ and $r$. When the last cut on a stick segment $(l, r)$ is made, the cost is simply the length of that segment, and the left and right subproblems become independent.

For _Burst Balloons_ we are given an array `nums`. We add virtual balloons with value 1 at both ends. Let $dp[l][r]$ be the maximum coins from bursting all balloons strictly between indices $l$ and $r$ (exclusive). The last balloon burst in this range is some $k$ with $l < k < r$. Its coins are $nums[l] \times nums[k] \times nums[r]$. So

$$
dp[l][r] = \max_{l < k < r} \bigl( dp[l][k] + dp[k][r] + nums[l] nums[k] nums[r] \bigr).
$$

For `nums = [3, 1, 5]` we extend to `[1, 3, 1, 5, 1]`, and the interval $(0,4)$ covers the whole array. Suppose the 5 is the last balloon to burst. Then the balloons 3 and 1 are burst first, between the boundaries 1 and 5. Bursting the 1 first gives $3\cdot1\cdot5=15$, then the 3 gives $1\cdot3\cdot5=15$, so that part is worth 30. The last balloon itself gives $1\cdot5\cdot1=5$, for a total of 35. Choosing the 3 as the last balloon gives only 33 and choosing the middle 1 gives only 9, so 35 is the best.

For _Minimum Cost to Cut a Stick_ we have a stick of length $n$ and cuts at positions `cuts`. Sort cuts, add 0 and $n$ as boundaries. $dp[l][r]$ = minimum cost to perform all cuts strictly between $l$ and $r$. The last cut at $k$ costs $cuts[r] - cuts[l]$ (the current segment length). So

$$
dp[l][r] = \min_{l < k < r} \bigl( dp[l][k] + dp[k][r] + cuts[r] - cuts[l] \bigr).
$$

For a stick of length 7 with cuts at [1,3,4,5], boundaries [0,1,3,4,5,7]. The interval (0,5) covers all cuts. Last cut at 3 (index 2): cost $7-0=7$ plus left (0,2) and right (2,5). This yields the optimal 16. Time and space for both are $O(m^3)$ and $O(m^2)$ where $m$ is the number of cuts or balloons.

```python
def max_coins(nums):
    """Burst Balloons: return max coins."""
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(3, n + 1):
        for l in range(0, n - length + 1):
            r = l + length - 1
            for k in range(l + 1, r):
                val = dp[l][k] + dp[k][r] + nums[l] * nums[k] * nums[r]
                if val > dp[l][r]:
                    dp[l][r] = val
    return dp[0][n-1]

def min_cost_cut_stick(n, cuts):
    """Minimum Cost to Cut a Stick."""
    cuts = sorted(cuts)
    cuts = [0] + cuts + [n]
    m = len(cuts)
    dp = [[0] * m for _ in range(m)]
    for length in range(3, m + 1):
        for l in range(0, m - length + 1):
            r = l + length - 1
            dp[l][r] = float('inf')
            for k in range(l + 1, r):
                cost = dp[l][k] + dp[k][r] + cuts[r] - cuts[l]
                if cost < dp[l][r]:
                    dp[l][r] = cost
    return dp[0][m-1]

assert max_coins([3, 1, 5, 8]) == 167
assert min_cost_cut_stick(7, [1, 3, 4, 5]) == 16
```

```cpp
int maxCoins(vector<int>& nums) {
    nums.insert(nums.begin(), 1);
    nums.push_back(1);
    int n = nums.size();
    vector<vector<int>> dp(n, vector<int>(n, 0));
    for (int len = 3; len <= n; ++len) {
        for (int l = 0; l + len - 1 < n; ++l) {
            int r = l + len - 1;
            for (int k = l + 1; k < r; ++k) {
                int val = dp[l][k] + dp[k][r] + nums[l] * nums[k] * nums[r];
                dp[l][r] = max(dp[l][r], val);
            }
        }
    }
    return dp[0][n-1];
}

int minCost(int n, vector<int>& cuts) {
    sort(cuts.begin(), cuts.end());
    cuts.insert(cuts.begin(), 0);
    cuts.push_back(n);
    int m = cuts.size();
    vector<vector<int>> dp(m, vector<int>(m, 0));
    for (int len = 3; len <= m; ++len) {
        for (int l = 0; l + len - 1 < m; ++l) {
            int r = l + len - 1;
            dp[l][r] = INT_MAX;
            for (int k = l + 1; k < r; ++k) {
                int cost = dp[l][k] + dp[k][r] + cuts[r] - cuts[l];
                dp[l][r] = min(dp[l][r], cost);
            }
        }
    }
    return dp[0][m-1];
}
```

## 7.3 Palindrome partitioning

In _Palindrome Partitioning II_ we want to cut a string into the fewest pieces so that every piece is a palindrome. For example, "aab" can be cut as "aa"|"b" (one cut) but not as "a"|"ab" because "ab" is not a palindrome. The minimum cuts for "aab" is 1.

A direct DP that tries every cut and checks palindrome on the fly would be $O(n^3)$. We can precompute a table `is_pal[l][r]` that tells whether substring $s[l..r]$ is a palindrome in $O(n^2)$ time: a substring is a palindrome if its ends match and the inside is a palindrome (or length $\le 2$). Then we do a 1D DP: $dp[i]$ = minimum cuts for prefix $s[0..i-1]$. We initialize $dp[0] = -1$ (so that a whole palindrome prefix gives 0 cuts). For each $i$ from 1 to $n$, we try every $j < i$; if $s[j..i-1]$ is a palindrome, we can cut before $j$ and get $dp[i] = \min(dp[i], dp[j] + 1)$.

For "aab": $n=3$. Palindromes: "a", "a", "b", "aa". $dp[0]=-1$. $i=1$: "a" is palindrome -> $dp[1]=dp[0]+1=0$. $i=2$: "a" -> $dp[2]=dp[1]+1=1$; "aa" -> $dp[2]=dp[0]+1=0$. $i=3$: "b" -> $dp[3]=dp[2]+1=1$; "ab" no; "aab" no. Answer $dp[3]=1$. Time $O(n^2)$, space $O(n^2)$ for the table (can be reduced to $O(n)$ with expand-around-center).

```python
def min_cut(s):
    """Palindrome Partitioning II: return min cuts."""
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n-1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_pal[i+1][j-1]):
                is_pal[i][j] = True
    dp = [0] * (n + 1)
    dp[0] = -1
    for i in range(1, n + 1):
        dp[i] = i - 1  # worst case: cut every char
        for j in range(i):
            if is_pal[j][i-1]:
                dp[i] = min(dp[i], dp[j] + 1)
    return dp[n]

assert min_cut("aab") == 1
assert min_cut("a") == 0
assert min_cut("ab") == 1
```

```cpp
int minCut(string s) {
    int n = s.size();
    vector<vector<bool>> is_pal(n, vector<bool>(n, false));
    for (int i = n - 1; i >= 0; --i) {
        for (int j = i; j < n; ++j) {
            if (s[i] == s[j] && (j - i <= 2 || is_pal[i+1][j-1]))
                is_pal[i][j] = true;
        }
    }
    vector<int> dp(n + 1, 0);
    dp[0] = -1;
    for (int i = 1; i <= n; ++i) {
        dp[i] = i - 1;
        for (int j = 0; j < i; ++j) {
            if (is_pal[j][i-1])
                dp[i] = min(dp[i], dp[j] + 1);
        }
    }
    return dp[n];
}
```

## 7.4 Longest valid parentheses

Given a string of '(' and ')', _Longest Valid Parentheses_ asks for the length of the longest contiguous substring that forms a valid parentheses sequence. A valid sequence is properly matched: every '(' has a matching ')' and they are correctly nested.

We can use DP where $dp[i]$ is the length of the longest valid substring **ending at index $i$** (0-based). If `s[i]` is an opening bracket `(`, then $dp[i]=0$, because a valid substring cannot end with an open bracket.

If `s[i]` is a closing bracket `)`, look at the valid block just before it, which ends at $i-1$ and has length $dp[i-1]$. The bracket that could match our `)` sits just before that block, at index $j = i - dp[i-1] - 1$. If $j \ge 0$ and `s[j]` is `(`, we found a match, and the new valid block is the old block, plus the two matching brackets, plus any valid block that ended right before $j$:

$$
dp[i] = dp[i-1] + 2 + dp[j-1] \quad (\text{use } 0 \text{ in place of } dp[j-1] \text{ when } j = 0).
$$

In every other case $dp[i]=0$.

Example: $s = $ `)()())`. We get $dp[0]=0$ and $dp[1]=0$. At $i=2$ the match is at $j=1$, so $dp[2]=0+2+0=2$. Then $dp[3]=0$. At $i=4$ we have $j=3$, so $dp[4]=0+2+dp[2]=4$. At $i=5$ we have $j=5-4-1=0$ and `s[0]` is `)`, so there is no match and $dp[5]=0$. The answer is the largest value, 4, for the block `()()`. Time $O(n)$, space $O(n)$.

```python
def longest_valid_parentheses(s):
    n = len(s)
    dp = [0] * n
    max_len = 0
    for i in range(1, n):
        if s[i] == ')':
            j = i - dp[i-1] - 1
            if j >= 0 and s[j] == '(':
                dp[i] = dp[i-1] + 2
                if j > 0:
                    dp[i] += dp[j-1]
                max_len = max(max_len, dp[i])
    return max_len

assert longest_valid_parentheses(")()())") == 4
assert longest_valid_parentheses("(()") == 2
assert longest_valid_parentheses("") == 0
```

```cpp
int longestValidParentheses(string s) {
    int n = s.size();
    vector<int> dp(n, 0);
    int max_len = 0;
    for (int i = 1; i < n; ++i) {
        if (s[i] == ')') {
            int j = i - dp[i-1] - 1;
            if (j >= 0 && s[j] == '(') {
                dp[i] = dp[i-1] + 2;
                if (j > 0) dp[i] += dp[j-1];
                max_len = max(max_len, dp[i]);
            }
        }
    }
    return max_len;
}
```

## 7.5 State machines: stock problems

Some DP problems are best understood as walking through a **state machine**. Each day we are in one of a few states (e.g., holding a stock, not holding, in cooldown), and we can transition between states by taking actions (buy, sell, rest). The DP value is the maximum profit reachable in each state after each day.

### Stock with Cooldown

After you sell, you must wait one day before buying again. Three states:

- `hold`: you own a stock.
- `not_hold`: you don't own a stock and can buy.
- `cooldown`: you just sold yesterday, cannot buy today.

Transitions:

- From `hold`: you can **rest** (stay in `hold`) or **sell** (go to `cooldown`).
- From `not_hold`: you can **rest** (stay) or **buy** (go to `hold`).
- From `cooldown`: you must **rest** (go to `not_hold`).

```
not_hold --buy--> hold --sell--> cooldown --rest--> not_hold
not_hold --rest--> not_hold          hold --rest--> hold
```

Let $h_i, n_i, c_i$ be max profit at end of day $i$ in each state. Initial: $h_0 = -price[0]$, $n_0 = 0$, $c_0 = -\infty$ (impossible). Recurrences:

$$
h_i = \max(h_{i-1}, n_{i-1} - price[i]) \\
c_i = h_{i-1} + price[i] \\
n_i = \max(n_{i-1}, c_{i-1})
$$

Answer is $\max(n_{last}, c_{last})$. This is exactly the problem _Stock with Cooldown_. Time $O(n)$, space $O(1)$.

### Stock with K Transactions

We are allowed at most $k$ buy-sell transactions. A transaction is a buy followed by a sell. We can have states for each transaction count and whether we hold. Let $hold[t]$ = max profit after $t$ transactions and currently holding a stock; $not\_hold[t]$ = max profit after $t$ transactions and not holding. A transaction is completed when we sell, so selling increments $t$. Recurrences for each day:

$$
hold[t] = \max(hold[t], not\_hold[t] - price) \quad \text{(buy doesn't change transaction count)} \\
not\_hold[t] = \max(not\_hold[t], hold[t-1] + price) \quad \text{(sell completes transaction t)}
$$

Initialize $hold[0] = -price[0]$, $hold[t>0] = -\infty$, $not\_hold[0] = 0$, $not\_hold[t>0] = -\infty$. Iterate $t$ from 1 to $k$ for sell transition. This is exactly the problem _Stock with K Transactions_. Time $O(nk)$, space $O(k)$.

```python
def max_profit_cooldown(prices):
    """Stock with Cooldown."""
    if not prices:
        return 0
    hold = -prices[0]
    not_hold = 0
    cooldown = float('-inf')
    for p in prices[1:]:
        hold, not_hold, cooldown = (
            max(hold, not_hold - p),
            max(not_hold, cooldown),
            hold + p
        )
    return max(not_hold, cooldown)

def max_profit_k_transactions(k, prices):
    """Stock with K Transactions."""
    if not prices or k == 0:
        return 0
    n = len(prices)
    if k >= n // 2:  # unlimited transactions
        return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))
    hold = [float('-inf')] * (k + 1)
    not_hold = [float('-inf')] * (k + 1)
    hold[0] = -prices[0]
    not_hold[0] = 0
    for p in prices[1:]:
        hold[0] = max(hold[0], not_hold[0] - p)
        for t in range(1, k + 1):
            hold[t] = max(hold[t], not_hold[t] - p)
            not_hold[t] = max(not_hold[t], hold[t-1] + p)
    return max(not_hold)

assert max_profit_cooldown([1,2,3,0,2]) == 3
assert max_profit_k_transactions(2, [3,2,6,5,0,3]) == 7
```

```cpp
int maxProfitCooldown(vector<int>& prices) {
    if (prices.empty()) return 0;
    int hold = -prices[0];
    int not_hold = 0;
    int cooldown = INT_MIN;
    for (int i = 1; i < (int)prices.size(); ++i) {
        int p = prices[i];
        int new_hold = max(hold, not_hold - p);
        int new_not_hold = max(not_hold, cooldown);
        int new_cooldown = hold + p;
        hold = new_hold;
        not_hold = new_not_hold;
        cooldown = new_cooldown;
    }
    return max(not_hold, cooldown);
}

int maxProfitKTransactions(int k, vector<int>& prices) {
    if (prices.empty() || k == 0) return 0;
    int n = prices.size();
    if (k >= n / 2) {
        int profit = 0;
        for (int i = 1; i < n; ++i)
            profit += max(0, prices[i] - prices[i-1]);
        return profit;
    }
    vector<int> hold(k + 1, INT_MIN);
    vector<int> not_hold(k + 1, INT_MIN);
    hold[0] = -prices[0];
    not_hold[0] = 0;
    for (int i = 1; i < n; ++i) {
        int p = prices[i];
        hold[0] = max(hold[0], not_hold[0] - p);
        for (int t = 1; t <= k; ++t) {
            hold[t] = max(hold[t], not_hold[t] - p);
            not_hold[t] = max(not_hold[t], hold[t-1] + p);
        }
    }
    return *max_element(not_hold.begin(), not_hold.end());
}
```

## 7.6 Egg drop

The _Egg Drop_ problem: given $k$ eggs and a building with $n$ floors, find the minimum number of moves (drops) in the worst case to determine the highest floor from which an egg won't break. The classic DP defines $dp[k][m]$ as the maximum number of floors we can check with $k$ eggs and $m$ moves. When we drop an egg from floor $x$, two things happen: if it breaks, we have $k-1$ eggs and $m-1$ moves left to check floors below $x$; if it survives, we have $k$ eggs and $m-1$ moves to check floors above $x$. So we can cover $dp[k-1][m-1]$ floors below, 1 floor at $x$, and $dp[k][m-1]$ floors above:

$$
dp[k][m] = dp[k-1][m-1] + dp[k][m-1] + 1.
$$

We want the smallest $m$ such that $dp[k][m] \ge n$. For $k=2, n=10$: $m=1$: $dp=1$; $m=2$: $dp=1+1+1=3$; $m=3$: $dp=2+3+1=6$; $m=4$: $dp=3+6+1=10$. So answer is 4 moves.

Alternatively, we can define $dp[k][n]$ as the minimum moves needed for $k$ eggs and $n$ floors. The recurrence tries every floor $x$:

$$
dp[k][n] = 1 + \min_{1 \le x \le n} \max(dp[k-1][x-1], dp[k][n-x]).
$$

This is $O(kn^2)$ and slower. The first formulation (counting floors by moves) is $O(k \cdot m)$ where $m$ is the answer, usually much smaller than $n$. Time $O(k \log n)$ roughly, space $O(k)$.

```python
def egg_drop(k, n):
    """Return min moves for k eggs, n floors."""
    dp = [0] * (k + 1)
    moves = 0
    while dp[k] < n:
        moves += 1
        for i in range(k, 0, -1):
            dp[i] = dp[i-1] + dp[i] + 1
    return moves

assert egg_drop(2, 10) == 4
assert egg_drop(1, 5) == 5
assert egg_drop(3, 14) == 4
```

```cpp
int eggDrop(int k, int n) {
    vector<int> dp(k + 1, 0);
    int moves = 0;
    while (dp[k] < n) {
        ++moves;
        for (int i = k; i >= 1; --i) {
            dp[i] = dp[i-1] + dp[i] + 1;
        }
    }
    return moves;
}
```

## 7.7 Job scheduling with profit

In _Job Scheduling with Profit_ we have jobs with start time, end time, and profit. We want to select a subset of non-overlapping jobs with maximum total profit. This is weighted interval scheduling.

Sort jobs by end time. Let $dp[i]$ be the maximum profit using the first $i$ jobs (1-indexed after sorting). For job $i$ with start $s_i$, end $e_i$, profit $p_i$, we find the last job $j < i$ with end time $\le s_i$. Then $dp[i] = \max(dp[i-1], p_i + dp[j])$. Finding $j$ can be done with binary search on the sorted end times.

Example: jobs = [(1,3,50), (2,5,20), (4,6,70), (6,7,60)]. Sorted by end: same order. Ends = [3,5,6,7].
$dp[0]=0$.
$i=1$: job (1,3,50), $j=0$ -> $dp[1]=50$.
$i=2$: job (2,5,20), $j=0$ -> $dp[2]=\max(50, 20)=50$.
$i=3$: job (4,6,70), $j=1$ (end 3 <= 4) -> $dp[3]=\max(50, 70+50)=120$.
$i=4$: job (6,7,60), $j=3$ (end 6 <= 6) -> $dp[4]=\max(120, 60+120)=180$.
Answer 180. Time $O(n \log n)$, space $O(n)$.

```python
from bisect import bisect_right

def job_scheduling(startTime, endTime, profit):
    """Job Scheduling with Profit."""
    jobs = sorted(zip(startTime, endTime, profit), key=lambda x: x[1])
    ends = [e for _, e, _ in jobs]
    n = len(jobs)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        s, e, p = jobs[i-1]
        # find rightmost job with end <= s
        j = bisect_right(ends, s, 0, i-1)
        dp[i] = max(dp[i-1], p + dp[j])
    return dp[n]

assert job_scheduling([1,2,4,6], [3,5,6,7], [50,20,70,60]) == 180
```

```cpp
int jobScheduling(vector<int>& startTime, vector<int>& endTime, vector<int>& profit) {
    int n = startTime.size();
    vector<array<int,3>> jobs(n);
    for (int i = 0; i < n; ++i)
        jobs[i] = {startTime[i], endTime[i], profit[i]};
    sort(jobs.begin(), jobs.end(), [](auto& a, auto& b) { return a[1] < b[1]; });
    vector<int> ends(n);
    for (int i = 0; i < n; ++i) ends[i] = jobs[i][1];
    vector<int> dp(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        int s = jobs[i-1][0];
        int p = jobs[i-1][2];
        int j = upper_bound(ends.begin(), ends.begin() + i - 1, s) - ends.begin();
        dp[i] = max(dp[i-1], p + dp[j]);
    }
    return dp[n];
}
```

## 7.8 Check yourself

1. In interval DP for matrix chain multiplication, what does the state $dp[l][r]$ represent, and why do we iterate by increasing interval length?
2. For Burst Balloons, why does thinking about the _last_ balloon to burst make the subproblems independent?
3. In the stock with cooldown state machine, why can't we transition directly from `cooldown` to `hold`?
4. In the egg drop problem, what is the meaning of $dp[k][m]$ in the "floors by moves" formulation, and why is it faster than the "moves by floors" formulation?

# Chapter 8. Sets as states: bitmask and profile DP

## 8.1 Sets stored in one integer

A set is just a collection where each item is either in or out. If we number the items $0, 1, 2, \dots$, we can write the answer for every item as a single bit: $1$ means the item is in the set, $0$ means it is not. An integer in most languages holds at least $32$ bits, so one `int` can store a set of up to $32$ items. In practice we stay near $20$ items because the number of subsets grows as $2^n$ and $2^{20} \approx 10^6$ is already a million states.

Let's see the three basic operations on a 5-bit set that represents the subset $\{1, 3\}$ of $\{0,1,2,3,4\}$. The binary pattern is `01010` (bit 1 and bit 3 are 1). In decimal that is $2^1 + 2^3 = 10$.

- **Test** if item $k$ is in the set: `mask & (1 << k)` is non-zero.
- **Add** item $k$: `mask | (1 << k)`.
- **Remove** item $k$: `mask & ~(1 << k)`.

Here is a tiny demonstration with the number $10$ (`01010`):

```python
def demo_bits():
    mask = 10          # binary 01010, set {1, 3}
    # test bit 1
    assert (mask & (1 << 1)) != 0
    # test bit 2
    assert (mask & (1 << 2)) == 0
    # add bit 0 -> set {0,1,3}
    mask2 = mask | (1 << 0)
    assert mask2 == 11     # 01011
    # remove bit 3 -> set {0,1}
    mask3 = mask2 & ~(1 << 3)
    assert mask3 == 3      # 00011
    return mask, mask2, mask3

demo_bits()
```

```cpp
// Bit operations on an integer mask
// test:  (mask & (1 << k)) != 0
// add:   mask | (1 << k)
// remove: mask & ~(1 << k)
```

## 8.2 The travelling salesman

The _Travelling Salesman_ problem asks: given $n$ cities and the cost to travel between each pair, find the cheapest tour that starts at city $0$, visits every other city exactly once, and returns to city $0$. This is exactly the problem _Travelling Salesman_.

A dynamic programming state needs to remember which cities have been visited and where we are now. A bitmask of length $n$ stores the visited set, and an integer $u$ stores the current city. The state is `dp[mask][u]` = minimum cost to start at $0$, visit exactly the cities in `mask`, and finish at $u$. The mask always includes $0$ and $u$.

Let's work through $n = 4$ cities with this cost matrix:

$$
\begin{array}{c|cccc}
 & 0 & 1 & 2 & 3 \\ \hline
0 & 0 & 10 & 15 & 20 \\
1 & 10 & 0 & 35 & 25 \\
2 & 15 & 35 & 0 & 30 \\
3 & 20 & 25 & 30 & 0
\end{array}
$$

We build the table bottom-up. There are $2^4 = 16$ masks but only those containing bit $0$ are reachable.

| mask (binary) | cities in mask | dp[mask][0] | dp[mask][1] | dp[mask][2] | dp[mask][3] |
| ------------- | -------------- | ----------- | ----------- | ----------- | ----------- |
| 0001          | {0}            | 0           | $\infty$    | $\infty$    | $\infty$    |
| 0011          | {0,1}          | $\infty$    | 10          | $\infty$    | $\infty$    |
| 0101          | {0,2}          | $\infty$    | $\infty$    | 15          | $\infty$    |
| 1001          | {0,3}          | $\infty$    | $\infty$    | $\infty$    | 20          |
| 0111          | {0,1,2}        | $\infty$    | 50          | 45          | $\infty$    |
| 1011          | {0,1,3}        | $\infty$    | 45          | $\infty$    | 35          |
| 1101          | {0,2,3}        | $\infty$    | $\infty$    | 50          | 45          |
| 1111          | {0,1,2,3}      | $\infty$    | 70          | 65          | 75          |

How did we get `dp[0111][1] = 50`? Cities {0,2} were visited before city 1, and we stood in city 2 (`dp[0101][2] = 15`). Going from 2 to 1 costs 35, so $15+35=50$. In general we remove the current city from the mask and try every possible previous city $v$ in what remains, keeping the smallest `dp[smaller mask][v] + cost[v][u]`.

The final answer is the minimum over $u$ of `dp[1111][u] + cost[u][0]`. Here `min(70+10, 65+15, 75+20) = 80`, which is the tour 0, 1, 3, 2, 0.

```python
def tsp_bitmask(dist):
    """dist is n x n matrix. Returns min tour cost starting and ending at 0."""
    n = len(dist)
    INF = 10**18
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0                     # mask 1 = only city 0 visited, at city 0
    for mask in range(1 << n):
        if not (mask & 1):           # city 0 must be in mask
            continue
        for u in range(n):
            if not (mask & (1 << u)):
                continue
            cur = dp[mask][u]
            if cur == INF:
                continue
            # try to go to a new city v
            for v in range(n):
                if mask & (1 << v):
                    continue
                nmask = mask | (1 << v)
                nd = cur + dist[u][v]
                if nd < dp[nmask][v]:
                    dp[nmask][v] = nd
    full = (1 << n) - 1
    ans = INF
    for u in range(n):
        if dp[full][u] < INF:
            ans = min(ans, dp[full][u] + dist[u][0])
    return ans

# Tiny test with the 4-city example above
dist4 = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
assert tsp_bitmask(dist4) == 80
```

```cpp
// Travelling Salesman with bitmask DP
// dist is n x n matrix, returns minimum tour cost starting and ending at 0
long long tsp_bitmask(vector<vector<long long>>& dist) {
    int n = dist.size();
    const long long INF = 4e18;
    vector<vector<long long>> dp(1 << n, vector<long long>(n, INF));
    dp[1][0] = 0;                     // mask 1 = only city 0 visited, at city 0
    for (int mask = 0; mask < (1 << n); ++mask) {
        if (!(mask & 1)) continue;    // city 0 must be in mask
        for (int u = 0; u < n; ++u) {
            if (!(mask & (1 << u))) continue;
            long long cur = dp[mask][u];
            if (cur == INF) continue;
            for (int v = 0; v < n; ++v) {
                if (mask & (1 << v)) continue;
                int nmask = mask | (1 << v);
                dp[nmask][v] = min(dp[nmask][v], cur + dist[u][v]);
            }
        }
    }
    int full = (1 << n) - 1;
    long long ans = INF;
    for (int u = 0; u < n; ++u) {
        if (dp[full][u] < INF)
            ans = min(ans, dp[full][u] + dist[u][0]);
    }
    return ans;
}
```

## 8.3 How much work bitmask DP is

The table has $2^n$ masks and $n$ choices for the current city, so $n 2^n$ states. For each state we try up to $n$ next cities. That gives $O(n^2 2^n)$ time. The memory is $O(n 2^n)$ for the table.

For $n = 20$, $2^{20} \approx 1.05 \times 10^6$ and $n^2 2^n \approx 4 \times 10^8$ operations, which runs in a couple of seconds in C++ and a bit slower in Python. For $n = 21$ it doubles, and for $n = 22$ it doubles again. So the practical limit is about $n = 20$ in contests.

If the graph is sparse we can iterate only over neighbors of $u$, but the worst case remains $O(n^2 2^n)$. This is exactly the complexity that makes the _Travelling Salesman_ solvable for $n \le 20$ with bitmask DP.

## 8.4 Profile DP for tilings

Now we switch to a different use of bitmasks: counting ways to tile an $n \times m$ rectangle with $2 \times 1$ dominoes. A domino covers two adjacent cells. We scan the grid row by row, cell by cell. The "profile" is the boundary between the already-tiled part and the rest. Because dominoes can stick out one cell into the next row, the profile is not a straight line; it is a _broken profile_.

Imagine we have finished some rows completely and are in the middle of row $x$. The mask has $m$ bits, one per column. Bit $j$ is $1$ if the cell $(x, j)$ is already occupied by a vertical domino coming from the row above, and $0$ if it is free. We also maintain a `next_mask` for the next row: when we place a vertical domino downward, we set the corresponding bit in `next_mask`.

Here is a tiny ASCII picture for $m = 3$. We are at row $x$, column $y = 1$. The current mask is `010` (column 1 is blocked from above). We try to fill the free cells.

```
Row x-1:  [ ][V][ ]   <- V means vertical domino going down
Row x:    [ ][X][ ]   <- X is blocked (bit 1 = 1), we are at column 1
          ^ y=1
```

At each cell $(x, y)$ we have two cases:

1. If the current mask has bit $y = 1$, the cell is already filled. We just move to $y+1$ with the same masks.
2. If bit $y = 0$, the cell is empty. We must cover it. Two choices:
   - Place a vertical domino downward: it occupies $(x,y)$ and $(x+1,y)$. So we set bit $y$ in `next_mask` and move to $y+1$.
   - Place a horizontal domino to the right: it needs $(x, y+1)$ also free (bit $y+1 = 0$ in current mask). Then we skip both cells and move to $y+2$.

When $y$ reaches $m$, the row is done. We add the accumulated ways to `dp[x+1][next_mask]` and start the next row with `next_mask` becoming the new current mask.

Let's trace a $2 \times 2$ board by hand. $n=2, m=2$. Start: `dp[0][0] = 1`.

Row 0, mask `00`:

- y=0, free. Try vertical: set next_mask bit 0 -> `01`, go to y=1.
  - y=1, free. Try vertical: set next_mask bit 1 -> `11`, go to y=2 (end row). Add to `dp[1][11]`.
  - y=1, free. Try horizontal: needs y+1=2 (out of bounds), skip.
- y=0, free. Try horizontal: needs y+1=1 free (yes). Go to y=2 (end row) with next_mask `00`. Add to `dp[1][00]`.

So after row 0: `dp[1][00] = 1`, `dp[1][11] = 1`.

Row 1, mask `00`:

- same as row 0, produces `dp[2][00] += 1`, `dp[2][11] += 1`.

Row 1, mask `11`:

- y=0 blocked, go to y=1.
- y=1 blocked, go to y=2 (end). Add to `dp[2][00] += 1`.

Final `dp[2][00] = 2`. Indeed a $2\times2$ board has 2 tilings (both horizontal or both vertical).

```python
def count_tilings(n, m):
    """Number of ways to tile n x m board with 2x1 dominoes."""
    dp = [[0] * (1 << m) for _ in range(n + 1)]
    dp[0][0] = 1

    def dfs(x, y, mask, next_mask):
        if y == m:
            dp[x + 1][next_mask] += dp[x][mask]
            return
        bit = 1 << y
        if mask & bit:                 # cell already occupied from above
            dfs(x, y + 1, mask, next_mask)
        else:
            # place vertical domino
            dfs(x, y + 1, mask, next_mask | bit)
            # place horizontal domino
            if y + 1 < m and not (mask & (bit << 1)):
                dfs(x, y + 2, mask, next_mask)

    for x in range(n):
        for mask in range(1 << m):
            if dp[x][mask]:
                dfs(x, 0, mask, 0)
    return dp[n][0]

# 2x2 -> 2, 2x3 -> 3, 3x2 -> 3
assert count_tilings(2, 2) == 2
assert count_tilings(2, 3) == 3
assert count_tilings(3, 2) == 3
```

```cpp
// Count tilings of n x m board with 2x1 dominoes using broken profile DP
long long count_tilings(int n, int m) {
    vector<vector<long long>> dp(n + 1, vector<long long>(1 << m, 0));
    dp[0][0] = 1;

    function<void(int,int,int,int)> dfs = [&](int x, int y, int mask, int next_mask) {
        if (y == m) {
            dp[x + 1][next_mask] += dp[x][mask];
            return;
        }
        int bit = 1 << y;
        if (mask & bit) {                     // cell already occupied from above
            dfs(x, y + 1, mask, next_mask);
        } else {
            // vertical domino
            dfs(x, y + 1, mask, next_mask | bit);
            // horizontal domino
            if (y + 1 < m && !(mask & (bit << 1)))
                dfs(x, y + 2, mask, next_mask);
        }
    };

    for (int x = 0; x < n; ++x)
        for (int mask = 0; mask < (1 << m); ++mask)
            if (dp[x][mask])
                dfs(x, 0, mask, 0);

    return dp[n][0];
}
```

The time complexity is $O(n \cdot 2^m \cdot m)$ because for each of the $n$ rows we iterate over $2^m$ masks and the recursion visits each column once. This works well when the smaller dimension $m$ is up to about $11$ ($2^{11} = 2048$). If $n$ is the smaller one, just transpose the board.

## 8.5 Check yourself

1. How many bits are needed to represent a subset of $\{0,1,\dots,19\}$?
2. In the TSP bitmask DP, what does `dp[mask][u]` store?
3. Why does the broken profile for domino tiling need a `next_mask` in addition to the current mask?
4. If a $3 \times 4$ board is tiled with dominoes, which dimension should be used as the mask width for faster DP?

# Chapter 9. Making a DP faster

## 9.1 When a DP is too slow

Imagine you want to split a sequence of numbers into a few contiguous groups. The cost of a group is some function of its elements, say the square of its sum. You want the minimum total cost over all ways to split the sequence into exactly _m_ groups. A natural dynamic programming state is `dp[i][j]` = minimum cost to split the first _j_ elements into _i_ groups. To compute `dp[i][j]` you try every possible place _k_ where the last group could start:

```
dp[i][j] = min over k ≤ j of ( dp[i-1][k-1] + cost(k, j) )
```

Here `cost(k, j)` is the cost of a group that covers elements _k_ through _j_. If you have _m_ rows and _n_ columns, there are _m·n_ states. For each state you might scan up to _n_ values of _k_, giving a total of _O(m n²)_ time. When _n_ is a few thousand, this is already too slow for a typical contest limit.

## 9.2 Divide and conquer optimization

The key observation is that for many cost functions the best split point _k_ for a fixed row _i_ does not jump around wildly. As _j_ increases, the optimal _k_ (let's call it `opt(i, j)`) either stays the same or moves to the right. In other words, `opt(i, j) ≤ opt(i, j+1)`. This **monotonicity** holds when the cost function satisfies the **quadrangle inequality**:

```
C(a, c) + C(b, d) ≤ C(a, d) + C(b, c)   for all a ≤ b ≤ c ≤ d
```

If this is true, we can compute a whole row much faster using divide and conquer. Instead of scanning all _k_ for every _j_, we pick the middle column `mid`, find its best `k` by scanning a limited range, and then recurse on the left and right halves. Because `opt` is monotone, the left half only needs to search `k` up to the `opt` we just found, and the right half only needs to search `k` from that `opt` onward.

```
         j indices:  0   1   2   3   4   5   6   7
                     |   |   |   |   |   |   |   |
                     v   v   v   v   v   v   v   v
         first call: compute(0, 7, 0, 7)
                       mid = 3, finds opt=2
                     /                   \
         left: compute(0, 2, 0, 2)      right: compute(4, 7, 2, 7)
                 mid = 1                     mid = 5
```

At each level of recursion the total length of all `k`‑ranges we scan is at most _n_, and there are _O(log n)_ levels. So one row takes _O(n log n)_ time, and the whole DP becomes _O(m n log n)_.

Here is a clean implementation. The function `divide_and_conquer_dp` computes one row given the previous row and a cost function `C(k, j)` (both 0‑indexed, inclusive). The driver `solve_dc` builds all _m_ rows.

```python
def divide_and_conquer_dp(dp_before, C, n):
    """Compute one DP row using divide and conquer optimization.
    dp_before[j] = dp(i-1, j) for j = 0..n-1.
    C(k, j) returns cost of segment [k, j] inclusive.
    Returns new list dp_cur of length n.
    """
    dp_cur = [0] * n

    def compute(l, r, optl, optr):
        if l > r:
            return
        mid = (l + r) // 2
        best_val = float('inf')
        best_k = -1
        # k can only lie in [optl, min(mid, optr)]
        for k in range(optl, min(mid, optr) + 1):
            prev = dp_before[k - 1] if k > 0 else 0
            val = prev + C(k, mid)
            if val < best_val:
                best_val = val
                best_k = k
        dp_cur[mid] = best_val
        compute(l, mid - 1, optl, best_k)
        compute(mid + 1, r, best_k, optr)

    compute(0, n - 1, 0, n - 1)
    return dp_cur


def solve_dc(m, n, C):
    """Return minimum cost to split n elements into m groups."""
    dp_before = [C(0, j) for j in range(n)]
    for _ in range(1, m):
        dp_before = divide_and_conquer_dp(dp_before, C, n)
    return dp_before[n - 1]


# --- tiny test: split [1,2,3,4] into 2 groups, cost = (sum)^2 ---
prefix = [0, 1, 3, 6, 10]
def C_sq(k, j):
    return (prefix[j + 1] - prefix[k]) ** 2

assert solve_dc(2, 4, C_sq) == 52   # 52 = (1+2+3)^2 + 4^2 = 36 + 16
```

```cpp
// Divide and conquer DP for one row
// dp_before: previous row, size n
// C(k, j): cost of segment [k, j] (0-indexed, inclusive)
// Returns dp_cur of size n
vector<long long> divide_and_conquer_dp(const vector<long long>& dp_before,
                                        function<long long(int,int)> C) {
    int n = dp_before.size();
    vector<long long> dp_cur(n);

    function<void(int,int,int,int)> compute = [&](int l, int r, int optl, int optr) {
        if (l > r) return;
        int mid = (l + r) >> 1;
        long long best_val = LLONG_MAX;
        int best_k = -1;
        for (int k = optl; k <= min(mid, optr); ++k) {
            long long prev = (k > 0) ? dp_before[k - 1] : 0;
            long long val = prev + C(k, mid);
            if (val < best_val) {
                best_val = val;
                best_k = k;
            }
        }
        dp_cur[mid] = best_val;
        compute(l, mid - 1, optl, best_k);
        compute(mid + 1, r, best_k, optr);
    };

    compute(0, n - 1, 0, n - 1);
    return dp_cur;
}

long long solve_dc(int m, int n, function<long long(int,int)> C) {
    vector<long long> dp_before(n);
    for (int j = 0; j < n; ++j) dp_before[j] = C(0, j);
    for (int i = 1; i < m; ++i) {
        dp_before = divide_and_conquer_dp(dp_before, C);
    }
    return dp_before[n - 1];
}
```

## 9.3 Knuth optimization

A different but related pattern appears in **interval DP**. The state is `dp[i][j]` for a subarray from _i_ to _j_, and the recurrence splits the interval at some _k_:

```
dp[i][j] = min over i ≤ k < j of ( dp[i][k] + dp[k+1][j] + C(i, j) )
```

Here `C(i, j)` is a cost that depends on the whole interval. Classic examples are optimal binary search trees, matrix chain multiplication, or merging stones. The naive triple loop runs in _O(n³)_.

Knuth discovered that if the cost function satisfies two conditions:

1. `C(b, c) ≤ C(a, d)` for `a ≤ b ≤ c ≤ d` (monotonicity),
2. `C(a, c) + C(b, d) ≤ C(a, d) + C(b, c)` (quadrangle inequality),

then the optimal split point `opt(i, j)` obeys

```
opt(i, j-1) ≤ opt(i, j) ≤ opt(i+1, j)
```

This means when we compute `dp[i][j]` we only need to try `k` between `opt(i, j-1)` and `opt(i+1, j)`. If we fill the table in decreasing order of _i_ and increasing order of _j_, those bounds are already known. The total number of iterations of the inner loop across the whole table telescopes to _O(n²)_, a full linear factor faster than _O(n³)_.

Below is a generic implementation. The base case `dp[i][i]` is usually 0 (a single element costs nothing to “merge”).

```python
def knuth_optimization(C, n):
    """Interval DP with Knuth optimization.
    C(i, j) returns cost for interval [i, j] inclusive (0-indexed).
    Returns (dp[0][n-1], opt_table).
    """
    dp = [[0] * n for _ in range(n)]
    opt = [[0] * n for _ in range(n)]
    for i in range(n):
        opt[i][i] = i
        dp[i][i] = 0          # base: single element

    for i in range(n - 2, -1, -1):      # i from n-2 down to 0
        for j in range(i + 1, n):       # j from i+1 up to n-1
            cost = C(i, j)
            best = float('inf')
            best_k = -1
            left = opt[i][j - 1]
            right = min(j - 1, opt[i + 1][j] if i + 1 < n else j - 1)
            for k in range(left, right + 1):
                val = dp[i][k] + dp[k + 1][j] + cost
                if val < best:
                    best = val
                    best_k = k
            dp[i][j] = best
            opt[i][j] = best_k
    return dp[0][n - 1], opt


# --- tiny test: merge [1,2,3,4] with cost = sum of interval ---
prefix = [0, 1, 3, 6, 10]
def C_sum(i, j):
    return prefix[j + 1] - prefix[i]

ans, _ = knuth_optimization(C_sum, 4)
assert ans == 19   # optimal merge cost: ((1+2)+3)+4 = 3+6+10 = 19
```

```cpp
// Knuth optimization for interval DP
// C(i, j): cost of interval [i, j] inclusive (0-indexed)
// Returns pair(dp[0][n-1], opt table)
pair<long long, vector<vector<int>>> knuth_optimization(
    function<long long(int,int)> C, int n) {

    vector<vector<long long>> dp(n, vector<long long>(n));
    vector<vector<int>> opt(n, vector<int>(n));

    for (int i = 0; i < n; ++i) {
        opt[i][i] = i;
        dp[i][i] = 0;
    }

    for (int i = n - 2; i >= 0; --i) {
        for (int j = i + 1; j < n; ++j) {
            long long cost = C(i, j);
            long long best = LLONG_MAX;
            int best_k = -1;
            int left = opt[i][j - 1];
            int right = min(j - 1, opt[i + 1][j]);
            for (int k = left; k <= right; ++k) {
                long long val = dp[i][k] + dp[k + 1][j] + cost;
                if (val < best) {
                    best = val;
                    best_k = k;
                }
            }
            dp[i][j] = best;
            opt[i][j] = best_k;
        }
    }
    return {dp[0][n - 1], opt};
}
```

## 9.4 Choosing a technique

Both optimizations rely on the quadrangle inequality, but they apply to different shapes of DP.

- **Divide and conquer DP** appears when you have a **sequence of rows** (like “split into _m_ groups”) and the transition is `dp[i][j] = min_{k≤j} (dp[i-1][k] + C(k, j))`. The monotone `opt` lets you compute a whole row in `O(n log n)`.
- **Knuth optimization** appears in **interval DP** where the transition is `dp[i][j] = min_{i≤k<j} (dp[i][k] + dp[k+1][j] + C(i, j))`. The double monotonicity `opt(i, j-1) ≤ opt(i, j) ≤ opt(i+1, j)` shrinks the inner loop to `O(n²)` total.

To decide which one fits, look at the recurrence:

- If the DP has a “previous row” and you add a segment at the end → divide and conquer.
- If the DP merges two adjacent sub‑intervals and adds a cost for the whole interval → Knuth.

## 9.5 Check yourself

1. What property of the cost function guarantees that the optimal split point `opt(i, j)` is non‑decreasing in `j` for divide and conquer DP?
2. In Knuth optimization, why does the inner loop run in `O(n²)` total instead of `O(n³)`?
3. You have a DP `dp[i][j] = min_{k<j} (dp[i-1][k] + (sum_{t=k+1}^j a_t)^2)`. Which optimization applies, and what is the resulting time complexity?
4. For an interval DP with `C(i, j) = max_{i≤t≤j} a_t`, does Knuth optimization apply? Why or why not?

# Chapter 10. Becoming fluent

## 10.1 A recipe for any DP

When you encounter a problem that might be solved with dynamic programming, follow these five plain steps. First, look for the smaller versions of the same problem; these are your _subproblems_. Second, give each subproblem a name; this name is called the _state_. For instance, if you need the best score up to position _i_, you could write `dp[i]` to mean “the best score using the first _i_ items”. Third, write down how to compute a state from already known states; this rule is the _recurrence_. Fourth, figure out the _base cases_, the simplest states you can answer directly without any recurrence. Fifth, decide the order in which you will fill the states: either start from the base cases and build up (called _bottom‑up_) or write a recursive function that remembers results (called _top‑down with memoization_). Following these steps turns a vague idea into a concrete plan you can code.

## 10.2 Common mistakes

Even when the recipe is clear, a few slip‑ups appear again and again:

- **Wrong base case** – forgetting the smallest input or giving it an incorrect value makes every later state wrong.
- **Wrong loop order** – in bottom‑up DP you must compute states in an order that guarantees every needed smaller state is already ready; looping backwards when you need forwards (or vice versa) breaks the recurrence.
- **Forgetting to reset** – when you reuse a DP table for multiple test cases, leftover values from the previous case pollute the new one.
- **Off by one** – an index that is one too large or too small shifts the whole table and often shows up as an out‑of‑bounds access or a wrong answer on the first or last element.

## 10.3 Testing against brute force

A great way to gain confidence in your DP is to run it side by side with a simple brute‑force solution on very small inputs. The brute force explores every possibility (often by plain recursion) and is too slow for large data, but for tiny _n_ it finishes instantly. If both agree on dozens of random tiny cases, the DP is almost certainly correct. Below is a complete Python script that does this for the classic “climbing stairs” problem: you can take 1 or 2 steps at a time, how many ways to reach step _n_? The DP uses a table, the brute force uses recursion, and the test harness compares them for _n_ up to 10.

```python
def dp_climb(n: int) -> int:
    """Return number of ways to climb n steps (1 or 2 at a time) using bottom‑up DP."""
    if n < 0:
        return 0
    dp = [0] * (n + 2)          # extra space avoids index checks for n=0,1
    dp[0] = 1                   # one way to stand at ground (do nothing)
    dp[1] = 1                   # one way to reach step 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def brute_climb(n: int) -> int:
    """Return number of ways by naive recursion (exponential time)."""
    if n < 0:
        return 0
    if n == 0:
        return 1
    return brute_climb(n - 1) + brute_climb(n - 2)


# Quick test: compare DP and brute for n = 0 .. 10
for n in range(11):
    assert dp_climb(n) == brute_climb(n), f"Mismatch at n={n}"
print("All small tests passed.")
```

```cpp
int dp_climb(int n) {
    if (n < 0) return 0;
    vector<int> dp(n + 2, 0);
    dp[0] = 1;
    dp[1] = 1;
    for (int i = 2; i <= n; ++i) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

int brute_climb(int n) {
    if (n < 0) return 0;
    if (n == 0) return 1;
    return brute_climb(n - 1) + brute_climb(n - 2);
}
```

Running the Python script prints “All small tests passed.”, a quick green light before you move to larger inputs.

## 10.4 Cheat sheet

| Problem type                   | Typical state                                                                     | Recurrence hint                                                 |
| ------------------------------ | --------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Longest Increasing Subsequence | `dp[i]` = length of LIS ending at index _i_                                       | `dp[i] = 1 + max(dp[j])` for all _j < i_ with `a[j] < a[i]`     |
| 0/1 Knapsack                   | `dp[i][w]` = max value using first _i_ items with weight limit _w_                | `dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] + val[i])`         |
| Edit Distance                  | `dp[i][j]` = min edits to turn first _i_ chars of _A_ into first _j_ chars of _B_ | `dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)` |
| Coin Change (min coins)        | `dp[x]` = min coins to make amount _x_                                            | `dp[x] = 1 + min(dp[x - c])` over all coin values _c_           |
| Maximum Subarray Sum           | `dp[i]` = max sum of subarray ending at _i_                                       | `dp[i] = max(a[i], dp[i-1] + a[i])`                             |

## 10.5 Check yourself

1. What are the five steps of the DP recipe in order?
2. Which mistake happens when you fill a DP table in the wrong direction?
3. Why is it useful to test a DP against a brute‑force solution on tiny inputs?
4. In the cheat sheet, what does `dp[i][w]` represent for the 0/1 Knapsack?

# Sources and credit

Several chapters adapt ideas from the articles on dynamic programming at [cp-algorithms.com](https://cp-algorithms.com) (intro to DP, knapsack, longest increasing subsequence, divide and conquer optimization, Knuth optimization, profile DP and the zero matrix problem). The text here is rewritten for beginners. Like the original, it is shared under the Creative Commons Attribution-ShareAlike 4.0 licence.
