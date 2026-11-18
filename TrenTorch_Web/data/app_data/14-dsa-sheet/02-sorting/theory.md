> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Sorting)

This page teaches sorting from the ground up: putting a list of numbers in order. We start with the three simple methods you could run by hand with a pack of cards (selection sort, bubble sort, insertion sort), then learn what makes a sort _stable_, and then move to the two big ideas that make sorting fast: **merge sort** (split in half, sort each half, merge) and **quicksort's partition** (split around a pivot value). Along the way we meet the clever uses of these ideas: counting how disordered a list is, sorting zeros, ones and twos in one pass, and finding the k-th largest value without sorting everything.

The page is a staircase. **Chapter 1 is deliberately gentle**: one simple method, one small list, traced by hand. Each chapter after it adds one idea, and the maths grows slowly. By the last chapters you will be able to solve the hardest sorting questions of this step. Every code example is shown in Python and in C++.

# Chapter 1. Sorting by hand: selection sort

## 1.1 What it means to sort

To **sort** a list means to rearrange its values so they go from smallest to largest. `[4, 1, 3]` becomes `[1, 3, 4]`. Python can do this for you with `sorted(...)`, and later chapters rely on that. But understanding _how_ sorting works teaches ideas that are used all over programming: the same tricks count disorder, split data around a value, and find the median.

We will build sorting methods the way you would sort a pack of cards in your hands. The first method is the easiest to explain.

## 1.2 Find the smallest, put it first

**Selection sort** works like this. Look at the whole list and find the smallest value. Swap it with the value in the first position. Now the first position is correct and never needs to change. Repeat on the rest of the list: find the smallest value there, swap it into the second position, and so on. Each repetition is called a **pass**.

Here is the list `[29, 10, 14, 37, 13]` pass by pass. The part before the bar is finished:

```
start        29 10 14 37 13
pass 1       10 | 29 14 37 13     smallest of all is 10, swapped into place 0
pass 2       10 13 | 14 37 29     smallest of the rest is 13, swapped into place 1
pass 3       10 13 14 | 37 29     smallest of the rest is 14, already in place 2
pass 4       10 13 14 29 | 37     smallest of the rest is 29, swapped into place 3
```

After four passes (one fewer than the number of values), the last value is automatically in the right place, because everything smaller has already been moved to the front.

## 1.3 Selection sort, pass by pass

Here is the method in code. The inner loop walks over the unsorted part to remember where the smallest value sits. We take the _leftmost_ smallest if there are ties (by checking with `<`, not `<=`). Then we swap it to the front. The optional `trace` list collects a copy of the list after every pass, so you can compare with the table above.

```python
def selection_sort(a, trace=None):
    for i in range(len(a) - 1):
        smallest = i
        for j in range(i + 1, len(a)):
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]
        if trace is not None:
            trace.append(a[:])


steps = []
data = [29, 10, 14, 37, 13]
selection_sort(data, steps)
assert data == [10, 13, 14, 29, 37]
assert steps == [[10, 29, 14, 37, 13], [10, 13, 14, 37, 29],
                 [10, 13, 14, 37, 29], [10, 13, 14, 29, 37]]
```

```cpp
void selection_sort(vector<int>& a, vector<vector<int>>* trace = nullptr) {
    int n = a.size();
    for (int i = 0; i + 1 < n; i++) {
        int smallest = i;
        for (int j = i + 1; j < n; j++) {
            if (a[j] < a[smallest]) smallest = j;
        }
        swap(a[i], a[smallest]);
        if (trace) trace->push_back(a);
    }
}
```

Look at pass 3 in the trace: the smallest value 14 was already in place, so swapping it with itself changed nothing, but the pass still happened and we still recorded a snapshot. This is exactly the problem _Selection Sort, Pass by Pass_: run the passes, and write down the list after each one. Remember two details: take the leftmost smallest value when there are ties, and always do the swap, even when it swaps a position with itself. A list with fewer than two values has no passes, so the trace is empty.

## 1.4 Cost of selection sort

The first pass looks at $n - 1$ values after position 0, the next at $n - 2$, and so on down to 1. That is the staircase sum

$$(n-1) + (n-2) + \dots + 1 = \frac{n(n-1)}{2},$$

so selection sort makes about $n^2/2$ comparisons, which we write $O(n^2)$. It does not matter whether the list was already sorted: it still does all the comparisons. It makes at most $n - 1$ swaps, which is a good feature when swapping is expensive. It uses no extra space beyond a few variables, so space is $O(1)$.

## 1.5 Check yourself

1. In selection sort, which part of the list is guaranteed correct after pass 2?
2. How many passes does selection sort make on a list of 7 values?
3. Why is it fine to skip a final pass on the last value?
4. About how many comparisons does selection sort make on 1000 values?

# Chapter 2. Bubble sort

## 2.1 Neighbours that swap

**Bubble sort** has a different feel. Walk along the list from left to right and look at each pair of neighbours. If the left one is bigger than the right one, swap them. One walk from start to end is a **pass**. Why "bubble"? Because during a pass the biggest value keeps getting swapped to the right until it reaches the end, like a bubble floating to the top.

Take `[5, 1, 4, 2, 8]`:

