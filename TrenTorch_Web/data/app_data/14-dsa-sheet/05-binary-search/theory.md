> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Binary search)

This page teaches binary search: the art of finding something in a huge sorted pile by throwing half of the pile away at every step. You will start with the plain "find this number" search, then learn the two small variations (lower bound and upper bound) that solve most list problems, then bend the idea to rotated lists, to searching for a _number that works_ instead of a position, to two lists at once, and finally to grids.

The page is a staircase. **Chapter 1 is deliberately gentle**: a guessing game and one short function. Every later chapter adds exactly one new idea and only uses what came before. By the last chapter you will be able to solve the hardest questions of this step, such as the median of two sorted lists. Every code example is shown in Python and in C++, so pick whichever language you like.

# Chapter 1. The guessing game

## 1.1 Guess my number

Think of a game. I pick a secret whole number from 1 to 100 and you try to find it. After every guess I answer only "too low", "too high" or "correct". How many guesses do you need?

If you guess 1, then 2, then 3, you may need 100 guesses. A much better plan is to guess 50 first. If I say "too high", the secret is somewhere in 1 to 49, and you have just thrown away 51 numbers with a single question. Guess the middle of what is left (25), and half of that disappears too. After only 7 guesses a single number remains, because $100 \to 50 \to 25 \to 12 \to 6 \to 3 \to 1$ (we round down when the count is odd).

That is the whole idea of **binary search**: keep a range of numbers that could still hold the answer, look at the middle one, and use the answer to cut the range in half. It works because of one fact: the numbers are in order, so "too high" tells you about _everything_ above the guess, not only about the guess itself.

## 1.2 Binary search on a list

Now the secret lives in a list that is sorted from small to large. We want the position (the index) of a target value, or `-1` if the target is not there. We keep two indexes, `lo` and `hi`, meaning "the target, if present, is somewhere between position `lo` and position `hi`, both included".

At each step we look at the middle position `mid`. If `nums[mid]` equals the target we are done. If it is smaller than the target, then everything at or before `mid` is too small as well, so we move `lo` to `mid + 1`. If it is bigger, everything at or after `mid` is too big, so we move `hi` to `mid - 1`. When `lo` passes `hi` the range is empty and the target is not in the list.

This is exactly the problem _Binary Search_.

```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


assert binary_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23) == 5
assert binary_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 30) == -1
assert binary_search([], 7) == -1
```

```cpp
int binary_search_index(const vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

In C++ we write `lo + (hi - lo) / 2` instead of `(lo + hi) / 2`. They are the same number, but the first can never overflow a 32-bit integer when `lo` and `hi` are huge. In Python integers never overflow, so either form is fine.

## 1.3 Tracing a search by hand

Let's search for 23 in `[2, 5, 8, 12, 16, 23, 38, 56, 72, 91]` (ten values, indexes 0 to 9).

- Start: `lo = 0`, `hi = 9`. Middle is index 4, value 16. That is smaller than 23, so `lo = 5`.
- Now `lo = 5`, `hi = 9`. Middle is index 7, value 56. Too big, so `hi = 6`.
- Now `lo = 5`, `hi = 6`. Middle is index 5, value 23. Found, return 5.

Three looks instead of six. If the target is 30, which is not in the list, the first three steps are the same, but then index 5 (value 23) is too small, so `lo = 6`; index 6 (value 38) is too big, so `hi = 5`. Now `lo > hi`, the range is empty, and the answer is `-1`.

Notice that each look at the middle either finds the target or removes the middle position from the range. That is why the loop must end.

## 1.4 Why it is so fast

Every step cuts the range roughly in half. Starting with $n$ values, after one step about $n/2$ remain, then $n/4$, and so on, until one remains. The number of halvings is about $\log_2 n$, so the running time is $O(\log n)$. We use only a few variables, so the extra memory is $O(1)$.

To feel how strong that is: a list of one million values needs at most 20 looks, and a list of one billion values needs at most 30. A step-by-step scan would need up to a billion. The little function below just counts how many times we can halve a number before reaching zero, and shows the 20 and the 30.

```python
def halvings(n):
    steps = 0
    while n > 0:
        n //= 2
        steps += 1
    return steps


