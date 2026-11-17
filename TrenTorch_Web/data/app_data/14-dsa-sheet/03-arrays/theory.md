> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Arrays)

This page teaches you how to work with arrays, the simplest and most common way to store many values in a row. It starts with the plainest kind of work, walking through a list once and keeping a couple of notes, and ends with the tricks that solve the hardest array questions you will meet: three-number sums, intervals, matrices, and counting pairs with merge sort.

The page is a staircase. **Chapter 1 is deliberately gentle**: one loop, one or two variables, small lists you can check by eye. Every chapter after that adds one new idea and only uses what came before, so if a later chapter looks scary, just make sure the one before it feels comfortable. Every code example is shown in Python and in C++, so pick whichever language you like.

# Chapter 1. Walking through a list once

## 1.1 What an array is

An **array** is a row of boxes, each holding one value, numbered from 0. In Python we usually call it a list, and in C++ we use a `vector`. If `nums = [4, 9, 6]`, then `nums[0]` is 4, `nums[1]` is 9 and `nums[2]` is 6. The number inside the square brackets is called the **index** (or position).

The most useful thing you can do with an array is a **scan**: a single loop that looks at every value once, from left to right. While scanning, we usually keep a few small notes in ordinary variables, like "the biggest value so far". The rest of this chapter is just different notes you can keep.

```python
def largest(nums):
    best = nums[0]
    for x in nums:
        if x > best:
            best = x
    return best


assert largest([4, 9, 6]) == 9
assert largest([-5, -2, -8]) == -2
```

```cpp
int largest(const vector<int>& nums) {
    int best = nums[0];
    for (int x : nums) {
        if (x > best) best = x;
    }
    return best;
}
```

The loop runs $n$ times for a list of $n$ values, so the time is $O(n)$. We only keep one extra variable, so the extra space is $O(1)$. Here $O(n)$ just means "the work grows in step with the length of the list".

## 1.2 Keeping two notes at once

What if we want the second largest value, counting equal values only once? We keep two notes: `best` and `second`. When a new value `x` is bigger than `best`, the old best is demoted to second place. When `x` is not the best, is different from the best, and beats `second`, it takes the second place.

Let us watch it on `[4, 9, 9, 6]`. After `4`, best is 4. The `9` is bigger, so second becomes 4 and best becomes 9. The next `9` equals the best, so we ignore it. Finally `6` is not the best but beats 4, so second becomes 6. The answer is 6.

To say "nothing yet" we use a very small number, `NEG`, that no real value can be as small as.

```python
NEG = -10**18


def second_biggest(nums):
    best = second = NEG
    for x in nums:
        if x > best:
            second = best
            best = x
        elif x != best and x > second:
            second = x
    return -1 if second == NEG else second


assert second_biggest([4, 9, 9, 6]) == 6
assert second_biggest([5, 5, 5]) == -1
assert second_biggest([1, 2]) == 1
```

```cpp
int second_biggest(const vector<int>& nums) {
    const long long NEG = -1000000000000000000LL;
    long long best = NEG, second = NEG;
    for (int x : nums) {
        if (x > best) {
            second = best;
            best = x;
        } else if (x != best && x > second) {
            second = x;
        }
    }
    return second == NEG ? -1 : (int)second;
}
```

One pass, $O(n)$ time, $O(1)$ space. This is exactly the problem _Second Largest Value_.

## 1.3 Counting a streak

Another kind of note is a **running counter** that grows while something stays true and resets the moment it stops. Suppose we want the longest streak of one particular value in a row. We keep `run` (the current streak) and `best` (the longest streak so far). A matching value adds one to `run` and may improve `best`. Anything else resets `run` to 0.

For `[1, 1, 0, 1, 1, 1, 0]` and the value 1, the run grows to 2, resets at the 0, grows to 3, and resets again. The best is 3.

```python
def longest_streak(nums, target):
    best = run = 0
    for x in nums:
        if x == target:
            run += 1
            if run > best:
                best = run
        else:
            run = 0
    return best


assert longest_streak([1, 1, 0, 1, 1, 1, 0], 1) == 3
assert longest_streak([5, 5, 5], 7) == 0
```

```cpp
int longest_streak(const vector<int>& nums, int target) {
    int best = 0, run = 0;
    for (int x : nums) {
        if (x == target) {
            run++;
            if (run > best) best = run;
        } else {
            run = 0;
        }
    }
    return best;
}
```

Time $O(n)$, space $O(1)$. Counting the longest run of ones in a list of 0s and 1s is the same loop with `target = 1`. This is exactly the problem _Longest Run of Ones_.

## 1.4 Counting the drops

Sometimes the note is not about values but about how neighbours compare. A **drop** is a place where a value is larger than the one right after it. A sorted list in increasing order has no drops at all, because every next value is equal or bigger.

Now imagine the list written around a circle, so that after the last value we come back to the first one. Rotating a sorted list just moves where the circle is cut, so on that circle a sorted list, rotated or not, has at most one drop. For `[3, 4, 5, 1, 2]` the only drop is from 5 to 1; the step from 2 back to 3 goes up. For the plain sorted list `[1, 2, 3]` the only drop is the wrap-around from 3 back to 1. A list that is not a rotation of a sorted one has two or more drops. For example, `[2, 1, 3, 4]` drops from 2 to 1 and again from 4 back around to 2.

To look at the "next" value on a circle we use the remainder operator: the index after `i` is `(i + 1) % n`, which wraps back to 0 at the end.

```python
def count_drops_circular(nums):
    n = len(nums)
    drops = 0
    for i in range(n):
        if nums[i] > nums[(i + 1) % n]:
            drops += 1
    return drops


assert count_drops_circular([3, 4, 5, 1, 2]) == 1
assert count_drops_circular([2, 1, 3, 4]) == 2
assert count_drops_circular([1, 2, 3]) == 1
assert count_drops_circular([4, 4]) == 0
```

```cpp
int count_drops_circular(const vector<int>& nums) {
    int n = nums.size();
    int drops = 0;
    for (int i = 0; i < n; i++) {
        if (nums[i] > nums[(i + 1) % n]) drops++;
    }
    return drops;
}
```

So a list is a rotated sorted list exactly when it has at most one circular drop. Time $O(n)$, space $O(1)$. This is exactly the problem _Sorted, Maybe Rotated_.

## 1.5 Scanning from the right

Notes do not have to be kept left to right. Imagine houses in a row and you stand at the right end looking left. A house is visible if it is strictly taller than every house between you and it. So as we walk from right to left we only need one note: the tallest height seen so far. A house is visible when it beats that note.

For heights `[3, 7, 8, 3, 6, 1]`, walking from the right: 1 is visible, 6 is taller than 1 so visible, 3 is hidden by 6, 8 is visible, and 7 and 3 are hidden behind 8. Three houses are visible.

```python
def count_visible(heights):
    tallest = -10**18
    count = 0
    for i in range(len(heights) - 1, -1, -1):
        if heights[i] > tallest:
            count += 1
            tallest = heights[i]
    return count


assert count_visible([3, 7, 8, 3, 6, 1]) == 3
assert count_visible([5, 4, 3]) == 3
assert count_visible([]) == 0
```

```cpp
int count_visible(const vector<int>& heights) {
    long long tallest = -1000000000000000000LL;
    int count = 0;
    for (int i = (int)heights.size() - 1; i >= 0; i--) {
        if (heights[i] > tallest) {
            count++;
            tallest = heights[i];
        }
    }
    return count;
}
```

Time $O(n)$, space $O(1)$. A value that is greater than everything to its right is called a **leader**, and the visible houses above are exactly the leaders. If you need them in the original order, collect them while scanning and reverse at the end. A slow idea is to compare each value to everything after it, which costs $O(n^2)$. This is exactly the problem _Leaders in an Array_.

## 1.6 Remembering the best so far

The last kind of note is a **best-so-far** that lets us answer a question about pairs of positions in a single pass. Suppose a stock price list is `[5, 9, 4, 7, 2]` and we want the largest fall from an earlier day to a later day. For each day we only need the highest price seen before it: the fall ending today is `peak - today`. So we keep `peak` and the best fall.

Day by day: peak 5; price 9 (peak becomes 9); price 4, fall 5; price 7, fall 2; price 2, fall 7. The best fall is 7, from 9 down to 2.

```python
def biggest_fall(prices):
    if len(prices) < 2:
        return 0
    peak = prices[0]
    best = 0
    for x in prices[1:]:
        if peak - x > best:
            best = peak - x
        if x > peak:
            peak = x
    return best


assert biggest_fall([5, 9, 4, 7, 2]) == 7
assert biggest_fall([1, 2, 3]) == 0
```

```cpp
int biggest_fall(const vector<int>& prices) {
    if (prices.size() < 2) return 0;
    int peak = prices[0];
    int best = 0;
    for (size_t i = 1; i < prices.size(); i++) {
        best = max(best, peak - prices[i]);
        peak = max(peak, prices[i]);
    }
    return best;
}
```

Time $O(n)$, space $O(1)$. Now flip it around. For the largest **gain** from buying on one day and selling later, keep the lowest price seen so far instead and compare each day's price with it. That is exactly the problem _Best Time to Buy and Sell_. Trying every pair of days would cost $O(n^2)$.

