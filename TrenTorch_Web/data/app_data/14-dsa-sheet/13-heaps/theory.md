> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Heaps)

This page teaches heaps, also called priority queues. A heap is a small, clever container that always hands you the smallest item (or the largest) very quickly, no matter how many items it holds or how often you add new ones. That one ability solves a surprising number of interview problems: keeping the top few items, merging many sorted lists, finding a running median, and planning meetings or fuel stops.

The page is a staircase. **Chapter 1 is gentle**: what a heap does and how to use it from Python and C++, with no theory at all. Chapter 2 opens the box and shows how a heap works inside. Then each chapter adds one new pattern: top-k, greedy "smallest first", merging sorted lists, two heaps for the median, scheduling, and finally lazy deletion. By the end you will be able to solve every problem in this step. Every code example is shown in Python and in C++.

# Chapter 1. What a heap is

## 1.1 Always give me the smallest

Imagine a hospital waiting room. Patients keep arriving, and the nurse always calls the most urgent one next, not the one who arrived first. A **priority queue** is exactly this: a container where you can add an item at any time, and ask for the item with the best priority (here, the smallest number). The most common way to build a priority queue is a **heap**.

Why not just keep a sorted list? Finding the smallest is easy (it is the first item), but inserting a new item into a sorted list means shifting many items, which takes $O(n)$ time. Re-sorting after every insert is even worse, about $O(n \log n)$. A heap does both jobs, adding an item and removing the smallest, in only $O(\log n)$ time. For a million items, $\log_2 n$ is about 20, so each operation takes about 20 small steps instead of a million.

A heap does _not_ keep everything sorted. It only promises one thing: the smallest item is always easy to reach. That weaker promise is why it is so fast.

## 1.2 Using a heap in Python and C++

Python has a ready-made heap in the `heapq` module. It works on a plain list. `heappush(heap, x)` adds `x`, `heappop(heap)` removes and returns the smallest item, and `heap[0]` is the smallest item (look but do not remove). `heapify(list)` turns an existing list into a heap in $O(n)$ time.

C++ calls it `priority_queue`. Be careful: by default it gives you the **largest** item first. To get the smallest first, we write `priority_queue<int, vector<int>, greater<int>>`. Here `push` adds, `top` looks at the best item, and `pop` removes it.

As a first example, we can sort a list by putting everything in a heap and taking items out one by one. The items come out smallest first, so the output is sorted.

```python
import heapq


def sort_with_heap(nums):
    heap = list(nums)
    heapq.heapify(heap)
    out = []
    while heap:
        out.append(heapq.heappop(heap))
    return out


assert sort_with_heap([5, 2, 9, 1, 5]) == [1, 2, 5, 5, 9]
assert sort_with_heap([]) == []
```

```cpp
vector<int> sort_with_heap(const vector<int>& nums) {
    priority_queue<int, vector<int>, greater<int>> pq(nums.begin(), nums.end());
    vector<int> out;
    while (!pq.empty()) {
        out.push_back(pq.top());
        pq.pop();
    }
    return out;
}
```

This is called heap sort in spirit and takes $O(n \log n)$ time: $n$ removals, each costing $O(\log n)$. The extra space is $O(n)$ here because we copied the list.

Heaps also work with pairs. Python compares tuples position by position, and C++ compares `pair`s the same way. So `(3, "x")` is "smaller" than `(5, "a")`, and when the first numbers tie, the second decides. This is how we store "priority plus extra information" in one heap item.

## 1.3 Largest first

Often we want the **largest** item instead. In C++ that is the default `priority_queue<int>`. Python's `heapq` only has a min-heap, so we use a simple trick: store the **negative** of every number. The smallest negative number is the largest original number, so popping the smallest gives us the largest. We just remember to flip the sign when we take a value out.

```python
import heapq


def two_largest(nums):
    heap = [-x for x in nums]
    heapq.heapify(heap)
    first = -heapq.heappop(heap)
    second = -heapq.heappop(heap)
    return first, second


assert two_largest([3, 9, 4, 7]) == (9, 7)
assert two_largest([5, 5]) == (5, 5)
```

```cpp
pair<int, int> two_largest(const vector<int>& nums) {
    priority_queue<int> pq(nums.begin(), nums.end());
    int first = pq.top();
    pq.pop();
    int second = pq.top();
    pq.pop();
    return {first, second};
}
```

Time is $O(n + \log n)$ for building and two removals, which is $O(n)$. Space is $O(n)$.

## 1.4 Smash the heaviest stones

Many problems have the same shape: "repeatedly take the biggest thing, do something with it, and put a result back." Let's practise with an easy cousin: we have some numbers, and for a given number of rounds we take the largest one and replace it with half of itself (rounded down). Finally we return the sum.

For `[10, 4, 7]` and 2 rounds: the largest is 10, it becomes 5, giving `[5, 4, 7]`. Next the largest is 7, it becomes 3, giving `[5, 4, 3]`. The sum is 12.

```python
import heapq


def sum_after_halving(nums, rounds):
    heap = [-x for x in nums]
    heapq.heapify(heap)
    for _ in range(rounds):
        biggest = -heapq.heappop(heap)
        heapq.heappush(heap, -(biggest // 2))
    return -sum(heap)


assert sum_after_halving([10, 4, 7], 2) == 12
assert sum_after_halving([8], 3) == 1
```

```cpp
int sum_after_halving(const vector<int>& nums, int rounds) {
    priority_queue<int> pq(nums.begin(), nums.end());
    for (int r = 0; r < rounds; ++r) {
        int biggest = pq.top();
        pq.pop();
        pq.push(biggest / 2);
    }
    int total = 0;
    while (!pq.empty()) {
        total += pq.top();
        pq.pop();
    }
    return total;
}
```

Each round costs $O(\log n)$, so $r$ rounds cost $O(r \log n)$. Sorting the list again after every round would cost $O(r\, n \log n)$.

This is exactly the problem _Last Stone Weight_. Instead of halving, you take the two heaviest stones, and if they differ you push their difference back. The loop shape is the same: pop the biggest, pop the next biggest, push the leftover. The sheet's starter code re-sorts after every smash; a heap removes that waste.

## 1.5 Check yourself

1. What two operations does a priority queue support, and how long does each take with a heap?
2. Why does a plain `priority_queue<int>` in C++ return the largest item, and how do you get the smallest?
3. How do we use Python's `heapq` as a max-heap?
4. After `heapify` on `[4, 1, 3]`, what is `heap[0]`?

# Chapter 2. How a heap works inside

You can solve many problems without this chapter, but knowing how a heap works makes everything later feel natural, and interviewers like to ask it.

## 2.1 A tree stored in a list

A heap is a **binary tree** (each node has at most two children) drawn level by level, but we store it in an ordinary list with no pointers. The item at index `i` has its children at indices `2i + 1` and `2i + 2`, and its parent at index $\lfloor (i-1)/2 \rfloor$. The tree is always filled from left to right, so there are no gaps.

```
index:   0   1   2   3   4   5
value:   1   3   2   7   4   9

              1            (index 0)
            /   \
           3     2         (indices 1, 2)
          / \   /
         7   4 9           (indices 3, 4, 5)
```

The one rule, called the **heap property** (for a min-heap), is: every node is less than or equal to its children. That is all. It means the smallest item is always at the top (index 0). Notice that siblings, like 3 and 2, are in no particular order, and 3's child 7 is bigger than 2. That is fine.

