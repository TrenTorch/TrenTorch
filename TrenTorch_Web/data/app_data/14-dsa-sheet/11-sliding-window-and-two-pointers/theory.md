> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Two pointers and sliding window)

This page teaches two of the most useful habits in array and string problems: moving **two markers** through the data instead of trying every pair, and sliding a **window** over the data instead of recomputing from scratch. Both turn slow "try everything" solutions that take $O(n^2)$ time into single passes that take $O(n)$.

The page is a staircase. **Chapter 1 is deliberately gentle**: two markers on a list and three small, friendly problems. Chapter 2 and 3 use sorted data and walls to make the markers smarter. Chapter 4 adds two classic tricks. Then we meet windows: fixed-size ones, ones that grow and shrink, the counting trick behind "at most $K$", and finally the famous minimum window substring. Each chapter only uses what came before. Every code example is shown in Python and in C++, so pick whichever language you like.

# Chapter 1. Two markers on a list

## 1.1 What a pointer is here

In this page a **pointer** is just a whole number that says "I am looking at position $i$ of the list". It is not a memory address. We keep two of them, usually called `i` and `j` (or `left` and `right`), and move them with a simple rule so that between them they visit the data only once.

There are two ways to move two pointers. In the first, they start at **opposite ends** and walk toward each other. In the second, both start at the **front** and walk in the same direction, one running ahead of the other. We will use both.

## 1.2 Starting at both ends: palindromes

A **palindrome** is a word that reads the same forwards and backwards, like `radar`. To test one, compare the first and the last letter, then the second and the second-to-last, and so on. Two pointers do exactly that: `i` starts at the front, `j` at the back, they compare, and move inward. If they ever meet or cross, everything matched.

```python
def is_palindrome(s):
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True


assert is_palindrome("radar") is True
assert is_palindrome("abca") is False
assert is_palindrome("") is True
```

```cpp
bool is_palindrome(const string& s) {
    int i = 0, j = (int)s.size() - 1;
    while (i < j) {
        if (s[i] != s[j]) return false;
        ++i;
        --j;
    }
    return true;
}
```

Time is $O(n)$ and extra space is $O(1)$.

## 1.3 Palindrome with one deletion

Now a twist: can the string become a palindrome if we are allowed to delete **at most one** character? For `raceacar` the answer is yes (delete the `e`), for `abc` the answer is no.

Walk inward as before. At the first mismatch, one of the two letters must be the one we delete. We do not know which, so we try both: skip the left letter and check that the rest between `i + 1` and `j` is a palindrome, or skip the right letter and check the rest between `i` and `j - 1`. If either works, the answer is yes. Notice that we only ever try this at the _first_ mismatch, so the extra work is two more linear passes, not a pile of them.

This is exactly the problem _Palindrome After Deleting One Character_.

```python
def is_pal_range(s, i, j):
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True


def almost_palindrome(s):
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return is_pal_range(s, i + 1, j) or is_pal_range(s, i, j - 1)
        i += 1
        j -= 1
    return True


assert almost_palindrome("raceacar") is True
assert almost_palindrome("abc") is False
assert almost_palindrome("abba") is True
assert almost_palindrome("") is True
```

```cpp
bool is_pal_range(const string& s, int i, int j) {
    while (i < j) {
        if (s[i] != s[j]) return false;
        ++i;
        --j;
    }
    return true;
}

bool almost_palindrome(const string& s) {
    int i = 0, j = (int)s.size() - 1;
    while (i < j) {
        if (s[i] != s[j]) return is_pal_range(s, i + 1, j) || is_pal_range(s, i, j - 1);
        ++i;
        --j;
    }
    return true;
}
```

Time is $O(n)$ and space $O(1)$.

## 1.4 Both pointers moving forward: subsequences

A **subsequence** of a string is what you get by deleting some letters and keeping the rest in order: `ace` is a subsequence of `abcde`, but `aec` is not (the order is broken). To check whether `s` is a subsequence of `t`, run one pointer `i` over `s` (how many letters of `s` we have matched so far) and let a loop run over every letter of `t`. When the current letter of `t` equals `s[i]`, we matched one more letter and `i` moves on. If `i` reaches the end of `s`, everything matched.

Here the pointer over `t` always moves, and the pointer over `s` moves only on a match. Neither ever goes back.

This is exactly the problem _Is It a Subsequence?_.

```python
def is_subsequence(s, t):
    i = 0
    for ch in t:
        if i < len(s) and s[i] == ch:
            i += 1
    return i == len(s)


assert is_subsequence("ace", "abcde") is True
assert is_subsequence("aec", "abcde") is False
assert is_subsequence("", "xyz") is True
assert is_subsequence("a", "") is False
```

```cpp
bool is_subsequence(const string& s, const string& t) {
    int i = 0;
    for (char ch : t) {
        if (i < (int)s.size() && s[i] == ch) ++i;
    }
    return i == (int)s.size();
}
```

Time is $O(|t|)$ and space $O(1)$. Matching each letter of `s` as early as possible is always safe: if some later match works, the earlier one works too.

## 1.5 Squares of a sorted list

The list `[-6, -2, 0, 1, 5]` is sorted. If we square every number we get `[36, 4, 0, 1, 25]`, which is no longer sorted, and sorting it costs $O(n \log n)$. We can do better by noticing where the largest square is: it is at one of the two ends. The most negative number and the most positive number have the largest absolute values.

So put a pointer at each end. Compare their absolute values; the bigger one gives the next-largest square, which we write at the **back** of the answer. Then move that pointer inward. Repeat, filling the answer from the back to the front.

Trace on `[-6, -2, 0, 1, 5]`: the ends are 6 and 5, so `36` goes last and the left pointer moves to `-2`. Now 2 against 5: `25` goes next to last and the right pointer moves to `1`. Then 2 against 1: `4` goes in. Then 0 against 1: `1`. Finally `0`. The answer is `[0, 1, 4, 25, 36]`.

This is exactly the problem _Squares of a Sorted Array_.

```python
def sorted_squares(nums):
    n = len(nums)
    out = [0] * n
    i, j = 0, n - 1
    for pos in range(n - 1, -1, -1):
        if abs(nums[i]) > abs(nums[j]):
            out[pos] = nums[i] * nums[i]
            i += 1
        else:
            out[pos] = nums[j] * nums[j]
            j -= 1
    return out


assert sorted_squares([-6, -2, 0, 1, 5]) == [0, 1, 4, 25, 36]
assert sorted_squares([-3, -3, 2]) == [4, 9, 9]
assert sorted_squares([]) == []
```

```cpp
vector<int> sorted_squares(const vector<int>& nums) {
    int n = (int)nums.size();
    vector<int> out(n);
    int i = 0, j = n - 1;
    for (int pos = n - 1; pos >= 0; --pos) {
        if (abs(nums[i]) > abs(nums[j])) {
            out[pos] = nums[i] * nums[i];
            ++i;
        } else {
            out[pos] = nums[j] * nums[j];
            --j;
        }
    }
    return out;
}
```