## 1.7 Check yourself

1. In `second_biggest`, what happens to `second` when a new value beats `best`?
2. Why does `[3, 4, 5, 1, 2]` have one circular drop while `[2, 1, 3, 4]` has two?
3. When scanning from the right for leaders, which single note do we keep?
4. For the largest gain from a buy day to a later sell day, what do we remember while scanning left to right?

# Chapter 2. Two fingers on the list

## 2.1 A read finger and a write finger

Many problems ask us to rebuild a list by **keeping** some values and **dropping** others, with the kept values in the same order. The neat way is to use two fingers. The **read finger** `r` looks at every position once. The **write finger** `w` marks where the next kept value should be placed. Because `w` never moves ahead of `r`, we can safely write kept values on top of the old ones.

Suppose we want to remove every copy of a value `v`. Read each value; if it is not `v`, copy it to position `w` and move `w` one step. At the end the first `w` positions hold the answer.

```python
def keep_not(nums, v):
    out = list(nums)
    w = 0
    for r in range(len(out)):
        if out[r] != v:
            out[w] = out[r]
            w += 1
    return out[:w]


assert keep_not([3, 0, 5, 0, 0, 7], 0) == [3, 5, 7]
assert keep_not([2, 2], 2) == []
```

```cpp
vector<int> keep_not(const vector<int>& nums, int v) {
    vector<int> out = nums;
    int w = 0;
    for (int r = 0; r < (int)out.size(); r++) {
        if (out[r] != v) {
            out[w] = out[r];
            w++;
        }
    }
    out.resize(w);
    return out;
}
```

To move all copies of a value to the end instead of deleting them, keep the same loop and afterwards fill the positions from `w` to the end with that value. Time $O(n)$, space $O(1)$ extra apart from the copy we return. This is exactly the problem _Move Zeros to the End_.

```python
def move_to_end(nums, v):
    out = list(nums)
    w = 0
    for r in range(len(out)):
        if out[r] != v:
            out[w] = out[r]
            w += 1
    for i in range(w, len(out)):
        out[i] = v
    return out


assert move_to_end([3, 0, 5, 0, 7], 0) == [3, 5, 7, 0, 0]
assert move_to_end([1, 2], 9) == [1, 2]
```

```cpp
vector<int> move_to_end(const vector<int>& nums, int v) {
    vector<int> out = nums;
    int w = 0;
    for (int r = 0; r < (int)out.size(); r++) {
        if (out[r] != v) {
            out[w] = out[r];
            w++;
        }
    }
    for (int i = w; i < (int)out.size(); i++) out[i] = v;
    return out;
}
```

## 2.2 Using the sorted order

When the list is sorted, equal values sit side by side, which makes duplicates easy to spot. Say we want to keep every value but allow **at most two copies** of each. A value may be written if fewer than two values have been written so far, or if it differs from the value two places behind the write finger. That second value, `out[w-2]`, would be the same one if we already kept two copies.

For `[1, 1, 1, 2, 2, 3]`, the third 1 equals `out[w-2]` (which is 1), so it is dropped. The result is `[1, 1, 2, 2, 3]`.

```python
def keep_at_most_two(nums):
    out = list(nums)
    w = 0
    for r in range(len(out)):
        if w < 2 or out[r] != out[w - 2]:
            out[w] = out[r]
            w += 1
    return out[:w]


assert keep_at_most_two([1, 1, 1, 2, 2, 3]) == [1, 1, 2, 2, 3]
assert keep_at_most_two([4, 4, 4, 4]) == [4, 4]
```

```cpp
vector<int> keep_at_most_two(const vector<int>& nums) {
    vector<int> out = nums;
    int w = 0;
    for (int r = 0; r < (int)out.size(); r++) {
        if (w < 2 || out[r] != out[w - 2]) {
            out[w] = out[r];
            w++;
        }
    }
    out.resize(w);
    return out;
}
```

To keep only **one** copy of each value, ask the same question one step closer: write the value if `w == 0` or if it differs from `out[w-1]`. Time $O(n)$, space $O(1)$ extra. This is exactly the problem _Remove Duplicates From Sorted_.

## 2.3 Merging two sorted lists

With two sorted lists we can use one finger on each. Compare the two values under the fingers, take the smaller one, and move that finger forward. When one list runs out, copy the rest of the other. This is called a **merge**, and it keeps the result sorted.

```python
def merge_sorted(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


assert merge_sorted([1, 4, 4], [2, 4, 9]) == [1, 2, 4, 4, 4, 9]
assert merge_sorted([], [3]) == [3]
```

```cpp
vector<int> merge_sorted(const vector<int>& a, const vector<int>& b) {
    size_t i = 0, j = 0;
    vector<int> out;
    while (i < a.size() && j < b.size()) {
        if (a[i] <= b[j]) out.push_back(a[i++]);
        else out.push_back(b[j++]);
    }
    while (i < a.size()) out.push_back(a[i++]);
    while (j < b.size()) out.push_back(b[j++]);
    return out;
}
```

If the two lists have lengths $p$ and $q$, the time is $O(p+q)$. To get the **union** (every value from either list, each once), use the same loop but only append a value if it differs from the last value already in the output; the sortedness guarantees that equal values arrive one after another. This is exactly the problem _Union of Two Sorted Lists_. You will meet this merge loop again in Chapter 9.

## 2.4 Finding what two lists share

The same two fingers can find shared values. If `a[i] < b[j]`, then `a[i]` is too small to match anything left in `b`, so move `i`. If `a[i] > b[j]`, move `j`. If they are equal, we have found a match, so count it and move both fingers. Because a value that appears $x$ times in one list and $y$ times in the other can match only $\min(x, y)$ times, moving both fingers gives exactly the right number.

For `a = [1, 2, 2, 3]` and `b = [2, 2, 2, 3, 4]`, the matches are 2, 2 and 3, so there are 3.

```python
def count_shared(a, b):
    i = j = 0
    count = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1
        elif a[i] > b[j]:
            j += 1
        else:
            count += 1
            i += 1
            j += 1
    return count


assert count_shared([1, 2, 2, 3], [2, 2, 2, 3, 4]) == 3
assert count_shared([1, 5], [2, 6]) == 0
```

```cpp
int count_shared(const vector<int>& a, const vector<int>& b) {
    size_t i = 0, j = 0;
    int count = 0;
    while (i < a.size() && j < b.size()) {
        if (a[i] < b[j]) i++;
        else if (a[i] > b[j]) j++;
        else {
            count++;
            i++;
            j++;
        }
    }
    return count;
}
```

Time $O(p+q)$, space $O(1)$. If you collect the matched value instead of counting it, you get the list of common values. This is exactly the problem _Common Values of Two Sorted Lists_.

## 2.5 Filling slots in turn

The write-finger idea also works with **two** write fingers. Suppose we must place the even numbers in the even positions (0, 2, 4, ...) and the odd numbers in the odd positions (1, 3, 5, ...) while keeping each group in its original order. Make one finger `e` start at 0 and another finger `o` start at 1. Each even value goes to `e` and `e` jumps by 2. Each odd value goes to `o` and `o` jumps by 2.

For `[3, 1, 2, 4]`, the evens 2 and 4 go to positions 0 and 2, and the odds 3 and 1 go to positions 1 and 3. The result is `[2, 3, 4, 1]`.

```python
def weave_by_parity(nums):
    out = [0] * len(nums)
    e, o = 0, 1
    for x in nums:
        if x % 2 == 0:
            out[e] = x
            e += 2
        else:
            out[o] = x
            o += 2
    return out


assert weave_by_parity([3, 1, 2, 4]) == [2, 3, 4, 1]
```

```cpp
vector<int> weave_by_parity(const vector<int>& nums) {
    vector<int> out(nums.size());
    int e = 0, o = 1;
    for (int x : nums) {
        if (x % 2 == 0) {
            out[e] = x;
            e += 2;
        } else {
            out[o] = x;
            o += 2;
        }
    }
    return out;
}
```

This works only when both groups have the same size. When the groups can differ in size, as in the sheet problem, first split the list into two lists (one per group, each in order), and then walk both lists together, taking one value from each in turn until one runs out and then adding the rest of the other. Either way it is one pass, $O(n)$ time. This is exactly the problem _Rearrange by Sign_.

## 2.6 Check yourself

1. In `keep_not`, why is it safe to overwrite positions that the read finger has already passed?
2. For keeping at most two copies, what do we compare the new value with?
3. In the shared-values walk, why do we move only the finger holding the smaller value when the two values differ?
4. Why does the weaving trick need the two groups to be the same size?

# Chapter 3. Sums and XOR tricks

## 3.1 Using a formula for the total

Sometimes the answer is hiding in a total. The numbers $1, 2, \dots, n$ add up to a famous value:

$$1 + 2 + \dots + n = \frac{n(n+1)}{2}$$

If a list should contain all of $1..n$ but one is missing, then the expected total minus the real total is exactly the missing value. For `[1, 2, 4, 5]` the list has 4 values, so $n = 5$, the expected total is 15, the actual total is 12, and the missing number is 3.

