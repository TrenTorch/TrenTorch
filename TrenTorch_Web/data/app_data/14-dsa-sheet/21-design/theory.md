> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Design problems)

This page teaches you how to build small, fast data structures: caches that forget the right thing, trees that answer "what is the sum or the minimum of this stretch?" in a blink, stores that remember the past, and groups that merge. In a **design** question you do not solve one puzzle. You build a little machine that must answer a long list of operations, and the whole art is to choose the pieces so that the busiest operations are cheap.

The page is a staircase. **Chapter 1 is gentle**: it shows what a design question looks like and builds the simplest machine, a browser history, from a list and one number. The next chapters add one idea at a time: queues and time windows, binary search on stored history, the least recently used (LRU) cache, the least frequently used (LFU) cache, the Fenwick tree, the segment tree with lazy updates, the sparse table, and finally union-find. By the end you will know the standard toolbox that most design questions are made from. Every code example is shown in Python and in C++.

# Chapter 1. Design questions and simple machines

## 1.1 What a design question asks

In a design question you are given a list of operations written as text, such as `"put 1 5"` or `"get 1"`. You must run them one after another on a structure that you build, and return the answers of the operations that produce an answer. For example, with a counter that supports `add x` (no answer) and `get` (the current total), the operations `["add 5", "get", "add 2", "get"]` give the answers `[5, 7]`.

Each text is split at the spaces into words, and the first word tells you which operation it is. Here is the smallest possible machine.

```python
def run_counter(ops):
    total = 0
    answers = []
    for op in ops:
        parts = op.split()
        if parts[0] == "add":
            total += int(parts[1])
        else:
            answers.append(total)
    return answers


assert run_counter(["add 5", "get", "add 2", "get"]) == [5, 7]
assert run_counter(["get"]) == [0]
```

```cpp
vector<int> run_counter(const vector<string>& ops) {
    long long total = 0;
    vector<int> answers;
    for (const string& op : ops) {
        istringstream in(op);
        string word;
        in >> word;
        if (word == "add") {
            long long x;
            in >> x;
            total += x;
        } else {
            answers.push_back((int)total);
        }
    }
    return answers;
}
```

The real design questions have the same shape, only the machine inside is cleverer. In later chapters we will write the machine as a class with one method per operation, and the text-splitting part stays this simple.

## 1.2 Pick the structure for the busy operation

The first question to ask is: which operation will be repeated most, and what does it need? If the machine must answer "is this name in the guest list?" a hundred thousand times, a plain list is a poor choice, because to check a name it walks through the whole list. A **hash set** (a container that jumps straight to an item using a number computed from the item) answers the same question in one step on average.

```python
def build_list(names):
    return list(names)


def build_set(names):
    return set(names)


guests_list = build_list(["ana", "bo", "cy"])
guests_set = build_set(["ana", "bo", "cy"])
assert ("bo" in guests_list) is True
assert ("bo" in guests_set) is True
assert ("zed" in guests_set) is False
```

```cpp
vector<string> build_list(const vector<string>& names) {
    return names;
}

unordered_set<string> build_set(const vector<string>& names) {
    return unordered_set<string>(names.begin(), names.end());
}
```

A membership test on the list costs $O(n)$, on the set it costs $O(1)$ on average. The two give identical answers; only the speed differs. Every design question on this page has a slow "starter" solution that is correct but too slow, and the lesson is always the same: find the operation that is slow and replace the structure behind it.

## 1.3 A list and a pointer

Now a real machine. A browser starts on a home page. `visit url` opens a new page and forgets everything ahead in the history. `back k` goes back up to $k$ pages and `forward k` goes forward up to $k$ pages, never past the ends. After each `back` and `forward` we report the current page.

The picture to hold in your head is a row of pages and a finger pointing at the current one.

```
pages:   a   b   c        finger at c (index 2)
back 1:  a   b   c        finger at b (index 1)
visit d: a   b   d        c is forgotten, finger at d (index 2)
```

We keep the pages in a list and the finger as an index `cur`. `back` subtracts from `cur` but never goes below 0. `forward` adds to `cur` but never goes beyond the last page. `visit` cuts off everything after `cur`, appends the new page, and moves the finger onto it.

```python
class BrowserHistory:
    def __init__(self, homepage):
        self.pages = [homepage]
        self.cur = 0

    def visit(self, url):
        del self.pages[self.cur + 1:]
        self.pages.append(url)
        self.cur += 1

    def back(self, k):
        self.cur = max(0, self.cur - k)
        return self.pages[self.cur]

    def forward(self, k):
        self.cur = min(len(self.pages) - 1, self.cur + k)
        return self.pages[self.cur]


h = BrowserHistory("a")
h.visit("b")
h.visit("c")
assert h.back(1) == "b"
assert h.back(5) == "a"
assert h.forward(1) == "b"
h.visit("d")
assert h.forward(3) == "d"
```

```cpp
struct BrowserHistory {
    vector<string> pages;
    int cur;

    BrowserHistory(const string& homepage) : pages{homepage}, cur(0) {}

    void visit(const string& url) {
        pages.resize(cur + 1);
        pages.push_back(url);
        cur++;
    }

    string back(int k) {
        cur = max(0, cur - k);
        return pages[cur];
    }

    string forward(int k) {
        cur = min((int)pages.size() - 1, cur + k);
        return pages[cur];
    }
};
```

`back` and `forward` take $O(1)$ time. `visit` deletes the forgotten pages, but every page is created once and deleted at most once, so over many operations the cost per operation is still $O(1)$ on average (this kind of counting is called **amortised** cost). The space is $O(\text{pages})$. This is exactly the problem _Browser History_.

## 1.4 Check yourself

1. In `["add 5", "get", "add 2", "get"]`, which operations produce an answer?
2. Why is `x in some_list` slow when the list is long, and what replaces it?
3. In the browser history, what does `visit` do with the pages ahead of the finger?
4. Why is `forward 100` safe even if only two pages exist ahead?

# Chapter 2. Queues and time windows

## 2.1 First in, first out

A **queue** is a line of items where new items join at the back and items leave from the front, like people waiting at a counter. The first one to arrive is the first to leave. Python's `deque` and C++'s `deque` give you this with $O(1)$ work at both ends. (A plain Python list is slow at the front, because removing the first item shifts all the others.)

A very common use is to keep only the recent part of a growing sequence. Say event times arrive in increasing order, and we want to drop all times at or before some limit.

```python
from collections import deque


def drop_old(times, limit):
    q = deque(times)
    while q and q[0] <= limit:
        q.popleft()
    return list(q)


assert drop_old([1, 2, 5, 9], 4) == [5, 9]
assert drop_old([1, 2], 10) == []
assert drop_old([7, 8], 3) == [7, 8]
```

```cpp
vector<int> drop_old(const vector<int>& times, int limit) {
    deque<int> q(times.begin(), times.end());
    while (!q.empty() && q.front() <= limit) q.pop_front();
    return vector<int>(q.begin(), q.end());
}
```

The loop only ever looks at the front, because the times are sorted: if the front is recent enough, everything behind it is too.

## 2.2 Counting hits in a sliding window

A web page counts hits. `hit t` records a hit at second $t$. `count t` asks how many hits happened in the last 300 seconds, that is at seconds $t-299$ up to $t$. The seconds never go down from one operation to the next.

Keep a queue of hit times. A hit goes to the back. For a count, first remove from the front every time that is at most $t - 300$ (those are too old), then the answer is the size of the queue. Because time only moves forward, a time that is too old now will be too old for ever, so we never need it again.