Time is $O(n)$ and space is $O(n)$ for the answer.

## 1.6 Check yourself

1. In the palindrome check, why do we stop when `i` and `j` meet?
2. Why do we try deleting only at the first mismatch?
3. In the subsequence check, which pointer always moves?
4. Why do we fill the squares from the back?

# Chapter 2. Pairs and sorted data

## 2.1 Two numbers that add up

Given a **sorted** list and a target, find two positions whose values add up to the target. Trying all pairs costs $O(n^2)$. With two pointers it costs $O(n)$.

Put `lo` at the front (the smallest value) and `hi` at the back (the largest). Look at the sum. If it is too small, we need a bigger number, and the only way to get one is to move `lo` right (moving `hi` left would only make the sum smaller). If it is too big, move `hi` left. If it matches, we are done. Each step removes one value from further consideration, so we take at most $n$ steps.

Why is it safe to throw a value away? Say the sum of `lo` and `hi` is too small. Then `nums[lo]` plus _any_ value at or before `hi` is also too small (the others are not bigger than `nums[hi]`), so `nums[lo]` cannot be part of any answer, and we can drop it.

```python
def pair_with_sum(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        total = nums[lo] + nums[hi]
        if total == target:
            return [lo, hi]
        if total < target:
            lo += 1
        else:
            hi -= 1
    return [-1, -1]


assert pair_with_sum([1, 3, 4, 6, 8, 11], 10) == [2, 3]
assert pair_with_sum([1, 3, 4, 6, 8, 11], 2) == [-1, -1]
```

```cpp
vector<int> pair_with_sum(const vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo < hi) {
        int total = nums[lo] + nums[hi];
        if (total == target) return {lo, hi};
        if (total < target) ++lo;
        else --hi;
    }
    return {-1, -1};
}
```

The trace for target 10 on `[1, 3, 4, 6, 8, 11]`: $1 + 11 = 12$ is too big, so `hi` moves; $1 + 8 = 9$ is too small, so `lo` moves; $3 + 8 = 11$ too big; $3 + 6 = 9$ too small; $4 + 6 = 10$ found at positions 2 and 3.

## 2.2 Three numbers, closest sum

Now choose **three** different positions and make their sum as close to a target as possible (if two sums are equally close, choose the smaller sum). First sort a copy of the list. Then fix the first number one position at a time, and use the pair idea on everything to its right. For each fixed `i`, the two pointers start at `i + 1` and the end, and we use the same moves as before: a sum below the target moves `lo` right, a sum above it moves `hi` left. We remember the best sum seen so far, comparing sums by the pair `(distance from target, sum)` so that ties go to the smaller sum.

For `[0, 2, 5, 10]` and target 9: the possible sums are $0+2+5 = 7$, $0+2+10 = 12$, $0+5+10 = 15$ and $2+5+10 = 17$. The distances are 2, 3, 6, 8, so the closest sum is 7.

This is exactly the problem _Three Sum Closest_.

```python
def three_sum_closest(nums, target):
    a = sorted(nums)
    best = a[0] + a[1] + a[2]
    for i in range(len(a) - 2):
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            if (abs(s - target), s) < (abs(best - target), best):
                best = s
            if s < target:
                lo += 1
            elif s > target:
                hi -= 1
            else:
                return s
    return best


assert three_sum_closest([0, 2, 5, 10], 9) == 7
assert three_sum_closest([1, 1, 1, 1], 5) == 3
assert three_sum_closest([-3, 0, 4, 8], 0) == 1
```

```cpp
int three_sum_closest(vector<int> nums, int target) {
    sort(nums.begin(), nums.end());
    int n = (int)nums.size();
    int best = nums[0] + nums[1] + nums[2];
    for (int i = 0; i + 2 < n; ++i) {
        int lo = i + 1, hi = n - 1;
        while (lo < hi) {
            int s = nums[i] + nums[lo] + nums[hi];
            if (make_pair(abs(s - target), s) < make_pair(abs(best - target), best)) best = s;
            if (s < target) ++lo;
            else if (s > target) --hi;
            else return s;
        }
    }
    return best;
}
```

Sorting takes $O(n \log n)$ and the sweeps take $O(n^2)$ in total, so the time is $O(n^2)$ and the space is $O(n)$ for the sorted copy.

## 2.3 Counting many answers at once

Two pointers can also _count_ answers in bulk. We want the number of triples of positions $i < j < k$ whose sum is **less than** a target. Sort the list, fix `i`, and put `lo = i + 1`, `hi = n - 1`. If `a[i] + a[lo] + a[hi] < target`, then `hi` can be replaced by _any_ position from `lo + 1` to `hi` and the sum is still small (those values are not bigger). That is `hi - lo` triples, counted in a single step. Then move `lo` right. If the sum is not small enough, move `hi` left.

For `[1, 2, 3, 4]` with target 8, the triples and sums are $1+2+3 = 6$, $1+2+4 = 7$, $1+3+4 = 8$, $2+3+4 = 9$, so two of them are below 8.

This is exactly the problem _Count Triplets With a Smaller Sum_.

```python
def count_triplets_smaller(nums, target):
    a = sorted(nums)
    count = 0
    for i in range(len(a) - 2):
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            if a[i] + a[lo] + a[hi] < target:
                count += hi - lo
                lo += 1
            else:
                hi -= 1
    return count


assert count_triplets_smaller([1, 2, 3, 4], 8) == 2
assert count_triplets_smaller([-2, 0, 1, 3], 2) == 2
assert count_triplets_smaller([], 0) == 0
```

```cpp
long long count_triplets_smaller(vector<int> nums, int target) {
    sort(nums.begin(), nums.end());
    int n = (int)nums.size();
    long long count = 0;
    for (int i = 0; i + 2 < n; ++i) {
        int lo = i + 1, hi = n - 1;
        while (lo < hi) {
            if (nums[i] + nums[lo] + nums[hi] < target) {
                count += hi - lo;
                ++lo;
            } else {
                --hi;
            }
        }
    }
    return count;
}
```

Time is $O(n^2)$, space $O(n)$ for the sorted copy.

## 2.4 Pairing the heavy with the light

A ferry boat holds at most two people and a total weight of at most `limit`. What is the fewest number of boats for everyone? After sorting the weights, look at the heaviest person who has not boarded yet. They need a boat anyway. The best companion is the _lightest_ person remaining: if even the lightest cannot fit with them, nobody can, and the heavy person goes alone. Otherwise the two board together. Then repeat with the next heaviest.

Two pointers do this with no extra work: `light` at the front, `heavy` at the back. The heavy one always leaves; the light one leaves too if they fit together.

For weights `[5, 1, 4, 2]` and limit 6, sorted `[1, 2, 4, 5]`: the 5 and 1 fit (6), so one boat; the 4 and 2 fit (6), so a second boat. Answer: 2.