```
pass 1:  5 1 4 2 8  ->  1 5 4 2 8  ->  1 4 5 2 8  ->  1 4 2 5 8  ->  1 4 2 5 8
pass 2:  1 4 2 5 8  ->  1 4 2 5 8  ->  1 2 4 5 8  ->  1 2 4 5 8  ->  1 2 4 5 8
pass 3:  1 2 4 5 8  (no swaps at all)
```

After pass 1 the largest value, 8, is at the end (it was already there here, but 5 bubbled up next to it). After pass 2 the list is sorted, but we do not know that yet. We learn it in pass 3, when nothing swaps.

## 2.2 Stopping early

That last pass tells us something useful: if a whole pass makes **no swap**, every neighbouring pair is in order, so the whole list is in order, and we can stop. Remembering whether any swap happened gives bubble sort an early exit.

```python
def bubble_sort(a):
    passes = 0
    while True:
        passes += 1
        swapped = False
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:
            return passes


data = [5, 1, 4, 2, 8]
assert bubble_sort(data) == 3
assert data == [1, 2, 4, 5, 8]
assert bubble_sort([1, 2, 3]) == 1       # already sorted: one pass with no swap
```

```cpp
int bubble_sort(vector<int>& a) {
    int passes = 0;
    while (true) {
        passes++;
        bool swapped = false;
        for (int i = 0; i + 1 < (int)a.size(); i++) {
            if (a[i] > a[i + 1]) {
                swap(a[i], a[i + 1]);
                swapped = true;
            }
        }
        if (!swapped) return passes;
    }
}
```

The function returns the number of passes it used, counting the final check pass. In the worst case (a list in reverse order) it needs about $n$ passes of about $n$ comparisons each, so $O(n^2)$. In the best case (already sorted) it needs one pass, so $O(n)$.

## 2.3 How many passes?

Can we predict the number of passes without running the sort? Yes, and it is a nice piece of reasoning. Look at a single value that has some **bigger values somewhere to its left**. During a pass, the walk carries the biggest value seen so far to the right. When that carried value reaches our value, it is bigger, so it swaps past it, and our value moves **exactly one place to the left in that pass**. This happens in every pass as long as some bigger value is still on its left. (Values with nothing bigger on their left never move left.)

So a value needs as many passes as it has bigger values to its left. Count that number for every value; the largest count tells how many passes do swaps; then one more pass finds no swap and stops. The formula is

$$\text{passes} = 1 + \max_i \bigl(\text{number of values left of } i \text{ that are bigger than } a_i\bigr).$$

Test it on three lists:

```
5 1 4 2 8   -> 1 has one bigger value left of it (5); 4 has one (5); 2 has two (5, 4)   max 2  -> 3 passes
2 3 4 5 1   -> the 1 has four bigger values left of it                                   max 4  -> 5 passes
5 1 2 3 4   -> every value 1,2,3,4 has exactly one bigger value left of it (the 5)       max 1  -> 2 passes
```

The second list shows a bubble sort weakness: a small value near the end travels left only one step per pass, so it takes very many passes. A big value near the start, in contrast, hops all the way right in a single pass. This is exactly the problem _How Many Bubble Sort Passes?_: you can either simulate the loop, or use the counting shortcut above.

```python
def bubble_passes(a):
    worst = 0
    for i in range(len(a)):
        bigger_before = sum(1 for j in range(i) if a[j] > a[i])
        worst = max(worst, bigger_before)
    return 1 + worst


assert bubble_passes([5, 1, 4, 2, 8]) == 3
assert bubble_passes([2, 3, 4, 5, 1]) == 5
assert bubble_passes([5, 1, 2, 3, 4]) == 2
assert bubble_passes([]) == 1
```

```cpp
int bubble_passes(const vector<int>& a) {
    int worst = 0;
    for (int i = 0; i < (int)a.size(); i++) {
        int biggerBefore = 0;
        for (int j = 0; j < i; j++)
            if (a[j] > a[i]) biggerBefore++;
        worst = max(worst, biggerBefore);
    }
    return 1 + worst;
}
```

This counting version is itself $O(n^2)$, so it is not faster than simulating. It is useful for _understanding_: it tells you exactly which values make bubble sort slow. (With a smarter data structure the counts can be found faster, but that goes beyond this page.)

## 2.4 Check yourself

1. What does one pass of bubble sort do to the largest value?
2. Why can bubble sort stop after a pass with no swaps?
3. How many passes does bubble sort need on `[3, 2, 1]`, counting the final check pass?
4. Which kind of list is bad for bubble sort: a small value near the end, or a large value near the start?

# Chapter 3. Insertion sort

## 3.1 Sorting playing cards

When you pick up cards one by one and slide each into the right place in your hand, you are doing **insertion sort**. The left part of the list is your sorted hand. Take the next value (call it the **key**), compare it with the sorted values to its left from right to left, and **shift** each bigger value one place to the right. When you meet a value that is not bigger, drop the key into the gap.

Take `[5, 2, 4, 6, 1, 3]`. The part before the bar is the sorted hand:

```
5 | 2 4 6 1 3
2 5 | 4 6 1 3      key 2: shifts 5 right (1 shift)
2 4 5 | 6 1 3      key 4: shifts 5 right (1 shift)
2 4 5 6 | 1 3      key 6: nothing to shift (0 shifts)
1 2 4 5 6 | 3      key 1: shifts 6, 5, 4, 2 right (4 shifts)
1 2 3 4 5 6 |      key 3: shifts 6, 5, 4 right (3 shifts)
```