```python
from collections import deque


class HitCounter:
    def __init__(self):
        self.window = deque()

    def hit(self, t):
        self.window.append(t)

    def count(self, t):
        while self.window and self.window[0] <= t - 300:
            self.window.popleft()
        return len(self.window)


c = HitCounter()
c.hit(1)
c.hit(2)
c.hit(3)
assert c.count(4) == 3
c.hit(300)
assert c.count(300) == 4
assert c.count(301) == 3
```

```cpp
struct HitCounter {
    deque<int> window;

    void hit(int t) {
        window.push_back(t);
    }

    int count(int t) {
        while (!window.empty() && window.front() <= t - 300) window.pop_front();
        return (int)window.size();
    }
};
```

Let's trace the last lines. After the hits at 1, 2, 3 and 300, `count(300)` removes times $\le 0$: nothing, so the answer is 4. Then `count(301)` removes times $\le 1$: the hit at second 1 goes away, and 3 remain (2, 3 and 300). Each hit enters the queue once and leaves once, so $n$ operations cost $O(n)$ in total. The space is $O(\text{hits in the window})$.

This is exactly the problem _Hit Counter_.

## 2.3 Buckets for a huge number of hits

Suppose a million hits arrive in the same few seconds. The queue then holds a million numbers, though we only need counts per second. The fix is to keep **buckets**, one little counter per second of the window. Since the window is 300 seconds long, we need only 300 buckets, and second $t$ goes to bucket $t \bmod 300$ (the remainder after dividing by 300). Two seconds that share a bucket are exactly 300 apart, so the old one is outside the window anyway. Each bucket remembers which second it currently stores. If a new hit finds a different second there, the bucket restarts from zero.

```python
class HitCounterBuckets:
    def __init__(self):
        self.stamp = [0] * 300
        self.hits = [0] * 300

    def hit(self, t):
        i = t % 300
        if self.stamp[i] != t:
            self.stamp[i] = t
            self.hits[i] = 0
        self.hits[i] += 1

    def count(self, t):
        total = 0
        for i in range(300):
            if t - self.stamp[i] < 300:
                total += self.hits[i]
        return total


b = HitCounterBuckets()
b.hit(1)
b.hit(2)
b.hit(3)
assert b.count(4) == 3
b.hit(300)
assert b.count(300) == 4
assert b.count(301) == 3
```

```cpp
struct HitCounterBuckets {
    int stamp[300] = {};
    int hits[300] = {};

    void hit(int t) {
        int i = t % 300;
        if (stamp[i] != t) {
            stamp[i] = t;
            hits[i] = 0;
        }
        hits[i]++;
    }

    int count(int t) {
        int total = 0;
        for (int i = 0; i < 300; i++) {
            if (t - stamp[i] < 300) total += hits[i];
        }
        return total;
    }
};
```

Now `hit` is $O(1)$, `count` costs a fixed 300 steps (so $O(1)$), and the memory is fixed at 600 numbers no matter how many hits arrive. The queue version is simpler; the bucket version is the one to use when the number of hits is enormous. A bucket that was never used has stamp 0 and 0 hits, so it adds nothing.

## 2.4 Check yourself

1. Why can we safely discard an old hit for ever?
2. In the queue version, how many times can one hit be pushed and popped?
3. In the bucket version, why do seconds $t$ and $t+300$ share a bucket without causing trouble?
4. When would you prefer buckets over the queue?

# Chapter 3. Remembering the past with binary search

## 3.1 Last position at most x

Several designs store a history in a sorted list and later ask "what was true at time $x$?" The answer is the last entry whose time is at most $x$. In a sorted list we find it by **binary search**: look at the middle, and throw away the half that cannot contain the answer. This costs $O(\log n)$ instead of $O(n)$. Here the function returns the index of the last element that is $\le x$, or $-1$ if there is none.

```python
def last_at_most(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1


assert last_at_most([10, 20, 30], 25) == 1
assert last_at_most([10, 20, 30], 5) == -1
assert last_at_most([10, 20, 30], 30) == 2
```

```cpp
int last_at_most(const vector<int>& a, int x) {
    int lo = 0, hi = (int)a.size();
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (a[mid] <= x) lo = mid + 1;
        else hi = mid;
    }
    return lo - 1;
}
```

The loop keeps the invariant that everything before `lo` is $\le x$ and everything from `hi` on is $> x$. When they meet, `lo` is the first position that is $> x$, so `lo - 1` is the last one that is $\le x$. (In Python the library function `bisect_right` and in C++ `upper_bound` do the same job; writing it ourselves shows what happens.)

## 3.2 A store with timestamps

Each key keeps a list of values stored at increasing times. `set key value t` appends to the list of that key. `get key t` returns the value stored at the latest time that is at most $t$, or an empty string if there is none. Since the `set` times only increase, each key's list of times is sorted without any extra work, and a `get` is one binary search on that key's list.

```python
class TimeMap:
    def __init__(self):
        self.times = {}
        self.values = {}

    def set(self, key, value, t):
        self.times.setdefault(key, []).append(t)
        self.values.setdefault(key, []).append(value)

    def get(self, key, t):
        i = last_at_most(self.times.get(key, []), t)
        return self.values[key][i] if i >= 0 else ""


m = TimeMap()
m.set("love", "high", 10)
assert m.get("love", 10) == "high"
assert m.get("love", 15) == "high"
m.set("love", "low", 20)
assert m.get("love", 15) == "high"
assert m.get("love", 25) == "low"
assert m.get("love", 5) == ""
```

```cpp
struct TimeMap {
    unordered_map<string, vector<int>> times;
    unordered_map<string, vector<string>> values;

    void set(const string& key, const string& value, int t) {
        times[key].push_back(t);
        values[key].push_back(value);
    }

    string get(const string& key, int t) {
        auto it = times.find(key);
        if (it == times.end()) return "";
        int i = last_at_most(it->second, t);
        return i >= 0 ? values[key][i] : "";
    }
};
```

(The Python block uses `last_at_most` from the previous section; in C++ it is the function from the previous section too.) A `set` costs $O(1)$, a `get` costs $O(\log m)$ where $m$ is the number of values of that key. The space is $O(\text{number of sets})$.

This is exactly the problem _Time-Based Key-Value Store_.

## 3.3 Snapshots without copying

An array of `length` zeros supports `set i v`, `snap` (freeze the whole array and return the next snapshot id: 0, 1, 2, ...) and `get i id` (the value at position $i$ when snapshot $id$ was taken). The wasteful way is to copy the entire array at every `snap`. That would cost $O(\text{length})$ per snapshot even if only one cell changed.

The clever way is to store only the **changes**. For each position keep two lists: the snapshot numbers in which the cell was changed, and the values. A `set` writes under the current snapshot number (if the cell was already changed in this same snapshot, we just overwrite the last value). A `snap` only increases a counter. To read position $i$ at snapshot $id$ we want the last change made in a snapshot that is $\le id$: that is again `last_at_most` on the change list of $i$. If no such change exists, the cell was still its original 0.

```
position 0:  changed in snapshot 0 (value 5), snapshot 1 (value 9)
get 0 at snapshot 0 -> 5    get 0 at snapshot 2 -> 9    get 3 anywhere -> 0
```