## 2.2 Adding an item: sift up

To add a new item, we put it at the end of the list (the next free spot in the tree). That might break the rule if the new item is smaller than its parent. So we **sift up**: while the item is smaller than its parent, swap them. Each swap moves it one level higher, and the tree has only about $\log_2 n$ levels, so this takes $O(\log n)$ time.

Let's add 5, 3, 8, 1 one after another. After 5: `[5]`. After 3: it goes at the end, is smaller than its parent 5, so they swap: `[3, 5]`. After 8: `[3, 5, 8]`, no swap needed. After 1: it goes to index 3, parent is index 1 (value 5), swap, then parent is index 0 (value 3), swap again: `[1, 3, 8, 5]`.

```python
def sift_up(a, i):
    while i > 0:
        parent = (i - 1) // 2
        if a[parent] <= a[i]:
            break
        a[parent], a[i] = a[i], a[parent]
        i = parent


def heap_push(a, x):
    a.append(x)
    sift_up(a, len(a) - 1)


h = []
for v in [5, 3, 8, 1]:
    heap_push(h, v)
assert h == [1, 3, 8, 5]
```

```cpp
void sift_up(vector<int>& a, int i) {
    while (i > 0) {
        int parent = (i - 1) / 2;
        if (a[parent] <= a[i]) break;
        swap(a[parent], a[i]);
        i = parent;
    }
}

void heap_push(vector<int>& a, int x) {
    a.push_back(x);
    sift_up(a, (int)a.size() - 1);
}
```

## 2.3 Removing the smallest: sift down

The smallest item is at index 0. We cannot just delete it, as that would leave a hole. Instead we take the **last** item in the list, move it to the top, and shrink the list by one. Now the top is probably too big, so we **sift down**: compare it with its two children, and if either is smaller, swap it with the _smaller_ child. Repeat until it is no larger than both children. Choosing the smaller child matters: it is the only choice that keeps the rule true for the other child.

From `[1, 3, 8, 5]`: remove 1, move the last item 5 to the top, giving `[5, 3, 8]`. Its children are 3 and 8; 3 is smaller and less than 5, so swap: `[3, 5, 8]`. Done.

```python
def sift_down(a, i, n):
    while True:
        left = 2 * i + 1
        right = left + 1
        smallest = i
        if left < n and a[left] < a[smallest]:
            smallest = left
        if right < n and a[right] < a[smallest]:
            smallest = right
        if smallest == i:
            break
        a[i], a[smallest] = a[smallest], a[i]
        i = smallest


def heap_pop(a):
    top = a[0]
    last = a.pop()
    if a:
        a[0] = last
        sift_down(a, 0, len(a))
    return top


h = [1, 3, 8, 5]
assert heap_pop(h) == 1
assert h == [3, 5, 8]
assert heap_pop(h) == 3
assert h == [5, 8]
```

```cpp
void sift_down(vector<int>& a, int i, int n) {
    while (true) {
        int left = 2 * i + 1;
        int right = left + 1;
        int smallest = i;
        if (left < n && a[left] < a[smallest]) smallest = left;
        if (right < n && a[right] < a[smallest]) smallest = right;
        if (smallest == i) break;
        swap(a[i], a[smallest]);
        i = smallest;
    }
}

int heap_pop(vector<int>& a) {
    int top = a[0];
    int last = a.back();
    a.pop_back();
    if (!a.empty()) {
        a[0] = last;
        sift_down(a, 0, (int)a.size());
    }
    return top;
}
```

## 2.4 Why it is fast

A tree where every level is full has about $\log_2 n$ levels: one node at the top, two on the next level, four on the next, and so on, doubling each time. Both sifts move along one path from a leaf to the root (or back), so each costs at most the height of the tree:

$$O(\log n)$$

Reading the smallest, `heap[0]`, costs $O(1)$. Space is $O(n)$, just the list itself. This is why a heap beats a sorted list for "add and remove smallest" workloads.

## 2.5 Building a heap quickly

If you already have $n$ items, pushing them one by one costs $O(n \log n)$. There is a faster way, called **heapify**. Start from the last node that has any child, which is at index $n/2 - 1$, and walk backwards to index 0, calling sift down on each node. Leaves are already valid little heaps, so we skip them. When we reach a node, both its subtrees are already heaps, so one sift down repairs it.

Why is it only $O(n)$? A node at height $h$ above the bottom moves at most $h$ steps, and there are at most $n / 2^{h+1}$ such nodes. So the total work is

$$\sum_{h=0}^{\log n} \frac{n}{2^{h+1}} \cdot h = O(n)$$

because the sum of $h / 2^{h}$ stays below a constant (it is 2). Most nodes are near the bottom and barely move.

```python
def build_heap(a):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n)


nums = [9, 4, 7, 1, 6, 2]
build_heap(nums)
assert nums == [1, 4, 2, 9, 6, 7]
```

```cpp
void build_heap(vector<int>& a) {
    int n = (int)a.size();
    for (int i = n / 2 - 1; i >= 0; --i) sift_down(a, i, n);
}
```

Python's `heapq.heapify` and C++'s `priority_queue` constructor from a range both do exactly this, so passing a whole list at once is faster than pushing items one at a time.

## 2.6 Check yourself

1. Where are the children and the parent of index 4 stored?
2. After pushing 6, 2, 9, 1 into an empty min-heap, what does the list look like?
3. In sift down, why do we swap with the smaller child and not the larger one?
4. Why is building a heap from $n$ items $O(n)$ and not $O(n \log n)$?

# Chapter 3. Keeping the top k

## 3.1 A small heap as a bouncer

A very common question is: "from a huge stream of numbers, keep only the $k$ largest." Sorting everything works but is wasteful. Instead, keep a **min-heap of size at most $k$**. The smallest of the current top $k$ sits at the top of the heap. When a new number arrives, push it in. If the heap now has more than $k$ items, pop the smallest. The heap acts like a bouncer: it only lets the $k$ best items stay in the club, and the weakest one is always at the door.

For `[5, 1, 9, 3, 7]` with $k = 2$: push 5, push 1 (heap holds 1, 5); push 9, now three items, pop 1 (holds 5, 9); push 3, pop 3 (holds 5, 9); push 7, pop 5 (holds 7, 9). The answer is 9 and 7.

```python
import heapq


def top_k_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return sorted(heap, reverse=True)


assert top_k_largest([5, 1, 9, 3, 7], 2) == [9, 7]
assert top_k_largest([4, 4, 4], 2) == [4, 4]
```

```cpp
vector<int> top_k_largest(const vector<int>& nums, int k) {
    priority_queue<int, vector<int>, greater<int>> pq;
    for (int x : nums) {
        pq.push(x);
        if ((int)pq.size() > k) pq.pop();
    }
    vector<int> out;
    while (!pq.empty()) {
        out.push_back(pq.top());
        pq.pop();
    }
    reverse(out.begin(), out.end());
    return out;
}
```

Each of the $n$ numbers costs $O(\log k)$, so time is $O(n \log k)$, and space is $O(k)$. When $k$ is small, this is much better than sorting in $O(n \log n)$.

To keep the $k$ **smallest** instead, flip everything: use a max-heap (negate in Python), and pop the largest whenever the size goes above $k$.

## 3.2 The k-th value so far

The top of that size-$k$ heap is special. For the $k$ largest, the heap's smallest item is exactly the **$k$-th largest** number seen so far. So after each new number, the answer to "what is the $k$-th largest now?" is just `heap[0]`, in $O(1)$.

