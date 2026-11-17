> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Hashing)

This page teaches hashing: the art of storing things so that you can find them almost instantly. You will learn dictionaries and sets, how to count things with them, how to group things that belong together, and a handful of clever patterns (prefix sums with a dictionary, splitting a hard problem into two halves, spotting a repeat) that turn slow nested loops into a single pass.

The page is a staircase. **Chapter 1 is deliberately gentle**: what a dictionary is and how to count with it. Each chapter after that adds one new idea and only uses what came before, so by the last chapter you will be able to solve the hardest hashing questions of this step. Every code example is shown in Python and in C++, so pick whichever language you like.

# Chapter 1. Dictionaries and counting

## 1.1 Why finding things can be instant

Suppose you keep a list of a million names and someone asks "is Priya in the list?" Looking at the names one by one may take a million steps. A **dictionary** (also called a hash map) answers the same question in a handful of steps, however big it is. A **set** is the simpler cousin that remembers only keys ("is this thing in here?") and no extra data.

The trick is a **hash function**: a function that turns a key into a whole number. We keep a row of small boxes, called **buckets**, and the key goes into box number `hash(key) % number_of_buckets`. To find a key later, we compute the same box number and look only in that box. Two different keys may land in the same box (a **collision**), so each box holds a short list and we compare keys inside it. With a sensible hash function the boxes stay short, so a lookup is **on average** $O(1)$: it does not grow with the number of items. Here is a toy version, using whole numbers as keys.

```python
class ToyTable:
    def __init__(self, size=8):
        self.buckets = [[] for _ in range(size)]

    def _bucket(self, key):
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key, value):
        box = self._bucket(key)
        for pair in box:
            if pair[0] == key:
                pair[1] = value
                return
        box.append([key, value])

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default


t = ToyTable()
t.put(3, 10)
t.put(11, 20)
t.put(3, 30)
assert t.get(3) == 30
assert t.get(11) == 20
assert t.get(5, 0) == 0
```

```cpp
struct ToyTable {
    vector<vector<pair<int, int>>> buckets;

    ToyTable(int size = 8) : buckets(size) {}

    vector<pair<int, int>>& bucket(int key) {
        return buckets[hash<int>()(key) % buckets.size()];
    }

    void put(int key, int value) {
        auto& box = bucket(key);
        for (auto& p : box) {
            if (p.first == key) {
                p.second = value;
                return;
            }
        }
        box.push_back({key, value});
    }

    int get(int key, int fallback) {
        for (auto& p : bucket(key)) {
            if (p.first == key) return p.second;
        }
        return fallback;
    }
};
```

In the example, 3 and 11 both land in box 3 (because $3 \bmod 8 = 11 \bmod 8 = 3$), which is a collision, yet both are still found. Real tables also grow the number of buckets when they fill up, so the boxes stay short. In Python the real thing is `dict` and `set`; in C++ it is `unordered_map` and `unordered_set`. Keys must be things that never change while stored: numbers, strings and tuples are fine in Python, but a list is not.

## 1.2 Counting how often things appear

The most common use of a dictionary is **counting**: the key is the thing and the value is how many times we have seen it. Walk through the list once; for each item add one to its count, starting from 0 if it is new. This is a **frequency table**.

```python
def count_all(nums):
    counts = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    return counts


assert count_all([2, 3, 2, 2]) == {2: 3, 3: 1}
assert count_all([]) == {}
```

```cpp
unordered_map<int, int> count_all(const vector<int>& nums) {
    unordered_map<int, int> counts;
    for (int x : nums) counts[x]++;
    return counts;
}
```

Building the table takes $O(n)$ on average. In C++, `counts[x]++` creates a missing key with value 0 first, which is exactly what we want. In Python we use `counts.get(x, 0)`, which gives 0 when the key is missing.

Once the table exists, any question about counts is easy. For example, how many different values appear exactly twice? Look at the values of the table. And if you are given many queries asking "how many times does this value appear?", you build the table once and answer each query by one lookup, instead of scanning the whole list for every query (which would cost $O(n)$ per query).

```python
def how_many_twice(nums):
    counts = count_all(nums)
    return sum(1 for c in counts.values() if c == 2)


def lookup_all(nums, queries):
    counts = count_all(nums)
    return [counts.get(q, 0) for q in queries]


assert how_many_twice([1, 1, 2, 3, 3, 3, 4, 4]) == 2
assert lookup_all([5, 5, 7], [5, 7, 9]) == [2, 1, 0]
```

```cpp
int how_many_twice(const vector<int>& nums) {
    unordered_map<int, int> counts = count_all(nums);
    int result = 0;
    for (auto& [value, c] : counts) {
        if (c == 2) result++;
    }
    return result;
}

vector<int> lookup_all(const vector<int>& nums, const vector<int>& queries) {
    unordered_map<int, int> counts = count_all(nums);
    vector<int> answers;
    for (int q : queries) {
        auto it = counts.find(q);
        answers.push_back(it == counts.end() ? 0 : it->second);
    }
    return answers;
}
```