The total number of shifts is $1 + 1 + 0 + 4 + 3 = 9$.

```python
def insertion_sort(a):
    shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]       # shift one place right
            shifts += 1
            j -= 1
        a[j + 1] = key            # drop the key into the gap
    return shifts


data = [5, 2, 4, 6, 1, 3]
assert insertion_sort(data) == 9
assert data == [1, 2, 3, 4, 5, 6]
```

```cpp
long long insertion_sort(vector<int>& a) {
    long long shifts = 0;
    for (int i = 1; i < (int)a.size(); i++) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            shifts++;
            j--;
        }
        a[j + 1] = key;
    }
    return shifts;
}
```

Notice the test `a[j] > key`, strictly bigger. Equal values do **not** shift past each other, so equal values keep their original order. We will see why that matters in Chapter 4.

## 3.2 Counting the shifts

The function above returns the number of shifts as a by-product. This is exactly the problem _Insertion Sort Shifts_. A list that is already sorted has 0 shifts, and a list in reverse order has the most: key number $i$ shifts $i$ values, giving $1 + 2 + \dots + (n-1) = n(n-1)/2$ shifts. The next chapter explains where that count really comes from, and how to compute it much faster than simulating.

## 3.3 Fast on nearly sorted data

Insertion sort does very little when the list is close to sorted: each key only moves a short distance. If every value is at most `d` places away from its final position, the total work is about $O(nd)$. For small lists, or for lists that are almost in order, insertion sort is often the fastest simple method. The running time is $O(n^2)$ in the worst case and $O(n)$ in the best case, with $O(1)$ extra space. Many real-world sort routines switch to insertion sort for very short pieces for exactly this reason.

## 3.4 Check yourself

1. Which part of the list is always sorted during insertion sort?
2. How many shifts does insertion sort make on an already sorted list?
3. Why do we compare with `>` and not `>=` when shifting?
4. How many shifts for the reverse-sorted list `[4, 3, 2, 1]`?

# Chapter 4. Disorder and stability

## 4.1 Inversions: pairs that are the wrong way round

How far from sorted is a list? One neat measure is the number of **inversions**. An inversion is a pair of positions $i < j$ where $a_i > a_j$: a bigger value stands in front of a smaller one. A sorted list has 0 inversions. The reverse-sorted list of $n$ values has every pair inverted, which is $n(n-1)/2$.

For `[5, 2, 4, 6, 1, 3]` the inversions are: (5,2), (5,4), (5,1), (5,3), (2,1), (4,1), (4,3), (6,1), (6,3). That is 9, the same number we found as shifts in Chapter 3. That is no coincidence. Here is the simple (slow) way to count them:

```python
def inversions_slow(a):
    count = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] > a[j]:
                count += 1
    return count


assert inversions_slow([5, 2, 4, 6, 1, 3]) == 9
assert inversions_slow([1, 2, 3]) == 0
assert inversions_slow([3, 2, 1]) == 3
assert inversions_slow([2, 2]) == 0          # equal values are not inversions
```

```cpp
long long inversions_slow(const vector<int>& a) {
    long long count = 0;
    for (int i = 0; i < (int)a.size(); i++)
        for (int j = i + 1; j < (int)a.size(); j++)
            if (a[i] > a[j]) count++;
    return count;
}
```

## 4.2 Why shifts equal inversions

Swapping two **neighbouring** values that are out of order changes exactly one pair: that pair stops being an inversion. Every other pair keeps its relative order. So an adjacent swap removes exactly one inversion. Sorting means getting to 0 inversions, so any method that fixes things only by adjacent swaps needs at least as many swaps as there are inversions, and insertion sort and bubble sort use exactly that many (each shift is half of a swap and removes one inversion). Let's check:

```python
def shifts_of_insertion(a):
    a = a[:]
    shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            shifts += 1
            j -= 1
        a[j + 1] = key
    return shifts


for sample in ([5, 2, 4, 6, 1, 3], [3, 3, 1], [1, 2, 3, 4], [9, 7, 5, 3, 1], []):
    assert shifts_of_insertion(sample) == inversions_slow(sample)
```

```cpp
long long shifts_of_insertion(vector<int> a) {
    long long shifts = 0;
    for (int i = 1; i < (int)a.size(); i++) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            shifts++;
            j--;
        }
        a[j + 1] = key;
    }
    return shifts;
}
```

So the number of shifts in insertion sort is exactly the number of inversions. That also means we can answer "how many shifts?" without simulating, if we can count inversions faster. We will do that in Chapter 7.

## 4.3 Stability

Imagine sorting a list of records, say students with a score, by score only. Two students have the same score. After sorting, should the one who came first in the original list still come first? A sort that always keeps equal items in their original relative order is called **stable**. Stability matters when you sort twice: for example sort by name, then sort by score, and the stability of the second sort preserves the name order among equal scores.

Insertion sort is stable (we shift only strictly bigger values), and so is bubble sort (we swap only when strictly bigger). Selection sort is **not** stable, because a swap can throw a value far over equal ones. Here is a small demo with `(score, name)` pairs sorted by score only:

```python
def selection_sort_by_score(items):
    items = items[:]
    for i in range(len(items) - 1):
        smallest = i
        for j in range(i + 1, len(items)):
            if items[j][0] < items[smallest][0]:
                smallest = j
        items[i], items[smallest] = items[smallest], items[i]
    return items


def insertion_sort_by_score(items):
    items = items[:]
    for i in range(1, len(items)):
        key = items[i]
        j = i - 1
        while j >= 0 and items[j][0] > key[0]:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = key
    return items


people = [(4, "a"), (2, "b"), (4, "c"), (1, "d")]
assert selection_sort_by_score(people) == [(1, "d"), (2, "b"), (4, "c"), (4, "a")]   # a and c swapped
assert insertion_sort_by_score(people) == [(1, "d"), (2, "b"), (4, "a"), (4, "c")]   # a still before c
assert sorted(people, key=lambda p: p[0]) == [(1, "d"), (2, "b"), (4, "a"), (4, "c")]  # Python's sort is stable
```

```cpp
vector<pair<int, string>> insertion_sort_by_score(vector<pair<int, string>> items) {
    for (int i = 1; i < (int)items.size(); i++) {
        auto key = items[i];
        int j = i - 1;
        while (j >= 0 && items[j].first > key.first) {
            items[j + 1] = items[j];
            j--;
        }
        items[j + 1] = key;
    }
    return items;
}
// For a library sort that keeps equal items in order, use stable_sort(items.begin(), items.end(), cmp).
```

In the demo, selection sort moved `(4, "a")` to the far end when it swapped it with the 1, so it ended up after `(4, "c")`. The insertion version keeps `a` before `c`. Python's built-in `sorted` is stable; in C++, `sort` is not guaranteed to be stable but `stable_sort` is.

## 4.4 Check yourself

1. How many inversions does `[2, 1, 3, 1]` have?
2. Why does swapping two neighbouring out-of-order values remove exactly one inversion?
3. What does it mean for a sort to be stable?
4. Which of the three simple sorts in this page is not stable?

# Chapter 5. Merging two sorted lists

## 5.1 Two pointers, one result

Here is a tiny but powerful building block. If you have two lists that are **already sorted**, you can combine them into one sorted list in a single sweep. Put a finger at the front of each list. Compare the two fingers' values, copy the smaller into the result, and move that finger forward. When one list runs out, copy whatever remains of the other list; it is already sorted and bigger than everything copied so far, so no comparisons are needed.

```
a = 1 4 6 9        b = 2 3 7
compare 1 vs 2 -> take 1
compare 4 vs 2 -> take 2
compare 4 vs 3 -> take 3
compare 4 vs 7 -> take 4
compare 6 vs 7 -> take 6
compare 9 vs 7 -> take 7      b is empty now
copy the rest of a: 9
result: 1 2 3 4 6 7 9          (6 comparisons)
```

Each comparison places one value in the result, so merging lists of lengths $p$ and $q$ takes at most $p + q$ steps: $O(p + q)$ time.

## 5.2 Merging with a comparison count

Here is the code, which also counts the comparisons. If two values are equal, we take the one from `a` first. That keeps the merge stable: equal values stay in the order of their lists.

```python
def merge_sorted(a, b):
    result = []
    i = j = 0
    comparisons = 0
    while i < len(a) and j < len(b):
        comparisons += 1
        if b[j] < a[i]:
            result.append(b[j])
            j += 1
        else:
            result.append(a[i])
            i += 1
    result.extend(a[i:])            # one of these two is empty
    result.extend(b[j:])
    return result, comparisons


assert merge_sorted([1, 4, 6, 9], [2, 3, 7]) == ([1, 2, 3, 4, 6, 7, 9], 6)
assert merge_sorted([1, 2, 3], [7, 8]) == ([1, 2, 3, 7, 8], 3)
assert merge_sorted([], [5]) == ([5], 0)
```

```cpp
pair<vector<int>, int> merge_sorted(const vector<int>& a, const vector<int>& b) {
    vector<int> result;
    size_t i = 0, j = 0;
    int comparisons = 0;
    while (i < a.size() && j < b.size()) {
        comparisons++;
        if (b[j] < a[i]) result.push_back(b[j++]);
        else result.push_back(a[i++]);
    }
    while (i < a.size()) result.push_back(a[i++]);
    while (j < b.size()) result.push_back(b[j++]);
    return {result, comparisons};
}
```

The second assert shows the effect of an early finish: `[1, 2, 3]` and `[7, 8]` need only 3 comparisons, because once `a` runs out, the 7 and 8 are copied for free. This is exactly the problem _Merge Two Sorted Lists_: follow the two-pointer method, take from `a` when values are equal, and count only the comparisons made while both lists still have values.

## 5.3 Check yourself

1. Why is it correct to copy the rest of one list without comparing, once the other is empty?
2. How many comparisons does merging two lists of length 3 and 3 take in the best case?
3. In which list do we take from first when two values are equal, and why?
4. What is the time cost of merging lists of lengths $p$ and $q$?

# Chapter 6. Merge sort

## 6.1 Divide and conquer

The idea of **divide and conquer** is to split a big problem into smaller copies of itself, solve each, and combine. For sorting: cut the list into a left half and a right half, sort each half (by the same method, called **recursively**, meaning the function calls itself on a smaller piece), and **merge** the two sorted halves with Chapter 5's two-pointer method. A list of length 0 or 1 is already sorted, which stops the recursion.