Let's see the mirror image with an example: the $k$-th **smallest** so far. We keep a max-heap of the $k$ smallest numbers; its top is the $k$-th smallest. For `[5, 2, 8, 1, 9]` and $k = 2$ we report only once we have seen at least 2 numbers: after 5, 2 the second smallest is 5; after 8 it is still 5; after 1 the two smallest are 1, 2 so the answer is 2; after 9 it is 2.

```python
import heapq


def kth_smallest_so_far(nums, k):
    heap = []  # max-heap of the k smallest, stored negated
    out = []
    for x in nums:
        heapq.heappush(heap, -x)
        if len(heap) > k:
            heapq.heappop(heap)
        if len(heap) == k:
            out.append(-heap[0])
    return out


assert kth_smallest_so_far([5, 2, 8, 1, 9], 2) == [5, 5, 2, 2]
```

```cpp
vector<int> kth_smallest_so_far(const vector<int>& nums, int k) {
    priority_queue<int> pq;  // max-heap of the k smallest
    vector<int> out;
    for (int x : nums) {
        pq.push(x);
        if ((int)pq.size() > k) pq.pop();
        if ((int)pq.size() == k) out.push_back(pq.top());
    }
    return out;
}
```

Every number costs $O(\log k)$ and the answer is read in $O(1)$.

This is exactly the problem _Kth Largest in a Stream_. The sheet version starts with some initial numbers and then reports after each added number, using a min-heap of size $k$ that keeps the $k$ largest. Load the starting numbers first (pushing and popping to stay at size $k$), then handle every added number the same way and record `heap[0]`.

## 3.3 Top k by a custom key

Sometimes "best" is not the number itself but something computed from it, like a distance. Put the key first in a tuple: Python compares tuples left to right, so the key decides, and later fields break ties.

Let's find the $k$ numbers nearest to a target. We keep a **max-heap on distance** of size $k$, so the farthest of our current choices is at the top, ready to be thrown out. In Python we negate the tuple's parts; in C++ the default max-heap on `pair<int,int>` already compares the first number first.

```python
import heapq


def nearest_numbers(nums, target, k):
    heap = []  # entries (-distance, -value): top is the farthest candidate
    for x in nums:
        heapq.heappush(heap, (-abs(x - target), -x))
        if len(heap) > k:
            heapq.heappop(heap)
    return sorted(-v for _, v in heap)


assert nearest_numbers([1, 4, 6, 9, 12], 7, 2) == [6, 9]
assert nearest_numbers([10, 20], 0, 1) == [10]
```

```cpp
vector<int> nearest_numbers(const vector<int>& nums, int target, int k) {
    priority_queue<pair<int, int>> pq;  // (distance, value): top is the farthest
    for (int x : nums) {
        pq.push({abs(x - target), x});
        if ((int)pq.size() > k) pq.pop();
    }
    vector<int> out;
    while (!pq.empty()) {
        out.push_back(pq.top().second);
        pq.pop();
    }
    sort(out.begin(), out.end());
    return out;
}
```

Time is $O(n \log k)$ and space $O(k)$. If two numbers are equally far, the smaller value is kept, in both versions.

This is exactly the problem _K Closest Points to the Origin_. A point `(x, y)` plays the role of the number; its key is the squared distance $x^2 + y^2$ (no square root needed, since squaring keeps the order). Store `(-(x*x + y*y), -x, -y)` in Python so that ties by `x` and then `y` also work out, and return the survivors sorted by their keys.

## 3.4 A sliding buffer for nearly sorted data

Suppose a list is _almost_ sorted: every item is at most $k$ places away from where it belongs. Then the smallest item overall must be among the first $k + 1$ items. So load the first $k + 1$ items into a min-heap. Pop the smallest, which is surely the true first item. Then feed in the next item from the list, pop the smallest again, and so on. The heap is a small window sliding along the list, and it never holds more than $k + 1$ items.

For `[3, 1, 2, 5, 4]` with $k = 2$: heap starts with 3, 1, 2. Pop 1; add 5, pop 2; add 4, pop 3; then empty the heap: 4, 5. Result `[1, 2, 3, 4, 5]`.

```python
import heapq


def fix_nearly_sorted(items, k):
    heap = items[:k + 1]
    heapq.heapify(heap)
    out = []
    for x in items[k + 1:]:
        out.append(heapq.heappushpop(heap, x))
    while heap:
        out.append(heapq.heappop(heap))
    return out


assert fix_nearly_sorted([3, 1, 2, 5, 4], 2) == [1, 2, 3, 4, 5]
assert fix_nearly_sorted([1, 2, 3], 0) == [1, 2, 3]
```

```cpp
vector<int> fix_nearly_sorted(const vector<int>& items, int k) {
    int n = (int)items.size();
    int first = min(n, k + 1);
    priority_queue<int, vector<int>, greater<int>> pq(items.begin(), items.begin() + first);
    vector<int> out;
    for (int i = first; i < n; ++i) {
        pq.push(items[i]);
        out.push_back(pq.top());
        pq.pop();
    }
    while (!pq.empty()) {
        out.push_back(pq.top());
        pq.pop();
    }
    return out;
}
```

`heappushpop` pushes and then pops the smallest in one step. Time is $O(n \log k)$ and space is $O(k)$.

This is exactly the problem _Sort a Nearly Sorted Array_. When $k$ is much smaller than $n$, $O(n \log k)$ beats a full sort at $O(n \log n)$.

## 3.5 Check yourself

1. To keep the $k$ largest numbers, do we use a min-heap or a max-heap, and what do we pop?
2. After the stream `[5, 1, 9]` with $k = 2$, what is the 2nd largest so far?
3. Why can we compare squared distances and skip the square root?
4. In a list where every item is at most $k$ places from its sorted position, why must the smallest item be within the first $k + 1$ positions?

# Chapter 4. Greedy with a heap: smallest first

## 4.1 Join the cheapest pair

A **greedy** strategy picks the best-looking choice at every step and never looks back. Heaps are perfect for it, because "pick the best choice" is exactly what a heap does.

Here is a classic: you have several pieces of rope with given lengths. Joining two ropes costs the sum of their lengths and gives one longer rope. Join them all into one rope as cheaply as possible. The trick is to always join the **two shortest** ropes. Long ropes then get added to the total as few times as possible.

For lengths `[1, 2, 3, 4]`: join 1 and 2 for cost 3, giving `[3, 3, 4]`. Join 3 and 3 for cost 6, giving `[4, 6]`. Join 4 and 6 for cost 10. Total cost $3 + 6 + 10 = 19$. Any other order costs more; for example joining 3 and 4 first, then 1 and 2, then everything: $7 + 3 + 10 = 20$.

```python
import heapq


def cheapest_join_cost(lengths):
    heap = list(lengths)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        total += a + b
        heapq.heappush(heap, a + b)
    return total


assert cheapest_join_cost([1, 2, 3, 4]) == 19
assert cheapest_join_cost([5]) == 0
```

```cpp
long long cheapest_join_cost(const vector<int>& lengths) {
    priority_queue<long long, vector<long long>, greater<long long>> pq(lengths.begin(), lengths.end());
    long long total = 0;
    while (pq.size() > 1) {
        long long a = pq.top();
        pq.pop();
        long long b = pq.top();
        pq.pop();
        total += a + b;
        pq.push(a + b);
    }
    return total;
}
```