With $n$ values and $q$ queries the time is $O(n + q)$ on average, and the space is $O(n)$. This is exactly the problem _Frequency Queries_.

## 1.3 Picking the winner and breaking ties

After counting, we often want the **most** frequent (or **least** frequent) item. A subtle point is what to do when several items tie. Dictionaries do not promise any particular order, so if the question says "take the smaller one", we must say so explicitly in our code.

A neat way is to visit the keys in sorted order and replace the current best only when a count is **strictly** greater. Since we meet the smaller keys first, a tie never replaces them. Here is the idea for words, where a smaller word means one that comes first alphabetically. In C++, `map` keeps its keys sorted, so a plain loop over it already visits them in order.

```python
def most_common_word(words):
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    best = ""
    best_count = 0
    for w in sorted(counts):
        if counts[w] > best_count:
            best = w
            best_count = counts[w]
    return best


assert most_common_word(["b", "a", "b", "a", "c"]) == "a"
assert most_common_word(["x"]) == "x"
assert most_common_word([]) == ""
```

```cpp
string most_common_word(const vector<string>& words) {
    map<string, int> counts;
    for (const string& w : words) counts[w]++;
    string best = "";
    int bestCount = 0;
    for (auto& [w, c] : counts) {
        if (c > bestCount) {
            best = w;
            bestCount = c;
        }
    }
    return best;
}
```

For the least frequent item, flip the test to "strictly smaller" (and start from a large number). Time is $O(n + d \log d)$ for $d$ different items, from the sorting. This is exactly the problem _Most and Least Frequent Value_.

## 1.4 Check yourself

1. What is a collision in a hash table, and why does a lookup still work after one?
2. In `count_all`, why do we use `counts.get(x, 0)` (Python) instead of `counts[x]`?
3. Why is building one frequency table better than scanning the list once for every query?
4. When two items tie for most frequent, why does looping in sorted order and using a strict "greater than" keep the smaller one?

# Chapter 2. Counting letters and strings

## 2.1 Counting letters

Strings are lists of characters, so counting letters is counting again. When the text uses only lowercase letters `a` to `z`, we do not even need a dictionary: an array of 26 counters is enough, where the counter for letter `ch` sits at position `ord(ch) - 97` (in C++ simply `ch - 'a'`).

A common pattern is **count first, then scan again**. The first pass builds the counts for the whole string, and the second pass walks the string in its original order asking about the counts. As an example, find the first letter that appears exactly twice in the whole string. For `"xyzy"` the counts are x:1, y:2, z:1, so the answer is `y`.

```python
def first_twice(s):
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - 97] += 1
    for ch in s:
        if counts[ord(ch) - 97] == 2:
            return ch
    return ""


assert first_twice("xyzy") == "y"
assert first_twice("abc") == ""
assert first_twice("abcab") == "a"
```

```cpp
string first_twice(const string& s) {
    vector<int> counts(26, 0);
    for (char ch : s) counts[ch - 'a']++;
    for (char ch : s) {
        if (counts[ch - 'a'] == 2) return string(1, ch);
    }
    return "";
}
```

Two passes, $O(n)$ time, and $O(1)$ extra space since the array always has 26 slots. If the text can contain any characters, use a dictionary instead. The sheet question asks for the **index** of the first character that appears exactly once, which is the same two-pass pattern with "exactly once" in place of "exactly twice". This is exactly the problem _First Unique Character_.

## 2.2 Counting up and counting down

Another useful pattern is to **count up with one string and count down with another**. Take the question "are two strings made of the same letters in a different order?" (these are called **anagrams**, like `listen` and `silent`). Count the letters of the first string up. Then walk the second string and take each letter away; if some letter is not available (its count is already 0), the answer is no.

For `aab` and `abb`: counting up gives a:2, b:1. Walking the second string, `a` leaves a:1, `b` leaves b:0, and the second `b` has nothing left, so the answer is no.

```python
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in t:
        if counts.get(ch, 0) == 0:
            return False
        counts[ch] -= 1
    return True


assert is_anagram("listen", "silent") is True
assert is_anagram("aab", "abb") is False
```

```cpp
bool is_anagram(const string& s, const string& t) {
    if (s.size() != t.size()) return false;
    unordered_map<char, int> counts;
    for (char ch : s) counts[ch]++;
    for (char ch : t) {
        if (counts[ch] == 0) return false;
        counts[ch]--;
    }
    return true;
}
```

Time $O(n)$. If the lengths may differ, as in the next question, you simply skip the length check: the second string is the one being "taken from the first", and we only fail when something is missing. For the ransom note, count the letters of the magazine up, then take away the letters of the note one by one; if a letter runs out, the note cannot be built. This is exactly the problem _Ransom Note_.