```
[38 27 43 3 9 82 10]
   [38 27 43] [3 9 82 10]
   [38] [27 43]   [3 9] [82 10]
        [27] [43]  [3] [9] [82] [10]
 merge up:
   [27 43]            [3 9] [10 82]
   [27 38 43]         [3 9 10 82]
 [3 9 10 27 38 43 82]
```

## 6.2 Merge sort in code

```python
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if right[j] < left[i]:
            result.append(right[j])
            j += 1
        else:
            result.append(left[i])
            i += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(a):
    if len(a) <= 1:
        return a[:]
    mid = len(a) // 2
    return merge(merge_sort(a[:mid]), merge_sort(a[mid:]))


assert merge_sort([38, 27, 43, 3, 9, 82, 10]) == [3, 9, 10, 27, 38, 43, 82]
assert merge_sort([]) == []
assert merge_sort([2, 1]) == [1, 2]
```

```cpp
vector<int> merge(const vector<int>& left, const vector<int>& right) {
    vector<int> result;
    size_t i = 0, j = 0;
    while (i < left.size() && j < right.size()) {
        if (right[j] < left[i]) result.push_back(right[j++]);
        else result.push_back(left[i++]);
    }
    while (i < left.size()) result.push_back(left[i++]);
    while (j < right.size()) result.push_back(right[j++]);
    return result;
}

vector<int> merge_sort(const vector<int>& a) {
    if (a.size() <= 1) return a;
    size_t mid = a.size() / 2;
    vector<int> left(a.begin(), a.begin() + mid);
    vector<int> right(a.begin() + mid, a.end());
    return merge(merge_sort(left), merge_sort(right));
}
```

Because `merge` takes from the left list on ties, merge sort is **stable**.

## 6.3 Why it costs n log n

Count the work level by level. At the top, one merge handles all $n$ values. At the next level, two merges handle $n/2$ values each, so again $n$ in total. At the level after that, four merges of $n/4$, again $n$ in total. Every level does about $n$ work. How many levels are there? We halve the list until we reach pieces of size 1, which takes $\log_2 n$ halvings. So the total is

$$n \cdot \log_2 n \quad\Rightarrow\quad O(n \log n).$$

For $n = 1{,}000{,}000$ that is about 20 million steps, compared to about $10^{12}$ for the simple $O(n^2)$ sorts. Merge sort always costs $O(n \log n)$, whatever order the input is in. The price is extra memory: the merge builds new lists, so space is $O(n)$.

## 6.4 Check yourself

1. What two things does merge sort do after splitting a list in half?
2. Why does the recursion stop at lists of length 0 or 1?
3. How many levels of halving does a list of 16 values have?
4. What do we pay (compared with selection sort) to get $O(n \log n)$ time?

# Chapter 7. Counting inversions with merge sort

## 7.1 Counting while merging

In Chapter 4 we counted inversions by checking every pair, in $O(n^2)$. Merge sort gives a much faster method. Split the list into a left half and a right half. Every inversion falls into exactly one of three kinds: both values in the left half, both in the right half, or one in each (a "crossing" inversion, with the bigger value on the left). We count the first two kinds by recursion. The crossing kind is where the trick happens.

Suppose both halves are already sorted. For a value `y` in the right half, the number of crossing inversions it takes part in is the number of left values bigger than `y`. Since the left half is sorted, those are all the left values from some position to the end. We can count them with the same two-pointer sweep as a merge: whenever we take `y` from the right half, all the left values **still waiting** are bigger than `y` (they have not been taken because they are not smaller), so we add "how many left values remain".

```python
def count_cross(left, right):
    # left and right are both sorted; count pairs (x in left, y in right) with x > y
    count = 0
    i = 0
    for y in right:
        while i < len(left) and left[i] <= y:
            i += 1                       # these left values are not bigger than y
        count += len(left) - i           # the rest of left is bigger than y
    return count


assert count_cross([2, 5, 7], [1, 6]) == 4      # (2,1) (5,1) (7,1) (7,6)
assert count_cross([1, 2], [3, 4]) == 0
assert count_cross([3, 3], [3]) == 0            # equal values are not inversions
```

```cpp
long long count_cross(const vector<int>& left, const vector<int>& right) {
    long long count = 0;
    size_t i = 0;
    for (int y : right) {
        while (i < left.size() && left[i] <= y) i++;
        count += (long long)(left.size() - i);
    }
    return count;
}
```

For `left = [2, 5, 7]` and `right = [1, 6]`: for y = 1, no left value is at most 1, so all 3 left values are bigger (+3). For y = 6, the pointer moves past 2 and 5, leaving only 7 bigger (+1). Total 4. ✓

Now we combine counting and sorting in one recursion. After counting the crossing inversions, we merge the halves so the caller gets a sorted list back, which it needs for its own crossing count.

```python
def sort_and_count(a):
    # returns (sorted copy of a, number of inversions in a)
    if len(a) <= 1:
        return a[:], 0
    mid = len(a) // 2
    left, inv_left = sort_and_count(a[:mid])
    right, inv_right = sort_and_count(a[mid:])
    crossing = count_cross(left, right)
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if right[j] < left[i]:
            merged.append(right[j])
            j += 1
        else:
            merged.append(left[i])
            i += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inv_left + inv_right + crossing


assert sort_and_count([5, 2, 4, 6, 1, 3]) == ([1, 2, 3, 4, 5, 6], 9)
assert sort_and_count([3, 2, 1]) == ([1, 2, 3], 3)
assert sort_and_count([]) == ([], 0)
assert sort_and_count([2, 2, 2])[1] == 0
```