There are $n - 1$ joins, each with a few $O(\log n)$ heap steps, so time is $O(n \log n)$ and space $O(n)$.

This is exactly the problem _Connect Ropes With Minimum Cost_. The reason greedy is correct: every rope's length gets counted once for each join it takes part in, so a rope that is joined late (near the top) is counted few times. Making the longest ropes join last is best. The same idea builds Huffman codes.

## 4.2 Growing numbers from smaller ones

Heaps can also _generate_ values in sorted order. Let's find the $n$-th number of the form $2^a \cdot 3^b$ (a number with only 2 and 3 as prime factors): 1, 2, 3, 4, 6, 8, 9, 12, 16, 18, and so on.

The idea: start the heap with 1. Every number in the sequence is built from a smaller one by multiplying by 2 or 3. So pop the smallest number $x$, then push $2x$ and $3x$ as new candidates. The next pop is always the next number in order. One catch: 6 can be reached as $2 \cdot 3$ and as $3 \cdot 2$, so we keep a set `seen` to push each value only once.

```python
import heapq


def nth_smooth(n):
    heap = [1]
    seen = {1}
    for _ in range(n - 1):
        x = heapq.heappop(heap)
        for m in (2, 3):
            if x * m not in seen:
                seen.add(x * m)
                heapq.heappush(heap, x * m)
    return heap[0]


assert nth_smooth(1) == 1
assert nth_smooth(10) == 18
```

```cpp
long long nth_smooth(int n) {
    priority_queue<long long, vector<long long>, greater<long long>> pq;
    unordered_set<long long> seen;
    pq.push(1);
    seen.insert(1);
    for (int i = 0; i < n - 1; ++i) {
        long long x = pq.top();
        pq.pop();
        for (long long m : {2LL, 3LL}) {
            if (!seen.count(x * m)) {
                seen.insert(x * m);
                pq.push(x * m);
            }
        }
    }
    return pq.top();
}
```

Time is $O(n \log n)$: we pop $n$ times, and each pop adds a constant number of pushes. Space is $O(n)$.

This is exactly the problem _The Nth Ugly Number_. Use the multipliers 2, 3 and 5 instead of 2 and 3. (There is also an $O(n)$ method with three moving pointers into the list of answers found so far; the heap method is easier to invent and just as correct.)

## 4.3 The smallest card must start a group

Our last greedy example uses a heap together with a count table. You have cards with numbers and want to split them into groups of exactly three **consecutive** numbers, like 4, 5, 6. The smallest card cannot be the middle or the end of any group (no smaller card exists to start it), so it **must start a group**. Remove the smallest card together with the next two numbers. Repeat. If any needed number is missing, the answer is no.

We keep a dictionary `count` from number to how many cards we have, and a min-heap of the distinct numbers so we can always find the smallest one still available. When a number's count drops to zero, it must be the heap's top (otherwise a smaller number is still waiting for it as a partner, and that group could never be completed), and we pop it.

```python
import heapq


def split_into_runs_of_three(cards):
    if len(cards) % 3:
        return False
    count = {}
    for c in cards:
        count[c] = count.get(c, 0) + 1
    heap = list(count)
    heapq.heapify(heap)
    while heap:
        start = heap[0]
        for x in (start, start + 1, start + 2):
            if count.get(x, 0) == 0:
                return False
            count[x] -= 1
            if count[x] == 0:
                if x != heap[0]:
                    return False
                heapq.heappop(heap)
    return True


assert split_into_runs_of_three([1, 2, 3, 2, 3, 4]) is True
assert split_into_runs_of_three([1, 2, 4, 5, 6, 7]) is False
assert split_into_runs_of_three([1, 2, 3, 4]) is False
```

```cpp
bool split_into_runs_of_three(const vector<int>& cards) {
    if (cards.size() % 3 != 0) return false;
    unordered_map<int, int> count;
    for (int c : cards) count[c]++;
    priority_queue<int, vector<int>, greater<int>> pq;
    for (auto& [value, cnt] : count) pq.push(value);
    while (!pq.empty()) {
        int start = pq.top();
        for (int x = start; x < start + 3; ++x) {
            auto it = count.find(x);
            if (it == count.end() || it->second == 0) return false;
            it->second--;
            if (it->second == 0) {
                if (x != pq.top()) return false;
                pq.pop();
            }
        }
    }
    return true;
}
```

Time is $O(n \log n)$ in the worst case (building the heap plus up to $n$ distinct values popped) and space is $O(n)$.

This is exactly the problem _Hand of Straights_, where the group size is a parameter `group_size`: replace `(start, start + 1, start + 2)` by every number from `start` to `start + group_size - 1`, and check that the total number of cards is divisible by `group_size` first.

## 4.4 Check yourself

1. Why does joining the two shortest ropes first give the smallest total cost?
2. In the smooth-number generator, why do we need the `seen` set?
3. Why must the smallest remaining card start a group of consecutive numbers?
4. What does it tell us if a number's count hits zero but it is not the heap's top?

# Chapter 5. Merging sorted lists (k-way merge)

## 5.1 Merging two lists

If two lists are already sorted, we can merge them with two pointers: compare the front items, take the smaller one, move that pointer forward. This is the merge step of merge sort and costs $O(n + m)$.

```python
def merge_two(a, b):
    out = []
    i = j = 0
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


assert merge_two([1, 4, 7], [2, 3, 9]) == [1, 2, 3, 4, 7, 9]
assert merge_two([], [5]) == [5]
```

```cpp
vector<int> merge_two(const vector<int>& a, const vector<int>& b) {
    vector<int> out;
    size_t i = 0, j = 0;
    while (i < a.size() && j < b.size()) {
        if (a[i] <= b[j]) out.push_back(a[i++]);
        else out.push_back(b[j++]);
    }
    while (i < a.size()) out.push_back(a[i++]);
    while (j < b.size()) out.push_back(b[j++]);
    return out;
}
```

## 5.2 Merging many lists with a heap

With $k$ lists, comparing all $k$ front items every time would be slow. The next item of the merged output is always the smallest of the $k$ current fronts, and "smallest of a group that keeps changing" is exactly a heap job. We keep one entry per list in the heap: `(value, which list, position in that list)`. Pop the smallest entry, write its value to the output, then push the next item from the same list (if any).

```python
import heapq


def merge_many(lists):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    out = []
    while heap:
        value, i, j = heapq.heappop(heap)
        out.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out


assert merge_many([[2, 6], [1, 4, 9], [3]]) == [1, 2, 3, 4, 6, 9]
assert merge_many([[], [1]]) == [1]
```

```cpp
vector<int> merge_many(const vector<vector<int>>& lists) {
    using T = array<int, 3>;  // value, which list, position
    priority_queue<T, vector<T>, greater<T>> pq;
    for (int i = 0; i < (int)lists.size(); ++i)
        if (!lists[i].empty()) pq.push({lists[i][0], i, 0});
    vector<int> out;
    while (!pq.empty()) {
        auto [value, i, j] = pq.top();
        pq.pop();
        out.push_back(value);
        if (j + 1 < (int)lists[i].size()) pq.push({lists[i][j + 1], i, j + 1});
    }
    return out;
}
```

The heap never holds more than $k$ entries. With $N$ items in total, each causes one push and one pop of $O(\log k)$, so time is $O(N \log k)$ and extra space is $O(k)$ (plus the output). This is much better than concatenating and sorting when $k$ is small.