This is exactly the problem _Boats to Save People_.

```python
def boats_needed(people, limit):
    p = sorted(people)
    light, heavy = 0, len(p) - 1
    boats = 0
    while light <= heavy:
        if light < heavy and p[light] + p[heavy] <= limit:
            light += 1
        heavy -= 1
        boats += 1
    return boats


assert boats_needed([5, 1, 4, 2], 6) == 2
assert boats_needed([3, 3, 3], 5) == 3
assert boats_needed([], 5) == 0
```

```cpp
int boats_needed(vector<int> people, int limit) {
    sort(people.begin(), people.end());
    int light = 0, heavy = (int)people.size() - 1;
    int boats = 0;
    while (light <= heavy) {
        if (light < heavy && people[light] + people[heavy] <= limit) ++light;
        --heavy;
        ++boats;
    }
    return boats;
}
```

Time is $O(n \log n)$ for sorting; the pairing is $O(n)$.

## 2.5 A reader and a writer

The second style of two pointers: both start at the front, but one is a **reader** that scans every element, and the other is a **writer** that marks where the next _kept_ element goes. This is the classic way to rewrite a list in place.

Take a sorted list and keep each value **at most twice**: `[1, 1, 1, 2, 2, 2, 3]` becomes `[1, 1, 2, 2, 3]`. The reader looks at every value `x`. The writer stands at the next free spot. We keep `x` if fewer than two values have been written yet, or if `x` is different from the value written two spots back (`a[write - 2]`). In a sorted list, if `x` equals the value two spots back, then the last two written values are both equal to `x`, and a third copy must be skipped. Otherwise, there are fewer than two copies of `x` kept so far, and we keep it.

This is exactly the problem _Keep at Most Two of Each Value_.

```python
def keep_at_most_twice(nums):
    a = list(nums)
    write = 0
    for x in a:
        if write < 2 or x != a[write - 2]:
            a[write] = x
            write += 1
    return a[:write]


assert keep_at_most_twice([1, 1, 1, 2, 2, 2, 3]) == [1, 1, 2, 2, 3]
assert keep_at_most_twice([5]) == [5]
assert keep_at_most_twice([]) == []
```

```cpp
vector<int> keep_at_most_twice(vector<int> a) {
    int write = 0;
    for (int x : vector<int>(a)) {
        if (write < 2 || x != a[write - 2]) {
            a[write] = x;
            ++write;
        }
    }
    a.resize(write);
    return a;
}
```

The writer never gets ahead of the reader, so we never overwrite a value we still need to read. Time is $O(n)$ and space $O(1)$ extra (the copy in the Python and C++ above only keeps the input safe; the idea needs no copy).

## 2.6 Check yourself

1. In the pair search, why can we drop `nums[lo]` when the sum is too small?
2. In the triple count, why does one success add `hi - lo` triples?
3. Why does the heavy person always leave in the boats problem?
4. What do the reader and the writer each stand for?

# Chapter 3. Walls and water

## 3.1 The widest container

Picture vertical lines of different heights standing side by side. Pick two lines; together with the ground they form a container, and water fills it up to the _shorter_ of the two lines. The amount of water is

$$\text{area} = \min(h_i, h_j) \cdot (j - i)$$

and we want the best pair. Trying every pair costs $O(n^2)$.

Start with the two outermost lines, which have the widest base. Compute the area. Now we must give up one of the two lines to make progress, and the shorter line is the one to give up. Why? Suppose the left line is shorter. Any container that uses this left line with a closer right line has a narrower base, and its height is limited by this same left line, so it cannot be bigger than what we just measured. The left line can never be part of a better answer, so we drop it and move that pointer inward.

Trace on heights `[3, 9, 2, 6, 4, 7]`: the outer pair (3 and 7) gives $3 \cdot 5 = 15$; the left is shorter, so move it. Now 9 and 7: $7 \cdot 4 = 28$; the right is shorter, so move it. Then 9 and 4: $4 \cdot 3 = 12$, then 9 and 6: $6 \cdot 2 = 12$, then 9 and 2: $2 \cdot 1 = 2$. The best seen is 28.

This is exactly the problem _Container With Most Water_.

```python
def max_water(heights):
    lo, hi = 0, len(heights) - 1
    best = 0
    while lo < hi:
        area = min(heights[lo], heights[hi]) * (hi - lo)
        best = max(best, area)
        if heights[lo] < heights[hi]:
            lo += 1
        else:
            hi -= 1
    return best


assert max_water([3, 9, 2, 6, 4, 7]) == 28
assert max_water([1, 1]) == 1
assert max_water([5]) == 0
```

```cpp
int max_water(const vector<int>& heights) {
    int lo = 0, hi = (int)heights.size() - 1;
    int best = 0;
    while (lo < hi) {
        int area = min(heights[lo], heights[hi]) * (hi - lo);
        best = max(best, area);
        if (heights[lo] < heights[hi]) ++lo;
        else --hi;
    }
    return best;
}
```

Time is $O(n)$ and space $O(1)$.

## 3.2 Rain between bars

Now the bars have width 1 and touch each other, and it rains. Water collects in the dips. How much water is trapped in total? For bars `[3, 0, 2, 0, 4]` the answer is 7.

Think about one position. The water above it rises until it spills over the lower of the tallest bar on its left and the tallest bar on its right. So

$$\text{water}_i = \min(\text{leftmax}_i, \text{rightmax}_i) - h_i$$

where $\text{leftmax}_i$ is the tallest bar at positions $0..i$ and $\text{rightmax}_i$ the tallest at $i..n-1$ (each includes the bar itself, so the result is never negative). The easiest solution computes both "tallest so far" lists first, then adds up. Check with `[3, 0, 2, 0, 4]`: position 1 has $\min(3, 4) - 0 = 3$, position 2 has $\min(3, 4) - 2 = 1$, position 3 has $\min(3, 4) - 0 = 3$, and positions 0 and 4 give 0. Total 7.

```python
def trap_with_arrays(h):
    n = len(h)
    if n == 0:
        return 0
    left_max = [0] * n
    right_max = [0] * n
    left_max[0] = h[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], h[i])
    right_max[n - 1] = h[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], h[i])
    return sum(min(left_max[i], right_max[i]) - h[i] for i in range(n))


assert trap_with_arrays([3, 0, 2, 0, 4]) == 7
assert trap_with_arrays([1, 2, 3]) == 0
assert trap_with_arrays([]) == 0
```

```cpp
long long trap_with_arrays(const vector<int>& h) {
    int n = (int)h.size();
    if (n == 0) return 0;
    vector<int> left_max(n), right_max(n);
    left_max[0] = h[0];
    for (int i = 1; i < n; ++i) left_max[i] = max(left_max[i - 1], h[i]);
    right_max[n - 1] = h[n - 1];
    for (int i = n - 2; i >= 0; --i) right_max[i] = max(right_max[i + 1], h[i]);
    long long total = 0;
    for (int i = 0; i < n; ++i) total += min(left_max[i], right_max[i]) - h[i];
    return total;
}
```