## 2.3 Check yourself

1. Why does the first-twice example need two passes over the string?
2. How much extra memory does an array of 26 counters need, and why?
3. In `is_anagram`, when do we answer no during the second pass?
4. For the ransom note, which string do we count up and which do we take from?

# Chapter 3. Matching one thing to another

## 3.1 A map that must stay consistent

Some questions ask whether two sequences "have the same pattern", for example `"abba"` against the words `dog cat cat dog`. The rule is that each letter must always stand for the same word. We check this with a dictionary from the first sequence to the second. For each pair of items, if the item on the left already has an entry and the entry disagrees with the item on the right, the answer is no; otherwise we record or confirm the entry.

```python
def follows_one_way(a, b):
    mapping = {}
    for x, y in zip(a, b):
        if x in mapping and mapping[x] != y:
            return False
        mapping[x] = y
    return True


assert follows_one_way(["a", "b", "b", "a"], ["dog", "cat", "cat", "dog"]) is True
assert follows_one_way(["a", "a"], ["x", "y"]) is False
assert follows_one_way(["a", "b"], ["x", "x"]) is True
```

```cpp
bool follows_one_way(const vector<string>& a, const vector<string>& b) {
    unordered_map<string, string> mapping;
    for (size_t i = 0; i < a.size() && i < b.size(); i++) {
        auto it = mapping.find(a[i]);
        if (it != mapping.end() && it->second != b[i]) return false;
        mapping[a[i]] = b[i];
    }
    return true;
}
```

Look at the third check: `a` and `b` give both letters the same word `x`, and this check still says yes. That is the weakness of a one-way map: it never notices that two **different** letters were sent to the **same** word.

## 3.2 Checking both directions

In many questions, the matching must be **one-to-one**: each item on the left stands for exactly one item on the right, and each item on the right is used by exactly one item on the left. So `a` and `b` mapping to the same word is forbidden. One way is to keep two dictionaries, one for each direction, and check both on every pair. A tidier way is to turn each sequence into its **shape**.

The shape of a sequence replaces each item by the number of the order in which it first appeared: 0 for the first new item, 1 for the second new item, and so on. So `egg` has shape `0 1 1`, and `add` also has shape `0 1 1`. The pattern `abba` and the words `dog cat cat dog` both have shape `0 1 1 0`. Two sequences match one-to-one exactly when they have the same length and the same shape. The pair `a, b` against `x, x` has shapes `0 1` and `0 0`, so it correctly fails.

```python
def shape(seq):
    first = {}
    out = []
    for x in seq:
        if x not in first:
            first[x] = len(first)
        out.append(first[x])
    return out


def same_shape(a, b):
    return len(a) == len(b) and shape(a) == shape(b)


assert shape(list("egg")) == [0, 1, 1]
assert same_shape(["a", "b", "b", "a"], ["dog", "cat", "cat", "dog"]) is True
assert same_shape(["a", "b"], ["x", "x"]) is False
assert same_shape(list("foo"), list("bar")) is False
```

```cpp
vector<int> shape(const vector<string>& seq) {
    unordered_map<string, int> first;
    vector<int> out;
    for (const string& x : seq) {
        if (!first.count(x)) {
            int id = first.size();
            first[x] = id;
        }
        out.push_back(first[x]);
    }
    return out;
}

bool same_shape(const vector<string>& a, const vector<string>& b) {
    return a.size() == b.size() && shape(a) == shape(b);
}
```

Time $O(n)$ on average. For two strings, split them into one-letter pieces first (in Python `list(s)`), and two strings of different lengths are never a match. Two strings of letters whose shapes agree are called **isomorphic**, which is exactly the problem _Isomorphic Strings_. For a pattern against a list of words, the pattern letters form one sequence and the words form the other, which is exactly the problem _Word Pattern_.

## 3.3 Check yourself

1. In the one-way check, which wrong pair of sequences still gets a yes?
2. What is the shape of `"paper"`?
3. Why is it enough to compare the shapes, with no second dictionary?
4. What must be checked first when two sequences may have different lengths?

# Chapter 4. Grouping with a key

## 4.1 Grouping into buckets

Counting stores a number per key. **Grouping** stores a **list** per key. Choose a rule that gives each item a key, and put items with the same key in the same list. Let us group numbers by the sum of their digits. The numbers 10 and 1 both have digit sum 1, and 19 and 28 both have digit sum 10.

```python
def group_by_digit_sum(nums):
    groups = {}
    for x in nums:
        key = sum(int(d) for d in str(x))
        if key not in groups:
            groups[key] = []
        groups[key].append(x)
    return groups


assert group_by_digit_sum([10, 1, 19, 28, 5]) == {1: [10, 1], 10: [19, 28], 5: [5]}
assert group_by_digit_sum([]) == {}
```