```python
def missing_from_one_to_n(nums):
    n = len(nums) + 1
    return n * (n + 1) // 2 - sum(nums)


assert missing_from_one_to_n([1, 2, 4, 5]) == 3
assert missing_from_one_to_n([2, 3]) == 1
```

```cpp
long long missing_from_one_to_n(const vector<int>& nums) {
    long long n = nums.size() + 1;
    long long total = 0;
    for (int x : nums) total += x;
    return n * (n + 1) / 2 - total;
}
```

Time $O(n)$, space $O(1)$. In C++ we use `long long` because the total can be too large for an `int`. When the list holds the numbers from $0$ to $n$ with one missing, the same idea works with the expected total $n(n+1)/2$ for the range $0..n$ (zero adds nothing). This is exactly the problem _Find the Missing Number_.

## 3.2 XOR, the cancelling operator

**XOR**, written `^`, combines two numbers bit by bit. For each bit position, the result is 1 when the two bits differ and 0 when they are the same. For example, $5 = 101_2$ and $3 = 011_2$, so $5 \oplus 3 = 110_2 = 6$.

Two facts make XOR powerful. First, a number XORed with itself is zero ($a \oplus a = 0$). Second, XOR with zero changes nothing ($a \oplus 0 = a$). Also the order does not matter. So if we XOR a whole list in which every value appears twice, all the pairs cancel and the result is 0. If one value appears an odd number of times, only that value is left.

Take `[4, 7, 4, 9, 9]`. The two 4s cancel, the two 9s cancel, and 7 remains.

```python
def odd_one_out(nums):
    result = 0
    for x in nums:
        result ^= x
    return result


assert odd_one_out([4, 7, 4, 9, 9]) == 7
assert odd_one_out([3]) == 3
```

```cpp
int odd_one_out(const vector<int>& nums) {
    int result = 0;
    for (int x : nums) result ^= x;
    return result;
}
```

Time $O(n)$, space $O(1)$, with no dictionary needed. This is exactly the problem _The Number That Appears Once_. XOR can also find a missing number: XOR all of $1..n$ together with all the values in the list, and every value present cancels, leaving the missing one.

## 3.3 Two unknowns need two equations

Now two numbers are wrong at once: one value in $1..n$ appears twice (call it $r$, for repeated) and another is missing (call it $m$). One total gives only one equation. Let $d$ be the real sum minus the expected sum. Then

$$d = r - m$$

A second fact gives a second equation: compare the sum of squares of the real list with the sum of squares $1^2 + \dots + n^2$. Let $e$ be that difference. Then

$$e = r^2 - m^2 = (r - m)(r + m) = d\,(r+m)$$

So $r + m = e / d$, and then $r = \frac{d + e/d}{2}$ and $m = r - d$. For `[1, 2, 2, 4, 5]` the real sum is 14 and the expected sum is 15, so $d = -1$. The real squares add to 50 and the expected add to 55, so $e = -5$. Then $r + m = 5$, giving $r = 2$ and $m = 3$.

```python
def solve_two(d, e):
    total = e // d
    r = (d + total) // 2
    return r, r - d


assert solve_two(-1, -5) == (2, 3)
assert solve_two(2, 10) == (3, 1)
```

```cpp
pair<long long, long long> solve_two(long long d, long long e) {
    long long total = e / d;
    long long r = (d + total) / 2;
    return {r, r - d};
}
```

Computing $d$ and $e$ takes one pass, so the whole method is $O(n)$ time and $O(1)$ space. In C++ use `long long`, because squares add up fast. This is exactly the problem _Repeating and Missing Number_: you compute $d$ and $e$ from the list and then solve as above.

## 3.4 Check yourself

1. What is the sum of $1..n$ for $n = 6$, and how does it help find a missing value?
2. What is $9 \oplus 9$, and what is $9 \oplus 0$?
3. If every value in a list appears twice except one, what does XORing the whole list give?
4. Why does one equation (the sum) not suffice when two numbers are wrong?

# Chapter 4. Prefix sums and windows

## 4.1 Prefix sums

Suppose we are asked many times "what is the sum of the values from position $l$ to position $r$?" Adding them up each time costs $O(n)$ per question. Instead we prepare a list once. The **prefix sum** list has one more entry than the data: `prefix[i]` is the sum of the first `i` values, with `prefix[0] = 0`.

For `[3, 1, 4, 1, 5]` the prefix list is `[0, 3, 4, 8, 9, 14]`. The sum from position 1 to position 3 (that is 1, 4, 1) is `prefix[4] - prefix[1] = 9 - 3 = 6`. In general, the sum of positions $l..r$ inclusive is

$$\text{prefix}[r+1] - \text{prefix}[l]$$

```python
def build_prefix(nums):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    return prefix


def range_sum(prefix, l, r):
    return prefix[r + 1] - prefix[l]


p = build_prefix([3, 1, 4, 1, 5])
assert p == [0, 3, 4, 8, 9, 14]
assert range_sum(p, 1, 3) == 6
```

```cpp
vector<long long> build_prefix(const vector<int>& nums) {
    vector<long long> prefix(1, 0);
    for (int x : nums) prefix.push_back(prefix.back() + x);
    return prefix;
}

long long range_sum(const vector<long long>& prefix, int l, int r) {
    return prefix[r + 1] - prefix[l];
}
```

Building takes $O(n)$ once; every query afterwards takes $O(1)$. The key habit to learn is this: **a sum of a run is a difference of two prefix sums.** Almost everything in this chapter and the next uses that sentence.

## 4.2 Left sum equals right sum

Let us count the places to cut a list into a non-empty left part and a non-empty right part so that both parts have the same sum. If the cut is after the first `c` values, the left sum is `prefix[c]` and the right sum is `total - prefix[c]`. We just compare them.

For `[1, 2, 3, 0, 6]` the total is 12 and the prefix sums are 1, 3, 6, 6, 12. Cuts after 3 values and after 4 values both leave 6 on each side, so the answer is 2.

```python
def equal_cuts(nums):
    prefix = build_prefix(nums)
    total = prefix[-1]
    count = 0
    for c in range(1, len(nums)):
        if prefix[c] == total - prefix[c]:
            count += 1
    return count


assert equal_cuts([1, 2, 3, 0, 6]) == 2
assert equal_cuts([1, 2]) == 0
```

```cpp
int equal_cuts(const vector<int>& nums) {
    int n = nums.size();
    vector<long long> prefix(n + 1, 0);
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
    long long total = prefix[n];
    int count = 0;
    for (int c = 1; c < n; c++) {
        if (prefix[c] == total - prefix[c]) count++;
    }
    return count;
}
```

Time $O(n)$, space $O(n)$. You can even skip the list: keep a running left sum and compute the right sum as `total - left - nums[i]` when the middle value is excluded. The same idea solves the sheet question, where the position `i` itself belongs to neither side. The slow way, adding both sides for every position, is $O(n^2)$.

## 4.3 A window that grows and shrinks

Prefix sums handle any numbers, but when all values are **zero or positive** there is an even simpler tool: a **window**, which is a run of neighbouring values marked by a left finger and a right finger. Adding a value on the right can only increase the sum, and removing a value on the left can only decrease it. That predictability lets us slide the window without ever going back.

As an example, find the length of the shortest run whose sum is at least a positive `target`. Move the right finger one step at a time, adding that value. While the window sum is at least the target, record the window length and then shrink from the left. For `[2, 3, 1, 2, 4, 3]` and target 7, the window `[4, 3]` (length 2) works and nothing shorter does.

```python
def shortest_at_least(nums, target):
    best = 0
    left = 0
    window = 0
    for right in range(len(nums)):
        window += nums[right]
        while window >= target and left <= right:
            length = right - left + 1
            if best == 0 or length < best:
                best = length
            window -= nums[left]
            left += 1
    return best


assert shortest_at_least([2, 3, 1, 2, 4, 3], 7) == 2
assert shortest_at_least([1, 1], 5) == 0
```

```cpp
int shortest_at_least(const vector<int>& nums, long long target) {
    int best = 0, left = 0;
    long long window = 0;
    for (int right = 0; right < (int)nums.size(); right++) {
        window += nums[right];
        while (window >= target && left <= right) {
            int length = right - left + 1;
            if (best == 0 || length < best) best = length;
            window -= nums[left];
            left++;
        }
    }
    return best;
}
```

Each finger moves only forward, so each value is added once and removed at most once. Time is $O(n)$, space $O(1)$. For the longest run with sum **exactly** `k` (all values non-negative), shrink the window from the left while the sum is **greater than** `k`, and whenever the sum equals `k` record the window length. This is exactly the problem _Longest Subarray With Sum K_.

The window needs non-negative values. If negative values are allowed, adding a value can make the sum go down, so we cannot know when to shrink. Chapter 5 fixes that with prefix sums and a dictionary.

## 4.4 Check yourself

1. For `[2, 5, 1]`, what is the prefix sum list?
2. How do you get the sum of positions 2 to 4 from the prefix list?
3. Why is it fine for the window method that both fingers only move to the right?
4. Why does the window method break when negative numbers are allowed?