```cpp
pair<vector<int>, long long> sort_and_count(const vector<int>& a) {
    if (a.size() <= 1) return {a, 0};
    size_t mid = a.size() / 2;
    auto [left, invLeft] = sort_and_count(vector<int>(a.begin(), a.begin() + mid));
    auto [right, invRight] = sort_and_count(vector<int>(a.begin() + mid, a.end()));
    long long crossing = count_cross(left, right);
    vector<int> merged;
    size_t i = 0, j = 0;
    while (i < left.size() && j < right.size()) {
        if (right[j] < left[i]) merged.push_back(right[j++]);
        else merged.push_back(left[i++]);
    }
    while (i < left.size()) merged.push_back(left[i++]);
    while (j < right.size()) merged.push_back(right[j++]);
    return {merged, invLeft + invRight + crossing};
}
```

Each level of the recursion does $O(n)$ extra work for the crossing counts, exactly as for the merges, so the total is $O(n \log n)$ time and $O(n)$ space. For a million values that means roughly 20 million steps instead of 500 billion. In C++, the answer can be as large as $n(n-1)/2$, so use `long long`. This is exactly the problem _Count Inversions_.

## 7.2 One more use of the same idea

Because shifts in insertion sort equal inversions (Chapter 4), this also gives the answer to "how many shifts?" for huge lists in $O(n \log n)$, without ever running the quadratic simulation. The pattern, "count pairs with a property between two sorted halves during a merge", is a standard tool and reappears in many problems about pairs of positions.

## 7.3 Check yourself

1. How many inversions does `[3, 1, 2]` have?
2. What are the three kinds of inversions when we split a list in two halves?
3. When we take `y` from the right half, how do we know how many left values are bigger?
4. Why do we need the halves to be sorted before counting crossings?

# Chapter 8. Partitioning and quicksort

## 8.1 Splitting around a pivot

Merge sort does its hard work at the _end_ (the merge). Quicksort does its hard work at the _start_. Pick one value, the **pivot**. **Partition** the list so that everything smaller or equal comes before the pivot and everything bigger comes after it. After that, the pivot is already in its final sorted position, and we sort the left part and the right part separately.

There are several ways to partition. The one we use is **Lomuto's scheme**, with the last value as the pivot. Keep a boundary `i` that marks the end of the "small" zone. Walk `j` over the list. Whenever `a[j] <= pivot`, grow the small zone by one and swap `a[j]` into it. At the end, swap the pivot into the slot just after the small zone.

```python
def lomuto(a, lo, hi):
    # partitions a[lo..hi] in place around a[hi]; returns the pivot's final index
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


data = [7, 2, 9, 4, 3, 5]
p = lomuto(data, 0, len(data) - 1)
assert (data, p) == ([2, 4, 3, 5, 9, 7], 3)
```

```cpp
int lomuto(vector<int>& a, int lo, int hi) {
    int pivot = a[hi];
    int i = lo - 1;
    for (int j = lo; j < hi; j++) {
        if (a[j] <= pivot) {
            i++;
            swap(a[i], a[j]);
        }
    }
    swap(a[i + 1], a[hi]);
    return i + 1;
}
```

## 8.2 Partition, step by step

Take `[7, 2, 9, 4, 3, 5]`, with pivot 5 (the last value). Start with `i = -1`.

```
j=0: 7 > 5          skip.                                  [7 2 9 4 3 5]   i=-1
j=1: 2 <= 5         i=0, swap a[0] and a[1].               [2 7 9 4 3 5]   i=0
j=2: 9 > 5          skip.                                  [2 7 9 4 3 5]   i=0
j=3: 4 <= 5         i=1, swap a[1] and a[3].               [2 4 9 7 3 5]   i=1
j=4: 3 <= 5         i=2, swap a[2] and a[4].               [2 4 3 7 9 5]   i=2
end: swap a[i+1]=a[3] with the pivot a[5].                 [2 4 3 5 9 7]   pivot at index 3
```

The result: everything left of index 3 is at most 5, everything right of it is bigger than 5. The order inside each side is not sorted, and it depends on the exact swaps, which is why a problem about partitioning has exactly one correct answer: you must follow the scheme step by step. This is exactly the problem _Partition Around the Last Value_: run Lomuto's loop exactly as shown, on a copy of the input, and return the list together with the pivot's final index.

Why does it work? At every moment the list has three zones: positions up to `i` hold values `<= pivot`; positions from `i+1` to `j-1` hold values `> pivot`; positions from `j` on are not looked at yet. When `a[j]` is small, swapping it with `a[i+1]` (the first "big" value) moves one small value into the small zone and one big value to the end of the big zone. When it is big, `j` moving forward just extends the big zone.

## 8.3 Quicksort

Now the full algorithm: partition, then do the same on the two sides.

```python
def quicksort(a, lo=0, hi=None):
    if hi is None:
        hi = len(a) - 1
    if lo >= hi:
        return
    p = lomuto(a, lo, hi)
    quicksort(a, lo, p - 1)
    quicksort(a, p + 1, hi)


data = [7, 2, 9, 4, 3, 5, 1]
quicksort(data)
assert data == [1, 2, 3, 4, 5, 7, 9]
empty = []
quicksort(empty)
assert empty == []
```