This is exactly the problem _Merge K Sorted Arrays_. The tuple trick matters: the list index is the second field so that ties on value never force Python to compare the lists themselves.

## 5.3 The k-th smallest across sorted lists

The same loop answers "what is the $k$-th smallest value overall?" Just stop after $k$ pops: the last popped value is the answer. We never needed the other items, so we stop early and save time.

```python
import heapq


def kth_in_sorted_lists(lists, k):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    value = None
    for _ in range(k):
        if not heap:
            return -1
        value, i, j = heapq.heappop(heap)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return value


assert kth_in_sorted_lists([[2, 6], [1, 4, 9], [3]], 4) == 4
assert kth_in_sorted_lists([[2, 6], [1, 4, 9], [3]], 10) == -1
```

```cpp
int kth_in_sorted_lists(const vector<vector<int>>& lists, int k) {
    using T = array<int, 3>;
    priority_queue<T, vector<T>, greater<T>> pq;
    for (int i = 0; i < (int)lists.size(); ++i)
        if (!lists[i].empty()) pq.push({lists[i][0], i, 0});
    int value = -1;
    for (int step = 0; step < k; ++step) {
        if (pq.empty()) return -1;
        auto [v, i, j] = pq.top();
        pq.pop();
        value = v;
        if (j + 1 < (int)lists[i].size()) pq.push({lists[i][j + 1], i, j + 1});
    }
    return value;
}
```

Time is $O((k + m) \log m)$ for $m$ lists.

This is exactly the problem _Kth Smallest in a Sorted Matrix_: every row of the matrix is a sorted list, so the matrix is a set of sorted lists. Because the columns are sorted too, you only need to start with the first $\min(k, \text{rows})$ rows, since a row deeper than $k$ cannot contain one of the $k$ smallest values.

## 5.4 Pairs are secretly sorted lists

Here is a clever disguise. Given two sorted lists `a` and `b` of positive numbers, find the $k$ smallest **products** $a_i \cdot b_j$. There are $n \cdot m$ pairs, far too many to list. But for a fixed $i$, the products $a_i b_0, a_i b_1, a_i b_2, \dots$ are _sorted increasing_, since `b` is sorted. So the pairs form $n$ sorted lists, and we only need the $k$ smallest across them: a k-way merge, where each list is generated on the fly.

Start with the first product of each row `i` (only the first $k$ rows can matter). Pop the smallest `(i, j)`; the next candidate from that row is `(i, j + 1)`.

```python
import heapq


def k_smallest_products(a, b, k):
    heap = [(a[i] * b[0], i, 0) for i in range(min(k, len(a)))]
    heapq.heapify(heap)
    out = []
    while heap and len(out) < k:
        value, i, j = heapq.heappop(heap)
        out.append(value)
        if j + 1 < len(b):
            heapq.heappush(heap, (a[i] * b[j + 1], i, j + 1))
    return out


assert k_smallest_products([1, 2, 3], [2, 3, 5], 4) == [2, 3, 4, 5]
assert k_smallest_products([1, 2, 3], [2, 3, 5], 6) == [2, 3, 4, 5, 6, 6]
```

```cpp
vector<int> k_smallest_products(const vector<int>& a, const vector<int>& b, int k) {
    using T = array<int, 3>;  // product, i, j
    priority_queue<T, vector<T>, greater<T>> pq;
    for (int i = 0; i < min<int>(k, a.size()); ++i) pq.push({a[i] * b[0], i, 0});
    vector<int> out;
    while (!pq.empty() && (int)out.size() < k) {
        auto [value, i, j] = pq.top();
        pq.pop();
        out.push_back(value);
        if (j + 1 < (int)b.size()) pq.push({a[i] * b[j + 1], i, j + 1});
    }
    return out;
}
```

Time is $O(k \log k)$ and space $O(k)$.

This is exactly the problem _K Smallest Pair Sums_: replace the product with the sum $a_i + b_j$. Sums grow with `j` for a fixed `i` just like products, so everything else stays the same.

## 5.5 Moving the smallest forward

One more twist on the merge. We have $k$ sorted lists and want the narrowest range of values that contains **at least one number from every list**. Think of one pointer in each list. The range covering the current pointers runs from the smallest pointed value to the largest. To make the range narrower, only moving the _smallest_ pointer forward can help (moving the largest forward would only widen it). So: keep a min-heap of the current pointed values, remember the maximum among them, and repeatedly advance the list that holds the minimum, updating the best (narrowest) range as we go. Stop when some list runs out.

To keep the example simple, this function returns only the narrowest width.

```python
import heapq


def narrowest_width(lists):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists)]
    heapq.heapify(heap)
    current_max = max(lst[0] for lst in lists)
    best = current_max - heap[0][0]
    while True:
        value, i, j = heapq.heappop(heap)
        if j + 1 == len(lists[i]):
            return best
        nxt = lists[i][j + 1]
        current_max = max(current_max, nxt)
        heapq.heappush(heap, (nxt, i, j + 1))
        best = min(best, current_max - heap[0][0])


assert narrowest_width([[1, 5], [3, 4], [2, 9]]) == 2
assert narrowest_width([[7], [7]]) == 0
```

```cpp
int narrowest_width(const vector<vector<int>>& lists) {
    using T = array<int, 3>;
    priority_queue<T, vector<T>, greater<T>> pq;
    int current_max = INT_MIN;
    for (int i = 0; i < (int)lists.size(); ++i) {
        pq.push({lists[i][0], i, 0});
        current_max = max(current_max, lists[i][0]);
    }
    int best = current_max - pq.top()[0];
    while (true) {
        auto [value, i, j] = pq.top();
        pq.pop();
        if (j + 1 == (int)lists[i].size()) return best;
        int nxt = lists[i][j + 1];
        current_max = max(current_max, nxt);
        pq.push({nxt, i, j + 1});
        best = min(best, current_max - pq.top()[0]);
    }
}
```

With $N$ total numbers and $k$ lists, each step is $O(\log k)$, so time is $O(N \log k)$ and space $O(k)$.

This is exactly the problem _Smallest Range Covering K Lists_. The sheet asks for the range itself, not just its width, so also save `lo` and `hi` whenever `best` improves, and break ties by the smaller `lo`.

## 5.6 Check yourself

1. Why does the k-way merge heap hold at most $k$ entries?
2. Why do we put the list index inside the heap tuple?
3. How can a matrix with sorted rows be seen as a set of sorted lists?
4. In the narrowest range idea, why do we always advance the list that holds the current minimum?

# Chapter 6. Two heaps and the running median

## 6.1 Why the median is awkward

The **median** is the middle value of a sorted list: for 5 numbers it is the 3rd smallest, and for an even count it is the average of the two middle ones. If numbers keep arriving and we must report the median after each one, sorting every time costs $O(n \log n)$ per number, and inserting into a sorted list costs $O(n)$. We want something much faster.

## 6.2 Splitting into a lower and an upper half

The key observation: to know the median we do not need the numbers sorted. We only need to know the largest number of the **lower half** and the smallest number of the **upper half**. So split the numbers into two heaps:

```
 lower half (max-heap)         upper half (min-heap)
 top = biggest of the small    top = smallest of the big
        [ ... 2, 5 ]    |    [ 7, 9 ... ]
                 ^            ^
                 the two middle numbers
```