assert halvings(1_000_000) == 20
assert halvings(1_000_000_000) == 30
```

```cpp
int halvings(long long n) {
    int steps = 0;
    while (n > 0) {
        n /= 2;
        ++steps;
    }
    return steps;
}
```

## 1.5 Common slips

Binary search is famous for being easy to understand and surprisingly easy to get slightly wrong. Three slips cause most bugs.

The first is the loop condition. With both ends included (`lo` and `hi` both point at real candidates), the loop must run while `lo <= hi`. If you write `lo < hi` you will skip the case where one candidate is left. The second is forgetting the `+ 1` or `- 1` when moving: `lo = mid` instead of `lo = mid + 1` can loop forever on a two-element range. The third is forgetting that the list must be sorted: binary search on an unsorted list gives nonsense, not an error.

In the next chapters we will switch to a slightly different style (the range `[lo, hi)` where `hi` is _not_ included) that avoids most of these slips.

## 1.6 Check yourself

1. How many guesses at most do you need for a secret number between 1 and 1000?
2. Why is it fine to throw away the left part when `nums[mid] < target`?
3. What does the loop `while lo <= hi` do when the list is empty?
4. Why can binary search not be used on an unsorted list?

# Chapter 2. Lower bound and upper bound

## 2.1 When values repeat

In Chapter 1 every value appeared once, so "found it" was a complete answer. Real lists have repeats: `[1, 2, 2, 2, 5]`. Now the questions change. Which `2` do you want, the first, the last? How many are there? Where should a new `2` be inserted so that the list stays sorted?

The trick is to stop asking "is it here?" and ask a sharper question: _where is the first position whose value is not smaller than the target?_ That position always exists (it can be one past the end), and once we know it, the other questions become easy.

## 2.2 Lower bound: first value not smaller

The **lower bound** of a target is the smallest index `i` with `nums[i] >= target`. If every value is smaller, the answer is `len(nums)`. In `[1, 2, 2, 2, 5]` the lower bound of 2 is index 1, and the lower bound of 6 is 5.

This is exactly the problem _Lower Bound_.

We now use a cleaner style. The range `[lo, hi)` includes `lo` but **not** `hi`, and the answer is always inside it or equal to `hi`. Start with `lo = 0`, `hi = len(nums)`. Look at `mid`: if `nums[mid] < target`, then `mid` and everything left of it is too small, so `lo = mid + 1`. Otherwise `mid` _could_ be the answer (it is not smaller than the target), so we keep it by setting `hi = mid`. When `lo == hi` the range holds one position and that is the answer.

```python
def lower_bound(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


assert lower_bound([1, 2, 2, 2, 5], 2) == 1
assert lower_bound([1, 2, 2, 2, 5], 3) == 4
assert lower_bound([1, 2, 2, 2, 5], 6) == 5
assert lower_bound([], 1) == 0
```

```cpp
int lower_bound_index(const vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

Let's trace the lower bound of 2 in `[1, 2, 2, 2, 5]`. Start `lo = 0`, `hi = 5`. Middle is 2 (value 2, not smaller), so `hi = 2`. Middle is 1 (value 2), so `hi = 1`. Middle is 0 (value 1, smaller), so `lo = 1`. Now `lo == hi == 1`: the answer is 1.

Why does it work? Think of the list as a row of "no" and "yes" answers to the question "is `nums[i] >= target`?". Because the list is sorted, the row looks like `no no no yes yes yes`: some "no"s followed by "yes"s. We are looking for the first "yes". Every step looks at one cell and learns whether the boundary is to its left or right. We will use this picture a lot in the next chapters.

Time is $O(\log n)$ and extra space is $O(1)$.

## 2.3 Upper bound: first value larger

The **upper bound** is the smallest index with `nums[i] > target` (strictly larger), or `len(nums)` if there is none. In `[1, 2, 2, 2, 5]` the upper bound of 2 is index 4: the first value bigger than 2 is the 5. It is where a new 2 would be inserted _after_ the existing 2s.

This is exactly the problem _Upper Bound_.

The code is the lower bound with a single character changed: the test `<` becomes `<=`. Now "too small" means "not bigger than the target", so equal values are also thrown away to the left.

```python
def upper_bound(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


assert upper_bound([1, 2, 2, 2, 5], 2) == 4
assert upper_bound([1, 3, 5], 0) == 0
assert upper_bound([1, 3, 5], 5) == 3
```

```cpp
int upper_bound_index(const vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] <= target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

Now the block of equal values `target` occupies positions from `lower_bound` up to, but not including, `upper_bound`. Everything else we need follows from these two numbers.

## 2.4 First, last and how many

The first position of the target is the lower bound, provided the target is really there. The last position is the upper bound minus one. The target is missing when the lower bound equals the length of the list, or when the value at the lower bound is not the target.

This is exactly the problem _First and Last Position_.

Counting is even simpler: the number of copies is the upper bound minus the lower bound. This is exactly the problem _Count Occurrences_. It even works when the target is absent, because then both bounds are the same index and the difference is 0.

```python
def lower_bound(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def find_range(nums, target):
    first = lower_bound(nums, target)
    if first == len(nums) or nums[first] != target:
        return [-1, -1]
    return [first, upper_bound(nums, target) - 1]


def count_equal(nums, target):
    return upper_bound(nums, target) - lower_bound(nums, target)


assert find_range([3, 4, 4, 4, 9, 9], 4) == [1, 3]
assert find_range([3, 4, 4, 4, 9, 9], 9) == [4, 5]
assert find_range([3, 4, 4, 4, 9, 9], 5) == [-1, -1]
assert count_equal([3, 4, 4, 4, 9, 9], 4) == 3
assert count_equal([3, 4, 4, 4, 9, 9], 5) == 0
```

```cpp
int lower_bound_index(const vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

int upper_bound_index(const vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] <= target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

vector<int> find_range(const vector<int>& nums, int target) {
    int first = lower_bound_index(nums, target);
    if (first == (int)nums.size() || nums[first] != target) return {-1, -1};
    return {first, upper_bound_index(nums, target) - 1};
}

int count_equal(const vector<int>& nums, int target) {
    return upper_bound_index(nums, target) - lower_bound_index(nums, target);
}
```

Each call is two binary searches, so time is $O(\log n)$ and space is $O(1)$.

## 2.5 Floor and ceil

Sometimes the target itself is not in the list and we want its closest neighbours. The **floor** of a target is the largest value that is `<= target`; the **ceil** is the smallest value that is `>= target`. For `[1, 2, 8, 10]` and target 5 the floor is 2 and the ceil is 8.

The ceil is simply the value at the lower bound, as long as the lower bound is inside the list. The floor is the value just before the upper bound: the upper bound is the first value _larger_ than the target, so the value right before it is the last one that is not larger. If there is no such value we report `-1`.

This is exactly the problem _Floor and Ceil_.

```python
def floor_and_ceil_values(nums, target):
    lo = lower_bound(nums, target)
    up = upper_bound(nums, target)
    floor_value = nums[up - 1] if up > 0 else -1
    ceil_value = nums[lo] if lo < len(nums) else -1
    return [floor_value, ceil_value]


assert floor_and_ceil_values([1, 2, 8, 10], 5) == [2, 8]
assert floor_and_ceil_values([1, 2, 8, 10], 8) == [8, 8]
assert floor_and_ceil_values([4, 6], 3) == [-1, 4]
assert floor_and_ceil_values([4, 6], 9) == [6, -1]
```

```cpp
vector<int> floor_and_ceil_values(const vector<int>& nums, int target) {
    int lo = lower_bound_index(nums, target);
    int up = upper_bound_index(nums, target);
    int floor_value = up > 0 ? nums[up - 1] : -1;
    int ceil_value = lo < (int)nums.size() ? nums[lo] : -1;
    return {floor_value, ceil_value};
}
```

## 2.6 Check yourself

1. In `[1, 2, 2, 2, 5]`, what are the lower bound and the upper bound of 3?
2. What single change turns the lower bound code into the upper bound code?
3. How do you count the copies of a value using the two bounds?
4. Why is it safe to set `hi = mid` (not `mid - 1`) in the lower bound?

# Chapter 3. Rotated lists

## 3.1 What "rotated" means

Take the sorted list `[10, 20, 30, 40, 50, 60]` and cut it somewhere, say after `30`. Move the front part to the back: you get `[40, 50, 60, 10, 20, 30]`. This is a **rotated** sorted list. Written out with the cut marked, it is `[40, 50, 60 | 10, 20, 30]`: the values climb, drop suddenly once, and climb again, and the whole second climb is lower than the first.

```
index:   0   1   2   3   4   5
value:  40  50  60  10  20  30
                 ^   ^
              the drop; the smallest value is right after it
```

It is no longer sorted, so plain binary search can fail. But the structure is so regular that we can still throw half away at each step, we just need a smarter rule. The key fact is: **the smallest value sits right after the drop, and if you split the list at any middle position, at least one of the two halves is perfectly sorted.**

## 3.2 Finding the smallest value

Compare the middle value with the last value of the current range. If `nums[mid] > nums[hi]`, then the drop is somewhere after `mid` (the middle is in the first, higher staircase, so the minimum is strictly to the right). Otherwise, the middle is in the second staircase (or the range has no drop in it), so the minimum is at `mid` or to its left, and `mid` stays a candidate.

This is exactly the problem _Minimum of a Rotated List_.

```python
def rotated_index_of_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return lo


def rotated_min(nums):
    return nums[rotated_index_of_min(nums)]


assert rotated_min([40, 50, 60, 10, 20, 30]) == 10
assert rotated_min([5, 6, 1, 2, 3, 4]) == 1
assert rotated_min([1, 2, 3]) == 1
assert rotated_min([9]) == 9
```

```cpp
int rotated_index_of_min(const vector<int>& nums) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

int rotated_min(const vector<int>& nums) {
    return nums[rotated_index_of_min(nums)];
}
```

Let's trace `[40, 50, 60, 10, 20, 30]`. Start `lo = 0`, `hi = 5`; middle is index 2 (value 60), which is bigger than the last value 30, so `lo = 3`. Now `lo = 3`, `hi = 5`; middle is index 4 (value 20), not bigger than 30, so `hi = 4`. Now `lo = 3`, `hi = 4`; middle is index 3 (value 10), not bigger than 20, so `hi = 3`. The range is one position: index 3, value 10.

The loop is `while lo < hi` and compares with `nums[hi]`, not `nums[lo]`. Comparing with the _last_ value is what makes the rule unambiguous even if the list was not rotated at all (then every middle value is smaller than the last one, so `hi` keeps shrinking toward the front).

Time is $O(\log n)$, space $O(1)$.

## 3.3 How many rotations

If a sorted list was rotated to the left by $r$ places, the original first value, the smallest one, is now at index $r$. So the number of rotations is exactly the index of the minimum, which is what `rotated_index_of_min` returned. For `[40, 50, 60, 10, 20, 30]` the answer is 3: the original was `[10, 20, 30, 40, 50, 60]`, and moving `10, 20, 30` from the front to the back gives our list, so it was rotated left by 3 places, and the minimum sits at index 3.

This is exactly the problem _How Many Times Was It Rotated?_.

```python
def rotation_amount(nums):
    return rotated_index_of_min(nums)


assert rotation_amount([40, 50, 60, 10, 20, 30]) == 3
assert rotation_amount([10, 20, 30]) == 0
assert rotation_amount([30, 10, 20]) == 1
```

```cpp
int rotation_amount(const vector<int>& nums) {
    return rotated_index_of_min(nums);
}
```

## 3.4 Searching a rotated list

Now we want a target in a rotated list with no repeats. Look at `mid`. We know that one of the two halves, `[lo..mid]` or `[mid..hi]`, is sorted. We can tell which: if `nums[lo] <= nums[mid]`, the left half is sorted (no drop inside it); otherwise the right half is.

Once we know a half is sorted, we can ask the simple question "does the target fall inside the value range of this half?" For a sorted left half, that means `nums[lo] <= target < nums[mid]`. If yes, search the left half. If not, the target can only be in the other half. The same logic mirrors for the right half.

This is exactly the problem _Search in a Rotated List_.

```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


assert search_rotated([40, 50, 60, 10, 20, 30], 20) == 4
assert search_rotated([40, 50, 60, 10, 20, 30], 50) == 1
assert search_rotated([40, 50, 60, 10, 20, 30], 35) == -1
assert search_rotated([], 3) == -1
```

```cpp
int search_rotated(const vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return -1;
}
```

Trace for target 20 in `[40, 50, 60, 10, 20, 30]`: `lo = 0`, `hi = 5`, `mid = 2` (value 60). The left half `40, 50, 60` is sorted but 20 is not between 40 and 60, so `lo = 3`. Now `mid = 4` (value 20). Found, return 4. The time is $O(\log n)$.

## 3.5 Rotated lists with repeats

Allow repeats, as in `[2, 5, 6, 0, 0, 1, 2]`, and the "which half is sorted?" test can break. Consider `[1, 1, 1, 2, 1]`: here `nums[lo]`, `nums[mid]` and `nums[hi]` are all `1`, so the values tell us nothing about where the drop is. The honest fix is to give up on this step and shrink the range by one from each end, throwing away two values that cannot be the only copy of the target (we already know `nums[mid]` is not the target, and the ends equal it). All the other steps stay exactly the same.

This is exactly the problem _Search in a Rotated List With Repeats_.

```python
def search_rotated_with_repeats(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return True
        if nums[lo] == nums[mid] == nums[hi]:
            lo += 1
            hi -= 1
        elif nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False


assert search_rotated_with_repeats([2, 5, 6, 0, 0, 1, 2], 0) is True
assert search_rotated_with_repeats([2, 5, 6, 0, 0, 1, 2], 3) is False
assert search_rotated_with_repeats([1, 1, 1, 2, 1], 2) is True
```

```cpp
bool search_rotated_with_repeats(const vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return true;
        if (nums[lo] == nums[mid] && nums[mid] == nums[hi]) {
            ++lo;
            --hi;
        } else if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return false;
}
```

The price is that a list full of equal values makes us shrink one step at a time. In the worst case the time is $O(n)$; when few values repeat it is still $O(\log n)$. No algorithm can do better in the worst case, because in `[1, 1, 1, 1, 2, 1, 1]` the single 2 could be hiding anywhere.

## 3.6 Check yourself

1. Why do we compare `nums[mid]` with `nums[hi]` and not with `nums[lo]` when finding the minimum?
2. If a list of length 8 is not rotated at all, what is the rotation count?
3. How do you decide which half of a rotated range is sorted?
4. Why can repeated values force linear time?

# Chapter 4. Binary search as a yes/no question

## 4.1 The row of "no" and "yes"

In Chapter 2 we met a picture: write the answer to some question for every position, and binary search finds the border where the answers flip from "no" to "yes". This works for _any_ question whose answers look like `no no no yes yes yes`. We call such a question **monotone**: once it turns "yes", it stays "yes". The list itself does not even need to be sorted; only the row of answers has to be ordered.

So let's write one tiny, reusable function: given a range of positions and a monotone yes/no question, return the first position with a "yes" (or the end of the range if there is none).

```python
def first_true(lo, hi, is_yes):
    # smallest x in [lo, hi) with is_yes(x) true, or hi if there is none
    while lo < hi:
        mid = (lo + hi) // 2
        if is_yes(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


assert first_true(0, 10, lambda x: x * x >= 30) == 6
assert first_true(0, 10, lambda x: False) == 10
assert first_true(3, 10, lambda x: True) == 3
```

```cpp
int first_true(int lo, int hi, const function<bool(int)>& is_yes) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (is_yes(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

The lower bound is the case "is `nums[i] >= target`?". From now on, whenever a problem looks hard, ask: _can I phrase it as a monotone yes/no question over positions?_ If so, the code is this function plus one small question.

## 4.2 The peak of a mountain

A **mountain** list strictly climbs up to a top (the peak) and then strictly falls, like `[1, 3, 5, 4, 2]`. Which index is the peak? The list is not sorted, but there is a monotone question: "is `nums[i] > nums[i + 1]`?" (is the next value lower than this one?). On the way up the answer is "no", from the peak onwards it is "yes". The first "yes" is the peak. We only ask the question for `i` up to the second-to-last index; if every answer is "no", the peak is the last index, which is exactly what `first_true` returns when it reaches the end of the range.

This is exactly the problem _Peak of a Mountain List_.

```python
def mountain_peak(nums):
    return first_true(0, len(nums) - 1, lambda i: nums[i] > nums[i + 1])


assert mountain_peak([1, 3, 5, 4, 2]) == 2
assert mountain_peak([1, 2, 3]) == 2
assert mountain_peak([9, 4, 1]) == 0
assert mountain_peak([7]) == 0
```

```cpp
int mountain_peak(const vector<int>& nums) {
    return first_true(0, (int)nums.size() - 1,
                      [&](int i) { return nums[i] > nums[i + 1]; });
}
```

Time is $O(\log n)$, space $O(1)$.

## 4.3 The single lonely value

Here is a puzzle. A sorted list contains every value exactly twice, except one value that appears once, like `[1, 1, 3, 3, 4, 5, 5]` (the lonely value is 4). Where is it?

Look at where the pairs start. Before the lonely value, each pair starts at an even index: the pair `1, 1` is at indexes 0 and 1, the pair `3, 3` at 2 and 3. After the lonely value, the pairing shifts by one, and pairs start at odd indexes: `5, 5` sits at indexes 5 and 6. So for any even index `i`, ask: "is `nums[i] != nums[i + 1]`?" Before the lonely value the answer is "no" (a proper pair starts here); at or after it, the answer is "yes". That is monotone, so we binary search over even indexes only. To stay on even indexes, if `mid` is odd we step it back by one.

This is exactly the problem _The Single Element in a Sorted List_.

```python
def single_non_duplicate(nums):
    lo, hi = 0, len(nums) - 1          # both always even
    while lo < hi:
        mid = (lo + hi) // 2
        if mid % 2 == 1:
            mid -= 1
        if nums[mid] == nums[mid + 1]:
            lo = mid + 2
        else:
            hi = mid
    return nums[lo]


assert single_non_duplicate([1, 1, 3, 3, 4, 5, 5]) == 4
assert single_non_duplicate([2, 3, 3, 8, 8]) == 2
assert single_non_duplicate([6]) == 6
```

```cpp
int single_non_duplicate(const vector<int>& nums) {
    int lo = 0, hi = (int)nums.size() - 1;   // both always even
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (mid % 2 == 1) --mid;
        if (nums[mid] == nums[mid + 1]) lo = mid + 2;
        else hi = mid;
    }
    return nums[lo];
}
```

Trace on `[1, 1, 3, 3, 4, 5, 5]`: `lo = 0`, `hi = 6`; `mid = 3` is odd so it becomes 2; `nums[2] == nums[3]` (3 and 3), so `lo = 4`. Now `lo = 4`, `hi = 6`; `mid = 5` becomes 4; `nums[4] = 4` differs from `nums[5] = 5`, so `hi = 4`. The answer is `nums[4] = 4`. The list length is odd, so `hi = len - 1` is even and the whole search keeps both ends even. Time is $O(\log n)$.

## 4.4 Counting the missing numbers

Here is a different kind of question. A sorted list of distinct positive numbers is given, like `[2, 3, 4, 7, 11]`. Counting `1, 2, 3, ...` and skipping those in the list, the missing numbers are `1, 5, 6, 8, 9, 10, 12, ...`. What is the 5th missing number?

Look at index `i`. If nothing were missing, the value at index `i` would be `i + 1` (index 0 holds 1, index 1 holds 2, and so on). The difference `nums[i] - (i + 1)` is therefore the number of missing values that come before `nums[i]`. For our list this gives 1, 1, 1, 3, 6. That count never goes down as `i` grows, so the question "are at least `k` numbers missing before `nums[i]`?" is monotone. Let `p` be the first index where it is "yes" (or `len(nums)` if never). Then exactly `p` list values lie below the answer, and the answer itself is the `k`-th missing number, so the numbers up to the answer are `p` present ones plus `k` missing ones: the answer is `p + k`.

For `k = 5`: the first index with a count of at least 5 is index 4 (count 6), so `p = 4` and the answer is `4 + 5 = 9`. That matches the list above.

This is exactly the problem _Kth Missing Positive Number_.

```python
def kth_missing_positive(nums, k):
    p = first_true(0, len(nums), lambda i: nums[i] - (i + 1) >= k)
    return p + k


assert kth_missing_positive([2, 3, 4, 7, 11], 5) == 9
assert kth_missing_positive([1, 2, 3, 4], 2) == 6
assert kth_missing_positive([], 3) == 3
assert kth_missing_positive([5], 2) == 2
```

```cpp
int kth_missing_positive(const vector<int>& nums, int k) {
    int p = first_true(0, (int)nums.size(),
                       [&](int i) { return nums[i] - (i + 1) >= k; });
    return p + k;
}
```

Time is $O(\log n)$. Notice that the answer can be far bigger than any value in the list (when `k` is huge), but we never loop through the numbers, we just compute with the formula.

## 4.5 Check yourself

1. What does "monotone" mean for a yes/no question?
2. For the mountain, which question do we ask at index `i`?
3. Why do we keep `mid` even in the lonely-value search?
4. In `[3, 5, 6]`, how many positive numbers are missing before the value 6?

# Chapter 5. Binary search on the answer

## 5.1 Searching numbers, not positions

So far we searched a list. But binary search needs only a monotone yes/no question over _numbers_, and the numbers can be possible answers to the problem itself. This is the most useful idea on the page.

Here is the pattern. A problem asks: "what is the smallest speed (or size, or capacity, ...) that makes some job possible?" It is hard to compute that smallest value directly. But it is easy to take a _guess_ and check whether the job is possible with it. And the check is monotone: if a speed of 5 works, then a speed of 6 works too. So the guesses form a row `no no no yes yes yes`, and we binary search for the first "yes". The recipe has three steps: choose the range of guesses, write a checker `works(guess)`, and call `first_true`.

The cost is $O(\log R \cdot C)$ where $R$ is the size of the range of guesses and $C$ is the cost of one check. Even a range of a billion guesses needs only 30 checks.

```python
def first_true(lo, hi, is_yes):
    while lo < hi:
        mid = (lo + hi) // 2
        if is_yes(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

```cpp
long long first_true(long long lo, long long hi,
                     const function<bool(long long)>& is_yes) {
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (is_yes(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

(We use `long long` in C++ this time because guesses can be large.)

## 5.2 The slowest speed that works

Imagine piles of bananas, and you eat at some speed $k$ bananas per hour. Each hour you pick one pile and eat up to $k$ from it; a pile of $p$ bananas takes $\lceil p / k \rceil$ hours (the symbol $\lceil x \rceil$ means "round up"). The question: what is the smallest $k$ that lets you finish all piles within $H$ hours?

The checker is easy: add up $\lceil p / k \rceil$ over all piles and compare with $H$. In integer code, rounding up is `(p + k - 1) // k`. A bigger $k$ never takes more hours, so the check is monotone. The smallest sensible speed is 1; the largest we would ever need is the biggest pile (more speed than that does not help, since one hour is the minimum per pile).

Take piles `[7, 2, 9]` and $H = 5$. For speed 4 we need $2 + 1 + 3 = 6$ hours, too slow. For speed 5 we need $2 + 1 + 2 = 5$ hours, fast enough. So the answer is 5.

This is exactly the problem _Eating Speed_.

```python
def hours_needed(piles, speed):
    return sum((p + speed - 1) // speed for p in piles)


def min_speed(piles, hours):
    return first_true(1, max(piles) + 1, lambda k: hours_needed(piles, k) <= hours)


assert hours_needed([7, 2, 9], 4) == 6
assert hours_needed([7, 2, 9], 5) == 5
assert min_speed([7, 2, 9], 5) == 5
assert min_speed([7, 2, 9], 3) == 9
```

```cpp
long long hours_needed(const vector<long long>& piles, long long speed) {
    long long total = 0;
    for (long long p : piles) total += (p + speed - 1) / speed;
    return total;
}

long long min_speed(const vector<long long>& piles, long long hours) {
    long long biggest = *max_element(piles.begin(), piles.end());
    return first_true(1, biggest + 1, [&](long long k) {
        return hours_needed(piles, k) <= hours;
    });
}
```

Time is $O(n \log M)$ where $M$ is the biggest pile.

## 5.3 Same pattern, new stories

Many problems are the same machine with a different checker. Two examples.

**Smallest divisor.** Pick a whole number $d$, divide every number of a list by $d$, round each result up and add them up. Find the smallest $d$ for which the sum is at most a given threshold. This is the banana problem in disguise: a bigger $d$ makes the sum smaller, so the check is monotone. This is exactly the problem _Smallest Divisor Within a Threshold_. The search range is from 1 to the largest number.

For `[8, 3, 10]` with threshold 6: $d = 3$ gives $3 + 1 + 4 = 8$ (too big) and $d = 4$ gives $2 + 1 + 3 = 6$ (fine), so the smallest divisor is 4.

```python
def smallest_divisor(nums, threshold):
    def ok(d):
        return sum((x + d - 1) // d for x in nums) <= threshold
    return first_true(1, max(nums) + 1, ok)


assert smallest_divisor([8, 3, 10], 6) == 4
assert smallest_divisor([8, 3, 10], 3) == 10
```

```cpp
long long smallest_divisor(const vector<long long>& nums, long long threshold) {
    long long biggest = *max_element(nums.begin(), nums.end());
    return first_true(1, biggest + 1, [&](long long d) {
        long long total = 0;
        for (long long x : nums) total += (x + d - 1) / d;
        return total <= threshold;
    });
}
```

**Days to make bouquets.** Flower $i$ blooms on day `bloom[i]`. A bouquet needs $k$ neighbouring flowers that have all bloomed. What is the earliest day on which we can make $m$ bouquets? On day $d$, walk through the flowers and count runs of consecutive bloomed flowers: every time a run reaches $k$ flowers, one bouquet is made and the run restarts. More days means more bouquets, so the check "can I make $m$ bouquets by day $d$?" is monotone. If $m \cdot k$ is more than the number of flowers it is impossible and we answer `-1`.

For `[5, 2, 9, 2, 4, 3]` with $m = 2$ bouquets of $k = 2$ flowers: on day 4 the bloomed flowers are at positions 1, 3, 4 and 5. Position 1 stands alone, and positions 3 to 5 form a run of three, which makes only one bouquet of two. On day 5 position 0 has bloomed too, so positions 0 and 1 form a second bouquet. The answer is day 5.

This is exactly the problem _Days to Make Bouquets_.

```python
def bouquets_by_day(bloom, k, day):
    made = run = 0
    for b in bloom:
        if b <= day:
            run += 1
            if run == k:
                made += 1
                run = 0
        else:
            run = 0
    return made


def min_days_for_bouquets(bloom, m, k):
    if m * k > len(bloom):
        return -1
    return first_true(min(bloom), max(bloom) + 1,
                      lambda day: bouquets_by_day(bloom, k, day) >= m)


assert bouquets_by_day([5, 2, 9, 2, 4, 3], 2, 4) == 1
assert bouquets_by_day([5, 2, 9, 2, 4, 3], 2, 5) == 2
assert min_days_for_bouquets([5, 2, 9, 2, 4, 3], 2, 2) == 5
assert min_days_for_bouquets([1, 2], 2, 2) == -1
```

```cpp
int bouquets_by_day(const vector<int>& bloom, int k, int day) {
    int made = 0, run = 0;
    for (int b : bloom) {
        if (b <= day) {
            ++run;
            if (run == k) {
                ++made;
                run = 0;
            }
        } else {
            run = 0;
        }
    }
    return made;
}

long long min_days_for_bouquets(const vector<int>& bloom, int m, int k) {
    if ((long long)m * k > (long long)bloom.size()) return -1;
    long long lo = *min_element(bloom.begin(), bloom.end());
    long long hi = *max_element(bloom.begin(), bloom.end()) + 1;
    return first_true(lo, hi, [&](long long day) {
        return bouquets_by_day(bloom, k, (int)day) >= m;
    });
}
```

In every case the range of guesses is a _value_ range (days, speeds, divisors), not an index range. The cost is $O(n \log R)$.

## 5.4 Cutting a row into days

A very common shape: items in a fixed order, and a _limit_ on what one day (or one truck, one student) can handle. Packages with weights must be shipped in order. Each day the ship carries a run of consecutive packages whose total weight is at most its capacity. What is the smallest capacity that ships everything within $D$ days?

The checker `days_needed(capacity)` goes greedily: keep adding packages to the current day while the total fits; when the next package does not fit, start a new day. This greedy is optimal because putting as many as possible on the earliest days never hurts. A bigger capacity never needs more days, so the check is monotone. The guess can never be smaller than the heaviest package (that package must fit alone), and never needs to be bigger than the total weight (everything in one day). So the range is from `max(weights)` to `sum(weights)`.

Take weights `[4, 8, 2, 6]` and 2 days. Capacity 11 needs 3 days (`4`, `8 2`, `6`), capacity 12 needs 2 days (`4 8`, `2 6`). The answer is 12.

This is exactly the problem _Ship Packages Within D Days_.

```python
def days_needed(weights, capacity):
    days, current = 1, 0
    for w in weights:
        if current + w > capacity:
            days += 1
            current = 0
        current += w
    return days


def ship_capacity(weights, days):
    return first_true(max(weights), sum(weights) + 1,
                      lambda cap: days_needed(weights, cap) <= days)


assert days_needed([4, 8, 2, 6], 11) == 3
assert days_needed([4, 8, 2, 6], 12) == 2
assert ship_capacity([4, 8, 2, 6], 2) == 12
assert ship_capacity([4, 8, 2, 6], 4) == 8
```

```cpp
int days_needed(const vector<int>& weights, long long capacity) {
    int days = 1;
    long long current = 0;
    for (int w : weights) {
        if (current + w > capacity) {
            ++days;
            current = 0;
        }
        current += w;
    }
    return days;
}

long long ship_capacity(const vector<int>& weights, int days) {
    long long lo = *max_element(weights.begin(), weights.end());
    long long hi = accumulate(weights.begin(), weights.end(), 0LL) + 1;
    return first_true(lo, hi, [&](long long cap) {
        return days_needed(weights, cap) <= days;
    });
}
```

Time is $O(n \log S)$ where $S$ is the sum of the weights.

## 5.5 Integer roots

The same machinery can invert a function. Suppose we want the whole number $x$ with $x^m = n$, or $-1$ if there is none (for example the cube root of 27 is 3, while 2 has no whole square root). The function $x \mapsto x^m$ goes up as $x$ goes up, so the question "is $x^m \ge n$?" is monotone. Find the first $x$ where it is "yes", and then check whether $x^m$ is exactly $n$.

In Python big numbers are no problem. In C++, $x^m$ can overflow, so we compute the power with an early stop: as soon as the running product would exceed $n$, we stop and say "too big". The product $r \cdot x$ exceeds $n$ exactly when $r > \lfloor n / x \rfloor$, and this test uses no big multiplication.

This is exactly the problem _Integer Root_.

```python
def integer_root(n, m):
    x = first_true(1, n + 1, lambda x: x ** m >= n)
    return x if x ** m == n else -1


assert integer_root(27, 3) == 3
assert integer_root(2, 2) == -1
assert integer_root(1, 5) == 1
assert integer_root(10 ** 18, 2) == 10 ** 9
```

```cpp
// returns true when x^m >= n, never overflowing
bool power_reaches(long long x, int m, long long n) {
    long long r = 1;
    for (int i = 0; i < m; ++i) {
        if (r > n / x) return true;      // r * x would already exceed n
        r *= x;
    }
    return r >= n;
}

long long integer_root(long long n, int m) {
    long long x = first_true(1, n + 1, [&](long long v) {
        return power_reaches(v, m, n);
    });
    // x^m >= n; it is an exact root only if x^(m) == n
    long long r = 1;
    for (int i = 0; i < m; ++i) {
        if (r > n / x) return -1;
        r *= x;
    }
    return r == n ? x : -1;
}
```

The range is $1 \ldots n$, so there are about $\log_2 n$ guesses (at most 60 for $n \le 10^{18}$), each costing $O(m)$.

## 5.6 Check yourself

1. In the banana problem, why is the range of speeds `1` to `max(piles)`?
2. Why must the ship capacity start at the heaviest package?
3. What makes a "can I do it with this guess?" check monotone?
4. Why does the C++ integer root test `r > n / x` instead of `r * x > n`?

# Chapter 6. Biggest smallest and smallest biggest

## 6.1 Looking for the last "yes"

First, the `first_true` helper from Chapter 5 once more, since this chapter uses it.

```python
def first_true(lo, hi, is_yes):
    while lo < hi:
        mid = (lo + hi) // 2
        if is_yes(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

```cpp
long long first_true(long long lo, long long hi,
                     const function<bool(long long)>& is_yes) {
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (is_yes(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

In Chapter 5 the checker was "yes" for large guesses, and we wanted the _first_ yes. Sometimes it is the other way round: the checker is "yes" for small guesses and "no" for large ones (`yes yes yes no no no`), and we want the _largest_ guess that still works. We can use the same function on the flipped question, or write the mirror image directly.

The mirror needs one careful detail. Because we move `lo = mid` (keeping `mid` as a candidate) when the answer is "yes", the middle must round **up**, `(lo + hi + 1) // 2`. If it rounded down, then with `lo = 3` and `hi = 4` we would get `mid = 3`, set `lo = 3` again, and loop forever.

```python
def last_true(lo, hi, is_yes):
    # largest x in [lo, hi] with is_yes(x) true; assumes is_yes(lo) is true
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if is_yes(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


assert last_true(0, 100, lambda x: x * x <= 50) == 7
assert last_true(5, 5, lambda x: True) == 5
assert last_true(1, 9, lambda x: x <= 1) == 1
```

```cpp
long long last_true(long long lo, long long hi,
                    const function<bool(long long)>& is_yes) {
    while (lo < hi) {
        long long mid = lo + (hi - lo + 1) / 2;
        if (is_yes(mid)) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}
```

## 6.2 Cows in stalls

Stalls stand at positions on a line, and we must place $c$ cows in different stalls so that the **smallest distance between any two cows is as large as possible**. This "maximise the minimum" wording is the signal for `last_true`.

Guess a distance $d$ and ask: can we place all $c$ cows with every pair at least $d$ apart? The greedy answer: sort the stalls, put the first cow in the first stall, and then put the next cow in the first stall that is at least $d$ beyond the previous cow. Count the cows; if we reach $c$, the guess works. A smaller $d$ is always easier, so the check is `yes yes yes no no no`. The range is from 1 (any placement works with distance 1 when positions are distinct integers) to the span between the first and last stall.

For stalls `[1, 3, 7, 12]` and 3 cows: with $d = 5$ the cows go to 1, 7, 12 (three cows), with $d = 6$ they go to 1, 7 and then 13 does not exist, so only two cows. The answer is 5.

This is exactly the problem _Place the Cows Far Apart_.

```python
def cows_placed(stalls, d):
    count, last = 1, stalls[0]
    for s in stalls[1:]:
        if s - last >= d:
            count += 1
            last = s
    return count


def aggressive_cows(stalls, cows):
    stalls = sorted(stalls)
    return last_true(1, stalls[-1] - stalls[0],
                     lambda d: cows_placed(stalls, d) >= cows)


assert cows_placed([1, 3, 7, 12], 5) == 3
assert cows_placed([1, 3, 7, 12], 6) == 2
assert aggressive_cows([12, 1, 7, 3], 3) == 5
assert aggressive_cows([4, 9], 2) == 5
```

```cpp
int cows_placed(const vector<int>& stalls, long long d) {
    int count = 1;
    int last = stalls[0];
    for (size_t i = 1; i < stalls.size(); ++i) {
        if (stalls[i] - last >= d) {
            ++count;
            last = stalls[i];
        }
    }
    return count;
}

long long aggressive_cows(vector<int> stalls, int cows) {
    sort(stalls.begin(), stalls.end());
    return last_true(1, stalls.back() - stalls[0], [&](long long d) {
        return cows_placed(stalls, d) >= cows;
    });
}
```

Time is $O(n \log n + n \log S)$: the sort, then about $\log S$ checks of $O(n)$ each.

## 6.3 Splitting books fairly

Now the opposite wording: "minimise the maximum". Books with various page counts are in a row. Give each of $s$ students a run of consecutive books (every book to exactly one student, everyone at least one book) so that the **largest page total given to anyone is as small as possible**.

This is the ship problem from Section 5.4 in new clothes: students are days, and the page limit is the capacity. Guess a limit; walk through the books, start a new student whenever the next book would push the current total above the limit, and count students. If the count is at most $s$ the guess works. (If fewer students are needed than we have, it is fine: we can always split a run further without raising the maximum, as long as there are at least $s$ books.) If there are fewer books than students, no valid split exists and the answer is `-1`.

The range is from the biggest book to the total pages. For pages `[10, 20, 30, 40]` and 2 students: limit 60 needs two students (`10 20 30` and `40`), limit 59 needs three. The answer is 60.

This is exactly the problem _Allocate Books_.

```python
def students_needed(pages, limit):
    students, current = 1, 0
    for p in pages:
        if current + p > limit:
            students += 1
            current = 0
        current += p
    return students


def allocate_books(pages, students):
    if len(pages) < students:
        return -1
    return first_true(max(pages), sum(pages) + 1,
                      lambda lim: students_needed(pages, lim) <= students)


assert students_needed([10, 20, 30, 40], 60) == 2
assert students_needed([10, 20, 30, 40], 59) == 3
assert allocate_books([10, 20, 30, 40], 2) == 60
assert allocate_books([10, 20], 3) == -1
assert allocate_books([10, 20, 30], 3) == 30
```

```cpp
int students_needed(const vector<int>& pages, long long limit) {
    int students = 1;
    long long current = 0;
    for (int p : pages) {
        if (current + p > limit) {
            ++students;
            current = 0;
        }
        current += p;
    }
    return students;
}

long long allocate_books(const vector<int>& pages, int students) {
    if ((int)pages.size() < students) return -1;
    long long lo = *max_element(pages.begin(), pages.end());
    long long hi = accumulate(pages.begin(), pages.end(), 0LL) + 1;
    return first_true(lo, hi, [&](long long lim) {
        return students_needed(pages, lim) <= students;
    });
}
```

## 6.4 Choosing the range

A binary search on the answer is only correct if the range contains the true answer, and the checker is monotone over the whole range. Here is a short routine for setting both up.

For the low end, ask "what is the smallest value that could possibly be the answer?" (the biggest single item for splitting problems, 1 for speeds and divisors). For the high end, ask "what value is certainly enough?" (the total for splitting, the largest pile for speeds). Slightly too wide is always safe; slightly too narrow gives wrong answers. If the answer might not exist at all (as in bouquets), handle that case before the search.

## 6.5 Check yourself

1. Which wording ("maximise the minimum" or "minimise the maximum") needs `last_true`, and which needs `first_true`?
2. Why must `last_true` round the middle up?
3. In the book problem, why does the low end start at the largest book?
4. What do you answer if there are fewer books than students?

# Chapter 7. Two sorted lists

## 7.1 The question

We have two sorted lists `a` and `b`, possibly of different lengths, and want the $k$-th smallest value of all of them put together (counting from 1), or their median. The easy way is to merge the two lists and read the answer, which costs $O(n + m)$. Can we do it in $O(\log)$, reading only a handful of values? Yes, with a clever cut.

## 7.2 Cutting both lists

Imagine we have already merged everything. The $k$ smallest values form a "left part", and the rest form a "right part". The left part is made of some `i` smallest values of `a` and some `j` smallest values of `b`, with $i + j = k$. So the whole problem is to find the number `i`: how many values we take from `a`.

When is a choice of `i` correct? The cut is valid when every value in the left part is at most every value in the right part. Inside one list that is already true (sorted). So we only need to compare across: the last value taken from `a` (`a[i-1]`) must not be larger than the first value left in `b` (`b[j]`), and the last value taken from `b` (`b[j-1]`) must not be larger than the first value left in `a` (`a[i]`).

Example: `a = [2, 3, 6, 7, 9]`, `b = [1, 4, 8, 10]`, $k = 5$. Try `i = 2`, so `j = 3`. Left part: `2, 3` and `1, 4, 8`. But `8` is bigger than `a[2] = 6`, which sits in the right part. Not valid, we took too many from `b`. Try `i = 3`, `j = 2`: left part `2, 3, 6` and `1, 4`; right part starts with `a[3] = 7` and `b[2] = 8`. The largest on the left is 6 and the smallest on the right is 7. Valid! The 5th smallest is the largest of the left part: 6.

## 7.3 Searching for the cut

The question "should we take more from `a`?" is monotone. For a candidate `i` (with `j = k - i`), we ask: is `a[i] >= b[j-1]`? (the first value left in `a` is not smaller than the last taken from `b`). When `i` is small this is false ("we have not taken enough from `a`"), and once it turns true it stays true: as `i` grows, `a[i]` grows and `b[j-1]` shrinks. So we look for the first `i` where it is true: that is the valid cut.

The bounds on `i` come from the sizes. We cannot take more than `k` values or more than `len(a)` from `a`, so `i <= min(k, len(a))`. And we cannot take more than `len(b)` from `b`, so `j = k - i <= len(b)`, which means `i >= k - len(b)`. Also `i >= 0`. To keep the search small and the code simple, we always search on the shorter list (swap them if needed).

The function returns the two "border" values: the largest value of the left part and the smallest of the right part. A value past the end of a list counts as infinity, and a value before the start as minus infinity.

```python
INF = float("inf")


def cut_values(a, b, k):
    # the k smallest of a+b form the "left part"; return (left_max, right_min)
    if len(a) > len(b):
        a, b = b, a
    n, m = len(a), len(b)
    lo, hi = max(0, k - m), min(k, n)
    while lo < hi:
        i = (lo + hi) // 2
        j = k - i
        if a[i] < b[j - 1]:
            lo = i + 1          # took too few from a
        else:
            hi = i
    i = lo
    j = k - i
    left_max = max(a[i - 1] if i > 0 else -INF, b[j - 1] if j > 0 else -INF)
    right_min = min(a[i] if i < n else INF, b[j] if j < m else INF)
    return left_max, right_min


def kth_of_two(a, b, k):
    return cut_values(a, b, k)[0]


assert kth_of_two([2, 3, 6, 7, 9], [1, 4, 8, 10], 5) == 6
assert kth_of_two([2, 3, 6, 7, 9], [1, 4, 8, 10], 1) == 1
assert kth_of_two([2, 3, 6, 7, 9], [1, 4, 8, 10], 9) == 10
assert kth_of_two([5, 6], [], 2) == 6
assert kth_of_two([], [4, 4, 4], 2) == 4
```

```cpp
pair<double, double> cut_values(vector<int> a, vector<int> b, int k) {
    if (a.size() > b.size()) swap(a, b);
    int n = (int)a.size(), m = (int)b.size();
    const double INF = 1e18;
    int lo = max(0, k - m), hi = min(k, n);
    while (lo < hi) {
        int i = (lo + hi) / 2;
        int j = k - i;
        if (a[i] < b[j - 1]) lo = i + 1;
        else hi = i;
    }
    int i = lo, j = k - i;
    double left_max = max(i > 0 ? (double)a[i - 1] : -INF,
                          j > 0 ? (double)b[j - 1] : -INF);
    double right_min = min(i < n ? (double)a[i] : INF,
                           j < m ? (double)b[j] : INF);
    return {left_max, right_min};
}

long long kth_of_two(const vector<int>& a, const vector<int>& b, int k) {
    return (long long)cut_values(a, b, k).first;
}
```

(The vectors are passed by value here only so the function can swap them; in a real program swap two references or two indexes instead.)

Why are the array reads safe? Inside the loop `lo < hi`, so `i < hi <= min(k, n)`, which means `i < n` and `i < k`; therefore `a[i]` exists and `j = k - i >= 1`. Also `i >= lo >= k - m`, so `j <= m` and `b[j-1]` exists.

The loop runs $O(\log \min(n, m))$ times. Each step reads two values, so the whole search reads $O(\log \min(n, m))$ values.

This is exactly the problem _Kth Value of Two Sorted Lists_.

## 7.4 The median

The **median** is the middle value of all the numbers when sorted: for an odd count it is the single middle value, for an even count it is the average of the two middle values. Let the total count be $t = n + m$. Let the left part contain $\lceil t / 2 \rceil$ values, that is, $k = (t + 1)//2$. For an odd $t$ the median is the largest value of the left part. For an even $t$ the two middle values are the largest of the left part and the smallest of the right part, so the median is their average. The function above already returns both numbers.

This is exactly the problem _Median of Two Sorted Lists_.

```python
def median_of_two(a, b):
    total = len(a) + len(b)
    left_max, right_min = cut_values(a, b, (total + 1) // 2)
    if total % 2 == 1:
        return float(left_max)
    return (left_max + right_min) / 2


assert median_of_two([1, 3], [2]) == 2.0
assert median_of_two([1, 2], [3, 4]) == 2.5
assert median_of_two([], [7]) == 7.0
assert median_of_two([0, 0], [0, 0]) == 0.0
```

```cpp
double median_of_two(const vector<int>& a, const vector<int>& b) {
    int total = (int)(a.size() + b.size());
    auto [left_max, right_min] = cut_values(a, b, (total + 1) / 2);
    if (total % 2 == 1) return left_max;
    return (left_max + right_min) / 2.0;
}
```

Time is $O(\log \min(n, m))$ and space $O(1)$ (apart from the copy in the C++ version above).

## 7.5 Check yourself

1. In the example, why is `i = 2` an invalid cut?
2. Why do we search on the shorter list?
3. Which two values are compared across the lists to test a cut?
4. For a total of 6 values, which two numbers are averaged for the median?

# Chapter 8. Searching grids

## 8.1 A grid as one long list

A **grid** (or matrix) is a table of rows and columns. Suppose each row is sorted, and each row starts with a value bigger than the last value of the row above, like

```
 1  3  5  7
10 11 16 20
23 30 34 60
```

Read the rows one after another and you get one long sorted list: `1 3 5 7 10 11 16 20 23 30 34 60`. We do not need to build that list. Position number `p` of the long list lives in row `p // cols` and column `p % cols` (integer division and remainder). So we can binary search on `p` from 0 to `rows * cols - 1` and translate each probe into a cell.

This is exactly the problem _Search a Sorted Matrix_.

```python
def search_flat(matrix, target):
    if not matrix or not matrix[0]:
        return False
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        value = matrix[mid // cols][mid % cols]
        if value == target:
            return True
        if value < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


grid = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
assert search_flat(grid, 16) is True
assert search_flat(grid, 4) is False
assert search_flat([], 1) is False
assert search_flat([[]], 1) is False
```

```cpp
bool search_flat(const vector<vector<int>>& matrix, int target) {
    if (matrix.empty() || matrix[0].empty()) return false;
    int rows = (int)matrix.size(), cols = (int)matrix[0].size();
    long long lo = 0, hi = (long long)rows * cols - 1;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        int value = matrix[mid / cols][mid % cols];
        if (value == target) return true;
        if (value < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return false;
}
```

Time is $O(\log(\text{rows} \cdot \text{cols}))$.

## 8.2 The staircase walk

Now a harder grid: every row is sorted and every column is sorted, but a row need not start after the previous row ends:

```
 1  4  7 11
 2  5  8 12
 3  6  9 16
10 13 14 17
```

The long-list trick no longer works. But the top-right corner is special: it is the largest value in its row and the smallest in its column. Compare it with the target. If the corner is bigger than the target, then everything _below_ it in its column is bigger still, so that whole column can go; we step left. If the corner is smaller than the target, then everything to its _left_ in its row is smaller still, so that whole row can go; we step down. At every step one row or one column is thrown away, so we need at most `rows + cols` steps. It looks like a walk down a staircase.

Let's search for 5. Start at the top-right, value 11, bigger than 5: go left to 7, bigger: go left to 4, smaller than 5: go down to 5. Found.

```python
def staircase_search(matrix, target):
    if not matrix or not matrix[0]:
        return False
    r, c = 0, len(matrix[0]) - 1
    while r < len(matrix) and c >= 0:
        value = matrix[r][c]
        if value == target:
            return True
        if value > target:
            c -= 1
        else:
            r += 1
    return False


g = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]]
assert staircase_search(g, 5) is True
assert staircase_search(g, 15) is False
assert staircase_search([[3]], 3) is True
```

```cpp
bool staircase_search(const vector<vector<int>>& matrix, int target) {
    if (matrix.empty() || matrix[0].empty()) return false;
    int r = 0, c = (int)matrix[0].size() - 1;
    while (r < (int)matrix.size() && c >= 0) {
        int value = matrix[r][c];
        if (value == target) return true;
        if (value > target) --c;
        else ++r;
    }
    return false;
}
```

Time is $O(\text{rows} + \text{cols})$ and space $O(1)$. For a square grid with $n$ rows, that is $O(n)$ instead of reading all $n^2$ cells.

## 8.3 Cutting a long thin grid

If the grid is very long and thin (say 3 rows and a million columns), $O(\text{rows} + \text{cols})$ is almost a million steps, yet a single sorted row of a million values would take only about 20. Can we get that benefit here too? Yes: use binary search _inside_ the grid.

Take the middle row of the current block and find, with a lower bound, the first column `lo` whose value is at least the target. If that cell equals the target we are done. Otherwise, think about what we learned. Every cell in this row to the left of `lo` is smaller than the target, and so is every cell above those (columns are sorted), so the whole top-left block is out. Every cell at `lo` or to the right in this row is bigger than the target, and so is every cell below those, so the whole bottom-right block is out. Only two smaller blocks remain: the top-right and the bottom-left. We search both in the same way. When the block is taller than it is wide, we cut along the middle column instead, so that we always cut the shorter side's line and the pieces get small quickly.

```python
def search_blocks(matrix, target):
    if not matrix or not matrix[0]:
        return False

    def first_ge_in_row(r, c0, c1):
        lo, hi = c0, c1 + 1
        while lo < hi:
            mid = (lo + hi) // 2
            if matrix[r][mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def first_ge_in_col(c, r0, r1):
        lo, hi = r0, r1 + 1
        while lo < hi:
            mid = (lo + hi) // 2
            if matrix[mid][c] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def search(r0, r1, c0, c1):
        if r0 > r1 or c0 > c1:
            return False
        if r1 - r0 <= c1 - c0:                      # cut the middle row
            r = (r0 + r1) // 2
            p = first_ge_in_row(r, c0, c1)
            if p <= c1 and matrix[r][p] == target:
                return True
            return search(r0, r - 1, p, c1) or search(r + 1, r1, c0, p - 1)
        c = (c0 + c1) // 2                          # cut the middle column
        p = first_ge_in_col(c, r0, r1)
        if p <= r1 and matrix[p][c] == target:
            return True
        return search(r0, p - 1, c + 1, c1) or search(p, r1, c0, c - 1)

    return search(0, len(matrix) - 1, 0, len(matrix[0]) - 1)


g = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]]
assert search_blocks(g, 9) is True
assert search_blocks(g, 15) is False
assert search_blocks([[1, 3, 5, 9, 12, 20]], 12) is True
assert search_blocks([[1], [4], [6], [8]], 5) is False
```

```cpp
bool search_blocks(const vector<vector<int>>& matrix, int target) {
    if (matrix.empty() || matrix[0].empty()) return false;

    auto first_ge_in_row = [&](int r, int c0, int c1) {
        int lo = c0, hi = c1 + 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (matrix[r][mid] < target) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    };
    auto first_ge_in_col = [&](int c, int r0, int r1) {
        int lo = r0, hi = r1 + 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (matrix[mid][c] < target) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    };

    function<bool(int, int, int, int)> search = [&](int r0, int r1, int c0, int c1) {
        if (r0 > r1 || c0 > c1) return false;
        if (r1 - r0 <= c1 - c0) {
            int r = (r0 + r1) / 2;
            int p = first_ge_in_row(r, c0, c1);
            if (p <= c1 && matrix[r][p] == target) return true;
            return search(r0, r - 1, p, c1) || search(r + 1, r1, c0, p - 1);
        }
        int c = (c0 + c1) / 2;
        int p = first_ge_in_col(c, r0, r1);
        if (p <= r1 && matrix[p][c] == target) return true;
        return search(r0, p - 1, c + 1, c1) || search(p, r1, c0, c - 1);
    };

    return search(0, (int)matrix.size() - 1, 0, (int)matrix[0].size() - 1);
}
```

For a matrix with $m$ lines on its shorter side and $n$ on the longer one, the work is $O(m \log(2n / m))$ reads. That equals the staircase for a square grid and shrinks to $O(\log n)$ for a single row. The recursion depth is $O(\log m)$.

This is exactly the problem _Search a Row- and Column-Sorted Matrix_.

## 8.4 The row with the most ones

Last, a grid of `0`s and `1`s where every row is sorted: zeros first, then ones. Which row has the most ones?

One way is a binary search in every row for the first `1`; the ones in that row number `cols - first`, giving $O(\text{rows} \cdot \log \text{cols})$. A smarter way keeps one pointer `col` shared between rows. It marks where the ones of the best row so far begin (`col = cols` means no ones yet). For the next row, we slide `col` left as long as the cell just before it is a `1`. If it moved at all, this row has strictly more ones than the best row so far, so it becomes the new best. Since `col` only ever moves left, the whole grid costs $O(\text{rows} + \text{cols})$. Ties keep the earlier row, because a tie does not move `col`.

For `[[0,1,1],[0,0,1],[1,1,1]]`: `col` starts at 3. Row 0 moves it to 1 (two ones), best row is 0. Row 1: the cell before column 1 is `0`, no move. Row 2: the cell before column 1 is `1`, and so is the next one, `col` becomes 0, best row is 2. If no cell is ever a one, the answer stays `-1`.

This is exactly the problem _Row With the Most Ones_.

```python
def row_with_most_ones(matrix):
    best = -1
    col = len(matrix[0]) if matrix else 0
    for r, row in enumerate(matrix):
        moved = False
        while col > 0 and row[col - 1] == 1:
            col -= 1
            moved = True
        if moved:
            best = r
    return best


assert row_with_most_ones([[0, 1, 1], [0, 0, 1], [1, 1, 1]]) == 2
assert row_with_most_ones([[0, 0], [0, 0]]) == -1
assert row_with_most_ones([[0, 1], [0, 1]]) == 0
assert row_with_most_ones([]) == -1
```

```cpp
int row_with_most_ones(const vector<vector<int>>& matrix) {
    int best = -1;
    int col = matrix.empty() ? 0 : (int)matrix[0].size();
    for (int r = 0; r < (int)matrix.size(); ++r) {
        bool moved = false;
        while (col > 0 && matrix[r][col - 1] == 1) {
            --col;
            moved = true;
        }
        if (moved) best = r;
    }
    return best;
}
```

## 8.5 Check yourself

1. Which row and column hold position 9 of the long list in a grid with 4 columns?
2. In the staircase walk, why can we throw away a whole column when the corner is larger than the target?
3. Which grid shape makes the block-cutting method much faster than the staircase?
4. Why does the shared `col` pointer never move to the right?