```cpp
map<int, vector<int>> group_by_digit_sum(const vector<int>& nums) {
    map<int, vector<int>> groups;
    for (int x : nums) {
        int key = 0;
        for (int y = x; y > 0; y /= 10) key += y % 10;
        groups[key].push_back(x);
    }
    return groups;
}
```

Computing the key costs a little per item; the grouping itself is $O(1)$ per item on average. The whole art of grouping is choosing a good **key**: a value that is identical for items that belong together and different otherwise.

## 4.2 Keys that ignore the order

Which key groups anagrams? Two words are anagrams when they use exactly the same letters. If we sort the letters of each word, all anagrams turn into the very same string: `eat`, `tea` and `ate` all become `aet`. That sorted string is our key.

```python
def anagram_key(word):
    return "".join(sorted(word))


def count_classes(words):
    return len({anagram_key(w) for w in words})


assert anagram_key("tea") == "aet"
assert anagram_key("ate") == "aet"
assert count_classes(["eat", "tea", "tan", "ate", "nat", "bat"]) == 3
```

```cpp
string anagram_key(string word) {
    sort(word.begin(), word.end());
    return word;
}

int count_classes(const vector<string>& words) {
    unordered_set<string> keys;
    for (const string& w : words) keys.insert(anagram_key(w));
    return keys.size();
}
```

Sorting a word of length $L$ costs $O(L \log L)$. If the words use only 26 letters, there is a faster key: the list of 26 letter counts, which can be built in $O(L)$. In Python you can use that list turned into a tuple as the key; in C++ a `vector<int>` can be the key of an ordered `map`.

To finish the sheet question you group the words by this key, sort each group, and sort the groups by their first word. This is exactly the problem _Group Anagrams_.

## 4.3 Sets for comparing two lists

When you need to compare two lists without caring about order or repeats, put one of them in a set and look up each value of the other. Which values of `a` are missing from `b`? Make a set of `b`, then keep each value of `a` that is not in it.

```python
def only_in_first(a, b):
    in_b = set(b)
    return sorted({x for x in a if x not in in_b})


assert only_in_first([4, 1, 2, 2, 7], [2, 9]) == [1, 4, 7]
assert only_in_first([], [1]) == []
```

```cpp
vector<int> only_in_first(const vector<int>& a, const vector<int>& b) {
    unordered_set<int> inB(b.begin(), b.end());
    set<int> result;
    for (int x : a) {
        if (!inB.count(x)) result.insert(x);
    }
    return vector<int>(result.begin(), result.end());
}
```

Building the set takes $O(m)$ and checking the other list takes $O(n)$ on average, so the whole job is $O(n + m)$, plus sorting the answer. Compare this with checking every value of `a` by scanning all of `b`, which costs $O(nm)$. The values that appear in **both** lists work the same way: keep the values of `a` that **are** in the set built from `b`. Python also offers `set(a) & set(b)` for this. This is exactly the problem _Common Values_.

## 4.4 Check yourself

1. In grouping, what must be true about the key of two items that belong in the same group?
2. Why do all anagrams end up with the same sorted key?
3. What is a faster key than sorting when the words use only lowercase letters?
4. Why is a set better than scanning the other list for every value?

# Chapter 5. The most frequent items

## 5.1 Sorting by count

To find the "top $k$" most frequent items, first count, then rank. Ranking means sorting the (count, item) pairs so that bigger counts come first, and so that ties are broken in a way the question defines (here: alphabetical order). The easiest way is to sort by the pair $(-\text{count}, \text{item})$, since a negative count sorts the biggest count first.

```python
def rank_words(words):
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    items = sorted(counts, key=lambda w: (-counts[w], w))
    return items


assert rank_words(["b", "a", "b", "c", "c", "d"]) == ["b", "c", "a", "d"]
assert rank_words([]) == []
```

```cpp
vector<string> rank_words(const vector<string>& words) {
    unordered_map<string, int> counts;
    for (const string& w : words) counts[w]++;
    vector<pair<int, string>> items;
    for (auto& [w, c] : counts) items.push_back({-c, w});
    sort(items.begin(), items.end());
    vector<string> result;
    for (auto& p : items) result.push_back(p.second);
    return result;
}
```

With $d$ different items the sort costs $O(d \log d)$, plus $O(n)$ for counting. Taking the first $k$ of the ranked list answers the "top $k$" question. For many inputs this is already fast enough.

## 5.2 Buckets for counts

We can do better by noticing that a count can only be a whole number from 1 up to $n$. So instead of sorting, make $n + 1$ **buckets**, where bucket $c$ holds all items with count exactly $c$. Then read the buckets from the biggest count down to the smallest, stopping when we have $k$ items. Inside one bucket the items are tied, so we sort only those few by the tie-break rule.