Time is $O(n)$, space is $O(n)$ for the two lists.

## 3.3 Trapping rain water with two pointers

We can save the memory with two pointers. Keep `left` and `right` at the two ends, together with `left_max` (the tallest bar seen from the left so far) and `right_max` (the tallest seen from the right). At each step, update both maxima with the bars under the pointers, then compare them.

If `left_max < right_max`, look at the left bar. We do not know the true tallest bar to its right, but we know it is at least `right_max`, which is taller than `left_max`. So the water above the left bar is limited by `left_max` alone: add `left_max - h[left]`, and move `left` inward. Otherwise `right_max` is the smaller (or equal) one, so do the same on the right side. At every step the side with the smaller wall is the one that is "decided".

This is exactly the problem _Trapping Rain Water_.

```python
def trap_water(h):
    left, right = 0, len(h) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        left_max = max(left_max, h[left])
        right_max = max(right_max, h[right])
        if left_max < right_max:
            water += left_max - h[left]
            left += 1
        else:
            water += right_max - h[right]
            right -= 1
    return water


assert trap_water([3, 0, 2, 0, 4]) == 7
assert trap_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
assert trap_water([2]) == 0
```

```cpp
long long trap_water(const vector<int>& h) {
    int left = 0, right = (int)h.size() - 1;
    int left_max = 0, right_max = 0;
    long long water = 0;
    while (left < right) {
        left_max = max(left_max, h[left]);
        right_max = max(right_max, h[right]);
        if (left_max < right_max) {
            water += left_max - h[left];
            ++left;
        } else {
            water += right_max - h[right];
            --right;
        }
    }
    return water;
}
```

Time is $O(n)$ and space is $O(1)$.

## 3.4 Check yourself

1. Why does the container's water level equal the shorter line?
2. Why can the shorter line be thrown away in the container search?
3. Which two numbers decide the water above a bar?
4. In the two-pointer rain water, why is it enough to know the smaller of the two maxima?

# Chapter 4. Mountains and loops

## 4.1 The longest mountain

A **mountain** in a list is a run of at least three neighbouring values that strictly climbs to a peak and then strictly falls, like `1, 3, 5, 4, 2`. Find the length of the longest mountain. For `[1, 3, 5, 4, 2, 2, 6, 7, 3]` there are two: `1 3 5 4 2` (length 5) and `2 6 7 3` (length 4), so the answer is 5.

Scan for a peak: a position strictly bigger than both neighbours. From the peak, one pointer walks left while the values keep decreasing, another walks right while they keep decreasing. The length is `right - left + 1`. After handling a mountain, we continue the scan from where the right pointer stopped: no position before that can start a longer mountain, since the part we just walked is a downhill (the next mountain can only start at its bottom). So every position is visited a small, constant number of times.

This is exactly the problem _Longest Mountain in an Array_.

```python
def longest_mountain(a):
    n = len(a)
    best = 0
    i = 1
    while i < n - 1:
        if a[i - 1] < a[i] > a[i + 1]:
            left = i - 1
            while left > 0 and a[left - 1] < a[left]:
                left -= 1
            right = i + 1
            while right + 1 < n and a[right] > a[right + 1]:
                right += 1
            best = max(best, right - left + 1)
            i = right
        else:
            i += 1
    return best


assert longest_mountain([1, 3, 5, 4, 2, 2, 6, 7, 3]) == 5
assert longest_mountain([2, 2, 2]) == 0
assert longest_mountain([1, 2, 3]) == 0
assert longest_mountain([0, 5, 0]) == 3
```

```cpp
int longest_mountain(const vector<int>& a) {
    int n = (int)a.size();
    int best = 0;
    int i = 1;
    while (i < n - 1) {
        if (a[i - 1] < a[i] && a[i] > a[i + 1]) {
            int left = i - 1;
            while (left > 0 && a[left - 1] < a[left]) --left;
            int right = i + 1;
            while (right + 1 < n && a[right] > a[right + 1]) ++right;
            best = max(best, right - left + 1);
            i = right;
        } else {
            ++i;
        }
    }
    return best;
}
```

Time is $O(n)$ and space $O(1)$.

## 4.2 A list that loops

Here is a surprising use of two pointers with a very different flavour. Imagine a list `nums` of $n + 1$ numbers, each between 1 and $n$, so some value must repeat (there are more numbers than possible values). Find the repeated value _without changing the list_ and using only constant extra memory.

Treat the list as a set of arrows: from index `i`, follow the arrow to index `nums[i]`. Starting at index 0 and following arrows again and again, we visit a path that must eventually revisit a position (there are only $n + 1$ positions and each arrow leads to a position between 1 and $n$), so it ends in a **cycle**, a loop that goes round and round. Position 0 itself is never a destination, so the path starts with a tail and then enters the cycle. And the spot where the path enters the cycle has two different arrows pointing at it (one from the tail and one from the cycle), which means exactly that two different indexes hold the same value. That value is the repeated number.

So we need to find the entrance of the cycle. The trick: use a slow pointer moving one arrow per step and a fast pointer moving two arrows per step, both starting at 0. If there is a cycle, the fast one laps the slow one and they meet somewhere inside the cycle. Let the tail have length $a$, and let the meeting point be $b$ steps past the entrance. The slow pointer has walked $a + b$ steps and the fast pointer twice as many, $2(a + b)$. The fast pointer has walked the same $a + b$ steps plus some whole laps of the cycle, so $a + b$ is a whole number of laps. Therefore walking $a$ more steps from the meeting point lands exactly on the entrance (that is, completing the laps). So, in a second phase, we start one pointer at 0 and keep the other at the meeting point, move both one step at a time, and they meet exactly at the entrance.

For `[1, 4, 4, 2, 3]` the arrows are $0 \to 1 \to 4 \to 3 \to 2 \to 4$, so the cycle is $4 \to 3 \to 2 \to 4$ and the entrance is 4. Phase 1: slow and fast take steps and meet at 3. Phase 2: from 0 and from 3 they walk $1, 2$ and then $4, 4$, meeting at 4. The repeated number is 4.

This is exactly the problem _Find the Duplicate Number_.

```python
def find_duplicate(nums):
    slow = fast = 0
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = 0
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


assert find_duplicate([1, 4, 4, 2, 3]) == 4
assert find_duplicate([3, 1, 3, 4, 2]) == 3
assert find_duplicate([1, 1]) == 1
```

```cpp
int find_duplicate(const vector<int>& nums) {
    int slow = 0, fast = 0;
    while (true) {
        slow = nums[slow];
        fast = nums[nums[fast]];
        if (slow == fast) break;
    }
    slow = 0;
    while (slow != fast) {
        slow = nums[slow];
        fast = nums[fast];
    }
    return slow;
}
```