The lower half is a max-heap, so its top is the largest small number. The upper half is a min-heap, so its top is the smallest big number. We keep two rules: every number in the lower half is at most every number in the upper half, and the sizes differ by at most one, with the lower half allowed to be the bigger one. Then the median is the top of the lower half when the count is odd, and the average of the two tops when the count is even.

## 6.3 Adding a number

To add $x$: if it belongs to the lower half (it is at most the lower top), push it there, otherwise push it to the upper half. Then fix the sizes: if the lower half has two more items, move its top to the upper half; if the upper half has more items than the lower half, move its top to the lower half. At most one move is needed.

```python
import heapq


class RunningMedian:
    def __init__(self):
        self.low = []   # max-heap of the lower half, stored negated
        self.high = []  # min-heap of the upper half

    def add(self, x):
        if not self.low or x <= -self.low[0]:
            heapq.heappush(self.low, -x)
        else:
            heapq.heappush(self.high, x)
        if len(self.low) > len(self.high) + 1:
            heapq.heappush(self.high, -heapq.heappop(self.low))
        elif len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self):
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2


rm = RunningMedian()
seen = []
for v in [2, 8, 1, 7]:
    rm.add(v)
    seen.append(rm.median())
assert seen == [2.0, 5.0, 2.0, 4.5]
```

```cpp
class RunningMedian {
    priority_queue<int> low;                              // max-heap, lower half
    priority_queue<int, vector<int>, greater<int>> high;  // min-heap, upper half

public:
    void add(int x) {
        if (low.empty() || x <= low.top()) low.push(x);
        else high.push(x);
        if (low.size() > high.size() + 1) {
            high.push(low.top());
            low.pop();
        } else if (high.size() > low.size()) {
            low.push(high.top());
            high.pop();
        }
    }

    double median() const {
        if (low.size() > high.size()) return (double)low.top();
        return ((double)low.top() + (double)high.top()) / 2.0;
    }
};
```

Let's trace `[2, 8, 1, 7]`. Add 2: lower `{2}`, median 2.0. Add 8: it is above 2, goes to upper `{8}`; sizes 1 and 1, so the median is $(2 + 8)/2 = 5.0$. Add 1: it is at most 2, goes to lower `{2, 1}`; sizes 2 and 1 are fine; the median is the lower top, 2.0. Add 7: it is above 2, goes to upper `{7, 8}`; sizes 2 and 2; median $(2 + 7)/2 = 4.5$.

## 6.4 Cost and why it works

Each `add` does a constant number of heap operations, so it costs $O(\log n)$. Each `median` call just looks at one or two tops, so it costs $O(1)$. Over $n$ numbers the total is $O(n \log n)$, with $O(n)$ space.

Why does this stay correct? Every lower-half number is at most every upper-half number (we only push where that stays true, and the moves between halves move a top, which is the extreme element closest to the boundary). The size rule then guarantees the boundary sits exactly in the middle. The balance rule is the reason we moved only one item: pushing one number can unbalance the sizes by at most one.

This is exactly the problem _Median After Each Number_. Feed each number to `add`, then read `median()` and collect the answers; the sheet wants decimals such as 2.0 and 2.5.

The two-heap idea also finds any "boundary" statistic: for example, if you wanted the 25th percentile you would keep the heaps at sizes 1 to 3 instead of 1 to 1.

## 6.5 Check yourself

1. Which half is a max-heap and which a min-heap, and why?
2. If the count is odd, which heap is bigger and where is the median?
3. After adding the number 4 to lower `{3, 1}` and upper `{6}`, what are the halves and the new median?
4. How long does `median()` take, and why?

# Chapter 7. Scheduling and planning with heaps

## 7.1 Which room is free first?

You are given bookings with start and end times, and you must find how many tables (or rooms) are needed so that no two overlapping bookings share one. Sort the bookings by start time. Keep a min-heap of the **end times** of the tables currently in use. When a new booking starts, look at the heap's top: that is the table that frees up first. If it is already free (its end time is at most the new start), reuse that table, which means replacing its end time with the new booking's end time. Otherwise open a new table. The answer is the number of tables at the end, which is the heap size.

For `[[1, 4], [2, 5], [4, 6]]`: booking (1,4) opens table A (heap `[4]`). Booking (2,5): the top 4 is later than 2, so open table B (heap `[4, 5]`). Booking (4,6): the top 4 is at most 4, so reuse A (heap `[5, 6]`). Two tables.

```python
import heapq


def min_tables(bookings):
    busy = []  # end times of tables in use
    for start, end in sorted(bookings):
        if busy and busy[0] <= start:
            heapq.heapreplace(busy, end)
        else:
            heapq.heappush(busy, end)
    return len(busy)


assert min_tables([[1, 4], [2, 5], [4, 6]]) == 2
assert min_tables([[1, 2], [3, 4]]) == 1
```

```cpp
int min_tables(vector<vector<int>> bookings) {
    sort(bookings.begin(), bookings.end());
    priority_queue<int, vector<int>, greater<int>> busy;  // end times
    for (auto& b : bookings) {
        if (!busy.empty() && busy.top() <= b[0]) busy.pop();
        busy.push(b[1]);
    }
    return (int)busy.size();
}
```

Sorting costs $O(n \log n)$ and each booking does $O(\log n)$ heap work, so time is $O(n \log n)$ and space $O(n)$.

This is exactly the problem _Meeting Rooms_: meetings are bookings and rooms are tables. Note that the problem says a meeting ending at time $t$ does not conflict with one starting at $t$, which is why the test is "at most", not "strictly less than".

## 7.2 Unlock, then pick the best

Now a different shape. You have some money `wealth` and may do at most $k$ jobs, one after another. Each job needs a minimum wealth to start and adds a gain to your wealth. Greedy says: among the jobs you can afford, always do the one with the biggest gain, because richer is never worse. But "affordable" changes as you grow richer. So sort the jobs by their requirement, keep a pointer into this sorted list, and a **max-heap of the gains of jobs you can afford**. Before each pick, move every newly affordable job into the heap, then pop the best.

With wealth 0 and jobs (needs, gains) = (0, 3), (0, 5), (6, 9): both cheap jobs are affordable, so pick the gain-5 job (wealth 5). The gain-9 job still needs 6, so we cannot take it; take gain 3 next (wealth 8).

```python
import heapq


def max_wealth(k, wealth, gains, needs):
    jobs = sorted(zip(needs, gains))
    affordable = []  # max-heap of gains, stored negated
    i = 0
    for _ in range(k):
        while i < len(jobs) and jobs[i][0] <= wealth:
            heapq.heappush(affordable, -jobs[i][1])
            i += 1
        if not affordable:
            break
        wealth += -heapq.heappop(affordable)
    return wealth


assert max_wealth(2, 0, [5, 3, 9], [0, 0, 6]) == 8
assert max_wealth(3, 0, [4], [10]) == 0
```

```cpp
long long max_wealth(int k, long long wealth, const vector<int>& gains, const vector<int>& needs) {
    int n = (int)gains.size();
    vector<pair<int, int>> jobs(n);
    for (int i = 0; i < n; ++i) jobs[i] = {needs[i], gains[i]};
    sort(jobs.begin(), jobs.end());
    priority_queue<int> affordable;  // max-heap of gains
    int i = 0;
    for (int round = 0; round < k; ++round) {
        while (i < n && jobs[i].first <= wealth) affordable.push(jobs[i++].second);
        if (affordable.empty()) break;
        wealth += affordable.top();
        affordable.pop();
    }
    return wealth;
}
```