# Chapter 5. Prefix sums with a dictionary

## 5.1 A quick look at dictionaries

A **dictionary** (Python `dict`, C++ `unordered_map`) stores pairs of a key and a value, and looks up a key almost instantly: on average the cost is $O(1)$ no matter how many pairs are stored. A **set** is like a dictionary with keys only. They are the main tool of the next step of this course (hashing), so here we only need three moves: ask "is this key present?", read the value for a key, and update it.

As a first use, let us ask: does a list contain two values whose difference is exactly `d` (with `d` greater than 0)? Scan the list and keep a set of values seen. For the current value `x`, a partner exists if `x - d` or `x + d` is already in the set.

```python
def has_pair_diff(nums, d):
    seen = set()
    for x in nums:
        if x - d in seen or x + d in seen:
            return True
        seen.add(x)
    return False


assert has_pair_diff([8, 1, 5, 11], 3) is True
assert has_pair_diff([8, 1, 5, 11], 2) is False
```

```cpp
bool has_pair_diff(const vector<int>& nums, int d) {
    unordered_set<int> seen;
    for (int x : nums) {
        if (seen.count(x - d) || seen.count(x + d)) return true;
        seen.insert(x);
    }
    return false;
}
```

Time $O(n)$ on average, space $O(n)$. Without the set, we would compare every pair at $O(n^2)$.

## 5.2 Looking back for a partner

Now let us count pairs of positions $i < j$ with `nums[i] + nums[j] == target`. When we stand at `j`, the partner we need is `target - nums[j]`, and it must have appeared earlier. So we keep a dictionary of how many times each value has appeared so far.

```python
def count_pairs_sum(nums, target):
    seen = {}
    total = 0
    for x in nums:
        total += seen.get(target - x, 0)
        seen[x] = seen.get(x, 0) + 1
    return total


assert count_pairs_sum([1, 5, 3, 3, 3], 6) == 4
assert count_pairs_sum([2, 2, 2], 4) == 3
```

```cpp
long long count_pairs_sum(const vector<int>& nums, int target) {
    unordered_map<int, int> seen;
    long long total = 0;
    for (int x : nums) {
        auto it = seen.find(target - x);
        if (it != seen.end()) total += it->second;
        seen[x]++;
    }
    return total;
}
```

Time $O(n)$ on average. For `[1, 5, 3, 3, 3]` and target 6, the pair (1, 5) gives one, and each 3 pairs with the earlier 3s: 0 + 1 + 2 = 3 more, for 4 in total.

The sheet question wants the pair `[i, j]` with the **smallest `i`**, and then the smallest `j`. A subtle point: scanning left to right and stopping at the first `j` that finds a partner gives the smallest `j`, not necessarily the smallest `i`. For `[1, 3, 5, 7]` and target 8, the scan first closes a pair at `j = 2` (the pair of indices 1 and 2, values 3 and 5), but the pair at indices 0 and 3 (values 1 and 7) has the smaller `i`, so it wins. The safe method is to remember the first index of each value, try every `j`, and keep the best pair `(i, j)` by comparing `i` first and then `j`. This is exactly the problem _Two Sum: First Pair_.

## 5.3 A set for neighbours in value

Sets also help when we care about numbers that are neighbours in **value**, such as 4, 5, 6. Take the numbers `[10, 4, 5, 11, 12, 1]`. They form groups of consecutive numbers: `{1}`, `{4, 5}` and `{10, 11, 12}`. To find where each group starts, look for a number `x` whose predecessor `x - 1` is **not** in the set. Then walk upward while `y + 1` is in the set to measure the group.

```python
def group_sizes(nums):
    s = set(nums)
    sizes = []
    for x in s:
        if x - 1 not in s:
            y = x
            while y + 1 in s:
                y += 1
            sizes.append(y - x + 1)
    return sorted(sizes)


assert group_sizes([10, 4, 5, 11, 12, 1]) == [1, 2, 3]
assert group_sizes([]) == []
```

```cpp
vector<int> group_sizes(const vector<int>& nums) {
    unordered_set<int> s(nums.begin(), nums.end());
    vector<int> sizes;
    for (int x : s) {
        if (!s.count(x - 1)) {
            int y = x;
            while (s.count(y + 1)) y++;
            sizes.push_back(y - x + 1);
        }
    }
    sort(sizes.begin(), sizes.end());
    return sizes;
}
```

Why is this fast? We only start walking at the beginning of a group, so every number is stepped over by exactly one walk. The total work is $O(n)$ on average. Sorting would cost $O(n \log n)$. The longest consecutive run is just the largest size. This is exactly the problem _Longest Consecutive Sequence_.

## 5.4 Prefix sums and counting

Here is the big idea of this chapter. Take any run from position $l$ to $r$. Its sum is `prefix[r+1] - prefix[l]`. So the run has sum $k$ exactly when

$$\text{prefix}[r+1] - \text{prefix}[l] = k \quad\Longleftrightarrow\quad \text{prefix}[l] = \text{prefix}[r+1] - k$$

Walking forward, at each new prefix sum we ask: how many earlier prefix sums equal "current minus $k$"? Each one is the start of a valid run ending here. A dictionary that counts earlier prefix sums answers this instantly, with no condition on signs: negative numbers are fine.

Let us see it for a simpler target: count runs of a 0/1 list that have equally many 0s and 1s. Replace each 0 by $-1$. A balanced run is then one with sum 0, so $k = 0$ and we look for earlier prefix sums that are **equal** to the current one. The dictionary starts as `{0: 1}`, which stands for the empty prefix.

For `[1, 0, 1, 0]` the running sums are 1, 0, 1, 0. At the second step, the value 0 was seen once before (the empty prefix), so one run ends there. At the third step 1 was seen once. At the fourth step 0 was seen twice. In total $1 + 1 + 2 = 4$ balanced runs.

```python
def count_balanced(bits):
    seen = {0: 1}
    prefix = 0
    total = 0
    for b in bits:
        prefix += 1 if b == 1 else -1
        total += seen.get(prefix, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return total


assert count_balanced([1, 0, 1, 0]) == 4
assert count_balanced([1, 1, 1]) == 0
```

```cpp
long long count_balanced(const vector<int>& bits) {
    unordered_map<int, int> seen;
    seen[0] = 1;
    int prefix = 0;
    long long total = 0;
    for (int b : bits) {
        prefix += (b == 1) ? 1 : -1;
        auto it = seen.find(prefix);
        if (it != seen.end()) total += it->second;
        seen[prefix]++;
    }
    return total;
}
```

For a general target $k$, the only change is to look up `prefix - k` instead of `prefix`, and to add the current `prefix` to the dictionary after counting. Time $O(n)$ on average, space $O(n)$. The slow way tries every start and end at $O(n^2)$. This is exactly the problem _Subarrays With Sum K_.

## 5.5 The longest run with any signs

To find the **longest** run, count is not enough: we want the earliest place a prefix sum appeared, because an earlier start makes a longer run. So the dictionary stores, for each prefix sum, the **first index** where it appeared. When the same prefix sum shows up again at index $i$, the run between those two places has sum 0 (or, with a target $k$, we look up `prefix - k`), and its length is $i$ minus the stored index. We never overwrite a stored index, because the first one is the best.

Again with the balanced 0/1 example: for `[1, 1, 0, 0, 1]` the running sums are 1, 2, 1, 0, 1. We start with `{0: -1}` (the empty prefix sits just before index 0). The sum 1 repeats at index 2, giving length $2 - 0 = 2$. The sum 0 at index 3 matches the start, giving $3 - (-1) = 4$. The sum 1 at index 4 gives $4 - 0 = 4$. The best length is 4.

```python
def longest_balanced(bits):
    first = {0: -1}
    prefix = 0
    best = 0
    for i, b in enumerate(bits):
        prefix += 1 if b == 1 else -1
        if prefix in first:
            best = max(best, i - first[prefix])
        else:
            first[prefix] = i
    return best


assert longest_balanced([1, 1, 0, 0, 1]) == 4
assert longest_balanced([1, 1]) == 0
```

```cpp
int longest_balanced(const vector<int>& bits) {
    unordered_map<int, int> first;
    first[0] = -1;
    int prefix = 0, best = 0;
    for (int i = 0; i < (int)bits.size(); i++) {
        prefix += (bits[i] == 1) ? 1 : -1;
        auto it = first.find(prefix);
        if (it != first.end()) best = max(best, i - it->second);
        else first[prefix] = i;
    }
    return best;
}
```

Time $O(n)$ on average, space $O(n)$. For the sheet question you look up `prefix - k` in the dictionary, and you store `prefix` only if it is not stored yet. This is exactly the problem _Longest Subarray With Sum K, Any Values_.

## 5.6 Prefix XOR

The same trick works with XOR in place of sum, because XOR also cancels. Let `px[i]` be the XOR of the first `i` values. The XOR of the run from $l$ to $r$ is `px[r+1] ^ px[l]`, since the shared first part cancels itself. So the run has XOR $k$ exactly when `px[l] = px[r+1] ^ k`.