Time is $O(n)$ and space is $O(1)$. This method is often called the tortoise and hare, or Floyd's cycle detection.

## 4.3 Check yourself

1. In the mountain scan, why can we continue from `right` after one mountain?
2. Why must the path from index 0 end in a cycle?
3. Why are there two arrows into the cycle's entrance?
4. After the two pointers meet, where do we start the second walk?

# Chapter 5. Windows of fixed size

## 5.1 What a window is

A **window** is a block of neighbouring positions, `nums[left..right]`. Think of a rectangular frame sliding along a long strip of numbers. The key idea of the whole rest of this page is: when the window moves one step, almost nothing changes. One value enters on the right, one value leaves on the left, and everything in the middle stays. So instead of recomputing the sum (or the count, or whatever) of the whole window each time, we **update** it with those two changes.

This turns $O(n \cdot k)$ work (a window of size $k$, recomputed at each of $n$ positions) into $O(n)$.

## 5.2 The best block of K values

Find the largest sum of $k$ consecutive values. Compute the sum of the first $k$ values once. Then slide: add the new value that enters on the right, subtract the old value that leaves on the left, and keep the largest total seen.

For `[1, 4, 2, 10, 2, 3, 1, 0, 20]` and $k = 4$: the first window `1 4 2 10` has sum 17. Slide: add 2, subtract 1 to get 18; add 3, subtract 4 to get 17; add 1, subtract 2 to get 16; add 0, subtract 10 to get 6; add 20, subtract 2 to get 24. The best is 24 (the block `3 1 0 20`).

This is exactly the problem _Maximum Sum of K Consecutive Values_.

```python
def max_sum_k(nums, k):
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]
        best = max(best, window)
    return best


assert max_sum_k([1, 4, 2, 10, 2, 3, 1, 0, 20], 4) == 24
assert max_sum_k([5, -1, 2], 3) == 6
assert max_sum_k([-3, -1, -2], 1) == -1
```

```cpp
long long max_sum_k(const vector<int>& nums, int k) {
    long long window = 0;
    for (int i = 0; i < k; ++i) window += nums[i];
    long long best = window;
    for (int right = k; right < (int)nums.size(); ++right) {
        window += nums[right] - nums[right - k];
        best = max(best, window);
    }
    return best;
}
```

Time is $O(n)$ and space $O(1)$.

## 5.3 Taking cards from the ends

Cards lie in a row. In each of $k$ steps, you take one card from the left end or the right end. What is the biggest total? You can end up taking some cards from the left and the rest from the right, which looks like many possible choices ($k + 1$ different splits). But think about what you do **not** take: it is a block of neighbouring cards in the middle, of size $n - k$. The total you take is the sum of all cards minus the sum of that untouched middle block. To maximise what you take, minimise the sum of the middle block of size $n - k$, which is a fixed-size window problem.

For cards `[4, 1, 6, 2, 9, 3, 5]` and $k = 3$: the total is 30 and the middle windows of size 4 have sums 13, 18, 20, 19. The smallest is 13, so the best you can take is $30 - 13 = 17$ (the three cards 9, 3 and 5 at the right end).

This is exactly the problem _Maximum Points From Cards_.

```python
def max_points(points, k):
    n = len(points)
    w = n - k
    window = sum(points[:w])
    smallest = window
    for right in range(w, n):
        window += points[right] - points[right - w]
        smallest = min(smallest, window)
    return sum(points) - smallest


assert max_points([4, 1, 6, 2, 9, 3, 5], 3) == 17
assert max_points([2, 2, 2], 3) == 6
assert max_points([1, 9, 1], 1) == 1
```

```cpp
long long max_points(const vector<int>& points, int k) {
    int n = (int)points.size();
    int w = n - k;
    long long window = 0;
    for (int i = 0; i < w; ++i) window += points[i];
    long long smallest = window;
    for (int right = w; right < n; ++right) {
        window += points[right] - points[right - w];
        smallest = min(smallest, window);
    }
    long long total = accumulate(points.begin(), points.end(), 0LL);
    return total - smallest;
}
```

When $k = n$ the window is empty (size 0), its sum is 0, and we take everything. Time is $O(n)$.

## 5.4 Windows of letter counts

A window does not have to hold a sum. It can hold a **count** of each letter. Two words are **anagrams** (one is a permutation of the other) if they have the same letters with the same counts, like `ab` and `ba`. To find every place where an anagram of a word `p` hides inside a longer string `s`, slide a window of length $|p|$ over `s`, keeping a list of 26 letter counts. When the window moves, increase the count of the entering letter and decrease the count of the leaving letter. If the 26 counts equal the 26 counts of `p`, we found one.

For `s = "aabbaab"` and `p = "ab"`: the windows are `aa`, `ab`, `bb`, `ba`, `aa`, `ab`, and the ones with one `a` and one `b` start at positions 1, 3 and 5. This is exactly the problem _Find All Anagrams in a String_.

```python
def find_anagram_starts(s, p):
    m = len(p)
    if m == 0 or m > len(s):
        return []
    need = [0] * 26
    have = [0] * 26
    for ch in p:
        need[ord(ch) - 97] += 1
    result = []
    for right, ch in enumerate(s):
        have[ord(ch) - 97] += 1
        if right >= m:
            have[ord(s[right - m]) - 97] -= 1
        if right >= m - 1 and have == need:
            result.append(right - m + 1)
    return result


assert find_anagram_starts("aabbaab", "ab") == [1, 3, 5]
assert find_anagram_starts("cbaebabacd", "abc") == [0, 6]
assert find_anagram_starts("abc", "") == []
```

```cpp
vector<int> find_anagram_starts(const string& s, const string& p) {
    int m = (int)p.size();
    vector<int> result;
    if (m == 0 || m > (int)s.size()) return result;
    vector<int> need(26, 0), have(26, 0);
    for (char ch : p) ++need[ch - 'a'];
    for (int right = 0; right < (int)s.size(); ++right) {
        ++have[s[right] - 'a'];
        if (right >= m) --have[s[right - m] - 'a'];
        if (right >= m - 1 && have == need) result.push_back(right - m + 1);
    }
    return result;
}
```

Comparing two lists of 26 numbers costs 26 steps, a constant, so the whole scan is $O(n)$ with $O(1)$ extra space (26 slots, twice).

Now the same scan answers a yes/no question: does `s2` contain a permutation of `s1`? Just return whether there is at least one start. This is exactly the problem _Permutation in a String_.

```python
def contains_permutation(s1, s2):
    return len(s1) > 0 and len(find_anagram_starts(s2, s1)) > 0


assert contains_permutation("ab", "xbaz") is True
assert contains_permutation("ab", "xbzaz") is False
assert contains_permutation("", "abc") is False
```