Each job enters and leaves the heap at most once, so time is $O(n \log n)$ and space $O(n)$.

This is exactly the problem _IPO: Maximize Capital_: capital is your wealth, `capital[i]` is the requirement of project $i$, and `profits[i]` is its gain.

## 7.3 Regret: take the fuel only when needed

A car drives along a line toward a target. It starts with some fuel (one unit moves it one mile) and there are stations along the way, each with a pile of fuel. We want to reach the target with the fewest stops. Deciding at each station whether to stop is hard, because we do not know the future. The trick is to **decide late**. We pass every station without stopping, but remember its fuel amount in a max-heap. Only when we run out of fuel before the next station do we say: "we should have stopped at the best station we passed", pop the biggest pile, add it to our fuel, and count one stop. This is a **regret** strategy: we undo a choice after the fact.

Take target 50, starting fuel 20, stations at (10, fuel 10), (20, fuel 10), (30, fuel 20). Drive to 10 and 20: remember piles 10 and 10. To reach 30 we need more fuel: pop a 10 (fuel 30, one stop), then remember the pile 20. To reach 50 we need more: pop the biggest remaining pile, 20 (fuel 50, two stops). Answer 2.

```python
import heapq


def fewest_stops(target, fuel, stations):
    passed = []  # max-heap of fuel piles we drove past, stored negated
    stops = 0
    for position, amount in list(stations) + [[target, 0]]:
        while fuel < position:
            if not passed:
                return -1
            fuel += -heapq.heappop(passed)
            stops += 1
        heapq.heappush(passed, -amount)
    return stops


assert fewest_stops(50, 20, [[10, 10], [20, 10], [30, 20]]) == 2
assert fewest_stops(20, 5, [[10, 5]]) == -1
assert fewest_stops(5, 10, []) == 0
```

```cpp
int fewest_stops(int target, long long fuel, vector<vector<int>> stations) {
    stations.push_back({target, 0});
    priority_queue<int> passed;  // max-heap of fuel piles we drove past
    int stops = 0;
    for (auto& s : stations) {
        while (fuel < s[0]) {
            if (passed.empty()) return -1;
            fuel += passed.top();
            passed.pop();
            ++stops;
        }
        passed.push(s[1]);
    }
    return stops;
}
```

Here `fuel` really means "how far we can reach in total". Time is $O(n \log n)$ and space $O(n)$.

This is exactly the problem _Minimum Refueling Stops_. The heap gives the greedy its power: each time we are stuck, the best pile we passed is the best way to fix it.

## 7.4 Regret again: ladders for the biggest climbs

The same "decide late" idea solves this: you walk across buildings of different heights. Going down or level is free. Climbing costs bricks equal to the height difference, or one ladder per climb of any size, and you have a limited number of ladders. Use ladders on the **biggest climbs**. But we do not know which climbs will be biggest yet. So for every climb, tentatively give it a ladder. Keep these ladder-climbs in a **min-heap**. If we have used more ladders than we own, take the _smallest_ ladder-climb out and pay for it with bricks instead. If the bricks run out, we cannot go further.

For heights `[1, 5, 2, 8, 3]` with 2 bricks and 1 ladder: the climb 1 to 5 is 4, ladder (heap `[4]`). Going down 5 to 2 is free. The climb 2 to 8 is 6, ladder too (heap `[4, 6]`), but we have only one ladder, so pop the smallest climb 4 and pay 4 bricks. We have only 2 bricks, so we are stuck while trying to reach building 3. The furthest building is index 2.

```python
import heapq


def furthest_step(heights, bricks, ladders):
    ladder_climbs = []  # min-heap of climbs currently covered by ladders
    for i in range(len(heights) - 1):
        climb = heights[i + 1] - heights[i]
        if climb <= 0:
            continue
        heapq.heappush(ladder_climbs, climb)
        if len(ladder_climbs) > ladders:
            bricks -= heapq.heappop(ladder_climbs)
            if bricks < 0:
                return i
    return len(heights) - 1


assert furthest_step([1, 5, 2, 8, 3], 2, 1) == 2
assert furthest_step([1, 2, 3], 0, 2) == 2
assert furthest_step([5, 4, 3], 0, 0) == 2
```

```cpp
int furthest_step(const vector<int>& heights, long long bricks, int ladders) {
    priority_queue<int, vector<int>, greater<int>> ladder_climbs;
    for (int i = 0; i + 1 < (int)heights.size(); ++i) {
        int climb = heights[i + 1] - heights[i];
        if (climb <= 0) continue;
        ladder_climbs.push(climb);
        if ((int)ladder_climbs.size() > ladders) {
            bricks -= ladder_climbs.top();
            ladder_climbs.pop();
            if (bricks < 0) return i;
        }
    }
    return (int)heights.size() - 1;
}
```

The heap never holds more than `ladders + 1` items, so time is $O(n \log L)$ for $L$ ladders and space $O(L)$.

This is exactly the problem _Furthest Building You Can Reach_. It looks like the "keep the top $k$" pattern of Chapter 3: the heap keeps the `ladders` biggest climbs, and everything pushed out is paid for with bricks.

## 7.5 Check yourself

1. In the meeting-room idea, what does the top of the heap represent?
2. Why do we move newly affordable jobs into the heap before every pick?
3. In the refuelling problem, why do we remember stations we did not stop at?
4. In the ladder problem, which climb gets pushed out of the heap when we own too many ladders, and why?

# Chapter 8. Lazy deletion

## 8.1 Heaps cannot delete from the middle

A heap is fast at one thing: removing the top. But sometimes a problem asks us to remove an item that is somewhere in the middle, for example when a number leaves a sliding window. Searching the heap list for it costs $O(n)$, and pulling an item out of the middle would break the heap property. So we use a trick.

## 8.2 The notebook trick

Lazy deletion means: when we want to remove an item, we do not touch the heap. We just write down in a notebook (a dictionary of counts) "this value is dead". Later, whenever the item reaches the top of the heap, we check the notebook; if the item is dead, we throw it away and look at the next one. Dead items buried deep inside do no harm, because nobody looks at them until they surface. Each item is thrown away at most once, so the total extra work is small.

We also keep a separate counter of the real (live) size, because the heap's own length now includes dead items.

```python
import heapq


class LazyMinHeap:
    def __init__(self):
        self.heap = []
        self.dead = {}  # value -> how many copies are waiting to be thrown away
        self.size = 0   # number of live items

    def push(self, x):
        heapq.heappush(self.heap, x)
        self.size += 1

    def remove(self, x):
        # the caller promises that x is currently in the heap
        self.dead[x] = self.dead.get(x, 0) + 1
        self.size -= 1

    def _clean(self):
        while self.heap and self.dead.get(self.heap[0], 0) > 0:
            self.dead[self.heap[0]] -= 1
            heapq.heappop(self.heap)

    def top(self):
        self._clean()
        return self.heap[0]

    def pop(self):
        self._clean()
        self.size -= 1
        return heapq.heappop(self.heap)


lh = LazyMinHeap()
for v in [5, 1, 3, 1]:
    lh.push(v)
lh.remove(1)
assert lh.top() == 1  # one copy of 1 is still alive
lh.remove(1)
assert lh.top() == 3
assert lh.size == 2
assert lh.pop() == 3
```