```python
def top_k_words_buckets(words, k):
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    buckets = [[] for _ in range(len(words) + 1)]
    for w, c in counts.items():
        buckets[c].append(w)
    result = []
    for c in range(len(words), 0, -1):
        result.extend(sorted(buckets[c]))
        if len(result) >= k:
            break
    return result[:k]


assert top_k_words_buckets(["b", "a", "b", "c", "c", "d"], 3) == ["b", "c", "a"]
assert top_k_words_buckets(["x", "y"], 5) == ["x", "y"]
```

```cpp
vector<string> top_k_words_buckets(const vector<string>& words, int k) {
    unordered_map<string, int> counts;
    for (const string& w : words) counts[w]++;
    vector<vector<string>> buckets(words.size() + 1);
    for (auto& [w, c] : counts) buckets[c].push_back(w);
    vector<string> result;
    for (int c = (int)words.size(); c >= 1; c--) {
        sort(buckets[c].begin(), buckets[c].end());
        for (const string& w : buckets[c]) result.push_back(w);
        if ((int)result.size() >= k) break;
    }
    if ((int)result.size() > k) result.resize(k);
    return result;
}
```

Counting and bucketing take $O(n)$. The only sorting happens inside buckets, whose total size is at most $d$. This is exactly the problem _Top K Frequent Values_ (there the items are numbers and ties go to the smaller number).

## 5.3 Keeping only the best k

A third way never builds the full ranking. We only need the best $k$ out of $d$ items, and the standard tools do that in $O(d \log k)$ time: a **heap** (a structure that always hands you the smallest item quickly) in Python's `heapq.nsmallest`, and `partial_sort` in C++, which puts only the first $k$ positions in order. This is a good choice when $k$ is much smaller than $d$.

```python
import heapq


def top_k_words_heap(words, k):
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    items = [(-c, w) for w, c in counts.items()]
    return [w for _, w in heapq.nsmallest(k, items)]


assert top_k_words_heap(["b", "a", "b", "c", "c", "d"], 3) == ["b", "c", "a"]
assert top_k_words_heap(["x", "y"], 5) == ["x", "y"]
```

```cpp
vector<string> top_k_words_heap(const vector<string>& words, int k) {
    unordered_map<string, int> counts;
    for (const string& w : words) counts[w]++;
    vector<pair<int, string>> items;
    for (auto& [w, c] : counts) items.push_back({-c, w});
    k = min(k, (int)items.size());
    partial_sort(items.begin(), items.begin() + k, items.end());
    vector<string> result;
    for (int i = 0; i < k; i++) result.push_back(items[i].second);
    return result;
}
```

All three methods give the same answer; they differ only in speed. If you are unsure, start with the simple sort of Section 5.1 and improve it only when needed.

## 5.4 Check yourself

1. Why do we sort by the negative of the count?
2. In the bucket method, what is the largest count an item can have?
3. Why do we only need to sort inside each bucket?
4. When is keeping only the best $k$ items better than sorting everything?

# Chapter 6. Remembering the recent past

## 6.1 Remembering the last place we saw it

Often we need to compare each item with the **previous time the same item appeared**. A dictionary from item to its last index does that. Let us find the smallest distance between two equal values in a list (or $-1$ if no value repeats). At each position, if the value is in the dictionary, the distance is the current index minus the stored index; then we update the stored index to the current one.

```python
def min_gap_equal(nums):
    last = {}
    best = -1
    for i, x in enumerate(nums):
        if x in last:
            gap = i - last[x]
            if best == -1 or gap < best:
                best = gap
        last[x] = i
    return best


assert min_gap_equal([1, 5, 1, 5, 5]) == 1
assert min_gap_equal([1, 2, 3]) == -1
```

```cpp
int min_gap_equal(const vector<int>& nums) {
    unordered_map<int, int> last;
    int best = -1;
    for (int i = 0; i < (int)nums.size(); i++) {
        auto it = last.find(nums[i]);
        if (it != last.end()) {
            int gap = i - it->second;
            if (best == -1 || gap < best) best = gap;
        }
        last[nums[i]] = i;
    }
    return best;
}
```

Time $O(n)$ on average. Storing only the most recent index is enough because any older copy of the same value is farther away. The question "are there two equal values at most $k$ positions apart?" is just "is the smallest gap at most $k$?", answered in the same single pass. This is exactly the problem _Nearby Duplicate_.

## 6.2 A window that adds and removes

A second way to look at the recent past is a **window**: the last $w$ values. As we move one step to the right, one value enters the window and one value leaves. We keep a dictionary of counts for the window. When a value enters, add one; when a value leaves, subtract one and delete its entry when it reaches zero. The number of different values in the window is then the size of the dictionary.

For `[1, 2, 1, 3, 1]` and windows of length 3: `[1, 2, 1]` has 2 different values, `[2, 1, 3]` has 3, and `[1, 3, 1]` has 2.