```python
class SnapshotArray:
    def __init__(self, length):
        self.ids = [[] for _ in range(length)]
        self.vals = [[] for _ in range(length)]
        self.snap_id = 0

    def set(self, i, v):
        if self.ids[i] and self.ids[i][-1] == self.snap_id:
            self.vals[i][-1] = v
        else:
            self.ids[i].append(self.snap_id)
            self.vals[i].append(v)

    def snap(self):
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, i, snap_id):
        k = last_at_most(self.ids[i], snap_id)
        return self.vals[i][k] if k >= 0 else 0


s = SnapshotArray(3)
s.set(0, 5)
assert s.snap() == 0
s.set(0, 6)
assert s.get(0, 0) == 5
assert s.snap() == 1
assert s.get(0, 1) == 6
assert s.get(2, 1) == 0
```

```cpp
struct SnapshotArray {
    vector<vector<int>> ids, vals;
    int snap_id = 0;

    SnapshotArray(int length) : ids(length), vals(length) {}

    void set(int i, int v) {
        if (!ids[i].empty() && ids[i].back() == snap_id) {
            vals[i].back() = v;
        } else {
            ids[i].push_back(snap_id);
            vals[i].push_back(v);
        }
    }

    int snap() {
        snap_id++;
        return snap_id - 1;
    }

    int get(int i, int id) {
        int k = last_at_most(ids[i], id);
        return k >= 0 ? vals[i][k] : 0;
    }
};
```

`set` and `snap` take $O(1)$, `get` takes $O(\log c)$ where $c$ is the number of changes at that position, and the space is $O(\text{length} + \text{number of sets})$. This is exactly the problem _Snapshot Array_.

## 3.4 Check yourself

1. What does `last_at_most([4, 8, 8, 12], 8)` return?
2. Why can a `get` in the time store use binary search?
3. Why does `snap` not need to copy anything?
4. What does `get` return for a position that was never set?

# Chapter 4. The LRU cache

## 4.1 What a cache is

A **cache** is a small, fast memory that keeps recently needed results so that we do not have to compute or fetch them again. Because it is small, it has a **capacity**: when it is full and a new item arrives, something must be thrown out. A **least recently used (LRU)** cache throws out the item that has gone unused for the longest time. The bet is that what you used lately you will probably use soon again.

Both `get k` and `put k v` count as a "use" of the key. With capacity 2, think of the cache as a row ordered from most recent to least recent.

```
put 1, put 2      row: 2 1
get 1             row: 1 2      (1 was just used)
put 3 (full)      remove the last, 2:   row: 3 1
```

To make this fast we need three things at once: find a key quickly, move a key to the front quickly, and remove the last one quickly. A list in an array fails at moving. A dictionary alone has no notion of order for the "who is oldest" question. So we combine two structures.

## 4.2 A doubly linked list

A **linked list** is a chain of small boxes called nodes. Each node holds a value and a pointer (a reference) to the next node. In a **doubly** linked list each node also points to the previous one. The big gift is this: if you already hold a node, you can cut it out of the chain, or insert a new one next to it, in $O(1)$ time, because you only change a few pointers and never shift anything.

To avoid special cases at the ends, we add two dummy nodes called **sentinels**: `head` at the front and `tail` at the back. Real nodes always sit between them, so every real node has a neighbour on both sides. We keep the most recent node right after `head`, and the least recent right before `tail`.

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class DList:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def last(self):
        return self.tail.prev

    def keys(self):
        out = []
        cur = self.head.next
        while cur is not self.tail:
            out.append(cur.key)
            cur = cur.next
        return out


d = DList()
nodes = {k: Node(k, k * 10) for k in (1, 2, 3)}
for k in (1, 2, 3):
    d.add_front(nodes[k])
assert d.keys() == [3, 2, 1]
d.remove(nodes[2])
assert d.keys() == [3, 1]
assert d.last().key == 1
```

```cpp
struct Node {
    int key = 0, val = 0;
    Node* prev = nullptr;
    Node* next = nullptr;
};

struct DList {
    Node head, tail;

    DList() {
        head.next = &tail;
        tail.prev = &head;
    }

    void add_front(Node* node) {
        node->prev = &head;
        node->next = head.next;
        head.next->prev = node;
        head.next = node;
    }

    void remove(Node* node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
    }

    Node* last() {
        return tail.prev;
    }

    vector<int> keys() {
        vector<int> out;
        for (Node* cur = head.next; cur != &tail; cur = cur->next) out.push_back(cur->key);
        return out;
    }
};
```

Look at `add_front`: four pointer changes, in an order that does not lose anything. We first set the new node's two pointers, then the neighbours' pointers. The order matters, because `head.next` must still be read before it is overwritten.

## 4.3 Dictionary plus list

Now the combination. A dictionary `table` maps each key to its node in the list. The list holds the use order. Then:

- `get k`: find the node through `table`; move it to the front (remove, then add_front); return its value.
- `put k v`: if the key exists, update the value and move the node to the front. Otherwise, if the cache is full, take the last node of the list, remove it, and delete its key from `table` (that is why a node stores its own key!). Then create the new node, add it at the front and record it in `table`.

```python
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.table = {}
        self.order = DList()

    def get(self, key):
        if key not in self.table:
            return -1
        node = self.table[key]
        self.order.remove(node)
        self.order.add_front(node)
        return node.val

    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.table:
            node = self.table[key]
            node.val = value
            self.order.remove(node)
            self.order.add_front(node)
            return
        if len(self.table) == self.cap:
            old = self.order.last()
            self.order.remove(old)
            del self.table[old.key]
        node = Node(key, value)
        self.table[key] = node
        self.order.add_front(node)


c = LRUCache(2)
c.put(1, 1)
c.put(2, 2)
assert c.get(1) == 1
c.put(3, 3)
assert c.get(2) == -1
c.put(4, 4)
assert c.get(1) == -1
assert c.get(3) == 3
assert c.get(4) == 4
```

```cpp
struct LRUCache {
    int cap;
    unordered_map<int, Node*> table;
    DList order;

    LRUCache(int capacity) : cap(capacity) {}

    ~LRUCache() {
        for (auto& kv : table) delete kv.second;
    }

    int get(int key) {
        auto it = table.find(key);
        if (it == table.end()) return -1;
        Node* node = it->second;
        order.remove(node);
        order.add_front(node);
        return node->val;
    }

    void put(int key, int value) {
        if (cap == 0) return;
        auto it = table.find(key);
        if (it != table.end()) {
            Node* node = it->second;
            node->val = value;
            order.remove(node);
            order.add_front(node);
            return;
        }
        if ((int)table.size() == cap) {
            Node* old = order.last();
            order.remove(old);
            table.erase(old->key);
            delete old;
        }
        Node* node = new Node();
        node->key = key;
        node->val = value;
        table[key] = node;
        order.add_front(node);
    }
};
```

Every step is a dictionary lookup or a few pointer changes, so each operation costs $O(1)$ on average, and the space is $O(\text{capacity})$. A capacity of 0 stores nothing, which we handle with the first line of `put`. This is exactly the problem _LRU Cache_.

## 4.4 Using the library for order

Both languages have a ready-made "dictionary that remembers order". Python's `OrderedDict` can move a key to the end in $O(1)$ (`move_to_end`) and remove from the front (`popitem(last=False)`). In C++ the usual trick is a `std::list` of pairs plus a map from key to the list iterator; `splice` moves an element to the front in $O(1)$ without invalidating iterators. Use these in a contest to save time, but know the version above, because it is what they do inside.

```python
from collections import OrderedDict