As an example, count the runs whose XOR is 0. We look for earlier prefix XORs equal to the current one. For `[5, 5, 5]` the prefix XORs are 0, 5, 0, 5, and the runs are `[5, 5]` twice, so the answer is 2.

```python
def count_xor_zero(nums):
    seen = {0: 1}
    px = 0
    total = 0
    for v in nums:
        px ^= v
        total += seen.get(px, 0)
        seen[px] = seen.get(px, 0) + 1
    return total


assert count_xor_zero([5, 5, 5]) == 2
assert count_xor_zero([1, 2, 3]) == 1
```

```cpp
long long count_xor_zero(const vector<int>& nums) {
    unordered_map<int, int> seen;
    seen[0] = 1;
    int px = 0;
    long long total = 0;
    for (int v : nums) {
        px ^= v;
        auto it = seen.find(px);
        if (it != seen.end()) total += it->second;
        seen[px]++;
    }
    return total;
}
```

For a general $k$, look up `px ^ k` instead of `px`, and record `px` afterwards. Time $O(n)$ on average. This is exactly the problem _Subarrays With XOR K_.

## 5.7 Check yourself

1. Why does `seen` start as `{0: 1}` in the counting versions?
2. When counting runs with sum $k$, which earlier prefix sum do we look for?
3. For the longest run, why do we keep the first index of a prefix sum and never overwrite it?
4. Why does XOR need no subtraction to get the XOR of a run?

# Chapter 6. Best runs and majority votes

## 6.1 Kadane, the best run

The **maximum subarray** problem asks for the contiguous run with the largest sum, where values may be negative. A clever one-pass method is named after **Kadane**. At each position keep `cur`, the best sum of a run that **ends here**. A run ending here is either just this one value (a fresh start) or the best run ending at the previous position with this value added. So

$$\text{cur}_i = \max(x_i,\ \text{cur}_{i-1} + x_i)$$

and the answer is the largest `cur` ever seen. Put simply: if the run so far has a negative sum, it can only hurt, so throw it away and start again.

For `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` the best run is `4, -1, 2, 1` with sum 6.

```python
def best_sum(nums):
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


assert best_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
assert best_sum([-3, -1, -2]) == -1
```

```cpp
long long best_sum(const vector<int>& nums) {
    long long cur = nums[0], best = nums[0];
    for (size_t i = 1; i < nums.size(); i++) {
        cur = max((long long)nums[i], cur + nums[i]);
        best = max(best, cur);
    }
    return best;
}
```

Time $O(n)$, space $O(1)$. To also learn where the best run is, remember where the current run started. Restart (set `begin = i`) only when the sum so far is **below zero**, and update the best only when the current sum is **strictly greater** than the best. That keeps the earliest start, and a shorter run wins on ties. Here is the full version returning the sum and both ends:

```python
def best_run(nums):
    best = [nums[0], 0, 0]
    cur = nums[0]
    begin = 0
    for i in range(1, len(nums)):
        if cur < 0:
            cur = nums[i]
            begin = i
        else:
            cur += nums[i]
        if cur > best[0]:
            best = [cur, begin, i]
    return best


assert best_run([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == [6, 3, 6]
assert best_run([0, 5]) == [5, 0, 1]
```

```cpp
vector<long long> best_run(const vector<int>& nums) {
    vector<long long> best = {nums[0], 0, 0};
    long long cur = nums[0];
    int begin = 0;
    for (int i = 1; i < (int)nums.size(); i++) {
        if (cur < 0) {
            cur = nums[i];
            begin = i;
        } else {
            cur += nums[i];
        }
        if (cur > best[0]) best = {cur, begin, i};
    }
    return best;
}
```

This is exactly the problem _Maximum Subarray With Its Range_.

## 6.2 Products need a minimum too

For products, the same idea has a catch: multiplying by a negative number flips big into small. A very negative product can become the largest after the next negative value. So at each position we track **two** numbers: the largest product of a run ending here (`hi`) and the smallest (`lo`). The new pair comes from three candidates: the value alone, `hi * x`, and `lo * x`.

To see it at work, here is a helper that returns the pair for every position. For `[2, 3, -2, 4]` it gives (2, 2), (6, 3), (-2, -12), (4, -48). The best product is the largest `hi`, which is 6.

```python
def product_trace(nums):
    hi = lo = nums[0]
    trace = [(hi, lo)]
    for x in nums[1:]:
        options = (x, hi * x, lo * x)
        hi, lo = max(options), min(options)
        trace.append((hi, lo))
    return trace


assert product_trace([2, 3, -2, 4]) == [(2, 2), (6, 3), (-2, -12), (4, -48)]
assert product_trace([-2, -3]) == [(-2, -2), (6, -3)]
```

```cpp
vector<pair<long long, long long>> product_trace(const vector<int>& nums) {
    long long hi = nums[0], lo = nums[0];
    vector<pair<long long, long long>> trace = {{hi, lo}};
    for (size_t i = 1; i < nums.size(); i++) {
        long long x = nums[i];
        long long a = x, b = hi * x, c = lo * x;
        hi = max({a, b, c});
        lo = min({a, b, c});
        trace.push_back({hi, lo});
    }
    return trace;
}
```

Time $O(n)$, space $O(1)$ if you keep only the latest pair. A zero resets everything automatically, because the "value alone" candidate takes over after it. This is exactly the problem _Maximum Product Subarray_.

## 6.3 The majority vote

A **majority** value appears more than half the time. Here is a lovely trick named after **Boyer and Moore**. Imagine every value is a voter and each time two different values meet, they cancel each other out as a pair. A true majority has more members than all the other values combined, so it can never be fully cancelled; something is left standing.

In code, keep one `candidate` and a `count`. If `count` is 0, the current value becomes the candidate. A value equal to the candidate adds one; any other value subtracts one. For `[2, 2, 1, 1, 2]`: candidate 2 with count 1, then 2; then count 1, then 0 after the second 1; then 2 becomes the candidate again. The survivor is 2.

The survivor is only a **candidate**: if no majority exists, the loop still ends with some value. So a second pass must count the candidate and check that it really appears more than half the time.

```python
def survivor(nums):
    candidate = None
    count = 0
    for x in nums:
        if count == 0:
            candidate = x
            count = 1
        elif x == candidate:
            count += 1
        else:
            count -= 1
    return candidate


def has_majority(nums):
    if not nums:
        return False
    c = survivor(nums)
    return nums.count(c) * 2 > len(nums)


assert survivor([2, 2, 1, 1, 2]) == 2
assert has_majority([2, 2, 1, 1, 2]) is True
assert has_majority([1, 2, 3]) is False
```

```cpp
int survivor(const vector<int>& nums) {
    int candidate = 0, count = 0;
    for (int x : nums) {
        if (count == 0) {
            candidate = x;
            count = 1;
        } else if (x == candidate) {
            count++;
        } else {
            count--;
        }
    }
    return candidate;
}

bool has_majority(const vector<int>& nums) {
    if (nums.empty()) return false;
    int c = survivor(nums);
    long long cnt = 0;
    for (int x : nums) if (x == c) cnt++;
    return cnt * 2 > (long long)nums.size();
}
```

Two passes, $O(n)$ time and $O(1)$ space; a dictionary would use $O(n)$ space. This is exactly the problem _Majority Element_.

## 6.4 More than a third

How many values can appear more than $n/3$ times? At most two, because three of them would already use more than all $n$ places. The cancelling idea grows: keep up to two candidates with counters. A new value that matches a candidate adds one to its counter. If it matches none and there is a free slot, it becomes a candidate. Otherwise it cancels **one copy of each candidate and itself**, which means all counters go down by one, and a counter that reaches zero frees its slot.

The general version for "more than $n/k$ times" keeps up to $k-1$ counters. After the pass, count the survivors for real and keep those with $\text{count} \cdot k > n$.

```python
def frequent_over(nums, k):
    counters = {}
    for x in nums:
        if x in counters:
            counters[x] += 1
        elif len(counters) < k - 1:
            counters[x] = 1
        else:
            for key in list(counters):
                counters[key] -= 1
                if counters[key] == 0:
                    del counters[key]
    n = len(nums)
    result = []
    for key in counters:
        if nums.count(key) * k > n:
            result.append(key)
    return sorted(result)


assert frequent_over([1, 1, 1, 3, 3, 2, 2, 2], 3) == [1, 2]
assert frequent_over([1, 2, 3], 3) == []
assert frequent_over([5, 5, 5], 2) == [5]
```

```cpp
vector<int> frequent_over(const vector<int>& nums, int k) {
    unordered_map<int, int> counters;
    for (int x : nums) {
        if (counters.count(x)) {
            counters[x]++;
        } else if ((int)counters.size() < k - 1) {
            counters[x] = 1;
        } else {
            for (auto it = counters.begin(); it != counters.end();) {
                if (--it->second == 0) it = counters.erase(it);
                else ++it;
            }
        }
    }
    long long n = nums.size();
    vector<int> result;
    for (auto& [key, unused] : counters) {
        long long cnt = 0;
        for (int x : nums) if (x == key) cnt++;
        if (cnt * k > n) result.push_back(key);
    }
    sort(result.begin(), result.end());
    return result;
}
```