```python
def distinct_in_windows(nums, w):
    counts = {}
    out = []
    for i, x in enumerate(nums):
        counts[x] = counts.get(x, 0) + 1
        if i >= w:
            old = nums[i - w]
            counts[old] -= 1
            if counts[old] == 0:
                del counts[old]
        if i >= w - 1:
            out.append(len(counts))
    return out


assert distinct_in_windows([1, 2, 1, 3, 1], 3) == [2, 3, 2]
assert distinct_in_windows([4, 4, 4], 2) == [1, 1]
```

```cpp
vector<int> distinct_in_windows(const vector<int>& nums, int w) {
    unordered_map<int, int> counts;
    vector<int> out;
    for (int i = 0; i < (int)nums.size(); i++) {
        counts[nums[i]]++;
        if (i >= w) {
            int old = nums[i - w];
            if (--counts[old] == 0) counts.erase(old);
        }
        if (i >= w - 1) out.push_back(counts.size());
    }
    return out;
}
```

Every value enters once and leaves once, so the time is $O(n)$ on average. The same add-and-remove idea with a plain set solves the nearby-duplicate question too: keep the last $k$ values in a set, and if a new value is already in it, a duplicate exists.

## 6.3 Check yourself

1. Why is it enough to store only the latest index of each value?
2. How do we turn the smallest gap into a yes or no answer for "within $k$ positions"?
3. When a value leaves the window, why do we delete its entry once the count reaches zero?
4. How many times is each value added to and removed from the window in total?

# Chapter 7. Prefix sums with a dictionary

## 7.1 Equal prefix sums mean a zero run

The **prefix sum** at a position is the sum of all values up to that point. Take any run of the list. Its sum is the difference between two prefix sums: the one at its end minus the one just before its start. So a run has sum 0 exactly when those two prefix sums are **equal**. That turns "find a run with sum zero" into "find two equal prefix sums", which a dictionary does in one pass. We start the dictionary with the prefix sum 0 at index $-1$, standing for the empty start of the list.

To find the **shortest** zero-sum run, we want the closest pair of equal prefix sums, so we store the **latest** index of each prefix sum. For `[4, -4, 1, 2, -3]` the prefix sums are 4, 0, 1, 3, 0. The sum 0 appears at index $-1$ and index 1 (a run of length 2, namely `4, -4`) and again at index 4 (a run of length 3, namely `1, 2, -3`). The shortest has length 2.

```python
def shortest_zero_sum(nums):
    last = {0: -1}
    prefix = 0
    best = 0
    for i, x in enumerate(nums):
        prefix += x
        if prefix in last:
            length = i - last[prefix]
            if best == 0 or length < best:
                best = length
        last[prefix] = i
    return best


assert shortest_zero_sum([4, -4, 1, 2, -3]) == 2
assert shortest_zero_sum([1, 2, 3]) == 0
```

```cpp
int shortest_zero_sum(const vector<int>& nums) {
    unordered_map<long long, int> last;
    last[0] = -1;
    long long prefix = 0;
    int best = 0;
    for (int i = 0; i < (int)nums.size(); i++) {
        prefix += nums[i];
        auto it = last.find(prefix);
        if (it != last.end()) {
            int length = i - it->second;
            if (best == 0 || length < best) best = length;
        }
        last[prefix] = i;
    }
    return best;
}
```

For the **longest** zero-sum run we want the farthest pair, so we store the **first** index of each prefix sum and never overwrite it. The code is the same except that `last[prefix] = i` happens only when the prefix sum is not yet in the dictionary, and `best` takes the larger length. Time $O(n)$ on average. This is exactly the problem _Longest Zero-Sum Subarray_.

## 7.2 Remainders instead of sums

What if the run sum must be **divisible by $k$**? A run's sum is a difference of two prefix sums, and a difference is divisible by $k$ exactly when the two numbers leave the **same remainder** when divided by $k$. For example, with $k = 5$ the numbers 7 and 17 both leave remainder 2, and their difference 10 is divisible by 5. So we store prefix sums by remainder instead of by the full value, and look for equal remainders.

A warning about negatives: in Python, `-3 % 5` is 2, which is what we want, but in C++ the result of `%` on a negative number is negative (`-3 % 5` is `-3`). To get a remainder from 0 to $k-1$ in C++, write `((p % k) + k) % k`.

As an example we find the **longest** run whose sum is divisible by $k$. With remainders, we store the first index at which each remainder appears (starting with remainder 0 at index $-1$).

```python
def longest_divisible(nums, k):
    first = {0: -1}
    prefix = 0
    best = 0
    for i, x in enumerate(nums):
        prefix = (prefix + x) % k
        if prefix in first:
            best = max(best, i - first[prefix])
        else:
            first[prefix] = i
    return best


assert longest_divisible([4, 5, 0, -2, -3, 1], 5) == 6
assert longest_divisible([2, 3, 5], 4) == 2
```