```cpp
void quicksort(vector<int>& a, int lo, int hi) {
    if (lo >= hi) return;
    int p = lomuto(a, lo, hi);
    quicksort(a, lo, p - 1);
    quicksort(a, p + 1, hi);
}
// call as: quicksort(a, 0, (int)a.size() - 1);
```

It works in place, so it needs no big extra arrays (only the recursion stack). When the pivot lands near the middle, the two sides are about half the size, and the cost is the same as merge sort: $O(n \log n)$.

## 8.4 When quicksort is slow

Suppose the list is already sorted and we always pick the last value as the pivot. The pivot is the largest value, so the partition puts everything on one side: pieces of size $n-1$, then $n-2$, and so on. That is the staircase again, and the cost is $O(n^2)$. The fix is to pick the pivot **at random**: swap a random position into the last place before partitioning. A random pivot is rarely very bad, so the expected cost is $O(n \log n)$ for every input, although the worst case is still $O(n^2)$. Quicksort is also not stable.

## 8.5 Check yourself

1. After a partition, where is the pivot, and what is true about the two sides?
2. In Lomuto's scheme, what does the variable `i` mark?
3. Why is quicksort slow on a sorted list when the last value is always the pivot?
4. How does choosing a random pivot help?

# Chapter 9. Three-way partitioning: sorting zeros, ones and twos

## 9.1 Three colours, one pass

What if the list contains only three kinds of values, say `0`, `1` and `2` (three paint colours)? We can sort it in **one pass**, without a general sort. This is the same partitioning idea, but with three zones instead of two: everything smaller than the pivot, everything equal to it, and everything bigger. Using the pivot `1` splits zeros, ones and twos exactly.

We keep three markers, `low`, `mid` and `high`, and this promise at all times:

```
a[0 .. low-1]      are all smaller than the pivot          (sorted zone: zeros)
a[low .. mid-1]    are all equal to the pivot              (middle zone: ones)
a[mid .. high]     not looked at yet
a[high+1 .. end]   are all bigger than the pivot           (end zone: twos)
```

Look at `a[mid]`, the next unexamined value. If it is smaller than the pivot, swap it into the first zone, with the value at `low` (which is a "one", or `mid` itself), and move both `low` and `mid` forward. If it equals the pivot, it is already in the right zone: move `mid` forward. If it is bigger, swap it to the end, with `a[high]`, and move `high` back. Note that we do **not** move `mid` in that last case, because the value swapped in from the end has not been looked at yet. The loop stops when `mid` passes `high`.

This idea is often called the **Dutch national flag** algorithm, after the three-coloured flag.

## 9.2 The one-pass code

```python
def three_way_partition(a, pivot):
    low, mid, high = 0, 0, len(a) - 1
    while mid <= high:
        if a[mid] < pivot:
            a[low], a[mid] = a[mid], a[low]
            low += 1
            mid += 1
        elif a[mid] == pivot:
            mid += 1
        else:
            a[mid], a[high] = a[high], a[mid]
            high -= 1
    return low, mid          # a[:low] < pivot, a[low:mid] == pivot, a[mid:] > pivot


data = [2, 0, 2, 1, 0, 1]
bounds = three_way_partition(data, 1)
assert data == [0, 0, 1, 1, 2, 2]
assert bounds == (2, 4)

other = [9, 1, 5, 5, 7, 2, 5]
assert three_way_partition(other, 5) == (2, 5)
assert sorted(other[:2]) == [1, 2] and other[2:5] == [5, 5, 5] and sorted(other[5:]) == [7, 9]
```

```cpp
pair<int, int> three_way_partition(vector<int>& a, int pivot) {
    int low = 0, mid = 0, high = (int)a.size() - 1;
    while (mid <= high) {
        if (a[mid] < pivot) {
            swap(a[low], a[mid]);
            low++;
            mid++;
        } else if (a[mid] == pivot) {
            mid++;
        } else {
            swap(a[mid], a[high]);
            high--;
        }
    }
    return {low, mid};
}
```

Trace for `[2, 0, 2, 1, 0, 1]` with pivot 1, writing the list and `(low, mid, high)` after each step:

```
start                          2 0 2 1 0 1   (0,0,5)
a[0]=2 is bigger: swap with a[5]   1 0 2 1 0 2   (0,0,4)
a[0]=1 equals pivot: mid moves     1 0 2 1 0 2   (0,1,4)
a[1]=0 is smaller: swap with a[0]  0 1 2 1 0 2   (1,2,4)
a[2]=2 is bigger: swap with a[4]   0 1 0 1 2 2   (1,2,3)
a[2]=0 is smaller: swap with a[1]  0 0 1 1 2 2   (2,3,3)
a[3]=1 equals pivot: mid moves     0 0 1 1 2 2   (2,4,3)   mid > high, stop
```

Each step moves `mid` forward or `high` backward, so the loop ends after at most $n$ steps: $O(n)$ time, one pass, and $O(1)$ extra space. This is exactly the problem _Sort Zeros, Ones and Twos_: call it with pivot `1`. An alternative that also works is to count how many zeros, ones and twos there are and then write them out, which takes two passes.

## 9.3 Why three zones help quicksort