For fixed $k$ (such as 2 or 3) the time is $O(n)$ with $O(1)$ space. This is exactly the problem _Elements Appearing More Than n/3 Times_.

## 6.5 Check yourself

1. In Kadane's method, when do we throw away the run so far?
2. Why must a product method track the smallest product as well as the largest?
3. After the Boyer-Moore pass, why is a second counting pass needed?
4. How many values can appear more than $n/3$ times in a list of length $n$?

# Chapter 7. Sort first, then squeeze

## 7.1 Two fingers from both ends

Sorting a list gives us an ordered world where we can reason about "too small" and "too big". Let us find out if a **sorted** list has two values adding up to `t`. Put one finger `lo` on the first value and one finger `hi` on the last. Look at their sum. If it is too small, `lo` is the only thing that can increase it, so move `lo` up. If it is too big, move `hi` down. Equal means we found it.

For `[1, 3, 4, 8, 9]` and `t = 12`: $1 + 9 = 10$ is small, so `lo` moves; $3 + 9 = 12$ is found.

```python
def has_pair_sorted(nums, t):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == t:
            return True
        if s < t:
            lo += 1
        else:
            hi -= 1
    return False


assert has_pair_sorted([1, 3, 4, 8, 9], 12) is True
assert has_pair_sorted([1, 3, 4, 8, 9], 6) is False
```

```cpp
bool has_pair_sorted(const vector<int>& nums, long long t) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo < hi) {
        long long s = (long long)nums[lo] + nums[hi];
        if (s == t) return true;
        if (s < t) lo++;
        else hi--;
    }
    return false;
}
```

Each step moves a finger inward, so there are at most $n$ steps: $O(n)$ after sorting, and $O(n \log n)$ overall.

## 7.2 Fix one, squeeze the rest

For triples, fix the first value with a loop, and then the remaining task is a pair-sum problem on the rest of the (sorted) list. That is a loop over $i$ with an $O(n)$ squeeze inside, so the total is $O(n^2)$ instead of the $O(n^3)$ of trying every triple.

To see the pattern on a different question, find the triple sum closest to a target. We sort, loop over `i`, and squeeze `lo` and `hi` over the rest, remembering whichever sum is nearest.

```python
def closest_triple_sum(nums, target):
    a = sorted(nums)
    best = a[0] + a[1] + a[2]
    for i in range(len(a) - 2):
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            if abs(s - target) < abs(best - target):
                best = s
            if s < target:
                lo += 1
            elif s > target:
                hi -= 1
            else:
                return s
    return best


assert closest_triple_sum([-1, 2, 1, -4], 1) == 2
assert closest_triple_sum([0, 0, 0], 1) == 0
```

```cpp
long long closest_triple_sum(vector<int> nums, long long target) {
    sort(nums.begin(), nums.end());
    int n = nums.size();
    long long best = (long long)nums[0] + nums[1] + nums[2];
    for (int i = 0; i + 2 < n; i++) {
        int lo = i + 1, hi = n - 1;
        while (lo < hi) {
            long long s = (long long)nums[i] + nums[lo] + nums[hi];
            if (llabs(s - target) < llabs(best - target)) best = s;
            if (s < target) lo++;
            else if (s > target) hi--;
            else return s;
        }
    }
    return best;
}
```

When the question wants every **different** group, duplicates become the main danger. The cure is to skip repeated values: in the outer loop, skip `a[i]` if it equals `a[i-1]`; inside the squeeze, after finding a match, move both fingers and keep moving past equal neighbours. Here is the squeeze alone, listing each different pair that adds to `t` in a sorted list:

```python
def unique_pairs(a, t):
    lo, hi = 0, len(a) - 1
    result = []
    while lo < hi:
        s = a[lo] + a[hi]
        if s < t:
            lo += 1
        elif s > t:
            hi -= 1
        else:
            result.append([a[lo], a[hi]])
            lo += 1
            hi -= 1
            while lo < hi and a[lo] == a[lo - 1]:
                lo += 1
            while lo < hi and a[hi] == a[hi + 1]:
                hi -= 1
    return result


assert unique_pairs([1, 1, 2, 2, 3, 3, 4], 5) == [[1, 4], [2, 3]]
assert unique_pairs([2, 2, 2], 4) == [[2, 2]]
```

```cpp
vector<vector<int>> unique_pairs(const vector<int>& a, long long t) {
    int lo = 0, hi = (int)a.size() - 1;
    vector<vector<int>> result;
    while (lo < hi) {
        long long s = (long long)a[lo] + a[hi];
        if (s < t) lo++;
        else if (s > t) hi--;
        else {
            result.push_back({a[lo], a[hi]});
            lo++;
            hi--;
            while (lo < hi && a[lo] == a[lo - 1]) lo++;
            while (lo < hi && a[hi] == a[hi + 1]) hi--;
        }
    }
    return result;
}
```

Put the outer loop with its own duplicate skip around this squeeze (looking for `-a[i]`) and you have the whole answer. Time $O(n^2)$, extra space $O(1)$ besides the output. This is exactly the problem _Three Sum_.

## 7.3 Any number of values

The pattern repeats for four values: two nested loops (each skipping repeated values), then the squeeze for the last two. Time $O(n^3)$. More generally, to find $k$ values, loop over the first one (skipping repeats) and recurse on $k-1$, stopping at $k = 2$ with the squeeze. To keep the code short, the function below only **counts** the different groups.

```python
def count_ksum(nums, k, target):
    a = sorted(nums)
    return ksum_from(a, 0, k, target)


def ksum_from(a, start, k, target):
    n = len(a)
    if k == 2:
        lo, hi = start, n - 1
        count = 0
        while lo < hi:
            s = a[lo] + a[hi]
            if s < target:
                lo += 1
            elif s > target:
                hi -= 1
            else:
                count += 1
                lo += 1
                hi -= 1
                while lo < hi and a[lo] == a[lo - 1]:
                    lo += 1
                while lo < hi and a[hi] == a[hi + 1]:
                    hi -= 1
        return count
    total = 0
    for i in range(start, n - k + 1):
        if i > start and a[i] == a[i - 1]:
            continue
        total += ksum_from(a, i + 1, k - 1, target - a[i])
    return total


assert count_ksum([1, 0, -1, 0, -2, 2], 4, 0) == 3
assert count_ksum([-1, 0, 1, 2, -1, -4], 3, 0) == 2
```

```cpp
long long ksum_from(const vector<int>& a, int start, int k, long long target) {
    int n = a.size();
    if (k == 2) {
        int lo = start, hi = n - 1;
        long long count = 0;
        while (lo < hi) {
            long long s = (long long)a[lo] + a[hi];
            if (s < target) lo++;
            else if (s > target) hi--;
            else {
                count++;
                lo++;
                hi--;
                while (lo < hi && a[lo] == a[lo - 1]) lo++;
                while (lo < hi && a[hi] == a[hi + 1]) hi--;
            }
        }
        return count;
    }
    long long total = 0;
    for (int i = start; i <= n - k; i++) {
        if (i > start && a[i] == a[i - 1]) continue;
        total += ksum_from(a, i + 1, k - 1, target - a[i]);
    }
    return total;
}

long long count_ksum(vector<int> nums, int k, long long target) {
    sort(nums.begin(), nums.end());
    return ksum_from(nums, 0, k, target);
}
```

In the sheet problem you list the groups instead of counting them, but the skeleton is the same. This is exactly the problem _Four Sum_.

## 7.4 Merging overlapping intervals

An **interval** is a pair `[start, end]`. Two intervals **overlap** when they share at least one point, and we also treat intervals that merely touch as overlapping. If we sort the intervals by their start, any overlap can only be with the group we are building right now, so one sweep is enough.

Keep the current group as `[cur_start, cur_end]`. For the next interval `[s, e]`: if `s` is bigger than `cur_end`, there is a gap, so the current group is finished and a new one starts. Otherwise the intervals touch or overlap, so extend `cur_end` to the larger of the two ends.

To practise on a related question, let us measure the **total length** covered. For `[[1, 3], [2, 6], [8, 10], [9, 12]]`, the groups are `[1, 6]` and `[8, 12]`, covering $5 + 4 = 9$. For `[[1, 3], [3, 5]]` the answer is 4.

```python
def covered_length(intervals):
    if not intervals:
        return 0
    items = sorted(intervals)
    cur_start, cur_end = items[0]
    total = 0
    for s, e in items[1:]:
        if s > cur_end:
            total += cur_end - cur_start
            cur_start, cur_end = s, e
        else:
            cur_end = max(cur_end, e)
    total += cur_end - cur_start
    return total


assert covered_length([[1, 3], [2, 6], [8, 10], [9, 12]]) == 9
assert covered_length([[1, 3], [3, 5]]) == 4
assert covered_length([]) == 0
```