```cpp
int longest_divisible(const vector<int>& nums, int k) {
    unordered_map<int, int> first;
    first[0] = -1;
    long long prefix = 0;
    int best = 0;
    for (int i = 0; i < (int)nums.size(); i++) {
        prefix = ((prefix + nums[i]) % k + k) % k;
        auto it = first.find((int)prefix);
        if (it != first.end()) best = max(best, i - it->second);
        else first[(int)prefix] = i;
    }
    return best;
}
```

To **count** the runs instead, keep a dictionary of how many times each remainder has appeared (start with remainder 0 counted once), and at each position add the current count of that remainder to the total before adding one to it. If a remainder has been seen $c$ times before, it pairs with each of those $c$ earlier prefix sums. Time $O(n)$ on average and space $O(k)$ at most. This is exactly the problem _Subarrays Divisible by K_.

## 7.3 Check yourself

1. Why does a repeated prefix sum mean there is a run with sum 0 between the two places?
2. To find the longest such run, do we store the first or the latest index of each prefix sum?
3. When is the sum of a run divisible by $k$, in terms of the remainders of two prefix sums?
4. In C++, how do we make sure the remainder of a negative number is never negative?

# Chapter 8. Splitting a problem in two halves

## 8.1 Two lists, one lookup

Look at this question: given two lists `a` and `b` and a target, how many pairs `(i, j)` have `a[i] + b[j] == target`? Trying every pair costs $O(n^2)$. But for each `a[i]` the partner we need is exactly `target - a[i]`. If we first count how often each value appears in `b`, one dictionary lookup tells us how many partners exist.

For `a = [1, 2]`, `b = [3, 4]` and target 5, the value 1 needs a 4 (one copy) and 2 needs a 3 (one copy), so the answer is 2.

```python
def count_pairs_two_lists(a, b, target):
    counts = {}
    for y in b:
        counts[y] = counts.get(y, 0) + 1
    total = 0
    for x in a:
        total += counts.get(target - x, 0)
    return total


assert count_pairs_two_lists([1, 2], [3, 4], 5) == 2
assert count_pairs_two_lists([1, 1], [4, 4, 4], 5) == 6
```

```cpp
long long count_pairs_two_lists(const vector<int>& a, const vector<int>& b, int target) {
    unordered_map<int, int> counts;
    for (int y : b) counts[y]++;
    long long total = 0;
    for (int x : a) {
        auto it = counts.find(target - x);
        if (it != counts.end()) total += it->second;
    }
    return total;
}
```

Time $O(n + m)$ on average, instead of $O(nm)$. This idea, "count one side, look up the other", is the heart of this chapter.

## 8.2 Four lists become two pairs

Now there are **four** lists and we count the tuples `(i, j, k, l)` with `a[i] + b[j] + c[k] + d[l] == 0`. Four nested loops cost $O(n^4)$. The key move is to split the four lists into two halves. Group the lists into the pair $(a, b)$ and the pair $(c, d)$. The sum $a[i] + b[j]$ takes at most $n^2$ different values, so we can list all of them in a dictionary, with how many times each sum occurs.

```python
def pair_sums_counter(a, b):
    sums = {}
    for x in a:
        for y in b:
            s = x + y
            sums[s] = sums.get(s, 0) + 1
    return sums


assert pair_sums_counter([1, 2], [3, 4]) == {4: 1, 5: 2, 6: 1}
assert pair_sums_counter([0], [0]) == {0: 1}
```

```cpp
unordered_map<long long, long long> pair_sums_counter(const vector<int>& a, const vector<int>& b) {
    unordered_map<long long, long long> sums;
    for (int x : a)
        for (int y : b)
            sums[(long long)x + y]++;
    return sums;
}
```

Building this dictionary costs $O(n^2)$. Then we visit every sum `c[k] + d[l]`, which is another $O(n^2)$ walk, and look up its negative `-(c[k] + d[l])` in the dictionary; the stored count says how many $(i, j)$ pairs complete the tuple. We add that count to the total each time. The whole algorithm is $O(n^2)$ time and $O(n^2)$ space, a huge improvement over $O(n^4)$. Because we count positions, equal values at different positions count separately, exactly as the stored counts do. This is exactly the problem _Four Lists Sum to Zero_.

This "meet in the middle" trick works whenever a hard search can be cut into two independent halves: compute everything from one half and store it, then for each answer from the other half look up what is needed.

## 8.3 Check yourself

1. In `count_pairs_two_lists`, what value do we look up for a given `x`?
2. If a value appears 3 times in `b`, how many pairs does it give with a matching `x`?
3. Why do we split four lists into two pairs, and not into three and one?
4. What are the time and space of the four-list method?

# Chapter 9. Spotting repeats and checking rules

## 9.1 Detecting a loop

Imagine a process: start with a number and apply the same rule again and again, for example $x \to (x^2 + 1) \bmod 10$. Because the numbers come from a small set, sooner or later the process meets a value it has met before, and from then on it repeats forever in a **cycle**. A dictionary that remembers the step number at which each value first appeared lets us detect this immediately.