```cpp
class LazyMinHeap {
    priority_queue<int, vector<int>, greater<int>> heap;
    unordered_map<int, int> dead;  // value -> copies waiting to be thrown away

    void clean() {
        while (!heap.empty() && dead[heap.top()] > 0) {
            dead[heap.top()]--;
            heap.pop();
        }
    }

public:
    int size = 0;  // number of live items

    void push(int x) {
        heap.push(x);
        ++size;
    }

    void remove(int x) {  // the caller promises that x is currently in the heap
        dead[x]++;
        --size;
    }

    int top() {
        clean();
        return heap.top();
    }

    int pop() {
        clean();
        int v = heap.top();
        heap.pop();
        --size;
        return v;
    }
};
```

Each `push` and each real removal costs $O(\log n)$ (a dead item is popped once, when it surfaces). So over $n$ operations the total time is $O(n \log n)$. Space is $O(n)$.

## 8.3 Expiring items by position

Sometimes we do not need a notebook at all: we can detect a dead item from its own data. In the sliding window maximum problem we ask for the largest value in every window of $k$ numbers. Keep a max-heap of `(value, index)` pairs. The window at position $i$ covers indices $i - k + 1$ to $i$. If the top has an index that is too old, it has left the window, so throw it away. The first top that is still inside the window is the answer, and any old items hiding below it are harmless.

For `[1, 3, -1, -3, 5, 3, 6, 7]` and $k = 3$ the window maximums are `[3, 3, 5, 5, 6, 7]`.

```python
import heapq


def window_maximums(nums, k):
    heap = []  # entries (-value, index)
    out = []
    for i, x in enumerate(nums):
        heapq.heappush(heap, (-x, i))
        if i >= k - 1:
            while heap[0][1] <= i - k:
                heapq.heappop(heap)
            out.append(-heap[0][0])
    return out


assert window_maximums([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
assert window_maximums([4, 2], 1) == [4, 2]
```

```cpp
vector<int> window_maximums(const vector<int>& nums, int k) {
    priority_queue<pair<int, int>> pq;  // (value, index), largest value on top
    vector<int> out;
    for (int i = 0; i < (int)nums.size(); ++i) {
        pq.push({nums[i], i});
        if (i >= k - 1) {
            while (pq.top().second <= i - k) pq.pop();
            out.push_back(pq.top().first);
        }
    }
    return out;
}
```

Time is $O(n \log n)$ and space $O(n)$, because old items may stay buried until they surface.

## 8.4 A median that slides

Now we combine two heaps (Chapter 6) with lazy deletion. We want the median of every window of $k$ numbers. When the window slides, one number enters and one leaves. Entering is just `add` from Chapter 6. Leaving is the hard part: the number sits inside one of the two heaps. We cannot delete it, so we mark it dead and **adjust the logical sizes** right away. The key points are:

- We track the live size of each half in two counters, `n_low` and `n_high`, because the heap lengths include dead items.
- To remove $x$, we decide which half it belongs to by comparing with the lower half's live top: if $x$ is at most that top, it is in the lower half. We then decrease the matching counter.
- Before looking at any top, we clean dead items off it.
- After every change we rebalance using the counters, not the heap lengths.

```python
import heapq


class WindowMedian:
    def __init__(self):
        self.low = []   # max-heap (negated values)
        self.high = []  # min-heap
        self.dead = {}  # value -> pending removals
        self.n_low = 0
        self.n_high = 0

    def _clean_low(self):
        while self.low and self.dead.get(-self.low[0], 0) > 0:
            self.dead[-self.low[0]] -= 1
            heapq.heappop(self.low)

    def _clean_high(self):
        while self.high and self.dead.get(self.high[0], 0) > 0:
            self.dead[self.high[0]] -= 1
            heapq.heappop(self.high)

    def _rebalance(self):
        if self.n_low > self.n_high + 1:
            self._clean_low()
            heapq.heappush(self.high, -heapq.heappop(self.low))
            self.n_low -= 1
            self.n_high += 1
        elif self.n_low < self.n_high:
            self._clean_high()
            heapq.heappush(self.low, -heapq.heappop(self.high))
            self.n_high -= 1
            self.n_low += 1

    def add(self, x):
        self._clean_low()
        if self.n_low == 0 or x <= -self.low[0]:
            heapq.heappush(self.low, -x)
            self.n_low += 1
        else:
            heapq.heappush(self.high, x)
            self.n_high += 1
        self._rebalance()

    def remove(self, x):
        self._clean_low()
        self.dead[x] = self.dead.get(x, 0) + 1
        if x <= -self.low[0]:
            self.n_low -= 1
        else:
            self.n_high -= 1
        self._rebalance()

    def median(self):
        self._clean_low()
        self._clean_high()
        if self.n_low > self.n_high:
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2


wm = WindowMedian()
for v in [2, 7, 4]:
    wm.add(v)
assert wm.median() == 4.0
wm.remove(2)
wm.add(1)
assert wm.median() == 4.0
wm.remove(7)
wm.add(8)
assert wm.median() == 4.0
```

```cpp
class WindowMedian {
    priority_queue<int> low;                              // max-heap
    priority_queue<int, vector<int>, greater<int>> high;  // min-heap
    unordered_map<int, int> dead;                         // pending removals
    int n_low = 0, n_high = 0;

    void clean_low() {
        while (!low.empty() && dead[low.top()] > 0) {
            dead[low.top()]--;
            low.pop();
        }
    }

    void clean_high() {
        while (!high.empty() && dead[high.top()] > 0) {
            dead[high.top()]--;
            high.pop();
        }
    }

    void rebalance() {
        if (n_low > n_high + 1) {
            clean_low();
            high.push(low.top());
            low.pop();
            --n_low;
            ++n_high;
        } else if (n_low < n_high) {
            clean_high();
            low.push(high.top());
            high.pop();
            --n_high;
            ++n_low;
        }
    }

public:
    void add(int x) {
        clean_low();
        if (n_low == 0 || x <= low.top()) {
            low.push(x);
            ++n_low;
        } else {
            high.push(x);
            ++n_high;
        }
        rebalance();
    }

    void remove(int x) {
        clean_low();
        dead[x]++;
        if (x <= low.top()) --n_low;
        else --n_high;
        rebalance();
    }

    double median() {
        clean_low();
        clean_high();
        if (n_low > n_high) return (double)low.top();
        return ((double)low.top() + (double)high.top()) / 2.0;
    }
};
```

In the test, the window starts as `{2, 7, 4}` with median 4. Remove 2 and add 1: the window `{7, 4, 1}` has median 4. Remove 7 and add 8: the window `{4, 1, 8}` still has median 4.

Each `add` and `remove` costs $O(\log n)$ amortised, so a slide costs $O(\log n)$ and the median is read in $O(1)$ after cleaning. Over a whole array that is $O(n \log n)$ time and $O(n)$ space.

This is exactly the problem _Sliding Window Median_. To use the class, add the first $k$ numbers, record the median, and then for each next index add the new number, remove the one that left (`nums[i - k]`), and record the median again. Careful with one detail: when the window has an even size, the median is the average of two tops, so use `/ 2` as above.

## 8.5 Check yourself

1. Why can a normal heap not remove an item from the middle quickly?
2. In lazy deletion, why do we keep a separate live size?
3. In the window maximum heap, how do we know the top has left the window?
4. In the sliding median, why do we rebalance with the counters and not with the heap lengths?