```cpp
long long covered_length(vector<vector<int>> intervals) {
    if (intervals.empty()) return 0;
    sort(intervals.begin(), intervals.end());
    long long curStart = intervals[0][0], curEnd = intervals[0][1];
    long long total = 0;
    for (size_t i = 1; i < intervals.size(); i++) {
        long long s = intervals[i][0], e = intervals[i][1];
        if (s > curEnd) {
            total += curEnd - curStart;
            curStart = s;
            curEnd = e;
        } else {
            curEnd = max(curEnd, e);
        }
    }
    total += curEnd - curStart;
    return total;
}
```

Sorting costs $O(n \log n)$ and the sweep $O(n)$. To produce the merged intervals themselves, write `[cur_start, cur_end]` to the answer whenever a group closes (and once at the very end). Because the test is `s > cur_end` and not `>=`, touching intervals merge. This is exactly the problem _Merge Intervals_.

## 7.5 The next arrangement

List all rearrangements of `1 2 3` in dictionary order: 123, 132, 213, 231, 312, 321. We want a fast way to jump from one to the next. Look at the **tail**. The tail that is in decreasing order (like `5 4 2` in `1 3 5 4 2`) is already the biggest arrangement of its digits, so to move on we must change a digit before that tail.

The recipe has three steps. First, from the right, find the **pivot**: the last digit that is smaller than its right neighbour (here `3`). Second, swap the pivot with the smallest digit in the tail that is bigger than it (here `4`), giving `1 4 5 3 2`. Third, reverse the tail so it becomes the smallest arrangement (the tail `5 3 2` becomes `2 3 5`), giving `1 4 2 3 5`. If there is no pivot, the digits are already the last arrangement.

```python
def next_bigger_digits(digits):
    d = list(digits)
    i = len(d) - 2
    while i >= 0 and d[i] >= d[i + 1]:
        i -= 1
    if i < 0:
        return []
    j = len(d) - 1
    while d[j] <= d[i]:
        j -= 1
    d[i], d[j] = d[j], d[i]
    d[i + 1:] = reversed(d[i + 1:])
    return d


assert next_bigger_digits([1, 3, 5, 4, 2]) == [1, 4, 2, 3, 5]
assert next_bigger_digits([3, 2, 1]) == []
assert next_bigger_digits([1, 1, 2]) == [1, 2, 1]
```

```cpp
vector<int> next_bigger_digits(vector<int> d) {
    int i = (int)d.size() - 2;
    while (i >= 0 && d[i] >= d[i + 1]) i--;
    if (i < 0) return {};
    int j = (int)d.size() - 1;
    while (d[j] <= d[i]) j--;
    swap(d[i], d[j]);
    reverse(d.begin() + i + 1, d.end());
    return d;
}
```

Time $O(n)$, space $O(1)$ besides the copy. The comparisons use `>=` and `<=` so that repeated digits are handled correctly. In the sheet problem, when there is no pivot, you return the digits sorted increasingly, which is exactly the reversed tail. This is exactly the problem _Next Permutation_.

## 7.6 Check yourself

1. In the sorted pair-sum squeeze, why do we move `lo` when the sum is too small?
2. What two places must skip repeated values to avoid duplicate triples?
3. When sorted intervals are swept, what tells us a new group must start?
4. In the next-arrangement recipe, why do we reverse the tail after the swap?

# Chapter 8. Matrices and rows of numbers

## 8.1 Matrices and the transpose

A **matrix** is a grid of numbers, stored as a list of rows. A matrix with $m$ rows and $n$ columns has `m[r][c]` for the value in row `r`, column `c`. The first row has index 0.

The **transpose** swaps rows and columns: the value at row `r`, column `c` moves to row `c`, column `r`. So an $m \times n$ matrix becomes $n \times m$. For `[[1, 2, 3], [4, 5, 6]]` the transpose is `[[1, 4], [2, 5], [3, 6]]`.

```python
def transpose(m):
    if not m:
        return []
    return [[m[r][c] for r in range(len(m))] for c in range(len(m[0]))]


assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
assert transpose([[7]]) == [[7]]
```

```cpp
vector<vector<int>> transpose(const vector<vector<int>>& m) {
    if (m.empty()) return {};
    int rows = m.size(), cols = m[0].size();
    vector<vector<int>> t(cols, vector<int>(rows));
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            t[c][r] = m[r][c];
    return t;
}
```

Time and space $O(mn)$, which is the size of the matrix itself, so no method can do better.

## 8.2 Rotating by combining moves

Rotating a matrix looks tricky, but it is really two simple moves in a row. To rotate **clockwise**, transpose the matrix and then reverse every row. For `[[1, 2], [3, 4]]`: the transpose is `[[1, 3], [2, 4]]`, and reversing each row gives `[[3, 1], [4, 2]]`, which is indeed the original turned a quarter-turn clockwise.

To rotate **counter-clockwise**, transpose and then reverse the **order of the rows** instead. For the same matrix, the transpose `[[1, 3], [2, 4]]` with rows reversed is `[[2, 4], [1, 3]]`.

```python
def rotate_ccw(m):
    if not m:
        return []
    t = [[m[r][c] for r in range(len(m))] for c in range(len(m[0]))]
    return t[::-1]


assert rotate_ccw([[1, 2], [3, 4]]) == [[2, 4], [1, 3]]
assert rotate_ccw([[1, 2, 3]]) == [[3], [2], [1]]
```

```cpp
vector<vector<int>> rotate_ccw(const vector<vector<int>>& m) {
    if (m.empty()) return {};
    int rows = m.size(), cols = m[0].size();
    vector<vector<int>> t(cols, vector<int>(rows));
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            t[c][r] = m[r][c];
    reverse(t.begin(), t.end());
    return t;
}
```

Time $O(mn)$. The matrix does not have to be square: an $m \times n$ matrix turns into an $n \times m$ one, as the second assert shows. This is exactly the problem _Rotate a Matrix_ (clockwise: transpose, then reverse each row).

## 8.3 Row and column flags

When one cell can affect its whole row and column, the beginner's mistake is to change the grid while still reading it, so the changes spread. The safe habit is to do two phases: first **look** and record flags, then **change**.

Let us practise on this question: which rows and which columns contain a negative number? Phase one scans every cell once and sets `bad_row[r]` and `bad_col[c]`. Afterwards, we can read the flags in any order.

```python
def rows_cols_with_negative(m):
    rows = len(m)
    cols = len(m[0]) if m else 0
    bad_row = [False] * rows
    bad_col = [False] * cols
    for r in range(rows):
        for c in range(cols):
            if m[r][c] < 0:
                bad_row[r] = True
                bad_col[c] = True
    return ([r for r in range(rows) if bad_row[r]],
            [c for c in range(cols) if bad_col[c]])


assert rows_cols_with_negative([[1, -2, 3], [4, 5, 6], [7, 8, -9]]) == ([0, 2], [1, 2])
assert rows_cols_with_negative([[1]]) == ([], [])
```

```cpp
pair<vector<int>, vector<int>> rows_cols_with_negative(const vector<vector<int>>& m) {
    int rows = m.size();
    int cols = rows ? m[0].size() : 0;
    vector<bool> badRow(rows, false), badCol(cols, false);
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            if (m[r][c] < 0) {
                badRow[r] = true;
                badCol[c] = true;
            }
    vector<int> rs, cs;
    for (int r = 0; r < rows; r++) if (badRow[r]) rs.push_back(r);
    for (int c = 0; c < cols; c++) if (badCol[c]) cs.push_back(c);
    return {rs, cs};
}
```

For _Set Matrix Zeroes_, phase one records which rows and columns hold a `0`, and phase two writes a `0` into every cell whose row or column is flagged. Time $O(mn)$, extra space $O(m+n)$. (A clever variant stores the flags inside the first row and first column of the matrix itself to use $O(1)$ extra space, but the two-phase version is easier to get right.) This is exactly the problem _Set Matrix Zeroes_.

## 8.4 Walking around the edge

To visit a matrix in a **spiral**, think of peeling it like an onion: first the outer ring clockwise, then the ring inside it, and so on. The outer ring has four sides: the top row left to right, the right column going down, the bottom row right to left, and the left column going up. Corners must not be visited twice.

Here is the outer ring alone. A matrix with a single row or a single column is special, because the sides would overlap, so we handle those first.

```python
def outer_ring(m):
    if not m:
        return []
    r, c = len(m), len(m[0])
    if r == 1:
        return m[0][:]
    if c == 1:
        return [row[0] for row in m]
    out = m[0][:]
    for i in range(1, r):
        out.append(m[i][c - 1])
    for j in range(c - 2, -1, -1):
        out.append(m[r - 1][j])
    for i in range(r - 2, 0, -1):
        out.append(m[i][0])
    return out


assert outer_ring([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4]
assert outer_ring([[1, 2, 3]]) == [1, 2, 3]
```

```cpp
vector<int> outer_ring(const vector<vector<int>>& m) {
    if (m.empty()) return {};
    int r = m.size(), c = m[0].size();
    if (r == 1) return m[0];
    vector<int> out;
    if (c == 1) {
        for (auto& row : m) out.push_back(row[0]);
        return out;
    }
    out = m[0];
    for (int i = 1; i < r; i++) out.push_back(m[i][c - 1]);
    for (int j = c - 2; j >= 0; j--) out.push_back(m[r - 1][j]);
    for (int i = r - 2; i > 0; i--) out.push_back(m[i][0]);
    return out;
}
```