```cpp
bool contains_permutation(const string& s1, const string& s2) {
    return !s1.empty() && !find_anagram_starts(s2, s1).empty();
}
```

(The sheet's function accepts an empty `s1` too; follow the problem statement for that edge case.)

## 5.5 Check yourself

1. When a window of size $k$ moves one step, which two values change?
2. In the cards problem, what is the untouched middle block?
3. What happens in the cards problem when $k$ equals $n$?
4. Why is comparing two 26-letter lists still a constant amount of work?

# Chapter 6. Windows that grow and shrink

## 6.1 The grow-and-shrink rhythm

Many questions do not fix the window size; they ask for the **longest** or **shortest** window that satisfies some rule. The pattern is always the same two moves:

- **Grow**: move `right` one step to include the next element, and update the window's information.
- **Shrink**: while the window breaks the rule (or, for "shortest" problems, while it still satisfies it), move `left` one step to drop an element, and update the information.

Why is this fast? Each of the $n$ positions enters the window once (when `right` passes it) and leaves the window at most once (when `left` passes it). So the two pointers together make at most $2n$ moves, and the time is $O(n)$, even though there is a loop inside a loop.

One condition makes this work: when the window grows, the rule must get "harder to satisfy", and when it shrinks, "easier", in a steady way. For sums of positive numbers, distinct-counts or counts of zeros that is true. Negative numbers would break it, so watch the problem statement.

## 6.2 The shortest block with a large sum

All numbers are positive. Find the length of the shortest block of neighbours whose sum is at least a target (or 0 if there is none). Grow `right`, adding each value to the running sum. As soon as the sum reaches the target, the block is long enough, so record its length and shrink from the left to see if a shorter block still works. Positive numbers guarantee that removing a value from the left only lowers the sum, so we never need to look back.

For `[5, 1, 3, 5, 10, 7, 4, 9, 2, 8]` and target 15, the shortest block is `5 10` (sum 15), of length 2.

This is exactly the problem _Smallest Subarray With a Large Sum_.

```python
def min_subarray_len(target, nums):
    best = len(nums) + 1
    left = 0
    total = 0
    for right, x in enumerate(nums):
        total += x
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best <= len(nums) else 0


assert min_subarray_len(15, [5, 1, 3, 5, 10, 7, 4, 9, 2, 8]) == 2
assert min_subarray_len(11, [1, 2, 3, 4, 5]) == 3
assert min_subarray_len(100, [1, 2, 3]) == 0
```

```cpp
int min_subarray_len(long long target, const vector<int>& nums) {
    int n = (int)nums.size();
    int best = n + 1;
    int left = 0;
    long long total = 0;
    for (int right = 0; right < n; ++right) {
        total += nums[right];
        while (total >= target) {
            best = min(best, right - left + 1);
            total -= nums[left];
            ++left;
        }
    }
    return best <= n ? best : 0;
}
```

Time is $O(n)$ and space $O(1)$.

## 6.3 At most K different letters

Find the longest piece of a string that contains at most $k$ different letters. Keep a dictionary `count` of how many times each letter appears in the window. Grow `right`: add its letter. If the dictionary now has more than $k$ different letters, the window breaks the rule, so shrink from the left: remove letters, and delete a letter from the dictionary when its count reaches zero (so that the size of the dictionary is the number of different letters). After the shrinking, the window is valid, so compare its length with the best.

For `"abaccc"` and $k = 2$ the longest piece is `accc`, length 4.

This is exactly the problem _Longest Substring With K Distinct Characters_.

```python
def longest_k_distinct(s, k):
    count = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        while len(count) > k:
            gone = s[left]
            count[gone] -= 1
            if count[gone] == 0:
                del count[gone]
            left += 1
        best = max(best, right - left + 1)
    return best


assert longest_k_distinct("abaccc", 2) == 4
assert longest_k_distinct("aaa", 1) == 3
assert longest_k_distinct("abc", 0) == 0
```

```cpp
int longest_k_distinct(const string& s, int k) {
    unordered_map<char, int> count;
    int left = 0, best = 0;
    for (int right = 0; right < (int)s.size(); ++right) {
        ++count[s[right]];
        while ((int)count.size() > k) {
            char gone = s[left];
            if (--count[gone] == 0) count.erase(gone);
            ++left;
        }
        best = max(best, right - left + 1);
    }
    return best;
}
```

The same code solves _Fruit Into Baskets_. Trees in a row each hold one type of fruit, you have two baskets, each basket holds one type, and you pick one fruit from each tree going right until something does not fit. That is exactly "the longest run of trees with at most 2 types". The fruit list works like the string, and $k = 2$; use a list of numbers instead of letters.

```python
def total_fruit(fruits):
    count = {}
    left = 0
    best = 0
    for right, f in enumerate(fruits):
        count[f] = count.get(f, 0) + 1
        while len(count) > 2:
            count[fruits[left]] -= 1
            if count[fruits[left]] == 0:
                del count[fruits[left]]
            left += 1
        best = max(best, right - left + 1)
    return best


assert total_fruit([1, 2, 3, 2, 2]) == 4
assert total_fruit([0, 1, 2, 2]) == 3
assert total_fruit([]) == 0
```

```cpp
int total_fruit(const vector<int>& fruits) {
    unordered_map<int, int> count;
    int left = 0, best = 0;
    for (int right = 0; right < (int)fruits.size(); ++right) {
        ++count[fruits[right]];
        while (count.size() > 2) {
            if (--count[fruits[left]] == 0) count.erase(fruits[left]);
            ++left;
        }
        best = max(best, right - left + 1);
    }
    return best;
}
```

This is exactly the problem _Fruit Into Baskets_. Time is $O(n)$, and space is $O(k)$ for the dictionary.

## 6.4 Flipping zeros

A list holds only 0s and 1s, and you may flip at most $k$ zeros to ones. What is the longest run of ones you can create? A window can hold at most $k$ zeros, because we can flip them all. So the question is simply "the longest window with at most $k$ zeros". Keep a count of zeros in the window; when it exceeds $k$, shrink from the left until it does not.

For `[1, 0, 0, 1, 1, 0, 1]` and $k = 1$ the longest window with at most one zero is `1 1 0 1` (the last four values), of length 4.

This is exactly the problem _Longest Run of Ones After K Flips_.

```python
def longest_ones(nums, k):
    zeros = 0
    left = 0
    best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


assert longest_ones([1, 0, 0, 1, 1, 0, 1], 1) == 4
assert longest_ones([0, 0, 1, 1, 1], 0) == 3
assert longest_ones([], 2) == 0
```

```cpp
int longest_ones(const vector<int>& nums, int k) {
    int zeros = 0, left = 0, best = 0;
    for (int right = 0; right < (int)nums.size(); ++right) {
        if (nums[right] == 0) ++zeros;
        while (zeros > k) {
            if (nums[left] == 0) --zeros;
            ++left;
        }
        best = max(best, right - left + 1);
    }
    return best;
}
```

Time is $O(n)$, space $O(1)$.

## 6.5 Replacing letters

You may change at most $k$ letters of a string to anything you like. What is the longest piece that you can make all one letter? In a window, the best plan is to keep the letter that already appears most often and change all the others. So a window is good when

$$\text{window length} - \text{(count of its most common letter)} \le k.$$

The clever trick: we do not need to shrink the window all the way. Keep `max_freq`, the highest letter count we have _seen_ in any window so far. If the window is too long for the rule, slide it by one (remove one letter on the left) instead of shrinking until it is valid. The window never gets smaller, and its size at the end is the answer. A stale `max_freq` is harmless: the window can only grow when a letter count beats the old record, which is exactly when `max_freq` is up to date.

For `"ABBBA"` and $k = 1$ the answer is 4 (change the first `A` to `B`, giving `BBBB`).

This is exactly the problem _Longest Repeating Character Replacement_.

```python
def character_replacement(s, k):
    count = [0] * 26
    left = 0
    max_freq = 0
    best = 0
    for right, ch in enumerate(s):
        idx = ord(ch) - 65
        count[idx] += 1
        max_freq = max(max_freq, count[idx])
        if (right - left + 1) - max_freq > k:
            count[ord(s[left]) - 65] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


assert character_replacement("ABBBA", 1) == 4
assert character_replacement("AABABBA", 1) == 4
assert character_replacement("", 3) == 0
```

```cpp
int character_replacement(const string& s, int k) {
    vector<int> count(26, 0);
    int left = 0, max_freq = 0, best = 0;
    for (int right = 0; right < (int)s.size(); ++right) {
        int idx = s[right] - 'A';
        ++count[idx];
        max_freq = max(max_freq, count[idx]);
        if ((right - left + 1) - max_freq > k) {
            --count[s[left] - 'A'];
            ++left;
        }
        best = max(best, right - left + 1);
    }
    return best;
}
```

Time is $O(n)$, space $O(1)$.

## 6.6 Counting windows: product below K

Windows can also _count_. We want the number of neighbouring blocks (subarrays) of positive numbers whose product is less than $k$. Keep the product of the window. Grow `right` (multiply). While the product is at least $k$, shrink from the left (divide). Now every block that **ends at `right`** and starts anywhere from `left` to `right` is good, because shrinking a block of positive whole numbers can only make its product smaller. There are `right - left + 1` such blocks. Add that to the answer.

For `[3, 2, 4, 1]` and $k = 10$: ending at 3 there is 1 block; ending at 2 (`2`, `3 2`) there are 2; ending at 4 the window shrinks to `2 4` (product 8) giving 2 blocks (`4` and `2 4`); ending at 1 the window `2 4 1` has product 8 and gives 3 blocks. Total $1 + 2 + 2 + 3 = 8$.

This is exactly the problem _Subarrays With Product Less Than K_.

```python
def count_product_less(nums, k):
    if k <= 1:
        return 0
    product = 1
    left = 0
    count = 0
    for right, x in enumerate(nums):
        product *= x
        while product >= k:
            product //= nums[left]
            left += 1
        count += right - left + 1
    return count


assert count_product_less([3, 2, 4, 1], 10) == 8
assert count_product_less([1, 2, 3], 0) == 0
assert count_product_less([10, 5, 2, 6], 100) == 8
```

```cpp
long long count_product_less(const vector<int>& nums, long long k) {
    if (k <= 1) return 0;
    long long product = 1, count = 0;
    int left = 0;
    for (int right = 0; right < (int)nums.size(); ++right) {
        product *= nums[right];
        while (product >= k) {
            product /= nums[left];
            ++left;
        }
        count += right - left + 1;
    }
    return count;
}
```

If $k \le 1$ no block works (every product is at least 1), so we return 0 at once. Time is $O(n)$.

## 6.7 Check yourself

1. Why is the total number of pointer moves at most $2n$ in a grow-and-shrink loop?
2. In the zero-flipping problem, what does the window hold at most?
3. In the product problem, why do `right - left + 1` blocks end at `right`?
4. Why does the "shortest sum" window need positive numbers?

# Chapter 7. The "at most K" counting trick

## 7.1 Exactly K is awkward

Sometimes a problem asks to _count_ the blocks with **exactly** $k$ of something: exactly $k$ different values, or exactly $k$ odd numbers. A window cannot count this directly. If the window has exactly $k$, growing may keep it at $k$ or break it, and shrinking may keep it or break it, so we cannot tell which blocks ending at `right` are good by moving one pointer.

But "**at most** $k$" is easy, because it behaves like the product problem: shrinking a block with at most $k$ different values keeps it that way. So for each `right`, all blocks that start in `left..right` are good, and there are `right - left + 1` of them. Now the trick:

$$\text{exactly } k = \text{at most } k - \text{at most } (k-1).$$

Every block with at most $k$ distinct values either has at most $k-1$ (counted in the second term and cancelled), or has exactly $k$ (the ones we want).

## 7.2 Exactly K different values

Let `at_most(nums, m)` count blocks with at most $m$ different values, with the sliding window: add the new value to a dictionary, shrink while the dictionary has more than $m$ keys, and add `right - left + 1` to the total. Then the answer is `at_most(k) - at_most(k - 1)`.

For `[1, 2, 1, 3, 1, 2]` and $k = 2$: there are 13 blocks with at most 2 different values and 6 with at most 1, so there are $13 - 6 = 7$ blocks with exactly 2. The asserts below check these numbers by running the code.

This is exactly the problem _Subarrays With K Different Values_.

```python
def at_most_distinct(nums, m):
    count = {}
    left = 0
    total = 0
    for right, x in enumerate(nums):
        count[x] = count.get(x, 0) + 1
        while len(count) > m:
            count[nums[left]] -= 1
            if count[nums[left]] == 0:
                del count[nums[left]]
            left += 1
        total += right - left + 1
    return total


def subarrays_with_k_distinct(nums, k):
    return at_most_distinct(nums, k) - at_most_distinct(nums, k - 1)


assert at_most_distinct([1, 2, 1, 3, 1, 2], 2) == 13
assert at_most_distinct([1, 2, 1, 3, 1, 2], 1) == 6
assert subarrays_with_k_distinct([1, 2, 1, 3, 1, 2], 2) == 7
assert subarrays_with_k_distinct([1, 2, 1, 2, 3], 2) == 7
```

```cpp
long long at_most_distinct(const vector<int>& nums, int m) {
    unordered_map<int, int> count;
    int left = 0;
    long long total = 0;
    for (int right = 0; right < (int)nums.size(); ++right) {
        ++count[nums[right]];
        while ((int)count.size() > m) {
            if (--count[nums[left]] == 0) count.erase(nums[left]);
            ++left;
        }
        total += right - left + 1;
    }
    return total;
}

long long subarrays_with_k_distinct(const vector<int>& nums, int k) {
    return at_most_distinct(nums, k) - at_most_distinct(nums, k - 1);
}
```

When $m = 0$ the window must be empty, so it adds 0 each time: that is why `k - 1 = 0` is fine. Time is $O(n)$ (two passes), space $O(k)$.

## 7.3 Exactly K odd numbers

Same trick, different rule. Count the blocks with exactly $k$ odd numbers. The window keeps a count of odd numbers; "at most $m$ odd numbers" is again closed under shrinking. For $m < 0$ nothing qualifies, so we return 0 (this matters when $k = 0$).

For `[2, 1, 1, 2, 1, 2]` and $k = 2$ there are 17 blocks with at most 2 odd numbers and 11 with at most 1, so there are $17 - 11 = 6$ with exactly 2.

This is exactly the problem _Count Nice Subarrays_.

```python
def at_most_odd(nums, m):
    if m < 0:
        return 0
    odd = 0
    left = 0
    total = 0
    for right, x in enumerate(nums):
        odd += x % 2
        while odd > m:
            odd -= nums[left] % 2
            left += 1
        total += right - left + 1
    return total


def number_of_subarrays(nums, k):
    return at_most_odd(nums, k) - at_most_odd(nums, k - 1)


assert at_most_odd([2, 1, 1, 2, 1, 2], 2) == 17
assert at_most_odd([2, 1, 1, 2, 1, 2], 1) == 11
assert number_of_subarrays([2, 1, 1, 2, 1, 2], 2) == 6
assert number_of_subarrays([2, 4, 6], 1) == 0
assert number_of_subarrays([2, 4, 6], 0) == 6
```

```cpp
long long at_most_odd(const vector<int>& nums, int m) {
    if (m < 0) return 0;
    int odd = 0, left = 0;
    long long total = 0;
    for (int right = 0; right < (int)nums.size(); ++right) {
        odd += nums[right] % 2;
        while (odd > m) {
            odd -= nums[left] % 2;
            ++left;
        }
        total += right - left + 1;
    }
    return total;
}

long long number_of_subarrays(const vector<int>& nums, int k) {
    return at_most_odd(nums, k) - at_most_odd(nums, k - 1);
}
```

Time is $O(n)$, space $O(1)$.

## 7.4 Check yourself

1. Why is "at most $k$" easier than "exactly $k$"?
2. In "at most $m$", how many blocks end at `right`?
3. Why does `at_most(0)` count nothing for distinct values?
4. What should `at_most_odd` return when $m$ is negative?

# Chapter 8. The minimum window substring

## 8.1 The hardest window

This is the classic final boss of sliding windows. Given a string `s` and a string `t`, find the **shortest piece** of `s` that contains every letter of `t`, counting repeats (if `t = "aab"` then the piece needs two `a`s and one `b`). If several pieces have the shortest length, take the leftmost. If there is none, return the empty string.

Unlike the earlier "shortest" problem, the rule is not about a sum but about a whole table of needs: every letter of `t` must appear often enough. We will track this table cheaply.

## 8.2 Tracking what is still missing

Make a table `need` with one slot per character. For each letter of `t` add 1 to its slot. A slot with a positive number means "we still need that many of this letter". Keep one more number, `missing`, equal to the total number of letters still needed (at the start it is $|t|$). When a letter enters the window: if its slot is positive, one need has been met, so decrease `missing`; then decrease its slot (a slot can go negative, which means "we have a surplus of this letter"). When a letter leaves the window we do the reverse: increase its slot; if the slot becomes positive, we have fallen short again, so increase `missing`.

The window is valid exactly when `missing == 0`. The loop is the familiar rhythm: grow `right` until valid, then shrink `left` as long as it stays valid, recording the shortest. Record _before_ removing the left letter, and use a strict `<` comparison so that the leftmost of several equal-length windows is kept.

Trace on `s = "abbcabcab"`, `t = "abc"`. Growing from the left, the window first becomes valid at `abbc` (indices 0 to 3), length 4. Shrinking removes `a` and the window `bbc` is missing an `a`, so we stop. Growing again to index 4 gives `bbca`, valid with length 4; shrinking drops the first `b` (still valid, length 3: `bca`), and then the second `b` (invalid). We record `bca` of length 3. Further windows never beat length 3 strictly, so the answer is `bca` (indices 2 to 4).

This is exactly the problem _Minimum Window Substring_.

```python
def min_window(s, t):
    if not t:
        return ""
    need = [0] * 128
    for ch in t:
        need[ord(ch)] += 1
    missing = len(t)
    left = 0
    best_len = len(s) + 1
    best_start = 0
    for right, ch in enumerate(s):
        c = ord(ch)
        if need[c] > 0:
            missing -= 1
        need[c] -= 1
        while missing == 0:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_start = left
            d = ord(s[left])
            need[d] += 1
            if need[d] > 0:
                missing += 1
            left += 1
    return "" if best_len > len(s) else s[best_start:best_start + best_len]


assert min_window("abbcabcab", "abc") == "bca"
assert min_window("a", "aa") == ""
assert min_window("aabxa", "aab") == "aab"
assert min_window("abc", "") == ""
```

```cpp
string min_window(const string& s, const string& t) {
    if (t.empty()) return "";
    vector<int> need(128, 0);
    for (char ch : t) ++need[(int)ch];
    int missing = (int)t.size();
    int left = 0;
    int best_len = (int)s.size() + 1, best_start = 0;
    for (int right = 0; right < (int)s.size(); ++right) {
        int c = (int)s[right];
        if (need[c] > 0) --missing;
        --need[c];
        while (missing == 0) {
            if (right - left + 1 < best_len) {
                best_len = right - left + 1;
                best_start = left;
            }
            int d = (int)s[left];
            ++need[d];
            if (need[d] > 0) ++missing;
            ++left;
        }
    }
    return best_len > (int)s.size() ? "" : s.substr(best_start, best_len);
}
```

Time is $O(|s| + |t|)$: every position of `s` enters and leaves the window once. Space is $O(1)$ for the 128-slot table (or $O(\sigma)$ for an alphabet of size $\sigma$).

## 8.3 Where this goes wrong

Three slips are common. The first is to compare letter counts only for letters of `t`; the table above handles letters not in `t` for free, because their slots start at zero and only go negative, never positive. The second is to record the answer after shrinking instead of before, which loses the last valid window. The third is the tie rule: with `<` (strictly smaller) the first window found of the best length is the leftmost, since windows are found in order of their right end and, for equal length, their left end.

With this table-and-counter idea you can adapt the same loop to many other problems: "contains all of these things" is always a table of needs plus a count of what is still missing.

## 8.4 Check yourself

1. What does a negative slot in `need` mean?
2. When exactly is the window valid?
3. Why do we record the window before moving `left`?
4. What is the time cost, and why is it linear although there is a loop inside a loop?