Three-way partitioning is not only for three colours. Used with any pivot value, it puts every copy of the pivot in the middle zone in one go. If a list has many repeated values, quicksort with a plain two-zone partition can slow down badly, while the three-way version removes all equal values from further work at once. We will use exactly this "smaller, equal, bigger" split in the next chapter to find the k-th largest value without sorting.

## 9.4 Check yourself

1. In the three-way partition, why do we not move `mid` after swapping with `high`?
2. What are the three zones, and what is true about each?
3. How many passes over the list does the one-pass method need?
4. After the loop ends, what do the returned `low` and `mid` tell you?

# Chapter 10. Quickselect: finding one value without sorting

## 10.1 Finding one value

Sometimes you need only _one_ value of the sorted order, such as the median or the k-th largest. Sorting everything costs $O(n \log n)$, but you only want one answer. **Quickselect** reuses the partition idea and throws away the half that cannot contain the answer.

Say we want the **k-th smallest** value, with `k = 1` the smallest. Pick a pivot and split the values into three groups: those smaller than the pivot, those equal to it, and those bigger. Let `s` be the size of the smaller group and `e` the size of the equal group.

- If $k \le s$, the answer is inside the smaller group: continue with that group only.
- If $k \le s + e$, the answer is the pivot itself.
- Otherwise the answer is in the bigger group, and since we have discarded $s + e$ smaller values, we now want the $(k - s - e)$-th smallest of the bigger group.

## 10.2 Quickselect in code

```python
import random


def kth_smallest(nums, k):
    pool = list(nums)
    while True:
        pivot = random.choice(pool)
        smaller = [x for x in pool if x < pivot]
        equal_count = sum(1 for x in pool if x == pivot)
        if k <= len(smaller):
            pool = smaller
        elif k <= len(smaller) + equal_count:
            return pivot
        else:
            bigger = [x for x in pool if x > pivot]
            k -= len(smaller) + equal_count
            pool = bigger


assert kth_smallest([3, 2, 1, 5, 6, 4], 1) == 1
assert kth_smallest([3, 2, 1, 5, 6, 4], 6) == 6
assert kth_smallest([5, 5, 3], 2) == 5
assert kth_smallest([7], 1) == 7
```

```cpp
int kth_smallest(const vector<int>& nums, int k) {
    static mt19937 rng(12345);
    vector<int> pool = nums;
    while (true) {
        int pivot = pool[rng() % pool.size()];
        vector<int> smaller, bigger;
        int equalCount = 0;
        for (int x : pool) {
            if (x < pivot) smaller.push_back(x);
            else if (x == pivot) equalCount++;
            else bigger.push_back(x);
        }
        if (k <= (int)smaller.size()) {
            pool = smaller;
        } else if (k <= (int)smaller.size() + equalCount) {
            return pivot;
        } else {
            k -= (int)smaller.size() + equalCount;
            pool = bigger;
        }
    }
}
```

Trace for `[3, 2, 1, 5, 6, 4]` and `k = 5`: suppose the pivot is 4. Smaller: `[3, 2, 1]` (size 3), equal: one 4. Since $5 > 3 + 1$, the answer is in the bigger group `[5, 6]`, and we now want the $5 - 4 = 1$st smallest of it: that is 5. Indeed in sorted order `1 2 3 4 5 6`, the 5th is 5. ✓

Equal values are handled because they all end up in the equal group, so the answer is correct even when the same number appears several times: in `[5, 5, 3]` the 2nd smallest is 5.

## 10.3 K-th largest and the cost

The **k-th largest** is a mirror image: the largest is the 1st largest, and in a list of `n` values the k-th largest is the $(n - k + 1)$-th smallest. For `[3, 2, 1, 5, 6, 4]`, the 2nd largest is the $6 - 2 + 1 = 5$th smallest, which is 5.

```python
def kth_largest(nums, k):
    return kth_smallest(nums, len(nums) - k + 1)


assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
assert kth_largest([5, 5, 3], 2) == 5
assert kth_largest([5, 5, 3], 3) == 3
assert kth_largest([9], 1) == 9
```

```cpp
int kth_largest(const vector<int>& nums, int k) {
    return kth_smallest(nums, (int)nums.size() - k + 1);
}
```

This is exactly the problem _Kth Largest Value_. How fast is it? With a random pivot, the pool shrinks by a constant fraction on average at each round. The work is about $n + \frac{n}{2} + \frac{n}{4} + \dots \approx 2n$, so the **expected** time is $O(n)$, faster than sorting. In the worst case (very unlucky pivots) it is $O(n^2)$, but a random pivot makes that extremely unlikely. This version builds new lists, so it uses $O(n)$ extra space; an in-place version using Lomuto or three-way partitioning is possible too.

Three other ways to get the answer, for comparison: sort and index, which is $O(n \log n)$ and the easiest; keep a heap of the `k` largest seen so far, which is $O(n \log k)$ and good when `k` is small or when the values arrive one by one; and, if you need guaranteed linear time, a more elaborate method called median of medians. For interviews, quickselect with a random pivot, or the heap, are the two answers to know.

## 10.4 Check yourself

1. How is the k-th largest value related to the k-th smallest in a list of `n` values?
2. In quickselect, what do we do when `k` falls inside the "equal to pivot" group?
3. Why is the expected time $O(n)$ and not $O(n \log n)$?
4. Why is a random pivot better than always taking the first value?