class LRUShort:
    def __init__(self, capacity):
        self.cap = capacity
        self.data = OrderedDict()

    def get(self, key):
        if key not in self.data:
            return -1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.data:
            self.data.move_to_end(key)
        elif len(self.data) == self.cap:
            self.data.popitem(last=False)
        self.data[key] = value


c = LRUShort(2)
c.put(1, 1)
c.put(2, 2)
assert c.get(1) == 1
c.put(3, 3)
assert c.get(2) == -1
```

```cpp
struct LRUShort {
    int cap;
    list<pair<int, int>> items;
    unordered_map<int, list<pair<int, int>>::iterator> pos;

    LRUShort(int capacity) : cap(capacity) {}

    int get(int key) {
        auto it = pos.find(key);
        if (it == pos.end()) return -1;
        items.splice(items.begin(), items, it->second);
        return it->second->second;
    }

    void put(int key, int value) {
        if (cap == 0) return;
        auto it = pos.find(key);
        if (it != pos.end()) {
            it->second->second = value;
            items.splice(items.begin(), items, it->second);
            return;
        }
        if ((int)items.size() == cap) {
            pos.erase(items.back().first);
            items.pop_back();
        }
        items.emplace_front(key, value);
        pos[key] = items.begin();
    }
};
```

In the Python version the front of the ordered dictionary is the least recent; in the C++ version the front of the list is the most recent. The idea is the same.

## 4.5 Check yourself

1. Which two operations of the cache count as a use of a key?
2. Why does each node store its own key?
3. What do the sentinel nodes save us from?
4. What is the time of one `get` or `put`?

# Chapter 5. The LFU cache

## 5.1 Counting uses instead of time

A **least frequently used (LFU)** cache evicts the key that has been used the fewest times. Every `get` of a stored key and every `put` counts as one use, and a new key starts with 1 use. If several keys share the lowest count, we evict the one that was used **least recently** among them. So there are two rules, and both matter: lowest count first, and the oldest use as the tie-break.

A natural first idea is to keep all keys sorted by (count, last use time) and always remove the smallest. That works, but each use changes a count and so moves the key within the sorted order, which costs $O(\log n)$ with a balanced tree. We can do better: counts only ever go up by exactly 1, which makes a simpler structure possible.

## 5.2 One bucket per count

Make a group, called a **bucket**, for every count value. Bucket $c$ holds the keys that have been used exactly $c$ times, in order from the least recently used to the most recently used. When a key is used, it leaves bucket $c$ and joins the **back** of bucket $c+1$. So inside a bucket, the front is always the oldest, which is exactly the tie-break we need.

To know where to evict, we also remember `low`, the smallest count that has a non-empty bucket. Eviction takes the front key of bucket `low`.

```
capacity 2:   put 1, put 2     bucket1: [1, 2]
get 1                          bucket1: [2]       bucket2: [1]      low = 1
put 3 (full): evict front of bucket1, key 2
                               bucket1: [3]       bucket2: [1]      low = 1
```

Why is it enough to update `low` so simply? Look at the two things that can change it. When a key moves from bucket $c$ to $c+1$ and bucket $c$ becomes empty, and $c$ was the lowest, then the new lowest count is $c+1$ (that bucket now has the key). And when a brand-new key arrives, it has count 1, which is the smallest possible, so `low` becomes 1. Nothing else can lower or raise it.

Here are the buckets in code. Each bucket is an ordered dictionary (keys in insertion order, removable by key in $O(1)$). In C++ it is a `list` plus a stored iterator for every key.

```python
from collections import OrderedDict


class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.val = {}
        self.cnt = {}
        self.bucket = {}
        self.low = 0

    def _touch(self, key):
        c = self.cnt[key]
        del self.bucket[c][key]
        if not self.bucket[c]:
            del self.bucket[c]
            if self.low == c:
                self.low = c + 1
        self.cnt[key] = c + 1
        self.bucket.setdefault(c + 1, OrderedDict())[key] = None

    def get(self, key):
        if key not in self.val:
            return -1
        self._touch(key)
        return self.val[key]

    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.val:
            self.val[key] = value
            self._touch(key)
            return
        if len(self.val) == self.cap:
            old, _ = self.bucket[self.low].popitem(last=False)
            if not self.bucket[self.low]:
                del self.bucket[self.low]
            del self.val[old]
            del self.cnt[old]
        self.val[key] = value
        self.cnt[key] = 1
        self.bucket.setdefault(1, OrderedDict())[key] = None
        self.low = 1


c = LFUCache(2)
c.put(1, 1)
c.put(2, 2)
assert c.get(1) == 1
c.put(3, 3)
assert c.get(2) == -1
assert c.get(3) == 3
c.put(4, 4)
assert c.get(1) == -1
assert c.get(3) == 3
assert c.get(4) == 4
```

```cpp
struct LFUCache {
    int cap, low = 0;
    unordered_map<int, int> val, cnt;
    unordered_map<int, list<int>> bucket;
    unordered_map<int, list<int>::iterator> where;

    LFUCache(int capacity) : cap(capacity) {}

    void touch(int key) {
        int c = cnt[key];
        bucket[c].erase(where[key]);
        if (bucket[c].empty()) {
            bucket.erase(c);
            if (low == c) low = c + 1;
        }
        cnt[key] = c + 1;
        bucket[c + 1].push_back(key);
        where[key] = prev(bucket[c + 1].end());
    }

    int get(int key) {
        if (!val.count(key)) return -1;
        touch(key);
        return val[key];
    }

    void put(int key, int value) {
        if (cap == 0) return;
        if (val.count(key)) {
            val[key] = value;
            touch(key);
            return;
        }
        if ((int)val.size() == cap) {
            int old = bucket[low].front();
            bucket[low].pop_front();
            if (bucket[low].empty()) bucket.erase(low);
            val.erase(old);
            cnt.erase(old);
            where.erase(old);
        }
        val[key] = value;
        cnt[key] = 1;
        bucket[1].push_back(key);
        where[key] = prev(bucket[1].end());
        low = 1;
    }
};
```

Let's follow the last part of the example. After `put 3` the cache holds key 1 (count 2) and key 3 (count 1). `get 3` makes key 3 count 2 and bucket 1 empty, so `low` becomes 2. Now bucket 2 is `[1, 3]`: key 1 was used earlier. `put 4` is a new key into a full cache, so we take the front of bucket 2, key 1, and evict it. That is why `get 1` then answers $-1$.

Every operation does a constant number of dictionary and list steps, so it costs $O(1)$ on average. The space is $O(\text{capacity})$. This is exactly the problem _LFU Cache_.

## 5.3 A common slip

When you evict, do it **before** you insert the new key, and set `low = 1` after inserting. If you evict after inserting, the new key (count 1) could be the one you throw away. Also remember that a `put` on an existing key is a use and may change the value: update the value, then call the same touch step.

## 5.4 Check yourself

1. What is the tie-break rule when two keys have the same count?
2. Why does the front of each bucket hold the key we want to evict?
3. When does `low` change?
4. Does `put` on an existing key count as a use?

# Chapter 6. Fenwick trees

## 6.1 Prefix sums and their weakness

Given a list `nums`, suppose we want the sum of any stretch `nums[l..r]` quickly. The classic answer is **prefix sums**: let `prefix[i]` be the sum of the first $i$ numbers. Then the sum of `nums[l..r]` is `prefix[r+1] - prefix[l]`. Building is $O(n)$, and each query costs $O(1)$.

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
assert range_sum(p, 0, 4) == 14
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

The weakness: if one number changes, every prefix after it changes, so an update costs $O(n)$. When the operations are a mix of "change a value" and "ask a sum", we need both to be fast, around $O(\log n)$. That is what a Fenwick tree does.

## 6.2 Blocks of power-of-two size

A **Fenwick tree** (also called a **binary indexed tree**) stores, instead of prefix sums, the sums of small blocks. It uses positions $1, 2, \dots, n$. Cell $i$ stores the sum of a block that ends at $i$, and the block length is the value of the lowest set bit of $i$ (the lowest 1 in the binary form of $i$). For example $6 = 110_2$ has lowest set bit $10_2 = 2$, so cell 6 covers 2 numbers: positions 5 and 6. The number $8 = 1000_2$ has lowest set bit 8, so cell 8 covers positions 1 to 8. A neat trick finds that value: `i & -i`.

```python
def lowbit(i):
    return i & -i