The full spiral repeats this for the inner rings. The usual way is to keep four walls, `top`, `bottom`, `left`, `right`, and shrink them after each side: after walking the top row, `top` goes down by one; after the right column, `right` moves left by one; and so on. The two things to watch are: before walking the bottom row, check `top <= bottom` still holds, and before walking the left column, check `left <= right` still holds, otherwise a thin leftover strip gets visited twice. Every cell is visited once, so the time is $O(mn)$. This is exactly the problem _Spiral Order_.

## 8.5 A row of Pascal's triangle

In Pascal's triangle every row begins and ends with 1, and every inner value is the sum of the two values above it. So the next row can be built from the current one by adding neighbours.

```python
def next_pascal(row):
    return [1] + [a + b for a, b in zip(row, row[1:])] + [1]


assert next_pascal([1]) == [1, 1]
assert next_pascal([1, 3, 3, 1]) == [1, 4, 6, 4, 1]
```

```cpp
vector<long long> next_pascal(const vector<long long>& row) {
    vector<long long> out;
    out.push_back(1);
    for (size_t i = 0; i + 1 < row.size(); i++) out.push_back(row[i] + row[i + 1]);
    out.push_back(1);
    return out;
}
```

Building row number $n$ this way costs $O(n^2)$, because we build every row before it. There is a faster way. The values of row $n$ are the **binomial coefficients** $\binom{n}{0}, \binom{n}{1}, \dots, \binom{n}{n}$, where $\binom{n}{k}$ counts how many ways there are to choose $k$ things from $n$. Each one follows from the previous by

$$\binom{n}{k+1} = \binom{n}{k} \cdot \frac{n-k}{k+1}$$

Starting from $\binom{n}{0} = 1$, each step multiplies and then divides. The division is always exact, because the result is a whole number. For example $\binom{5}{2}$: start with 1, then $1 \cdot 5 / 1 = 5$, then $5 \cdot 4 / 2 = 10$.

```python
def binomial(n, k):
    value = 1
    for i in range(k):
        value = value * (n - i) // (i + 1)
    return value


assert binomial(5, 2) == 10
assert binomial(4, 0) == 1
assert [binomial(4, k) for k in range(5)] == [1, 4, 6, 4, 1]
```

```cpp
long long binomial(int n, int k) {
    long long value = 1;
    for (int i = 0; i < k; i++) {
        value = value * (n - i) / (i + 1);
    }
    return value;
}
```

Computing the whole row this way takes $O(n)$ time, since each entry comes from the previous one in constant time. In C++ the values overflow `long long` for large $n$ (around 60 and beyond), while Python integers never overflow. This is exactly the problem _A Row of Pascal's Triangle_.

## 8.6 Check yourself

1. What is the shape of the transpose of a matrix with 3 rows and 5 columns?
2. How do you rotate a matrix clockwise using a transpose?
3. Why do we record flags first and change the grid afterwards?
4. In the spiral walk, why are the checks `top <= bottom` and `left <= right` needed?

# Chapter 9. Counting pairs with merge sort

## 9.1 Counting inversions

An **inversion** is a pair of positions $i < j$ with `a[i] > a[j]`, that is, two values that are in the wrong order. The list `[3, 1, 2]` has two inversions: (3, 1) and (3, 2). Checking every pair costs $O(n^2)$. We can do better by borrowing the **merge** from Chapter 2.

Merge sort splits the list in halves, sorts each half by the same method, and merges the two sorted halves. Every inversion is either inside the left half, inside the right half, or has its first value in the left half and its second in the right half. The recursion counts the first two kinds. For the third kind, look at the merge: when we take a value from the **right** half because it is smaller than the current left value `a[i]`, then **all** the values still waiting in the left half (from `i` up to the middle) are bigger than it. That is `mid - i` inversions at once.

```python
def sort_count(a, tmp, lo, hi):
    if hi - lo < 2:
        return 0
    mid = (lo + hi) // 2
    count = sort_count(a, tmp, lo, mid) + sort_count(a, tmp, mid, hi)
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if a[i] <= a[j]:
            tmp[k] = a[i]
            i += 1
        else:
            tmp[k] = a[j]
            j += 1
            count += mid - i
        k += 1
    while i < mid:
        tmp[k] = a[i]
        i += 1
        k += 1
    while j < hi:
        tmp[k] = a[j]
        j += 1
        k += 1
    a[lo:hi] = tmp[lo:hi]
    return count


def count_inversions(nums):
    a = list(nums)
    return sort_count(a, [0] * len(a), 0, len(a))


assert count_inversions([3, 1, 2]) == 2
assert count_inversions([2, 4, 1, 3, 5]) == 3
assert count_inversions([1, 2, 3]) == 0
```

```cpp
long long sort_count(vector<int>& a, vector<int>& tmp, int lo, int hi) {
    if (hi - lo < 2) return 0;
    int mid = (lo + hi) / 2;
    long long count = sort_count(a, tmp, lo, mid) + sort_count(a, tmp, mid, hi);
    int i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        if (a[i] <= a[j]) {
            tmp[k++] = a[i++];
        } else {
            tmp[k++] = a[j++];
            count += mid - i;
        }
    }
    while (i < mid) tmp[k++] = a[i++];
    while (j < hi) tmp[k++] = a[j++];
    for (int t = lo; t < hi; t++) a[t] = tmp[t];
    return count;
}

long long count_inversions(vector<int> nums) {
    vector<int> tmp(nums.size());
    return sort_count(nums, tmp, 0, (int)nums.size());
}
```

The list is halved about $\log_2 n$ times and every level does $O(n)$ merging work, so the time is $O(n \log n)$ and the extra space is $O(n)$.

## 9.2 A different pair condition

The merge trick is not tied to the plain "bigger than" rule. What matters is that, once both halves are sorted, the **cross pairs** can be counted by walking two fingers forward. Let us count pairs $i < j$ with `a[i] > 3 * a[j]` as an example.

Before merging, both halves are sorted. For each value `a[i]` in the left half, from smallest to largest, advance a pointer `p` in the right half while `a[i] > 3 * a[p]`. As `a[i]` grows, the number of right values it beats can only grow, so `p` never has to move backwards. Every position of the right half before `p` forms a pair with `a[i]`, which is `p - mid` pairs. Only after counting do we merge.

```python
def big_sort_count(a, tmp, lo, hi):
    if hi - lo < 2:
        return 0
    mid = (lo + hi) // 2
    count = big_sort_count(a, tmp, lo, mid) + big_sort_count(a, tmp, mid, hi)
    p = mid
    for i in range(lo, mid):
        while p < hi and a[i] > 3 * a[p]:
            p += 1
        count += p - mid
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if a[i] <= a[j]:
            tmp[k] = a[i]
            i += 1
        else:
            tmp[k] = a[j]
            j += 1
        k += 1
    while i < mid:
        tmp[k] = a[i]
        i += 1
        k += 1
    while j < hi:
        tmp[k] = a[j]
        j += 1
        k += 1
    a[lo:hi] = tmp[lo:hi]
    return count


def count_big_pairs(nums):
    a = list(nums)
    return big_sort_count(a, [0] * len(a), 0, len(a))


data = [1, 2, 5, 0, -3, 7, 2]
brute = sum(1 for i in range(len(data)) for j in range(i + 1, len(data)) if data[i] > 3 * data[j])
assert count_big_pairs(data) == brute
assert count_big_pairs([1, 2, 5, 0]) == 3
```

```cpp
long long big_sort_count(vector<int>& a, vector<int>& tmp, int lo, int hi) {
    if (hi - lo < 2) return 0;
    int mid = (lo + hi) / 2;
    long long count = big_sort_count(a, tmp, lo, mid) + big_sort_count(a, tmp, mid, hi);
    int p = mid;
    for (int i = lo; i < mid; i++) {
        while (p < hi && (long long)a[i] > 3LL * a[p]) p++;
        count += p - mid;
    }
    int i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];
        else tmp[k++] = a[j++];
    }
    while (i < mid) tmp[k++] = a[i++];
    while (j < hi) tmp[k++] = a[j++];
    for (int t = lo; t < hi; t++) a[t] = tmp[t];
    return count;
}

long long count_big_pairs(vector<int> nums) {
    vector<int> tmp(nums.size());
    return big_sort_count(nums, tmp, 0, (int)nums.size());
}
```

The counting walk costs $O(n)$ per level (both fingers only move forward), so the total is still $O(n \log n)$. Two details matter. First, count **before** merging, because merging destroys the sorted halves we need. Second, in C++ compute `3 * a[p]` as a `long long`, since doubling or tripling a large value can overflow an `int`. The sheet problem uses `2 * a[j]` in place of `3 * a[j]`. This is exactly the problem _Count Reverse Pairs_.

## 9.3 Check yourself

1. In the merge, when a value is taken from the right half, how many inversions does that add?
2. Why is the time of the merge-sort counting method $O(n \log n)$ and not $O(n^2)$?
3. Why must pairs be counted before merging the two halves?
4. Why can the pointer `p` only move forward as `i` increases?
