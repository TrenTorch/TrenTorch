> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Tries)

This page teaches the trie (say "try"), also called a prefix tree. A trie stores a collection of words letter by letter in a tree, so that all words with the same beginning share the same path. That makes questions about _prefixes_ very fast: does any word start with these letters? How many do? What are the first three words that continue from here? Tries also power autocomplete, spell checkers, word games, and some surprising tricks with binary numbers.

The page is a staircase. **Chapter 1 is gentle**: what a trie looks like and how to build one with insert, search and "starts with". Chapters 2 and 3 count things and walk along words. Chapters 4 to 6 add wildcard search, autocomplete and a board game solver. Chapter 7 turns numbers into bit-strings for a maximum-xor trick, and Chapter 8 finishes with reversed words, streams and palindromes. Every code example is shown in Python and in C++.

# Chapter 1. Your first trie

## 1.1 Why not just use a set of words

Suppose you store words in a set. Asking "is `apple` in the set?" is fast. But asking "does any word **start with** `app`?" forces you to look at every word, which is slow if there are many. A **prefix** is the beginning part of a word: `a`, `ap`, `app`, `appl`, `apple` are all prefixes of `apple`.

A trie solves this by sharing beginnings. Each **node** is a spot in a tree, and each edge between nodes is labelled with one letter. A word is spelled by walking from the top node (the **root**) down along its letters. Here is a trie holding `car`, `cat`, `do` and `dog`:

```
            (root)
            /    \
           c      d
           |      |
           a      o*        <- "do" ends here
          / \     |
         r*  t*   g*        <- "car", "cat", "dog" end here
```

A star marks a node where a stored word ends. Notice that `car` and `cat` share the path `c`, `a`. Walking along `c`, `a` takes two steps and reaches a node that stands for the prefix `ca`, no matter how many words start with `ca`.

## 1.2 Building nodes and inserting a word