def block(i):
    return (i - lowbit(i) + 1, i)


assert lowbit(6) == 2
assert lowbit(8) == 8
assert block(6) == (5, 6)
assert block(7) == (7, 7)
assert block(8) == (1, 8)
```

```cpp
int lowbit(int i) {
    return i & -i;
}

pair<int, int> block(int i) {
    return {i - lowbit(i) + 1, i};
}
```

For $n = 8$ the cells cover:

```
cell:   1    2     3    4       5    6     7    8
covers: [1]  [1,2] [3]  [1..4]  [5]  [5,6] [7]  [1..8]
```

To find the sum of the first $i$ numbers, we jump along blocks: take cell $i$, then go to $i - \text{lowbit}(i)$ (the position just before that block), take that cell, and so on until we reach 0. For $i = 7$: cell 7 covers [7], cell 6 covers [5,6], cell 4 covers [1..4]. Together they cover $1..7$ with only three cells. The number of jumps is at most the number of 1 bits in $i$, so at most $\log_2 n$.

## 6.3 Query, update and set

To **update** (add a value $d$ to position $i$) we must fix every cell whose block contains $i$. Those are found by going upward: cell $i$, then $i + \text{lowbit}(i)$, then again, until we pass $n$. This also takes at most about $\log_2 n$ steps. The two loops mirror each other: query goes down by removing the lowest bit, update goes up by adding it.

To **set** a position to a new value $v$, we remember the current values and add the difference $v - \text{old}$. The class below takes positions starting at 0, as the problems do, and shifts them by one inside.

```python
class Fenwick:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (self.n + 1)
        self.values = [0] * self.n
        for i, x in enumerate(nums):
            self.set(i, x)

    def add(self, i, delta):
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix(self, count):
        total = 0
        while count > 0:
            total += self.tree[count]
            count -= count & -count
        return total

    def set(self, i, v):
        self.add(i, v - self.values[i])
        self.values[i] = v

    def range_sum(self, l, r):
        return self.prefix(r + 1) - self.prefix(l)


f = Fenwick([3, 1, 4, 1, 5, 9, 2, 6])
assert f.prefix(7) == 25
assert f.range_sum(2, 4) == 10
f.set(3, 10)
assert f.range_sum(2, 4) == 19
assert f.prefix(8) == 40
```

```cpp
struct Fenwick {
    int n;
    vector<long long> tree, values;

    Fenwick(const vector<int>& nums) : n(nums.size()), tree(nums.size() + 1, 0), values(nums.size(), 0) {
        for (int i = 0; i < n; i++) set(i, nums[i]);
    }

    void add(int i, long long delta) {
        for (i++; i <= n; i += i & -i) tree[i] += delta;
    }

    long long prefix(int count) {
        long long total = 0;
        for (; count > 0; count -= count & -count) total += tree[count];
        return total;
    }

    void set(int i, long long v) {
        add(i, v - values[i]);
        values[i] = v;
    }

    long long range_sum(int l, int r) {
        return prefix(r + 1) - prefix(l);
    }
};
```

Let's check the example by hand. With `[3,1,4,1,5,9,2,6]`, the cells are $t_1 = 3$, $t_2 = 4$, $t_3 = 4$, $t_4 = 9$, $t_5 = 5$, $t_6 = 14$, $t_7 = 2$, $t_8 = 31$. Then `prefix(7)` $= t_7 + t_6 + t_4 = 2 + 14 + 9 = 25$. Setting position 3 (the second 1) to 10 adds 9 to the cells 4 and 8, so the sum of positions 2 to 4 grows from 10 to 19.

Building by inserting every value costs $O(n \log n)$, each query and update costs $O(\log n)$, and the space is $O(n)$. This is exactly the problem _Fenwick Tree (Prefix Sums With Updates)_.

## 6.4 Range add with a difference array

Now the reverse problem. We start with $n$ zeros. `add l r v` adds $v$ to every number in $l..r$, and `get i` asks for the current value at position $i$. Adding to every number is slow when ranges are long.

Think about the **difference array** $d$: $d[i]$ is the value at $i$ minus the value at $i-1$ (with $d[0]$ being the first value). The value at $i$ is the sum $d[0] + d[1] + \dots + d[i]$, a prefix sum. Adding $v$ to the whole range $l..r$ changes the differences in only two places: $d[l]$ goes up by $v$ (the range starts here), and $d[r+1]$ goes down by $v$ (the range ends just before it). So we keep a Fenwick tree of differences. A range add is two point updates, and a point query is one prefix sum.

```python
class RangeAddPointQuery:
    def __init__(self, n):
        self.n = n
        self.diff = Fenwick([0] * n)

    def add(self, l, r, v):
        self.diff.add(l, v)
        if r + 1 < self.n:
            self.diff.add(r + 1, -v)

    def get(self, i):
        return self.diff.prefix(i + 1)


r = RangeAddPointQuery(5)
r.add(1, 3, 10)
assert r.get(2) == 10
assert r.get(4) == 0
r.add(0, 4, -1)
assert r.get(0) == -1
assert r.get(3) == 9
```

```cpp
struct RangeAddPointQuery {
    int n;
    Fenwick diff;

    RangeAddPointQuery(int n_) : n(n_), diff(vector<int>(n_, 0)) {}

    void add(int l, int r, long long v) {
        diff.add(l, v);
        if (r + 1 < n) diff.add(r + 1, -v);
    }

    long long get(int i) {
        return diff.prefix(i + 1);
    }
};
```

(The C++ block uses the `Fenwick` struct from the previous section.) Both operations cost $O(\log n)$ and the space is $O(n)$. This is exactly the problem _Range Add, Point Query_. A word of warning for later: if you need range add **and** range sum, a single Fenwick tree is not enough; people use two of them, or the lazy segment tree of the next chapter.

## 6.5 Check yourself

1. Why is a plain prefix-sum array bad when values change?
2. What does `i & -i` compute, and what block size does it give?
3. Which cells does an update of position 3 (1-based) touch when $n = 8$?
4. In the range-add trick, why is a point query a prefix sum of the differences?

# Chapter 7. Segment trees

## 7.1 When a Fenwick tree is not enough

A Fenwick tree needs to subtract: sum of $l..r$ is a prefix minus a prefix. But the **minimum** of a range cannot be obtained by "subtracting" two prefix minima. We need a structure that can answer an operation like minimum over _any_ stretch directly. That is the **segment tree**.

The idea is to split the list into halves, again and again, and store the answer for every piece. The whole list is the root. Its two halves are the children. Each half splits again until a piece has one element (a leaf).

```
nums = [5, 2, 8, 1]

              [0..3] min 1
             /            \
       [0..1] min 2     [2..3] min 1
        /      \          /      \
   [0] 5     [1] 2     [2] 8    [3] 1