The function below walks until a value repeats. It returns two numbers: how many steps there are before the cycle starts (the "tail"), and the length of the cycle. Starting at 0 the walk goes 0, 1, 2, 5, 6, 7 and then back to 0, so there is no tail and the cycle has length 6. Starting at 3 it goes 3, 0, 1, 2, 5, 6, 7, 0, so the tail is 1 and the cycle is again 6.

```python
def walk_until_repeat(start, step):
    seen = {}
    x = start
    i = 0
    while x not in seen:
        seen[x] = i
        x = step(x)
        i += 1
    return seen[x], i - seen[x]


rule = lambda x: (x * x + 1) % 10
assert walk_until_repeat(0, rule) == (0, 6)
assert walk_until_repeat(3, rule) == (1, 6)
```

```cpp
pair<int, int> walk_until_repeat(int start, function<int(int)> step) {
    unordered_map<int, int> seen;
    int x = start, i = 0;
    while (!seen.count(x)) {
        seen[x] = i;
        x = step(x);
        i++;
    }
    return {seen[x], i - seen[x]};
}
```

The loop stops after at most as many steps as there are different values, so memory is $O(\text{number of values})$. This helps with the **happy number** question: replace a number by the sum of the squares of its digits, again and again. A number is happy if the walk reaches 1, and not happy if it falls into a loop that does not contain 1. The step function is the digit-square sum below, and the numbers stay small (a number with $d$ digits turns into at most $81d$), so a repeat is guaranteed. Note that 1 maps to itself, so reaching 1 means the repeating value is 1.

```python
def digit_square_sum(n):
    total = 0
    while n > 0:
        n, digit = divmod(n, 10)
        total += digit * digit
    return total


assert digit_square_sum(19) == 82
assert digit_square_sum(100) == 1
```

```cpp
int digit_square_sum(int n) {
    int total = 0;
    while (n > 0) {
        int digit = n % 10;
        total += digit * digit;
        n /= 10;
    }
    return total;
}
```

So the number is happy exactly when the walk, using this step, ends up cycling on the value 1. (There is also a method called Floyd's tortoise and hare that finds the loop with only $O(1)$ memory, using two walkers of different speed, but the dictionary version is easier to understand.) This is exactly the problem _Happy Number_.

## 9.2 Checking rules with sets

A set is perfect for checking "no repeats" rules. Keep one set for each group that must have no repeats, and when you see a value, check the set of its group before adding it to the set.

Here is a small example: in a square grid, with 0 meaning an empty cell, does any row or any column contain the same non-zero value twice? We keep one set per row and one set per column.

```python
def grid_has_repeats(grid):
    rows = [set() for _ in grid]
    cols = [set() for _ in grid[0]] if grid else []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            v = grid[r][c]
            if v == 0:
                continue
            if v in rows[r] or v in cols[c]:
                return True
            rows[r].add(v)
            cols[c].add(v)
    return False


assert grid_has_repeats([[1, 2], [2, 1]]) is False
assert grid_has_repeats([[1, 0], [1, 2]]) is True
assert grid_has_repeats([[3, 3], [0, 0]]) is True
```

```cpp
bool grid_has_repeats(const vector<vector<int>>& grid) {
    if (grid.empty()) return false;
    int R = grid.size(), C = grid[0].size();
    vector<unordered_set<int>> rows(R), cols(C);
    for (int r = 0; r < R; r++) {
        for (int c = 0; c < C; c++) {
            int v = grid[r][c];
            if (v == 0) continue;
            if (rows[r].count(v) || cols[c].count(v)) return true;
            rows[r].insert(v);
            cols[c].insert(v);
        }
    }
    return false;
}
```

Time $O(RC)$, which is the number of cells. A Sudoku board adds one more kind of group: the nine $3 \times 3$ boxes. We simply keep nine more sets, one per box, and we need a way to find the box number of a cell. Rows of boxes are $r // 3$ and columns of boxes are $c // 3$, so the box number is

$$\text{box}(r, c) = 3\,\lfloor r/3 \rfloor + \lfloor c/3 \rfloor$$

```python
def box_id(r, c):
    return (r // 3) * 3 + c // 3


assert box_id(0, 0) == 0
assert box_id(4, 7) == 5
assert box_id(8, 8) == 8
```

```cpp
int box_id(int r, int c) {
    return (r / 3) * 3 + c / 3;
}
```

With 9 row sets, 9 column sets and 9 box sets, each filled cell is checked against three sets. The board has 81 cells, so the work is tiny and constant. This is exactly the problem _Valid Sudoku Board_.

## 9.3 Check yourself

1. Why must a process on a small set of values eventually repeat a value?
2. What do the two numbers returned by `walk_until_repeat` mean?
3. For a Sudoku board, how many sets do we need in total?
4. Which box number does the cell in row 4, column 7 belong to?