We store the tree in plain lists. Node number 0 is the root. For every node we keep a table `child` mapping a letter to the number of the child node (in C++ an array of 26 slots, where 0 means "no child", which is safe because the root can never be someone's child), and a flag `is_end` saying a word stops here.

To **insert** a word, start at the root. For each letter, if the current node has no child for that letter, create a new node. Then step into that child. After the last letter, mark the node as the end of a word.

```python
class Trie:
    def __init__(self):
        self.child = [{}]       # node -> {letter: child node}
        self.is_end = [False]   # node -> does a word end here?

    def new_node(self):
        self.child.append({})
        self.is_end.append(False)
        return len(self.child) - 1

    def insert(self, word):
        cur = 0
        for ch in word:
            if ch not in self.child[cur]:
                self.child[cur][ch] = self.new_node()
            cur = self.child[cur][ch]
        self.is_end[cur] = True


t = Trie()
t.insert("car")
t.insert("cat")
assert len(t.child) == 5  # root, c, a, r, t
```

```cpp
struct Trie {
    vector<array<int, 26>> child;  // 0 means "no child"
    vector<char> is_end;

    Trie() { new_node(); }

    int new_node() {
        child.push_back(array<int, 26>{});
        is_end.push_back(0);
        return (int)child.size() - 1;
    }

    void insert(const string& word) {
        int cur = 0;
        for (char ch : word) {
            int c = ch - 'a';
            if (child[cur][c] == 0) {
                int fresh = new_node();
                child[cur][c] = fresh;
            }
            cur = child[cur][c];
        }
        is_end[cur] = 1;
    }
};
```

Inserting a word of length $L$ takes $O(L)$ time. It does not depend on how many words are already stored.

## 1.3 Search and starts with

Both questions walk the same road. We follow the letters from the root. If at some point the needed child is missing, the answer is no. If we survive all the letters, we stand on a node. For **starts with** it is enough that we got there. For **search** (the whole word is stored) we also need `is_end` to be true on that node. Otherwise `app` would wrongly count as stored just because `apple` is.

We write the walk once as a helper that returns the node we stopped on, or -1 if the road broke.

```python
class Trie:
    def __init__(self):
        self.child = [{}]
        self.is_end = [False]

    def new_node(self):
        self.child.append({})
        self.is_end.append(False)
        return len(self.child) - 1

    def insert(self, word):
        cur = 0
        for ch in word:
            if ch not in self.child[cur]:
                self.child[cur][ch] = self.new_node()
            cur = self.child[cur][ch]
        self.is_end[cur] = True

    def walk(self, text):
        cur = 0
        for ch in text:
            nxt = self.child[cur].get(ch)
            if nxt is None:
                return -1
            cur = nxt
        return cur

    def search(self, word):
        node = self.walk(word)
        return node != -1 and self.is_end[node]

    def starts_with(self, prefix):
        return self.walk(prefix) != -1


t = Trie()
t.insert("apple")
assert t.search("apple") is True
assert t.search("app") is False
assert t.starts_with("app") is True
t.insert("app")
assert t.search("app") is True
assert t.starts_with("b") is False
```

```cpp
struct Trie {
    vector<array<int, 26>> child;
    vector<char> is_end;

    Trie() { new_node(); }

    int new_node() {
        child.push_back(array<int, 26>{});
        is_end.push_back(0);
        return (int)child.size() - 1;
    }

    void insert(const string& word) {
        int cur = 0;
        for (char ch : word) {
            int c = ch - 'a';
            if (child[cur][c] == 0) {
                int fresh = new_node();
                child[cur][c] = fresh;
            }
            cur = child[cur][c];
        }
        is_end[cur] = 1;
    }

    int walk(const string& text) const {
        int cur = 0;
        for (char ch : text) {
            cur = child[cur][ch - 'a'];
            if (cur == 0) return -1;
        }
        return cur;
    }

    bool search(const string& word) const {
        int node = walk(word);
        return node != -1 && is_end[node];
    }

    bool starts_with(const string& prefix) const { return walk(prefix) != -1; }
};
```

Search and starts-with take $O(L)$ time. The trie uses at most one node per letter of all inserted words, so space is $O(\text{total letters})$ (times 26 slots per node in the C++ array version).

This is exactly the problem _Implement a Trie_: run the operations `insert`, `search` and `starts` on one trie and collect the answers of the last two.

## 1.4 Check yourself

1. In the trie of `car`, `cat`, `do`, `dog`, how many nodes are there, counting the root?
2. Why does `search("app")` need the `is_end` flag, while `starts_with("app")` does not?
3. How long does inserting a word of length $L$ take, and does it depend on how many words are stored?
4. Why can the value 0 mean "no child" in the C++ array?

# Chapter 2. Counting through the trie

## 2.1 Keeping a counter on every node

Sometimes we do not just ask "is there a word with this prefix?" but "**how many** words have this prefix?" The idea is small: put a counter on each node that counts how many inserted words pass through it. When we insert a word, every node we step on, from the first letter to the last, gets its counter increased by one. Then the number of words with prefix `p` is the counter of the node reached by walking `p`. If the walk breaks, the count is 0.

We also keep a second counter, `ends`, that says how many words stop exactly at the node. That lets us count a repeated word several times, and also lets us delete a word: walk its path, subtract one from every `passes` counter and one from `ends`.

```python
class CountTrie:
    def __init__(self):
        self.child = [{}]
        self.ends = [0]      # words that stop exactly at this node
        self.passes = [0]    # words that go through this node (including those stopping here)

    def insert(self, word):
        cur = 0
        self.passes[0] += 1
        for ch in word:
            if ch not in self.child[cur]:
                self.child.append({})
                self.ends.append(0)
                self.passes.append(0)
                self.child[cur][ch] = len(self.child) - 1
            cur = self.child[cur][ch]
            self.passes[cur] += 1
        self.ends[cur] += 1

    def walk(self, text):
        cur = 0
        for ch in text:
            nxt = self.child[cur].get(ch)
            if nxt is None:
                return -1
            cur = nxt
        return cur

    def count_prefix(self, prefix):
        node = self.walk(prefix)
        return 0 if node == -1 else self.passes[node]

    def count_word(self, word):
        node = self.walk(word)
        return 0 if node == -1 else self.ends[node]

    def erase(self, word):
        # the caller promises that word is currently stored
        cur = 0
        self.passes[0] -= 1
        for ch in word:
            cur = self.child[cur][ch]
            self.passes[cur] -= 1
        self.ends[cur] -= 1


t = CountTrie()
for w in ["car", "cart", "cat", "car"]:
    t.insert(w)
assert t.count_prefix("ca") == 4
assert t.count_prefix("car") == 3
assert t.count_prefix("cart") == 1
assert t.count_prefix("dog") == 0
assert t.count_word("car") == 2
t.erase("car")
assert t.count_prefix("car") == 2
assert t.count_word("car") == 1
```

```cpp
struct CountTrie {
    vector<array<int, 26>> child;
    vector<int> ends;    // words that stop exactly at this node
    vector<int> passes;  // words that go through this node

    CountTrie() {
        child.push_back(array<int, 26>{});
        ends.push_back(0);
        passes.push_back(0);
    }

    void insert(const string& word) {
        int cur = 0;
        passes[0]++;
        for (char ch : word) {
            int c = ch - 'a';
            if (child[cur][c] == 0) {
                child.push_back(array<int, 26>{});
                ends.push_back(0);
                passes.push_back(0);
                child[cur][c] = (int)child.size() - 1;
            }
            cur = child[cur][c];
            passes[cur]++;
        }
        ends[cur]++;
    }

    int walk(const string& text) const {
        int cur = 0;
        for (char ch : text) {
            cur = child[cur][ch - 'a'];
            if (cur == 0) return -1;
        }
        return cur;
    }

    int count_prefix(const string& prefix) const {
        int node = walk(prefix);
        return node == -1 ? 0 : passes[node];
    }

    int count_word(const string& word) const {
        int node = walk(word);
        return node == -1 ? 0 : ends[node];
    }

    void erase(const string& word) {  // the caller promises that word is stored
        int cur = 0;
        passes[0]--;
        for (char ch : word) {
            cur = child[cur][ch - 'a'];
            passes[cur]--;
        }
        ends[cur]--;
    }
};
```

Insert, count and erase each take $O(L)$ time for a word of length $L$. Space is $O(\text{total letters})$.

## 2.2 Answering many prefix queries

With this counter, a batch of prefix queries is easy: insert all words once, then answer each query by one walk. For $W$ words of average length $L$ and $Q$ queries, the time is $O((W + Q) \cdot L)$. Checking every word against every query would cost $O(W \cdot Q \cdot L)$, which is hopeless when both numbers are large.

This is exactly the problem _Count Words With a Prefix_. A word equal to the query counts too, and that is automatic: the node of the whole word also has the word passing through it. Repeated words count each time because `passes` goes up on every insert, as in the `car` example above.

A small warning: erasing a word leaves its nodes in the trie (with counters at zero). That is harmless for counting, and it keeps the code simple.

## 2.3 Check yourself

1. What does `passes` count that `ends` does not?
2. After inserting `to`, `top`, `to`, what are `count_prefix("to")` and `count_word("to")`?
3. Why does the node of the whole word `car` have `passes` at least as large as `ends`?
4. How long does a prefix query take when there are a million stored words?

# Chapter 3. Walking along a word

In Chapter 1 we walked a _query_ along the trie. Now we use the trie to answer questions about long texts: which stored word does this text start with? Which stored words appear inside it? Which stored words can be built one letter at a time?

## 3.1 The shortest stored prefix

Given a word like `cattle` and a set of stored roots like `cat`, `ca`, `bat`, we want the **shortest** root that is a prefix of the word. Walk the word letter by letter in the trie. The first time we land on a node marked `is_end`, we have found the shortest stored prefix, because we meet prefixes in order of length. If the road breaks before that, there is none.

```python
class Trie:
    def __init__(self):
        self.child = [{}]
        self.is_end = [False]

    def insert(self, word):
        cur = 0
        for ch in word:
            if ch not in self.child[cur]:
                self.child.append({})
                self.is_end.append(False)
                self.child[cur][ch] = len(self.child) - 1
            cur = self.child[cur][ch]
        self.is_end[cur] = True


def shortest_stored_prefix(trie, word):
    cur = 0
    for k, ch in enumerate(word):
        nxt = trie.child[cur].get(ch)
        if nxt is None:
            return ""
        cur = nxt
        if trie.is_end[cur]:
            return word[:k + 1]
    return ""


t = Trie()
for r in ["cat", "ca", "bat"]:
    t.insert(r)
assert shortest_stored_prefix(t, "cattle") == "ca"
assert shortest_stored_prefix(t, "battery") == "bat"
assert shortest_stored_prefix(t, "dog") == ""
```

```cpp
struct Trie {
    vector<array<int, 26>> child;
    vector<char> is_end;

    Trie() {
        child.push_back(array<int, 26>{});
        is_end.push_back(0);
    }

    void insert(const string& word) {
        int cur = 0;
        for (char ch : word) {
            int c = ch - 'a';
            if (child[cur][c] == 0) {
                child.push_back(array<int, 26>{});
                is_end.push_back(0);
                child[cur][c] = (int)child.size() - 1;
            }
            cur = child[cur][c];
        }
        is_end[cur] = 1;
    }
};

string shortest_stored_prefix(const Trie& trie, const string& word) {
    int cur = 0;
    for (size_t k = 0; k < word.size(); ++k) {
        cur = trie.child[cur][word[k] - 'a'];
        if (cur == 0) return "";
        if (trie.is_end[cur]) return word.substr(0, k + 1);
    }
    return "";
}
```

The walk takes at most the length $L$ of the word, so the time is $O(L)$, and it does not depend on how many roots are stored.

This is exactly the problem _Replace Words With Their Roots_. Insert all roots, split the sentence into words, replace each word by its shortest stored prefix if there is one (otherwise keep the word), and join the words back with single spaces.

## 3.2 All stored words that start at a position

Now the opposite: we have a long text and want to find every place where a stored word appears. Fix a **start position** in the text. Walk the trie along the text from that position. Every time we stand on an `is_end` node, a stored word ends at the current letter. We stop when the road breaks. Doing this for every start position finds all occurrences.

```python
def match_ends(trie, text, start):
    out = []
    cur = 0
    for j in range(start, len(text)):
        nxt = trie.child[cur].get(text[j])
        if nxt is None:
            break
        cur = nxt
        if trie.is_end[cur]:
            out.append(j)
    return out


t2 = Trie()
for w in ["he", "hers", "she"]:
    t2.insert(w)
assert match_ends(t2, "ushers", 0) == []
assert match_ends(t2, "ushers", 1) == [3]
assert match_ends(t2, "ushers", 2) == [3, 5]
```

```cpp
vector<int> match_ends(const Trie& trie, const string& text, int start) {
    vector<int> out;
    int cur = 0;
    for (int j = start; j < (int)text.size(); ++j) {
        cur = trie.child[cur][text[j] - 'a'];
        if (cur == 0) break;
        if (trie.is_end[cur]) out.push_back(j);
    }
    return out;
}
```

One call costs at most $O(M)$, where $M$ is the length of the longest stored word, since the walk cannot go deeper than that. Running it from all $n$ start positions costs $O(n \cdot M)$. This is far better than testing every stored word at every position.

This is exactly the problem _Index Pairs of a String_. For each start `i`, take every end `j` returned by `match_ends` and record the pair `[i, j]`. Because we visit starts in increasing order and each call returns ends in increasing order, the pairs come out already sorted by start then end. A repeated word in the list makes no difference, since the trie stores it once.

## 3.3 Only walk through words

Here is a different kind of question. Find the longest word in a list such that **every prefix** of it is also in the list. Think of building the word by adding one letter at a time, where each step must give a real word. In the trie this means we may only step onto nodes marked `is_end`. A depth-first search (DFS) that only enters word-ending nodes visits exactly the words whose prefixes are all words. A **DFS** goes as deep as possible along one path before backing up and trying the next branch.

If we try children in alphabetical order and replace our best answer only when we find a strictly longer word, ties are won by the alphabetically smallest word.

```python
def longest_chain_word(trie):
    best = ""

    def dfs(node, path):
        nonlocal best
        if len(path) > len(best):
            best = path
        for ch in sorted(trie.child[node]):
            nxt = trie.child[node][ch]
            if trie.is_end[nxt]:
                dfs(nxt, path + ch)

    dfs(0, "")
    return best


t3 = Trie()
for w in ["b", "ba", "bad", "c", "cat"]:
    t3.insert(w)
assert longest_chain_word(t3) == "bad"  # "cat" fails: "ca" is missing
t4 = Trie()
for w in ["y", "x"]:
    t4.insert(w)
assert longest_chain_word(t4) == "x"
t5 = Trie()
t5.insert("xa")
assert longest_chain_word(t5) == ""
```

```cpp
void chain_dfs(const Trie& trie, int node, string& path, string& best) {
    if (path.size() > best.size()) best = path;
    for (int c = 0; c < 26; ++c) {
        int nxt = trie.child[node][c];
        if (nxt != 0 && trie.is_end[nxt]) {
            path.push_back((char)('a' + c));
            chain_dfs(trie, nxt, path, best);
            path.pop_back();
        }
    }
}

string longest_chain_word(const Trie& trie) {
    string path, best;
    chain_dfs(trie, 0, path, best);
    return best;
}
```

The DFS touches each node at most once, so it takes $O(\text{nodes})$ time (times 26 for the C++ array scan). The recursion is as deep as the longest word.

This is exactly the problem _Longest Word Built Letter by Letter_.

## 3.4 Check yourself

1. Why does the first `is_end` node we meet while walking a word give the shortest stored prefix?
2. For text `ushers` and the words `he`, `hers`, `she`, what does `match_ends` return when we start at index 2?
3. Why does the walk from one start position never cost more than the length of the longest stored word?
4. In the chain DFS, why do we skip children that are not word ends?

# Chapter 4. Wildcards and DFS in a trie

## 4.1 A dot that matches any letter

Now suppose a search pattern may contain the character `.`, a **wildcard** that matches any single letter. The pattern `.ad` matches `bad`, `dad` and `mad`. A normal walk fails here, because at a dot we do not know which child to follow. The answer: try **all** children. If any of them leads to a match, the pattern matches.

This is a recursive search. Let `dfs(node, i)` answer: "starting at this node, does the pattern from position `i` onwards match some stored word?" If `i` is at the end of the pattern, we must be standing on an `is_end` node. If the pattern letter is a normal letter, follow that single child (if it exists). If it is a dot, try every child.

```python
class Trie:
    def __init__(self):
        self.child = [{}]
        self.is_end = [False]

    def insert(self, word):
        cur = 0
        for ch in word:
            if ch not in self.child[cur]:
                self.child.append({})
                self.is_end.append(False)
                self.child[cur][ch] = len(self.child) - 1
            cur = self.child[cur][ch]
        self.is_end[cur] = True


def matches_pattern(trie, pattern):
    def dfs(node, i):
        if i == len(pattern):
            return trie.is_end[node]
        ch = pattern[i]
        if ch == ".":
            return any(dfs(nxt, i + 1) for nxt in trie.child[node].values())
        nxt = trie.child[node].get(ch)
        return nxt is not None and dfs(nxt, i + 1)

    return dfs(0, 0)


t = Trie()
for w in ["bad", "dad", "mad"]:
    t.insert(w)
assert matches_pattern(t, "pad") is False
assert matches_pattern(t, "bad") is True
assert matches_pattern(t, ".ad") is True
assert matches_pattern(t, "b..") is True
assert matches_pattern(t, "b.e") is False
assert matches_pattern(t, "....") is False
```

```cpp
struct Trie {
    vector<array<int, 26>> child;
    vector<char> is_end;

    Trie() {
        child.push_back(array<int, 26>{});
        is_end.push_back(0);
    }

    void insert(const string& word) {
        int cur = 0;
        for (char ch : word) {
            int c = ch - 'a';
            if (child[cur][c] == 0) {
                child.push_back(array<int, 26>{});
                is_end.push_back(0);
                child[cur][c] = (int)child.size() - 1;
            }
            cur = child[cur][c];
        }
        is_end[cur] = 1;
    }
};

bool wildcard_dfs(const Trie& trie, int node, const string& pattern, size_t i) {
    if (i == pattern.size()) return trie.is_end[node];
    if (pattern[i] == '.') {
        for (int c = 0; c < 26; ++c) {
            int nxt = trie.child[node][c];
            if (nxt != 0 && wildcard_dfs(trie, nxt, pattern, i + 1)) return true;
        }
        return false;
    }
    int nxt = trie.child[node][pattern[i] - 'a'];
    return nxt != 0 && wildcard_dfs(trie, nxt, pattern, i + 1);
}

bool matches_pattern(const Trie& trie, const string& pattern) {
    return wildcard_dfs(trie, 0, pattern, 0);
}
```

## 4.2 How slow can it get

Without dots, a search is one walk, $O(L)$. Each dot may branch into up to 26 children, so a pattern with $d$ dots could in theory try up to $26^d$ paths. But the search can never visit more nodes than the trie has, so the cost is also bounded by $O(\text{number of nodes} \cdot L)$ in a crude way, and in practice the length of the pattern limits the depth. Patterns with few dots are fast. Space is the trie itself, plus the recursion depth $O(L)$.

The pattern and the word must have the same length, and that is automatic here: the search ends only when the pattern is used up, and a match needs an `is_end` node exactly at that depth.

This is exactly the problem _Add and Search Words With Wildcards_. Insert words with `add`, and answer `search` with `matches_pattern`.

## 4.3 Check yourself

1. At a dot, why must we try every child and not just one?
2. With stored words `bad`, `dad` and `mad`, does `b..` match? Does `..` match?
3. When the pattern is used up, what must be true about the node we stand on?
4. Roughly how many steps does a pattern without any dots take?

# Chapter 5. Autocomplete

## 5.1 Listing the words below a node

When a user types `ca`, we want to suggest words that continue from there. In the trie, the node reached by walking `ca` is the top of a small sub-tree containing exactly the words that start with `ca`. If we explore that sub-tree with a DFS, trying children in alphabetical order (smaller letter first), then words come out in **dictionary order**. A word is output when we reach a node where it ends, and before we go deeper, because a word is smaller than its own extensions (`car` comes before `card`).

We usually need only the first few suggestions, say `limit` of them, so the DFS stops as soon as it has enough. We also keep a counter `ends` instead of a flag, so a word stored twice is suggested twice.

```python
class Trie:
    def __init__(self):
        self.child = [{}]
        self.ends = [0]  # how many copies of a word stop at this node

    def insert(self, word):
        cur = 0
        for ch in word:
            if ch not in self.child[cur]:
                self.child.append({})
                self.ends.append(0)
                self.child[cur][ch] = len(self.child) - 1
            cur = self.child[cur][ch]
        self.ends[cur] += 1


def first_words(trie, node, path, limit, out):
    for _ in range(trie.ends[node]):
        if len(out) >= limit:
            return
        out.append(path)
    for ch in sorted(trie.child[node]):
        if len(out) >= limit:
            return
        first_words(trie, trie.child[node][ch], path + ch, limit, out)


t = Trie()
for w in ["car", "card", "care", "cat", "dog", "car"]:
    t.insert(w)
res = []
first_words(t, t.child[0]["c"], "c", 3, res)
assert res == ["car", "car", "card"]
```

```cpp
struct Trie {
    vector<array<int, 26>> child;
    vector<int> ends;  // how many copies of a word stop at this node

    Trie() {
        child.push_back(array<int, 26>{});
        ends.push_back(0);
    }

    void insert(const string& word) {
        int cur = 0;
        for (char ch : word) {
            int c = ch - 'a';
            if (child[cur][c] == 0) {
                child.push_back(array<int, 26>{});
                ends.push_back(0);
                child[cur][c] = (int)child.size() - 1;
            }
            cur = child[cur][c];
        }
        ends[cur]++;
    }
};

void first_words(const Trie& trie, int node, string& path, int limit, vector<string>& out) {
    for (int copies = 0; copies < trie.ends[node]; ++copies) {
        if ((int)out.size() >= limit) return;
        out.push_back(path);
    }
    for (int c = 0; c < 26; ++c) {
        if ((int)out.size() >= limit) return;
        int nxt = trie.child[node][c];
        if (nxt != 0) {
            path.push_back((char)('a' + c));
            first_words(trie, nxt, path, limit, out);
            path.pop_back();
        }
    }
}
```

## 5.2 Suggestions after every typed letter

The user types one letter at a time. We keep a variable `node` that follows the typed letters in the trie. After each letter we move `node` to the matching child. If the child is missing, we are off the trie forever, so every later suggestion list is empty. Otherwise we call `first_words` from `node` with the prefix typed so far.

```python
def autocomplete(words, typed, limit):
    trie = Trie()
    for w in words:
        trie.insert(w)
    out = []
    node = 0
    for k, ch in enumerate(typed):
        if node != -1:
            node = trie.child[node].get(ch, -1)
        found = []
        if node != -1:
            first_words(trie, node, typed[:k + 1], limit, found)
        out.append(found)
    return out


assert autocomplete(["car", "card", "care", "cat", "dog"], "cat", 2) == [
    ["car", "card"],
    ["car", "card"],
    ["cat"],
]
assert autocomplete(["dog"], "dx", 3) == [["dog"], []]
```

```cpp
vector<vector<string>> autocomplete(const vector<string>& words, const string& typed, int limit) {
    Trie trie;
    for (const string& w : words) trie.insert(w);
    vector<vector<string>> out;
    int node = 0;
    for (size_t k = 0; k < typed.size(); ++k) {
        if (node != -1) {
            int nxt = trie.child[node][typed[k] - 'a'];
            node = (nxt == 0) ? -1 : nxt;
        }
        vector<string> found;
        if (node != -1) {
            string path = typed.substr(0, k + 1);
            first_words(trie, node, path, limit, found);
        }
        out.push_back(found);
    }
    return out;
}
```

Building the trie takes $O(\text{total letters})$. Each suggestion call visits at most the nodes on the way to `limit` words, which is bounded by about `limit` times the word length, so it is small and independent of how many other words exist.

A different, also fine, approach is to sort the words once and use binary search to find where the prefix begins; the trie avoids sorting and gives each prefix directly.

This is exactly the problem _Search Suggestions_, with `limit` equal to 3. The words are products, and repeated product names are suggested separately, which is why we count `ends` instead of using a flag.

## 5.3 Check yourself

1. Why do we try children in alphabetical order inside the DFS?
2. Why is `car` listed before `card`?
3. Once the typed prefix leaves the trie, what are all later suggestion lists?
4. Why does the work per suggestion list depend on `limit` and not on the total number of words?

# Chapter 6. Pruning a board search

## 6.1 Why one word at a time is too slow

In a letter grid, a word is found by walking between neighbouring cells (up, down, left, right) without using a cell twice. Finding a _single_ word is a standard backtracking search: from each cell matching the first letter, try all four directions, mark the cell as used, recurse, then unmark it (this "try and undo" is called **backtracking**). With many words, repeating that search once per word repeats a lot of work, especially for words with the same beginning.

The trie fixes this. We run **one** search over the board, but carry along the trie node for the letters walked so far. At each new cell we ask the trie: is there a child for this cell's letter? If not, **no stored word starts with these letters**, so we stop right there and never explore this path further. That is the pruning. If the trie node marks the end of a word, we record that word and keep going, because a longer word may continue.

## 6.2 The solver

We store the whole word at its end node (`word_at`), so we do not need to rebuild strings along the path. Two details make this much faster. First, we keep the result in a set, because one word can be traced along several different paths. Second, once a trie node has no children left (all its words have been found), we cut it away from its parent, so later searches never enter dead ends again. We track the number of children in `kids`.

```python
def boggle_words(board, words):
    child = [{}]
    word_at = [None]
    for w in words:
        cur = 0
        for ch in w:
            if ch not in child[cur]:
                child.append({})
                word_at.append(None)
                child[cur][ch] = len(child) - 1
            cur = child[cur][ch]
        word_at[cur] = w

    rows, cols = len(board), len(board[0])
    used = [[False] * cols for _ in range(rows)]
    found = set()

    def dfs(r, c, node):
        ch = board[r][c]
        nxt = child[node].get(ch)
        if nxt is None:
            return
        if word_at[nxt] is not None:
            found.add(word_at[nxt])
        used[r][c] = True
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not used[nr][nc]:
                dfs(nr, nc, nxt)
        used[r][c] = False
        if not child[nxt]:
            del child[node][ch]  # nothing below: never come here again

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, 0)
    return sorted(found)


assert boggle_words(["oa", "et"], ["oat", "eat", "oe", "oao"]) == ["oat", "oe"]
assert boggle_words(["ab"], ["ba", "ab", "b"]) == ["ab", "b", "ba"]
```

```cpp
vector<string> boggle_words(const vector<string>& board, const vector<string>& words) {
    vector<array<int, 26>> child(1);
    vector<int> kids(1, 0);
    vector<string> word_at(1);
    for (const string& w : words) {
        int cur = 0;
        for (char ch : w) {
            int c = ch - 'a';
            if (child[cur][c] == 0) {
                child.push_back(array<int, 26>{});
                kids.push_back(0);
                word_at.push_back("");
                child[cur][c] = (int)child.size() - 1;
                kids[cur]++;
            }
            cur = child[cur][c];
        }
        word_at[cur] = w;
    }

    int rows = (int)board.size(), cols = (int)board[0].size();
    vector<vector<char>> used(rows, vector<char>(cols, 0));
    set<string> found;
    const int dr[4] = {1, -1, 0, 0};
    const int dc[4] = {0, 0, 1, -1};

    function<void(int, int, int)> dfs = [&](int r, int c, int node) {
        int idx = board[r][c] - 'a';
        int nxt = child[node][idx];
        if (nxt == 0) return;
        if (!word_at[nxt].empty()) found.insert(word_at[nxt]);
        used[r][c] = 1;
        for (int d = 0; d < 4; ++d) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && !used[nr][nc]) dfs(nr, nc, nxt);
        }
        used[r][c] = 0;
        if (kids[nxt] == 0) {  // nothing below: never come here again
            child[node][idx] = 0;
            kids[node]--;
        }
    };

    for (int r = 0; r < rows; ++r)
        for (int c = 0; c < cols; ++c) dfs(r, c, 0);
    return vector<string>(found.begin(), found.end());
}
```

The first test shows two rules at once. The word `oao` would need the single `o` twice, and `used` forbids it, so it is not found. The word `eat` fails because `e` and `a` touch only diagonally.

## 6.3 Why the search stays fast

Building the trie costs $O(\text{total letters})$. The search starts at each of the $R \cdot C$ cells and goes at most as deep as the longest word $M$; each step has at most 4 directions (3 after the first, since we cannot go back), so the worst case is about $O(R \cdot C \cdot 3^{M})$. But the trie prunes whole branches that no word follows, so on real inputs it explores a tiny fraction of that, and it is much faster than running a separate search for each word. Extra space is the trie plus the recursion depth $O(M)$.

This is exactly the problem _Word Search II_. The sheet passes the board as a list of strings, like `"oaan"`, and wants the found words sorted; `sorted(found)` does that. The idea of the pruning is the lesson of this chapter: **the trie tells the search when to give up early.**

## 6.4 Check yourself

1. Why can a search stop when the current trie node has no child for the next cell's letter?
2. Why do we keep the found words in a set?
3. Why do we continue searching after finding a word that ends at the current node?
4. What does removing an empty trie node from its parent save us later?

# Chapter 7. A trie of bits: maximum xor

## 7.1 Numbers as strings of bits

A trie does not have to hold letters. It can hold the **binary digits** (bits) of numbers. Every number below $2^{B}$ is a string of exactly $B$ bits, written from the most significant (leftmost, biggest value) to the least. We build a trie where each node has only two possible children, `0` and `1`. Every number is a path of exactly $B$ steps from the root.

The **xor** of two numbers (written $a \oplus b$) compares them bit by bit: the result bit is 1 when the two bits are different and 0 when they are the same. For example $5 \oplus 3$: 101 and 011 differ in the first two positions and agree in the last, giving 110, which is 6.

## 7.2 Greedy from the top bit

We want, for a number $x$, the stored number $n$ that makes $x \oplus n$ as large as possible. The leftmost bits matter the most: a 1 in the top position is worth more than every lower bit combined ($2^{k} > 2^{k-1} + \dots + 1$). So we decide bit by bit from the top. At each level, look at the bit of $x$ and try to go to the child with the **opposite** bit, because different bits give a 1 in the result. If that child exists, take it and add that bit's value to the answer. If it does not exist, we have to take the same-bit child and the result bit stays 0. We never regret the choice, because the higher bit always outweighs everything below.

```python
BITS = 30


class BitTrie:
    def __init__(self):
        self.child = [[0, 0]]  # node -> [child for bit 0, child for bit 1]; 0 means none

    def insert(self, x):
        cur = 0
        for b in range(BITS - 1, -1, -1):
            bit = (x >> b) & 1
            if self.child[cur][bit] == 0:
                self.child.append([0, 0])
                self.child[cur][bit] = len(self.child) - 1
            cur = self.child[cur][bit]

    def best_xor(self, x):
        # the trie must contain at least one number
        cur = 0
        result = 0
        for b in range(BITS - 1, -1, -1):
            bit = (x >> b) & 1
            want = 1 - bit
            if self.child[cur][want] != 0:
                result |= 1 << b
                cur = self.child[cur][want]
            else:
                cur = self.child[cur][bit]
        return result


bt = BitTrie()
for v in [5, 9, 12]:
    bt.insert(v)
assert bt.best_xor(3) == 15   # 3 ^ 12
assert bt.best_xor(12) == 9   # 12 ^ 5
assert bt.best_xor(0) == 12
```

```cpp
const int BITS = 30;

struct BitTrie {
    vector<array<int, 2>> child;  // 0 means none

    BitTrie() { child.push_back({0, 0}); }

    void insert(int x) {
        int cur = 0;
        for (int b = BITS - 1; b >= 0; --b) {
            int bit = (x >> b) & 1;
            if (child[cur][bit] == 0) {
                child.push_back({0, 0});
                child[cur][bit] = (int)child.size() - 1;
            }
            cur = child[cur][bit];
        }
    }

    int best_xor(int x) const {  // the trie must contain at least one number
        int cur = 0;
        int result = 0;
        for (int b = BITS - 1; b >= 0; --b) {
            int bit = (x >> b) & 1;
            int want = 1 - bit;
            if (child[cur][want] != 0) {
                result |= 1 << b;
                cur = child[cur][want];
            } else {
                cur = child[cur][bit];
            }
        }
        return result;
    }
};
```

Both insert and query take $O(B)$ steps, so about 30 steps per number. With $n$ stored numbers and $q$ queries the total is $O((n + q) \cdot B)$ time and $O(n \cdot B)$ space. A brute-force check of every pair would cost $O(n \cdot q)$.

This is exactly the problem _Maximum XOR With Each Query_: insert all of `nums`, then answer each `x` in `queries` with `best_xor(x)`. Since `nums` is not empty, the trie always has a path to follow.

## 7.3 The best pair inside one array

The same structure finds the largest xor of any two numbers in a single array. Process the numbers in order: before inserting a number, ask the trie (holding the earlier numbers) for its best partner, and keep the maximum.

```python
def max_pair_xor(nums):
    trie = BitTrie()
    trie.insert(nums[0])
    best = 0
    for x in nums[1:]:
        best = max(best, trie.best_xor(x))
        trie.insert(x)
    return best


assert max_pair_xor([3, 10, 5, 25, 2, 8]) == 28  # 5 ^ 25
assert max_pair_xor([7]) == 0
```

```cpp
int max_pair_xor(const vector<int>& nums) {
    BitTrie trie;
    trie.insert(nums[0]);
    int best = 0;
    for (size_t i = 1; i < nums.size(); ++i) {
        best = max(best, trie.best_xor(nums[i]));
        trie.insert(nums[i]);
    }
    return best;
}
```

## 7.4 Check yourself

1. How many children can a node of a bit trie have, and how long is every path?
2. Why is it correct to prefer the opposite bit at the highest level even if it costs us at lower levels?
3. What is $6 \oplus 3$?
4. How many steps does one query take if numbers are below $2^{30}$?

# Chapter 8. Reversed words: streams, suffixes and palindromes

## 8.1 Matching the end of a stream

A new idea: a trie is great at _prefixes_, but sometimes we care about _suffixes_, the ends of strings. The trick is to insert each word **reversed**. A suffix of the text then becomes a prefix of the reversed text, and we can walk it in the trie.

Letters arrive one at a time, and after each one we must say whether some **suffix** of everything received so far is a stored word. For example, with words `ab`, `bca`, `z` and the stream `xabcaz`, after `b` the received text is `xab`, which ends with `ab`: yes. We keep the received letters in a list. On each new letter we read the received letters **from the newest backwards**, which spells a suffix reversed, and walk that in the trie of reversed words. If we ever stand on a word end, the answer is yes. If the road breaks, no.

```python
class Trie:
    def __init__(self):
        self.child = [{}]
        self.is_end = [False]

    def insert(self, word):
        cur = 0
        for ch in word:
            if ch not in self.child[cur]:
                self.child.append({})
                self.is_end.append(False)
                self.child[cur][ch] = len(self.child) - 1
            cur = self.child[cur][ch]
        self.is_end[cur] = True


class StreamChecker:
    def __init__(self, words):
        self.trie = Trie()
        for w in words:
            self.trie.insert(w[::-1])
        self.seen = []

    def query(self, ch):
        self.seen.append(ch)
        cur = 0
        for i in range(len(self.seen) - 1, -1, -1):
            nxt = self.trie.child[cur].get(self.seen[i])
            if nxt is None:
                return False
            cur = nxt
            if self.trie.is_end[cur]:
                return True
        return False


sc = StreamChecker(["ab", "bca", "z"])
assert [sc.query(c) for c in "xabcaz"] == [False, False, True, False, True, True]
```

```cpp
struct Trie {
    vector<array<int, 26>> child;
    vector<char> is_end;

    Trie() {
        child.push_back(array<int, 26>{});
        is_end.push_back(0);
    }

    void insert(const string& word) {
        int cur = 0;
        for (char ch : word) {
            int c = ch - 'a';
            if (child[cur][c] == 0) {
                child.push_back(array<int, 26>{});
                is_end.push_back(0);
                child[cur][c] = (int)child.size() - 1;
            }
            cur = child[cur][c];
        }
        is_end[cur] = 1;
    }
};

class StreamChecker {
    Trie trie;
    string seen;

public:
    StreamChecker(const vector<string>& words) {
        for (const string& w : words) trie.insert(string(w.rbegin(), w.rend()));
    }

    bool query(char ch) {
        seen.push_back(ch);
        int cur = 0;
        for (int i = (int)seen.size() - 1; i >= 0; --i) {
            cur = trie.child[cur][seen[i] - 'a'];
            if (cur == 0) return false;
            if (trie.is_end[cur]) return true;
        }
        return false;
    }
};
```

Each query walks at most as far as the longest stored word, so it costs $O(M)$ for longest word length $M$, no matter how long the stream has been. Building costs $O(\text{total letters})$.

This is exactly the problem _Stream of Characters_. The sheet gives the whole stream at once as a string, but the logic is the same: call `query` for each letter and collect the answers.

## 8.2 A word hiding at the end of another

Here is a puzzle on the same theme. We want to write a list of words into one string, each word followed by `#`, and make the string as short as possible. A word can **share space** with a longer word if it is a suffix of it: writing `time#` also contains `me` ending right before the `#`. So a word that is a suffix of another stored word costs nothing. Only the words that are _not_ a suffix of any other word need their own space, each costing its length plus one for the `#`.

In the reversed-word trie, a word being a suffix of another means its reversed spelling is a prefix of the other's reversed spelling, so it lies on a path that continues to a **leaf** (a node with no children). Every leaf corresponds to a word that is not a suffix of any other, and its depth equals the word length. So the answer is the sum of (depth + 1) over all leaves.

```python
def shortest_encoding_length(words):
    child = [{}]
    depth = [0]
    for w in set(words):
        cur = 0
        for ch in reversed(w):
            if ch not in child[cur]:
                child.append({})
                depth.append(depth[cur] + 1)
                child[cur][ch] = len(child) - 1
            cur = child[cur][ch]
    return sum(depth[node] + 1 for node in range(1, len(child)) if not child[node])


assert shortest_encoding_length(["abc", "bc", "x", "xx"]) == 7  # "abc#xx#"
assert shortest_encoding_length(["a", "a"]) == 2
```

```cpp
int shortest_encoding_length(const vector<string>& words) {
    vector<array<int, 26>> child(1);
    vector<int> depth(1, 0);
    set<string> unique_words(words.begin(), words.end());
    for (const string& w : unique_words) {
        int cur = 0;
        for (int i = (int)w.size() - 1; i >= 0; --i) {
            int c = w[i] - 'a';
            if (child[cur][c] == 0) {
                int d = depth[cur] + 1;
                child.push_back(array<int, 26>{});
                depth.push_back(d);
                child[cur][c] = (int)child.size() - 1;
            }
            cur = child[cur][c];
        }
    }
    int total = 0;
    for (int node = 1; node < (int)child.size(); ++node) {
        bool leaf = true;
        for (int c = 0; c < 26; ++c)
            if (child[node][c] != 0) leaf = false;
        if (leaf) total += depth[node] + 1;
    }
    return total;
}
```

Time is $O(\text{total letters})$ and space is the same. We use `set(words)` so duplicates do not matter.

This is exactly the problem _Short Encoding of Words_.

## 8.3 When is two words glued a palindrome

A **palindrome** reads the same forwards and backwards, like `abba`. We are given distinct words and want pairs of different positions $(i, j)$ such that `words[i] + words[j]` is a palindrome. Testing all pairs works but is too slow for many words. Let's find a way using a trie of reversed words.

Let $w$ be `words[i]` and $v$ be `words[j]`. For $w + v$ to be a palindrome, the first letter of $w$ must equal the last letter of $v$, the second letter of $w$ must equal the second-to-last of $v$, and so on. In other words, **$w$ read forwards must match $v$ read backwards**, as long as both still have letters. Then one of three things happens:

1. They have the same length: $v$ is exactly $w$ reversed, and we are done.
2. $w$ is longer: we used up all of $v$, and what is left of $w$ (its last part) sits in the middle of the glued word, so it must be a palindrome itself.
3. $w$ is shorter: we used up all of $w$, and what is left of $v$ (read backwards, the part we have not matched yet) sits in the middle, so it must be a palindrome itself.

Now put every $v$ **reversed** into a trie. Walking $w$ forwards in this trie compares exactly "w forwards" with "v backwards". Case 1 and 3 happen when $w$ is used up: we stand on a node, and every word $v$ whose reversed spelling continues below this node with a palindromic rest qualifies (the rest may be empty, which is case 1). To find them fast, each node stores a list `rest_pal` of word numbers whose leftover below this node is a palindrome. Case 2 happens on the way down: while walking, whenever we stand on a node where some word $v$ ends and the remaining part of $w$ is a palindrome, $v$ is a partner.

```python
def is_pal_from(s, k):
    part = s[k:]
    return part == part[::-1]


class ReverseTrie:
    def __init__(self, words):
        self.child = [{}]
        self.end_id = [-1]     # index of the word ending here (reversed), or -1
        self.rest_pal = [[]]   # indices whose leftover below this node is a palindrome
        for j, v in enumerate(words):
            rev = v[::-1]
            cur = 0
            for k in range(len(rev) + 1):
                if is_pal_from(rev, k):
                    self.rest_pal[cur].append(j)
                if k == len(rev):
                    break
                ch = rev[k]
                if ch not in self.child[cur]:
                    self.child.append({})
                    self.end_id.append(-1)
                    self.rest_pal.append([])
                    self.child[cur][ch] = len(self.child) - 1
                cur = self.child[cur][ch]
            self.end_id[cur] = j

    def partners_of(self, w):
        # indices j such that w + words[j] is a palindrome (j may equal the index of w itself)
        out = []
        cur = 0
        for k in range(len(w) + 1):
            if k == len(w):
                out.extend(self.rest_pal[cur])
                break
            if self.end_id[cur] != -1 and is_pal_from(w, k):
                out.append(self.end_id[cur])
            nxt = self.child[cur].get(w[k])
            if nxt is None:
                break
            cur = nxt
        return out


demo = ["ab", "ba", "a", "", "xyx", "yx"]
rt = ReverseTrie(demo)
for w in demo:
    brute = [j for j in range(len(demo)) if (w + demo[j]) == (w + demo[j])[::-1]]
    assert sorted(rt.partners_of(w)) == brute
assert sorted(rt.partners_of("ab")) == [1, 2]
```

```cpp
bool is_pal_from(const string& s, int k) {
    int lo = k, hi = (int)s.size() - 1;
    while (lo < hi) {
        if (s[lo] != s[hi]) return false;
        ++lo;
        --hi;
    }
    return true;
}

struct ReverseTrie {
    vector<array<int, 26>> child;
    vector<int> end_id;
    vector<vector<int>> rest_pal;

    ReverseTrie(const vector<string>& words) : child(1), end_id(1, -1), rest_pal(1) {
        for (int j = 0; j < (int)words.size(); ++j) {
            string rev(words[j].rbegin(), words[j].rend());
            int cur = 0;
            for (int k = 0; k <= (int)rev.size(); ++k) {
                if (is_pal_from(rev, k)) rest_pal[cur].push_back(j);
                if (k == (int)rev.size()) break;
                int c = rev[k] - 'a';
                if (child[cur][c] == 0) {
                    child.push_back(array<int, 26>{});
                    end_id.push_back(-1);
                    rest_pal.push_back(vector<int>());
                    child[cur][c] = (int)child.size() - 1;
                }
                cur = child[cur][c];
            }
            end_id[cur] = j;
        }
    }

    vector<int> partners_of(const string& w) const {
        vector<int> out;
        int cur = 0;
        for (int k = 0; k <= (int)w.size(); ++k) {
            if (k == (int)w.size()) {
                out.insert(out.end(), rest_pal[cur].begin(), rest_pal[cur].end());
                break;
            }
            if (end_id[cur] != -1 && is_pal_from(w, k)) out.push_back(end_id[cur]);
            int nxt = child[cur][w[k] - 'a'];
            if (nxt == 0) break;
            cur = nxt;
        }
        return out;
    }
};
```

In the test, the partners of `ab` are `ba` (giving `abba`, case 1, equal lengths) and `a` (giving `aba`, case 2: `a` is used up, and the leftover `b` of `ab` is a palindrome). The test also compares every word against a brute-force search that glues all pairs, and the trie agrees every time.

## 8.4 Putting the pairs together

Each word number appears at most once in `partners_of`. To get the final answer you loop over all indices $i$, take `partners_of(words[i])`, and keep the pair $[i, j]$ whenever $j \ne i$. Finally sort the pairs. The words must be distinct for this simple version (with repeated words, store a list of indices at each end node instead of one).

Building the trie costs $O(\text{total letters} \cdot M)$ in the worst case, because testing whether a leftover is a palindrome costs up to the word length $M$ for each position. Each query costs the same. For many short words this is far better than testing all $n^2$ pairs, each with a palindrome check.

This is exactly the problem _Palindrome Pairs_.

## 8.5 Check yourself

1. Why do we insert the words reversed when we care about the ends of a stream?
2. In the encoding puzzle, why does a word that is a suffix of another cost nothing?
3. For $w$ = `abc`, which stored word $v$ makes $w + v$ a palindrome in the equal-length case?
4. In the palindrome-pair idea, which of the three cases is detected while walking and which at the end of $w$?