```

Any range is then the union of a few of these pieces, at most about $2\log_2 n$ of them, so combining their answers is fast.

## 7.2 The array layout

We store the tree in an array. A neat layout for point updates: put the $n$ leaves at positions $n, n+1, \dots, 2n-1$, and the parent of node $i$ is $i/2$ (rounded down), with children $2i$ and $2i+1$. Node 1 is the root. To build, fill the leaves, then for $i$ from $n-1$ down to 1 set the node to the minimum of its two children.

```
index:   1  2  3  4  5  6  7
value:   1  2  1  5  2  8  1      leaves are 4..7
```

To **update** position $p$, change leaf $p+n$ and then walk up, recomputing each parent from its two children. That is $O(\log n)$ steps.

To **query** the range $l..r$ we use a half-open range `[lo, hi)` on leaf positions. While `lo < hi`: if `lo` is a right child (odd), its piece is fully inside the range, so take it and step `lo` one to the right; if `hi` is odd, step `hi` one to the left and take that node. Then move both up to their parents. In this way the loop collects exactly the big pieces that exactly cover the range.

```python
class MinSegTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.inf = float("inf")
        self.tree = [self.inf] * self.n + list(nums)
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, p, v):
        i = p + self.n
        self.tree[i] = v
        i //= 2
        while i >= 1:
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
            i //= 2

    def query(self, l, r):
        lo, hi = l + self.n, r + self.n + 1
        best = self.inf
        while lo < hi:
            if lo & 1:
                best = min(best, self.tree[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                best = min(best, self.tree[hi])
            lo //= 2
            hi //= 2
        return best


t = MinSegTree([5, 2, 8, 1])
assert t.query(0, 3) == 1
assert t.query(1, 2) == 2
t.update(3, 9)
assert t.query(0, 3) == 2
assert t.query(2, 3) == 8
```

```cpp
struct MinSegTree {
    int n;
    vector<int> tree;

    MinSegTree(const vector<int>& nums) : n(nums.size()), tree(2 * nums.size(), INT_MAX) {
        for (int i = 0; i < n; i++) tree[n + i] = nums[i];
        for (int i = n - 1; i >= 1; i--) tree[i] = min(tree[2 * i], tree[2 * i + 1]);
    }

    void update(int p, int v) {
        int i = p + n;
        tree[i] = v;
        for (i /= 2; i >= 1; i /= 2) tree[i] = min(tree[2 * i], tree[2 * i + 1]);
    }

    int query(int l, int r) {
        int lo = l + n, hi = r + n + 1, best = INT_MAX;
        while (lo < hi) {
            if (lo & 1) best = min(best, tree[lo++]);
            if (hi & 1) best = min(best, tree[--hi]);
            lo /= 2;
            hi /= 2;
        }
        return best;
    }
};
```

Let's trace `query(1, 2)` on `[5, 2, 8, 1]` ($n = 4$, leaves at 4 to 7 hold 5, 2, 8, 1). We start with `lo = 5`, `hi = 7`. `lo` is odd, so we take `tree[5] = 2` and `lo` becomes 6. `hi` is odd, so `hi` becomes 6 and we take `tree[6] = 8`. The best is 2. Now `lo = 3`, `hi = 3`, and the loop stops. The answer is 2.

Building costs $O(n)$, each update and each query costs $O(\log n)$, and the space is $O(n)$. This is exactly the problem _Segment Tree (Range Minimum With Updates)_. The same code works for sums, maximums or greatest common divisors by changing `min` and the "empty" value.

## 7.3 The recursive view

The array trick above is short, but it cannot do range updates. For those we use the recursive version, which follows the picture of halves directly. A node covers a range `[l, r]`. We number the root 1 and use children $2k$ and $2k+1$. A query with range `[ql, qr]` asks each node one of three things:

- the node's range lies completely **outside** the query: return a neutral answer (for minimum, infinity);
- the node's range lies completely **inside** the query: return the stored answer;
- otherwise they **partly overlap**: ask both children and combine.

Only the partly-overlapping nodes recurse, and at each level there are at most two of them, so the total work is $O(\log n)$.

```python
class RecMinTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.mn = [0] * (4 * self.n)
        self._build(1, 0, self.n - 1, nums)

    def _build(self, node, l, r, nums):
        if l == r:
            self.mn[node] = nums[l]
            return
        m = (l + r) // 2
        self._build(2 * node, l, m, nums)
        self._build(2 * node + 1, m + 1, r, nums)
        self.mn[node] = min(self.mn[2 * node], self.mn[2 * node + 1])

    def _query(self, node, l, r, ql, qr):
        if qr < l or r < ql:
            return float("inf")
        if ql <= l and r <= qr:
            return self.mn[node]
        m = (l + r) // 2
        return min(self._query(2 * node, l, m, ql, qr),
                   self._query(2 * node + 1, m + 1, r, ql, qr))

    def query(self, ql, qr):
        return self._query(1, 0, self.n - 1, ql, qr)


t = RecMinTree([4, 7, 2, 9, 5])
assert t.query(0, 4) == 2
assert t.query(3, 4) == 5
assert t.query(0, 1) == 4
```

```cpp
struct RecMinTree {
    int n;
    vector<int> mn;

    RecMinTree(const vector<int>& nums) : n(nums.size()), mn(4 * nums.size(), 0) {
        build(1, 0, n - 1, nums);
    }

    void build(int node, int l, int r, const vector<int>& nums) {
        if (l == r) {
            mn[node] = nums[l];
            return;
        }
        int m = (l + r) / 2;
        build(2 * node, l, m, nums);
        build(2 * node + 1, m + 1, r, nums);
        mn[node] = min(mn[2 * node], mn[2 * node + 1]);
    }

    int query(int node, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return INT_MAX;
        if (ql <= l && r <= qr) return mn[node];
        int m = (l + r) / 2;
        return min(query(2 * node, l, m, ql, qr), query(2 * node + 1, m + 1, r, ql, qr));
    }

    int query(int ql, int qr) {
        return query(1, 0, n - 1, ql, qr);
    }
};
```

The array needs $4n$ cells because the recursive tree of an awkward size $n$ may be a bit deeper than the perfect shape; $4n$ is always enough.

## 7.4 Lazy updates for whole ranges

Now suppose we also want `add l r v`: add $v$ to every number in the range, while still answering range minimum quickly. Updating every leaf is slow. Here is the key insight: if a node's range is completely inside the update range, then **all** of its numbers go up by $v$, so its minimum also goes up by $v$. We can fix that node right now and leave a note, called a **lazy tag**, saying "my two children still owe this $v$". We do not touch the children at all.

Later, if a query or an update needs to go _down_ into the children of a node that has a note, we first **push the note down**: give it to both children (they update their minimum and their own note) and clear the note. This way work is only done when somebody actually looks.

For a range minimum with range add, applying a note of size $v$ to a node means: `mn[node] += v` and `lazy[node] += v`. Notes add up, which is fine because additions combine.

```python
class LazyMinTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.mn = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(1, 0, self.n - 1, nums)

    def _build(self, node, l, r, nums):
        if l == r:
            self.mn[node] = nums[l]
            return
        m = (l + r) // 2
        self._build(2 * node, l, m, nums)
        self._build(2 * node + 1, m + 1, r, nums)
        self.mn[node] = min(self.mn[2 * node], self.mn[2 * node + 1])

    def _apply(self, node, v):
        self.mn[node] += v
        self.lazy[node] += v

    def _push(self, node):
        if self.lazy[node] != 0:
            self._apply(2 * node, self.lazy[node])
            self._apply(2 * node + 1, self.lazy[node])
            self.lazy[node] = 0

    def _add(self, node, l, r, ql, qr, v):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            self._apply(node, v)
            return
        self._push(node)
        m = (l + r) // 2
        self._add(2 * node, l, m, ql, qr, v)
        self._add(2 * node + 1, m + 1, r, ql, qr, v)
        self.mn[node] = min(self.mn[2 * node], self.mn[2 * node + 1])

    def _query(self, node, l, r, ql, qr):
        if qr < l or r < ql:
            return float("inf")
        if ql <= l and r <= qr:
            return self.mn[node]
        self._push(node)
        m = (l + r) // 2
        return min(self._query(2 * node, l, m, ql, qr),
                   self._query(2 * node + 1, m + 1, r, ql, qr))

    def add(self, ql, qr, v):
        self._add(1, 0, self.n - 1, ql, qr, v)

    def query(self, ql, qr):
        return self._query(1, 0, self.n - 1, ql, qr)


t = LazyMinTree([4, 7, 2, 9, 5])
t.add(1, 3, 10)
assert t.query(0, 4) == 4
assert t.query(1, 2) == 12
t.add(0, 0, -10)
assert t.query(0, 4) == -6
assert t.query(3, 4) == 5
```

```cpp
struct LazyMinTree {
    int n;
    vector<long long> mn, lazy;

    LazyMinTree(const vector<int>& nums) : n(nums.size()), mn(4 * nums.size(), 0), lazy(4 * nums.size(), 0) {
        build(1, 0, n - 1, nums);
    }

    void build(int node, int l, int r, const vector<int>& nums) {
        if (l == r) {
            mn[node] = nums[l];
            return;
        }
        int m = (l + r) / 2;
        build(2 * node, l, m, nums);
        build(2 * node + 1, m + 1, r, nums);
        mn[node] = min(mn[2 * node], mn[2 * node + 1]);
    }

    void apply(int node, long long v) {
        mn[node] += v;
        lazy[node] += v;
    }

    void push(int node) {
        if (lazy[node] != 0) {
            apply(2 * node, lazy[node]);
            apply(2 * node + 1, lazy[node]);
            lazy[node] = 0;
        }
    }

    void add(int node, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) {
            apply(node, v);
            return;
        }
        push(node);
        int m = (l + r) / 2;
        add(2 * node, l, m, ql, qr, v);
        add(2 * node + 1, m + 1, r, ql, qr, v);
        mn[node] = min(mn[2 * node], mn[2 * node + 1]);
    }

    long long query(int node, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return LLONG_MAX;
        if (ql <= l && r <= qr) return mn[node];
        push(node);
        int m = (l + r) / 2;
        return min(query(2 * node, l, m, ql, qr), query(2 * node + 1, m + 1, r, ql, qr));
    }

    void add(int ql, int qr, long long v) {
        add(1, 0, n - 1, ql, qr, v);
    }

    long long query(int ql, int qr) {
        return query(1, 0, n - 1, ql, qr);
    }
};
```

Let's trace the example. The list is `[4, 7, 2, 9, 5]`, and `add(1, 3, 10)` makes it `[4, 17, 12, 19, 5]`. The minimum of everything is 4, and the minimum of positions 1 to 2 is 12. Then subtracting 10 from position 0 gives `[-6, 17, 12, 19, 5]`, whose minimum is $-6$.

After changing the children of a node, the parent always recomputes its own minimum from them (the last line of `_add`). Forgetting this line is the most common bug. Range add, point query, range min and range sum all cost $O(\log n)$ with this scheme, and the space is $O(n)$. The same pattern works for other lazy updates, like "assign this value to a whole range" (the note then means "overwrite") or "add to a range, ask for the sum" (a node with $k$ numbers gets $k \cdot v$ added to its sum).

## 7.5 Check yourself

1. Why can a Fenwick tree not answer range minimum?
2. In a recursive query, what are the three cases for a node?
3. What does a lazy tag on a node promise?
4. After pushing a note and updating the children, what must the node do last?

# Chapter 8. The sparse table

## 8.1 Static data and many questions

Sometimes the list never changes and we only ask range minimum queries, many of them. Then we can spend time once building a table and answer each query in $O(1)$. This is the **sparse table**.

The idea: precompute the minimum of every block whose length is a power of two. Let `table[k][i]` be the minimum of the $2^k$ numbers starting at position $i$. Level 0 is the list itself. A block of length $2^k$ is made of two halves of length $2^{k-1}$, so

$$\text{table}[k][i] = \min(\text{table}[k-1][i],\ \text{table}[k-1][i + 2^{k-1}])$$

For `[5, 2, 8, 1, 9]` the levels are:

```
level 0 (length 1): 5 2 8 1 9
level 1 (length 2): 2 2 1 1
level 2 (length 4): 1 1
```

Level $k$ has $n - 2^k + 1$ entries, so the whole table has about $n \log_2 n$ numbers, and building it costs $O(n \log n)$.

## 8.2 Two overlapping blocks

Take a query `[l, r]` with length $\text{len} = r - l + 1$. Let $k$ be the largest number with $2^k \le \text{len}$. Then two blocks of length $2^k$ cover the whole range: one starting at $l$, and one ending at $r$ (it starts at $r - 2^k + 1$). They overlap in the middle, and together they leave nothing out. Because "minimum" does not mind seeing a number twice (the minimum of a set stays the same if some of its members are counted twice), the answer is just the smaller of the two stored values.

For the query `[1, 4]` on the list above, $\text{len} = 4$ and $k = 2$, both blocks are the same one, and the answer is `table[2][1] = 1`. For `[0, 2]`: $\text{len} = 3$, $k = 1$; the blocks are positions 0 to 1 (min 2) and positions 1 to 2 (min 2), so the answer is 2.

To get $k$ quickly we use the position of the highest set bit of the length: in Python `len.bit_length() - 1`, in C++ `31 - __builtin_clz(len)`.

```python
class SparseTable:
    def __init__(self, nums):
        self.table = [list(nums)]
        k = 1
        while 2 ** k <= len(nums):
            prev = self.table[-1]
            half = 2 ** (k - 1)
            self.table.append([min(prev[i], prev[i + half]) for i in range(len(nums) - 2 ** k + 1)])
            k += 1

    def query(self, l, r):
        k = (r - l + 1).bit_length() - 1
        row = self.table[k]
        return min(row[l], row[r - 2 ** k + 1])


s = SparseTable([5, 2, 8, 1, 9])
assert s.table[1] == [2, 2, 1, 1]
assert s.table[2] == [1, 1]
assert s.query(1, 4) == 1
assert s.query(0, 2) == 2
assert s.query(2, 2) == 8
```

```cpp
struct SparseTable {
    vector<vector<int>> table;

    SparseTable(const vector<int>& nums) {
        int n = nums.size();
        table.push_back(nums);
        for (int k = 1; (1 << k) <= n; k++) {
            int half = 1 << (k - 1);
            vector<int> row(n - (1 << k) + 1);
            for (int i = 0; i < (int)row.size(); i++) {
                row[i] = min(table[k - 1][i], table[k - 1][i + half]);
            }
            table.push_back(row);
        }
    }

    int query(int l, int r) {
        int k = 31 - __builtin_clz(r - l + 1);
        return min(table[k][l], table[k][r - (1 << k) + 1]);
    }
};
```

Each query is $O(1)$, building is $O(n \log n)$ and the space is $O(n \log n)$. The overlap trick works for any operation that does not mind repeats, such as minimum, maximum and greatest common divisor, but **not** for sums, where counting a number twice would give a wrong answer. This is exactly the problem _Sparse Table (Static Range Minimum)_.

## 8.3 Which structure to choose

The four range tools fit different jobs. Here $n$ is the list length.

| Tool         | Build         | Query       | Update      | Best for                                   |
| ------------ | ------------- | ----------- | ----------- | ------------------------------------------ |
| Prefix sums  | $O(n)$        | $O(1)$      | $O(n)$      | sums, no changes                           |
| Fenwick tree | $O(n \log n)$ | $O(\log n)$ | $O(\log n)$ | sums with changes                          |
| Segment tree | $O(n)$        | $O(\log n)$ | $O(\log n)$ | any combinable query, changes, lazy ranges |
| Sparse table | $O(n \log n)$ | $O(1)$      | none        | minimum or maximum, no changes             |

If the data never changes and the operation is min or max, the sparse table wins. If there are changes, think Fenwick for sums and segment tree for everything else.

## 8.4 Check yourself

1. What does `table[2][1]` mean for a list of numbers?
2. Why do the two blocks in a query overlap, and why is that fine for minimum?
3. Why does the sparse table not work for sums?
4. How many levels does a list of 1000 numbers have?

# Chapter 9. Union-find

## 9.1 Groups that merge

Imagine $n$ items, each in its own group. Operations: `union a b` merges the groups of $a$ and $b$; `connected a b` asks whether two items are in the same group; `size a` asks how big the group of $a$ is. This data structure is called **union-find** or **disjoint set union** (disjoint means no item is in two groups).

The first idea is to give every item a label (its group name). `connected` compares labels. `union` relabels one whole group with the other label. It works, but a union scans the whole list.

```python
class LabelGroups:
    def __init__(self, n):
        self.label = list(range(n))

    def union(self, a, b):
        la, lb = self.label[a], self.label[b]
        for i in range(len(self.label)):
            if self.label[i] == lb:
                self.label[i] = la

    def connected(self, a, b):
        return self.label[a] == self.label[b]

    def size(self, a):
        return self.label.count(self.label[a])


g = LabelGroups(5)
g.union(0, 1)
g.union(1, 2)
assert g.connected(0, 2) is True
assert g.connected(0, 3) is False
assert g.size(2) == 3
```

```cpp
struct LabelGroups {
    vector<int> label;

    LabelGroups(int n) : label(n) {
        iota(label.begin(), label.end(), 0);
    }

    void unite(int a, int b) {
        int la = label[a], lb = label[b];
        for (int i = 0; i < (int)label.size(); i++) {
            if (label[i] == lb) label[i] = la;
        }
    }

    bool connected(int a, int b) {
        return label[a] == label[b];
    }

    int size(int a) {
        return count(label.begin(), label.end(), label[a]);
    }
};
```

(C++ calls the method `unite` since `union` is a reserved word.) Each union and each size costs $O(n)$, too slow for many operations.

## 9.2 A forest of parents

A better picture: each group is a tree. Every item stores a **parent**. The item at the top, whose parent is itself, is the **root**, and the root names the group. To find the group of an item, follow the parents up until you reach the root. Two items are connected exactly when their roots are the same. To merge two groups, hang one root under the other.

```
union(0,1), union(1,2):     2          find(0): 0 -> 1 -> 2   (root 2)
                            |
                            1
                            |
                            0
```

```python
class PlainUF:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        steps = 0
        while self.parent[x] != x:
            x = self.parent[x]
            steps += 1
        return x, steps

    def union(self, a, b):
        ra, _ = self.find(a)
        rb, _ = self.find(b)
        self.parent[ra] = rb


u = PlainUF(5)
for i in range(4):
    u.union(i, i + 1)
assert u.find(0) == (4, 4)
assert u.find(4) == (4, 0)
```

```cpp
struct PlainUF {
    vector<int> parent;

    PlainUF(int n) : parent(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        while (parent[x] != x) x = parent[x];
        return x;
    }

    void unite(int a, int b) {
        parent[find(a)] = find(b);
    }
};
```

This is faster on average, but we can build a long chain. Above, uniting $0,1$ then $1,2$ and so on hangs each old root under the next one, and `find(0)` walks 4 steps. With a million items a find could walk a million steps. We need to keep the trees short, and there are two simple tricks.

## 9.3 Union by size and path compression

**Union by size**: when merging two roots, hang the smaller tree under the larger one. A tree then only gets deeper when it is merged with one at least as big, so its size at least doubles each time its depth grows. This keeps the depth at most $\log_2 n$. As a bonus, the root can keep the size of the group, which answers the `size` operation for free.

**Path compression**: while walking up in `find`, make the items on the way point closer to the root (here: to their grandparent, a variant called path halving). The next find on the same path is shorter. Over many operations the trees become almost flat.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.sz = [1] * n
        self.groups = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.sz[ra] += self.sz[rb]
        self.groups -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def size(self, a):
        return self.sz[self.find(a)]


u = UnionFind(5)
u.union(0, 1)
u.union(1, 2)
assert u.connected(0, 2) is True
assert u.connected(0, 3) is False
assert u.size(2) == 3
assert u.groups == 3
assert u.union(0, 2) is False
```

```cpp
struct UnionFind {
    vector<int> parent, sz;
    int groups;

    UnionFind(int n) : parent(n), sz(n, 1), groups(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    bool unite(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;
        if (sz[ra] < sz[rb]) swap(ra, rb);
        parent[rb] = ra;
        sz[ra] += sz[rb];
        groups--;
        return true;
    }

    bool connected(int a, int b) {
        return find(a) == find(b);
    }

    int size(int a) {
        return sz[find(a)];
    }
};
```

Notice that the size is read only at the root (`sz[find(a)]`), since non-roots keep stale numbers. `union` returns whether it really merged two different groups, and `groups` counts how many groups are left; both are very handy in other problems (for example, detecting a cycle when adding edges to a graph).

With both tricks, a find costs $O(\alpha(n))$ amortised, where $\alpha$ is the inverse Ackermann function, a function that grows so slowly that it is below 5 for any $n$ you will ever see. For practical purposes every operation is $O(1)$. The space is $O(n)$. This is exactly the problem _Union-Find Operations_.

## 9.4 Check yourself

1. What identifies a group in a union-find forest?
2. Why does union by size keep the trees shallow?
3. Why must we read the size from the root?
4. What does `union` return when both items are already in the same group?

# Sources and credit

Chapters 6 to 9 adapt ideas from the data-structure articles at [cp-algorithms.com](https://cp-algorithms.com): the Fenwick tree (including the range update tricks), the segment tree (including lazy propagation), the sparse table and the disjoint set union. The caches, the time store, the snapshot array, the browser history and the hit counter are written from standard knowledge. The text here is rewritten for beginners. Like the original, it is shared under the Creative Commons Attribution-ShareAlike 4.0 licence.
