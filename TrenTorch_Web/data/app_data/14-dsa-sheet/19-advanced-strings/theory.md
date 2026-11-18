> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Advanced strings)

This page teaches the classic algorithms for searching inside text: how to find a pattern fast, how to tell what a string repeats, how to compare many pieces of text with one number, how to find all palindromes at once, how to sort all suffixes of a string, and how to pick the smallest rotation. These are the tools behind text editors, search boxes and DNA analysis. You only need to be comfortable with strings and loops.

The page is a staircase. **Chapter 1 is gentle**: it starts with the obvious way of searching and shows exactly why it can be slow. Chapters 2 to 5 teach two linear-time tools (the prefix function and the Z-function) that never repeat a comparison. Chapter 6 brings hashing, Chapter 7 palindromes, Chapter 8 rotations, Chapter 9 suffix arrays, and Chapter 10 a divide-and-conquer trick. Each chapter uses only what came before. Every code example is shown in Python and in C++, so pick whichever language you like.

# Chapter 1. Finding a word inside a text

## 1.1 The vocabulary

We call the long string the **text** and the short string we look for the **pattern**. A **substring** is a run of consecutive characters of a string, so `"ana"` is a substring of `"banana"`. A **prefix** is a substring that starts at the very beginning (`"ban"`), and a **suffix** is a substring that ends at the very end (`"nana"`). The **length** of a string is its number of characters. We say a pattern **occurs** at position `i` of the text if the pattern is equal to the piece of the text that starts at index `i`.

Throughout this page, $n$ is the length of the text and $m$ is the length of the pattern. The question we keep asking is: "how fast can we find the occurrences of the pattern?"

## 1.2 The obvious way

The most natural idea is to place the pattern at every start position of the text, and compare letter by letter until we find a mismatch or finish the whole pattern. If we finish, we found an occurrence.

```python
def find_naive(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i
    return -1


assert find_naive("sadbutsad", "sad") == 0
assert find_naive("leetcode", "leeto") == -1
assert find_naive("hello", "llo") == 2
assert find_naive("abc", "") == 0
```

```cpp
int find_naive(const string& text, const string& pattern) {
    int n = text.size(), m = pattern.size();
    if (m == 0) return 0;
    for (int i = 0; i + m <= n; i++) {
        int j = 0;
        while (j < m && text[i + j] == pattern[j]) j++;
        if (j == m) return i;
    }
    return -1;
}
```

This is correct. The outer loop runs about $n$ times and the inner loop up to $m$ times, so the cost is $O(nm)$ in the worst case. For ordinary words, the inner loop stops almost immediately, so this is usually fast. But watch what happens on a repetitive text.

## 1.3 The slow case

Take the text `aaaa...a` (many letters `a`) and the pattern `aaaaab`. At every start position the first five letters match and only the sixth letter fails. We do about six comparisons for every start, and then we throw away everything we learned and move one step right. Let us count the comparisons by adding a counter:

```python
def count_comparisons(text, pattern):
    n, m = len(text), len(pattern)
    comparisons = 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            return i, comparisons
    return -1, comparisons


assert count_comparisons("a" * 20 + "b", "aaaaab") == (15, 96)
assert count_comparisons("a" * 20, "aaaaab") == (-1, 90)
assert count_comparisons("abcdefghij", "j") == (9, 10)
```

```cpp
pair<int, int> count_comparisons(const string& text, const string& pattern) {
    int n = text.size(), m = pattern.size();
    int comparisons = 0;
    for (int i = 0; i + m <= n; i++) {
        int j = 0;
        while (j < m) {
            comparisons++;
            if (text[i + j] != pattern[j]) break;
            j++;
        }
        if (j == m) return {i, comparisons};
    }
    return {-1, comparisons};
}
```

On a text of 20 letters `a` the failed search costs 90 comparisons; with a text of length $n$ and a pattern of length $m$ made this way it costs about $nm$. For $n = 200000$ and $m = 2000$ that is four hundred million steps. The wasted work is the real problem: when the pattern `aaaaab` has matched five letters and then failed, we already _know_ the last five letters of the text are `aaaaa`. A smarter algorithm should use that knowledge instead of looking at those letters again. The next chapters show how.

## 1.4 Check yourself

1. In the text `"banana"`, what are all the occurrences of the pattern `"ana"`? (They overlap.)
2. What is a suffix of `"hello"` that is also a prefix of `"hello"` other than the whole string?
3. For which kind of text and pattern does the naive search become slow?
4. What does the naive algorithm forget when it moves the pattern one step to the right?

# Chapter 2. Borders and the prefix function

## 2.1 What a border is

A **border** of a string is a piece that is both a prefix and a suffix of it, and is shorter than the whole string. The string `"abcabca"` has the border `"a"` (the first letter equals the last letter) and the border `"abca"` (the first four letters equal the last four), but not `"abc"`, because its suffix of length 3 is `"bca"`. Every string has the trivial border of length 0 (the empty string), which we ignore.

```
 a b c a b c a
 a b c a . . .     prefix "abca"
 . . . a b c a     suffix "abca"  -> equal, so "abca" is a border (length 4)
```

Borders are the key idea behind many string algorithms, because a border tells us that a string _overlaps with itself_, and overlaps are exactly the places where the naive search wasted its work.

## 2.2 The prefix function

The **prefix function** of a string $s$ is a list `pi` with one number for every position. The number `pi[i]` is the length of the _longest border of the piece `s[0..i]`_ (the first $i+1$ characters). For `"abcabca"`:

```
 index :  0  1  2  3  4  5  6
 char  :  a  b  c  a  b  c  a
 pi    :  0  0  0  1  2  3  4
```

At index 6 the piece is the whole `"abcabca"` and its longest border is `"abca"`, of length 4. At index 4 the piece is `"abcab"` and its longest border is `"ab"`, of length 2. A single letter has no border, so `pi[0]` is always 0.

Computing this naively means trying every length for every position, which costs $O(n^3)$ or at best $O(n^2)$. Here is the naive way, mostly so that we can use it later to check the fast one:

```python
def border_table_slow(s):
    pi = []
    for i in range(len(s)):
        piece = s[:i + 1]
        best = 0
        for length in range(1, len(piece)):
            if piece[:length] == piece[-length:]:
                best = length
        pi.append(best)
    return pi


assert border_table_slow("abcabca") == [0, 0, 0, 1, 2, 3, 4]
assert border_table_slow("aaaa") == [0, 1, 2, 3]
assert border_table_slow("") == []
```

```cpp
vector<int> border_table_slow(const string& s) {
    int n = s.size();
    vector<int> pi(n, 0);
    for (int i = 0; i < n; i++) {
        int len_piece = i + 1;
        for (int length = 1; length < len_piece; length++) {
            if (s.compare(0, length, s, len_piece - length, length) == 0) pi[i] = length;
        }
    }
    return pi;
}
```

## 2.3 Computing it in one pass

The clever part is to reuse the previous answer. Suppose we know that the longest border of `s[0..i-1]` has length $k$ (this is `pi[i-1]`). A border of the longer piece `s[0..i]` must be a border of the shorter piece, extended by one letter. So we simply try to extend our current border: if the next letter `s[i]` equals `s[k]` (the letter that follows the border's prefix), then the border grows to length $k + 1$.

What if `s[i]` does not equal `s[k]`? Then the border of length $k$ cannot be extended, and we need the _next longest_ border of `s[0..i-1]`. But the border of a border is again a border: the next candidate is the longest border of the prefix of length $k$, which we already computed, `pi[k-1]`. So we set $k$ to `pi[k-1]` and try again. We keep falling back until the letter fits or $k$ reaches 0.

```
 s = a a b a a a b        computing pi[5]  (letter at index 5 is 'a')
 pi so far: 0 1 0 1 2 ?
 k = pi[4] = 2   (border "aa" of "aabaa")
 s[5] = 'a'   and   s[k] = s[2] = 'b'   -> not equal, fall back
 k = pi[k-1] = pi[1] = 1   (border "a")
 s[5] = 'a'   and   s[1] = 'a'          -> equal, so k = 2
 pi[5] = 2
```

Running this for the whole string `aabaaab` gives `pi = [0, 1, 0, 1, 2, 2, 3]`. Here is the code:

```python
def border_table(s):
    pi = [0] * len(s)
    k = 0
    for i in range(1, len(s)):
        while k > 0 and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


assert border_table("aabaaab") == [0, 1, 0, 1, 2, 2, 3]
assert border_table("abcabca") == [0, 0, 0, 1, 2, 3, 4]
assert border_table("aaaa") == [0, 1, 2, 3]
assert border_table("abcabca") == border_table_slow("abcabca")
```

```cpp
vector<int> border_table(const string& s) {
    int n = s.size();
    vector<int> pi(n, 0);
    int k = 0;
    for (int i = 1; i < n; i++) {
        while (k > 0 && s[i] != s[k]) k = pi[k - 1];
        if (s[i] == s[k]) k++;
        pi[i] = k;
    }
    return pi;
}
```

This is exactly the problem _The Prefix Function_.

## 2.4 Why it is fast

The loop contains an inner `while`, so it is not obvious that the total time is linear. Here is the standard argument. The value of $k$ goes up by at most 1 for each letter (the line `k += 1`), so over the whole run it goes up at most $n$ times. Each pass of the inner `while` makes $k$ strictly smaller, and $k$ never goes below 0. So the total number of passes of the inner loop cannot be larger than the total amount $k$ ever went up, which is at most $n$. Therefore the whole algorithm runs in $O(n)$ time, with $O(n)$ memory for the table.

## 2.5 The longest happy prefix

The prefix function immediately answers one famous question. A **happy prefix** is a non-empty prefix of $s$, shorter than $s$, that is also a suffix: in other words, a border of the whole string. The longest one is the longest border of the whole string, which is the _last_ value of the table, `pi[n-1]`. We cut that many letters from the front. For `"level"` the table is `[0, 0, 0, 0, 1]`, the last value is 1, and the answer is `"l"`. For `"ababab"` the table is `[0, 0, 1, 2, 3, 4]` and the answer is `"abab"`. This is exactly the problem _Longest Happy Prefix_.

```python
def widest_border(s):
    if len(s) == 0:
        return ""
    return s[:border_table(s)[-1]]


assert widest_border("level") == "l"
assert widest_border("ababab") == "abab"
assert widest_border("abc") == ""
assert widest_border("") == ""
```

```cpp
string widest_border(const string& s) {
    if (s.empty()) return "";
    return s.substr(0, border_table(s).back());
}
```

Time $O(n)$ and space $O(n)$.

## 2.6 Check yourself

1. What are the borders of `"aabaa"`?
2. What is the prefix function of `"abab"`?
3. In the fall-back step, why is the next candidate `pi[k-1]` and not `k - 1`?
4. Why does the whole computation take only $O(n)$ steps although it has a loop inside a loop?

# Chapter 3. Knuth-Morris-Pratt search

## 3.1 Using borders to search

Now we can fix the slow search of Chapter 1. Suppose the pattern is `ababca` and we have matched its first 4 letters `abab`, but the next letter of the text is wrong. The naive search would move the pattern one step and start over. But `abab` has the border `ab`. That means the last two letters we matched are _also_ the first two letters of the pattern, so we can slide the pattern forward and continue from the third letter without looking at those two text letters again.

This is the idea of **Knuth-Morris-Pratt** search, or **KMP** (named after its three inventors). We keep one number $k$, the number of pattern letters currently matched. For each new text letter:

- while the letter does not match `pattern[k]`, fall back to the longest border of the matched part: $k$ becomes `pi[k-1]` (exactly like when we built the table);
- if it matches, $k$ grows by one;
- if $k$ reaches the pattern length, we found an occurrence; to continue we fall back too, using the border of the _whole_ pattern, because the next occurrence may overlap this one.

The text pointer never moves backwards. Let us trace the pattern `ababca` over the text `abababcab` (the border table of the pattern is `[0, 0, 1, 2, 0, 1]`):

```
 text index :  0  1  2  3  4  5  6  7  8
 text char  :  a  b  a  b  a  b  c  a  b
 k after    :  1  2  3  4  3  4  5  6  2
```

At index 4 the letter `a` does not fit after `abab` (the pattern wants `c`), so $k$ falls back from 4 to `pi[3]` = 2 and then the letter `a` does fit after `ab`, giving $k = 3$. At index 7, $k$ reaches 6, the pattern length, so there is an occurrence ending at index 7, starting at $7 - 6 + 1 = 2$. After that $k$ falls back to `pi[5]` = 1, and the next letter `b` makes it 2.

## 3.2 KMP in code

We write one function that returns all starting positions of the pattern in the text. From it you can read the first occurrence, or the number of occurrences.

```python
def border_table(s):
    pi = [0] * len(s)
    k = 0
    for i in range(1, len(s)):
        while k > 0 and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def kmp_positions(text, pattern):
    m = len(pattern)
    pi = border_table(pattern)
    found = []
    k = 0
    for i in range(len(text)):
        while k > 0 and text[i] != pattern[k]:
            k = pi[k - 1]
        if text[i] == pattern[k]:
            k += 1
        if k == m:
            found.append(i - m + 1)
            k = pi[k - 1]
    return found


assert kmp_positions("abababcab", "ababca") == [2]
assert kmp_positions("aaaa", "aa") == [0, 1, 2]
assert kmp_positions("abababa", "aba") == [0, 2, 4]
assert kmp_positions("leetcode", "leeto") == []
```

```cpp
vector<int> border_table(const string& s) {
    int n = s.size();
    vector<int> pi(n, 0);
    int k = 0;
    for (int i = 1; i < n; i++) {
        while (k > 0 && s[i] != s[k]) k = pi[k - 1];
        if (s[i] == s[k]) k++;
        pi[i] = k;
    }
    return pi;
}

vector<int> kmp_positions(const string& text, const string& pattern) {
    int m = pattern.size();
    vector<int> pi = border_table(pattern);
    vector<int> found;
    int k = 0;
    for (int i = 0; i < (int)text.size(); i++) {
        while (k > 0 && text[i] != pattern[k]) k = pi[k - 1];
        if (text[i] == pattern[k]) k++;
        if (k == m) {
            found.push_back(i - m + 1);
            k = pi[k - 1];
        }
    }
    return found;
}
```

The pattern must not be empty for this function (an empty pattern would make `pattern[k]` invalid). The cost is $O(m)$ to build the table and $O(n)$ for the scan, by the same argument as before: $k$ rises by at most one per text letter and every fall-back lowers it. The total is $O(n + m)$ time and $O(m)$ extra space.

## 3.3 Find the first occurrence

To find the position of the first occurrence, take the first element of the list, or $-1$ if it is empty. An empty pattern occurs at index 0 by convention. In a real solution you would also stop the scan right after the first match, but the idea is the same. This is exactly the problem _Find the Needle_.

```python
def first_occurrence(text, pattern):
    if pattern == "":
        return 0
    found = kmp_positions(text, pattern)
    return found[0] if found else -1


assert first_occurrence("sadbutsad", "sad") == 0
assert first_occurrence("leetcode", "leeto") == -1
assert first_occurrence("abc", "") == 0
assert first_occurrence("aaaaaaaaab", "aaab") == 6
```

```cpp
int first_occurrence(const string& text, const string& pattern) {
    if (pattern.empty()) return 0;
    vector<int> found = kmp_positions(text, pattern);
    return found.empty() ? -1 : found[0];
}
```

## 3.4 Counting overlapping occurrences

The same function counts occurrences, and it counts overlapping ones correctly. The reason is the fall-back after a full match: setting $k$ to `pi[m-1]`, the longest border of the whole pattern, is exactly where a second occurrence that overlaps the first one would have to continue. For the text `aaaa` and the pattern `aa` the table of the pattern is `[0, 1]`, so after every match $k$ becomes 1, and the matches are found at positions 0, 1, 2: three overlapping occurrences. This is exactly the problem _Count Overlapping Occurrences_.

```python
def count_matches(text, pattern):
    return len(kmp_positions(text, pattern))


assert count_matches("aaaa", "aa") == 3
assert count_matches("abababa", "aba") == 3
assert count_matches("abcabc", "abc") == 2
assert count_matches("", "a") == 0
```

```cpp
int count_matches(const string& text, const string& pattern) {
    return (int)kmp_positions(text, pattern).size();
}
```

Python's own `str.count` does _not_ count overlapping matches (`"aaaa".count("aa")` is 2), so we need our own function here. Time $O(n + m)$.

## 3.5 Check yourself

1. In the trace above, why does $k$ drop from 4 to 3 at text index 4 instead of going to 0?
2. After finding a full match, what does $k$ become, and why?
3. Why can the text pointer never move backwards in KMP?
4. What are the time and space costs of KMP in terms of $n$ and $m$?

# Chapter 4. Borders as periods

## 4.1 A border is a repeating pattern

Look at the string `"abcabcabc"`. It is the block `abc` written three times. Its longest border is `"abcabc"` (length 6): the first six letters equal the last six. The two copies overlap, and the amount by which the string is shifted is $9 - 6 = 3$, the size of the block.

This works in general. If a string of length $n$ has a border of length $b$, then the string is _periodic_ with **period** $n - b$: every letter equals the letter $n - b$ places before it. (Shifting the string by $n-b$ places lines it up with itself.) The smallest period belongs to the longest border, so:

$$\text{smallest period} = n - \text{pi}[n-1].$$

For `"abcabcabc"`, $\text{pi}[8] = 6$ and the period is $9 - 6 = 3$. For `"abcab"`, $\text{pi}[4] = 2$ and the period is $5 - 2 = 3$, but $3$ does not divide 5, so the string is not made of whole blocks (the last block is cut short).

## 4.2 Repeated substring pattern

A string is built from a whole block repeated two or more times exactly when its smallest period $p$ divides the length $n$ and $p < n$. (If $p = n$, the "block" is the whole string, repeated once.) So we compute the table and test:

- for `"abab"`: $\text{pi}[3] = 2$, period $2$, and $2$ divides $4$: yes, the block is `ab`;
- for `"abcab"`: period $3$ does not divide $5$: no;
- for `"aaa"`: $\text{pi}[2] = 2$, period $1$ divides $3$: yes, the block is `a`;
- for `"abc"`: period $3 = n$: no.

This is exactly the problem _Repeated Substring Pattern_.

```python
def border_table(s):
    pi = [0] * len(s)
    k = 0
    for i in range(1, len(s)):
        while k > 0 and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def is_repeated_block(s):
    n = len(s)
    if n < 2:
        return False
    period = n - border_table(s)[-1]
    return period < n and n % period == 0


assert is_repeated_block("abab")
assert is_repeated_block("aaa")
assert not is_repeated_block("abcab")
assert not is_repeated_block("abc")
assert not is_repeated_block("a")
```

```cpp
vector<int> border_table(const string& s) {
    int n = s.size();
    vector<int> pi(n, 0);
    int k = 0;
    for (int i = 1; i < n; i++) {
        while (k > 0 && s[i] != s[k]) k = pi[k - 1];
        if (s[i] == s[k]) k++;
        pi[i] = k;
    }
    return pi;
}

bool is_repeated_block(const string& s) {
    int n = s.size();
    if (n < 2) return false;
    int period = n - border_table(s).back();
    return period < n && n % period == 0;
}
```

Time and space $O(n)$.

## 4.3 Joining two strings with a separator

A neat trick: to compare a string with something else using the prefix function, glue the two strings together with a **separator** character that appears in neither string (we will use `#`). Then a border of the glued string can never be longer than the first part, because it cannot cross the `#`. So `pi` of `A + "#" + B` tells us, at each position of `B`, how much of the beginning of `A` ends there.

```python
def overlap_length(a, b):
    glued = a + "#" + b
    return border_table(glued)[-1]


assert overlap_length("abcd", "xyabc") == 3
assert overlap_length("abc", "xyz") == 0
assert overlap_length("aaa", "aaaa") == 3
```

```cpp
int overlap_length(const string& a, const string& b) {
    string glued = a + "#" + b;
    return border_table(glued).back();
}
```

The last value is the longest prefix of `a` that is also a suffix of `b`. (It is at most the length of `a` because of the separator.) We use this in the next section.

## 4.4 The shortest palindrome

Now a puzzle. You may add letters only **in front** of $s$. What is the shortest palindrome you can get? If $s$ = `"abcd"`, adding `dcb` in front gives `"dcbabcd"`. The idea: the longest prefix of $s$ that is already a palindrome can stay as it is, and the remaining tail must be mirrored in front. For `"aacecaaa"` the longest palindromic prefix is `"aacecaa"` (7 letters), the tail is `"a"`, and the answer is `"a" + "aacecaaa"`.

How do we find the longest palindromic prefix quickly? A prefix of $s$ is a palindrome exactly when it equals its own reverse, and its reverse is a _suffix_ of the reversed string $r$ = `s[::-1]`. So "the longest palindromic prefix of $s$" is "the longest prefix of $s$ that is also a suffix of $r$". That is the overlap from the previous section. We compute it with the prefix function of `s + "#" + r` and read the last value, call it `border`. The answer is `r`'s first `n - border` letters (the reversed tail), followed by $s$. For `"aacecaaa"` the glued string is `aacecaaa#aaacecaa`, its last prefix-function value is 7, so the tail is one letter. This is exactly the problem _Shortest Palindrome_.

```python
def shortest_palindrome_front(s):
    border = overlap_length(s, s[::-1])
    return s[border:][::-1] + s


assert shortest_palindrome_front("aacecaaa") == "aaacecaaa"
assert shortest_palindrome_front("abcd") == "dcbabcd"
assert shortest_palindrome_front("") == ""
assert shortest_palindrome_front("aba") == "aba"
```

```cpp
string shortest_palindrome_front(const string& s) {
    string r(s.rbegin(), s.rend());
    int border = overlap_length(s, r);
    string tail = s.substr(border);
    reverse(tail.begin(), tail.end());
    return tail + s;
}
```

The whole thing takes $O(n)$ time and $O(n)$ space.

## 4.5 Check yourself

1. What is the smallest period of `"abababab"`?
2. Why must the separator `#` be a character that is not in the strings?
3. Is `"abcabcab"` a repetition of a block? Explain with its period.
4. What is the shortest palindrome you can form from `"ab"` by adding letters in front?

# Chapter 5. The Z-function

## 5.1 A second view of the same idea

The prefix function looks at borders. The **Z-function** asks a slightly different question: for every position $i$, how many letters starting at $i$ agree with the beginning of the string? Formally, `z[i]` is the length of the longest common prefix of $s$ and the suffix that starts at $i$. By convention we leave `z[0] = 0`. For `"aabxaab"`:

```
 index :  0  1  2  3  4  5  6
 char  :  a  a  b  x  a  a  b
 z     :  0  1  0  0  3  1  0
```

At index 4 the suffix is `aab`, which agrees with `aab...` of the start for 3 letters, so `z[4] = 3`. At index 5 the suffix is `ab`; it agrees with `aa...` for only 1 letter (`a`), then `b` differs from `a`.

The direct way is to compare, for every $i$, letter by letter until a mismatch. That costs $O(n^2)$ on a string like `aaaa...a`.

## 5.2 The window trick

Like the prefix function, the Z-function can be computed in $O(n)$ by reusing earlier answers. We maintain a **window** `[l, r)`: among all positions seen so far, the one whose match reaches farthest to the right. Inside this window, the text is a copy of the beginning of the string: `s[l..r)` equals `s[0..r-l)`.

Now take a new position $i$. If $i$ is inside the window ($i < r$), then the letters from $i$ onwards, up to $r$, are copies of the letters from $i - l$ onwards at the start of the string. So `z[i]` is at least `min(r - i, z[i - l])`: we already know that many letters match, for free. We only need to keep comparing from there, and only if the guess reached the edge of the window. If $i$ is outside the window, we start from 0. Every time the comparison goes on, it goes past $r$, and so it makes $r$ larger. Since $r$ never moves left and never goes beyond $n$, the total number of comparisons that go beyond the window is at most $n$.

```
 s = a a b x a a b       building z, window shown as [l, r)
 i=1: outside window, compare:  a==a, then b!=a  -> z[1]=1, window [1,2)
 i=2: i=2 is not < r=2, outside, b!=a           -> z[2]=0
 i=3: x!=a                                      -> z[3]=0, window moves to [3,3)
 i=4: outside: a a b all match until the end    -> z[4]=3, window [4,7)
 i=5: inside, min(r-i, z[i-l]) = min(2, z[1]) = 1; then the next letters differ
 i=6: inside, min(1, z[2]) = 0; next letters differ
```

```python
def z_table(s):
    n = len(s)
    z = [0] * n
    left = right = 0
    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z


assert z_table("aabxaab") == [0, 1, 0, 0, 3, 1, 0]
assert z_table("aaaaa") == [0, 4, 3, 2, 1]
assert z_table("abc") == [0, 0, 0]
assert z_table("") == []
```

```cpp
vector<int> z_table(const string& s) {
    int n = s.size();
    vector<int> z(n, 0);
    int left = 0, right = 0;
    for (int i = 1; i < n; i++) {
        if (i < right) z[i] = min(right - i, z[i - left]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] > right) {
            left = i;
            right = i + z[i];
        }
    }
    return z;
}
```

This is exactly the problem _The Z-Function_. Time $O(n)$, space $O(n)$.

## 5.3 Searching with the Z-function

The Z-function can also search for a pattern, using the separator trick again. Build `pattern + "#" + text` and compute its Z-function. At a position inside the text part, `z` is the length of the match with the _pattern_ (the separator stops it from becoming longer than the pattern). So the pattern occurs at a text position exactly when `z` there equals the pattern length.

```python
def z_positions(text, pattern):
    m = len(pattern)
    z = z_table(pattern + "#" + text)
    return [i - m - 1 for i in range(m + 1, len(z)) if z[i] == m]


assert z_positions("abababa", "aba") == [0, 2, 4]
assert z_positions("aaaa", "aa") == [0, 1, 2]
assert z_positions("leetcode", "leeto") == []
```

```cpp
vector<int> z_positions(const string& text, const string& pattern) {
    int m = pattern.size();
    vector<int> z = z_table(pattern + "#" + text);
    vector<int> found;
    for (int i = m + 1; i < (int)z.size(); i++) {
        if (z[i] == m) found.push_back(i - m - 1);
    }
    return found;
}
```

It does the same job as KMP, in $O(n + m)$ time. Choose whichever one you find easier to remember. A rule of thumb: the Z-function is easier to _understand_ ("how far does the match from here go?"), the prefix function is easier to use for _periods and borders_.

## 5.4 Check yourself

1. What is the Z-function of `"abcabc"`?
2. When we compute `z[i]` and $i$ is inside the window, why can we start with `min(r - i, z[i - l])`?
3. Why do we add a separator when searching with the Z-function?
4. Why can the total number of comparisons that extend the window not exceed $n$?

# Chapter 6. Hashing: a number for a string

## 6.1 The idea

Comparing two long strings letter by letter costs time proportional to their length. What if each string had a short **fingerprint**, a single number that depends on all its letters, so that equal strings always have equal fingerprints? Then comparing two strings would take one comparison of two numbers. Such a fingerprint is a **hash** of the string.

A good way to build it is the **polynomial hash**. Read the string as digits of a number written in some base $b$, and take the remainder modulo a large number $m$ (the **modulus**) so that the result stays small:

$$H(s) = \left(s_0 b^{L-1} + s_1 b^{L-2} + \dots + s_{L-1}\right) \bmod m, \qquad L = |s|.$$

Here $s_i$ is a number for the letter (for example its code). To get a feel for it, forget the modulus for a moment, take base 10, and give the letters the values $a=1, b=2, c=3, \dots$. Then `"abc"` has the value $1\cdot 100 + 2\cdot 10 + 3 = 123$ and `"bcd"` has $234$.

If two different strings have the same hash, we call that a **collision**. Collisions cannot be avoided completely (there are more strings than numbers), but with a big modulus and a base chosen at random they are extremely unlikely. If the hashes differ, the strings are certainly different; if they are equal, the strings are _almost certainly_ equal.

## 6.2 Prefix hashes and substring hashes

The real power of this hash is that we can get the hash of **any substring** in constant time after one preparation pass. Build `h` where `h[i]` is the hash of the first $i$ letters: `h[0] = 0` and `h[i+1] = h[i] * b + s[i]`. Also precompute the powers of the base, `p[i] = b^i`.

Now, how do we get the hash of `s[l:r]`? The hash of the first $r$ letters, `h[r]`, contains the letters of `s[l:r]` at the end, but also the first $l$ letters, shifted left by $r - l$ places. Remove them:

$$H(s[l:r]) = h[r] - h[l] \cdot b^{\,r-l} \pmod m.$$

Check with the base-10 toy example: for `"abc"` the prefix values are `h = [0, 1, 12, 123]`. The hash of `"bc"` is $h[3] - h[1]\cdot 10^2 = 123 - 100 = 23$, which is indeed $2\cdot 10 + 3$.

We use the modulus $m = 2^{61} - 1$ (a large prime number). In Python, integers never overflow, so we can multiply freely. In C++ the product of two numbers below $2^{61}$ needs 122 bits, so we use the 128-bit type `__uint128_t` for the multiplication. We use a fixed base here so that the examples are reproducible; in a real contest program, pick the base at random so nobody can build a test against it.

```python
MOD = (1 << 61) - 1


class StringHash:
    def __init__(self, s, base=911382323):
        n = len(s)
        self.h = [0] * (n + 1)
        self.p = [1] * (n + 1)
        for i in range(n):
            self.h[i + 1] = (self.h[i] * base + ord(s[i])) % MOD
            self.p[i + 1] = self.p[i] * base % MOD

    def get(self, l, r):
        return (self.h[r] - self.h[l] * self.p[r - l]) % MOD


sh = StringHash("abcabc")
assert sh.get(0, 3) == sh.get(3, 6)
assert sh.get(0, 2) != sh.get(1, 3)
assert sh.get(2, 2) == 0
```

```cpp
typedef unsigned long long ull;
const ull MOD = (1ULL << 61) - 1;

ull mulmod(ull a, ull b) {
    return (ull)((__uint128_t)a * b % MOD);
}

struct StringHash {
    vector<ull> h, p;
    StringHash(const string& s, ull base = 911382323ULL) {
        int n = s.size();
        h.assign(n + 1, 0);
        p.assign(n + 1, 1);
        for (int i = 0; i < n; i++) {
            h[i + 1] = (mulmod(h[i], base) + (ull)(unsigned char)s[i]) % MOD;
            p[i + 1] = mulmod(p[i], base);
        }
    }
    ull get(int l, int r) const {
        return (h[r] + MOD - mulmod(h[l], p[r - l])) % MOD;
    }
};
```

After the $O(n)$ preparation, any substring hash costs $O(1)$.

## 6.3 Rabin-Karp: searching with hashes

Now searching becomes easy. Compute the hash of the pattern, then compute the hash of every window of length $m$ in the text (each in $O(1)$ with the prefix hashes) and report the windows whose hash equals the pattern's. This is the **Rabin-Karp** algorithm. The expected time is $O(n + m)$.

```python
def rabin_karp(text, pattern):
    m = len(pattern)
    if m == 0 or m > len(text):
        return []
    target = StringHash(pattern).get(0, m)
    th = StringHash(text)
    return [i for i in range(len(text) - m + 1) if th.get(i, i + m) == target]


assert rabin_karp("abababa", "aba") == [0, 2, 4]
assert rabin_karp("aaaa", "aa") == [0, 1, 2]
assert rabin_karp("leetcode", "leeto") == []
```

```cpp
vector<int> rabin_karp(const string& text, const string& pattern) {
    int n = text.size(), m = pattern.size();
    vector<int> found;
    if (m == 0 || m > n) return found;
    ull target = StringHash(pattern).get(0, m);
    StringHash th(text);
    for (int i = 0; i + m <= n; i++) {
        if (th.get(i, i + m) == target) found.push_back(i);
    }
    return found;
}
```

KMP never makes a mistake, while Rabin-Karp can be wrong with a probability of roughly $n / 2^{61}$, which for practical sizes is far smaller than the chance of a hardware error. The real advantage of hashing is that it solves problems where KMP does not apply, such as the next two sections.

## 6.4 Fixed-size windows: repeated DNA sequences

DNA is a string of the four letters `A`, `C`, `G`, `T`. Suppose we want all 10-letter sequences that appear more than once in a long DNA string. A window of 10 letters is short, so storing each window as a string in a set works. But hashing gives us a neat exact trick: since there are only 4 letters, give each a 2-bit code (`A=0, C=1, G=2, T=3`), and a window of 10 letters becomes a 20-bit number. Sliding the window by one letter is a shift: shift the number left by 2 bits, add the new letter, and cut off the bits that fell out of the window with a mask (`& (2^20 - 1)`). Because 20 bits describe all $4^{10}$ windows without clashes, this hash has **no collisions at all**.

We keep one set of numbers seen once and one set of numbers seen again. At the end we convert the repeated numbers back to letters (here we remember the starting index of the first window instead, and slice the text). This is exactly the problem _Repeated DNA Sequences_.

```python
def repeated_windows(s, size=10):
    code = {"A": 0, "C": 1, "G": 2, "T": 3}
    mask = (1 << (2 * size)) - 1
    value = 0
    first_seen = {}
    repeated = set()
    for i, ch in enumerate(s):
        value = ((value << 2) | code[ch]) & mask
        if i >= size - 1:
            start = i - size + 1
            if value in first_seen:
                repeated.add(s[start:start + size])
            else:
                first_seen[value] = start
    return sorted(repeated)


assert repeated_windows("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT") == ["AAAAACCCCC", "CCCCCAAAAA"]
assert repeated_windows("AAAAAAAAAAAAA") == ["AAAAAAAAAA"]
assert repeated_windows("ACGT") == []
assert repeated_windows("ACGTACGT", 4) == ["ACGT"]
```

```cpp
vector<string> repeated_windows(const string& s, int size = 10) {
    auto code = [](char c) { return c == 'A' ? 0 : c == 'C' ? 1 : c == 'G' ? 2 : 3; };
    long long mask = (1LL << (2 * size)) - 1;
    long long value = 0;
    unordered_map<long long, int> first_seen;
    set<string> repeated;
    for (int i = 0; i < (int)s.size(); i++) {
        value = ((value << 2) | code(s[i])) & mask;
        if (i >= size - 1) {
            int start = i - size + 1;
            if (first_seen.count(value)) repeated.insert(s.substr(start, size));
            else first_seen[value] = start;
        }
    }
    return vector<string>(repeated.begin(), repeated.end());
}
```

The time is $O(n)$ (each window is updated in constant time, and the window size is a fixed number), and the space is $O(n)$ for the sets.

## 6.5 Binary search on the length: longest repeated substring

Here is a harder question: what is the length of the **longest substring that occurs at least twice** in $s$ (the two copies may overlap)? For `"banana"` it is 3 (`"ana"`, at positions 1 and 3). This is exactly the problem _Longest Repeated Substring_.

Checking all lengths and all substrings is far too slow, but there is a monotone property to exploit: if some substring of length $L$ occurs twice, then its first $L - 1$ letters (a shorter substring) also occur twice. So "is there a repeated substring of length $L$?" is true for all small $L$ up to some limit, and false after it. That is exactly the shape that **binary search** can find: we search for the biggest $L$ for which the answer is "yes".

To answer one question "is there a repeated substring of length $L$?" quickly, hash every window of length $L$ with the prefix hashes and look for a repeated hash with a set. This takes $O(n)$ per question, and binary search needs $O(\log n)$ questions. The total is $O(n \log n)$.

```python
def longest_repeat_length(s):
    n = len(s)
    sh = StringHash(s)

    def has_repeat(length):
        seen = set()
        for i in range(n - length + 1):
            v = sh.get(i, i + length)
            if v in seen:
                return True
            seen.add(v)
        return False

    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if has_repeat(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo if n > 0 else 0


assert longest_repeat_length("banana") == 3
assert longest_repeat_length("abcd") == 0
assert longest_repeat_length("aaaa") == 3
assert longest_repeat_length("") == 0
```

```cpp
int longest_repeat_length(const string& s) {
    int n = s.size();
    if (n == 0) return 0;
    StringHash sh(s);
    auto has_repeat = [&](int length) {
        unordered_set<ull> seen;
        for (int i = 0; i + length <= n; i++) {
            ull v = sh.get(i, i + length);
            if (seen.count(v)) return true;
            seen.insert(v);
        }
        return false;
    };
    int lo = 0, hi = n - 1;
    while (lo < hi) {
        int mid = (lo + hi + 1) / 2;
        if (has_repeat(mid)) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}
```

Here `lo` is always a length known to work (0 trivially) and `hi` a length that might. When `has_repeat(mid)` is true we keep `mid`, otherwise we throw it away. A hash collision could report a repeat that is not real, but with a 61-bit modulus this is practically impossible. In Chapter 9 you will see a second, collision-free way to solve the same problem with a suffix array.

## 6.6 Check yourself

1. What is the base-10 toy hash of `"cab"` with $a=1, b=2, c=3$? (Compute $3\cdot 100 + 1\cdot 10 + 2$.)
2. Why is it fine that equal hashes do not _prove_ equal strings, but different hashes do prove different strings?
3. Why do we multiply `h[l]` by `p[r - l]` when extracting a substring hash?
4. Why does "is there a repeated substring of length $L$?" allow binary search?

# Chapter 7. Palindromes all at once: Manacher's algorithm

## 7.1 Counting palindromes around every centre

A **palindrome** reads the same forwards and backwards. Every palindrome has a _centre_: a letter (odd length, like `aba`) or the gap between two letters (even length, like `abba`). We want to know, for every centre, the biggest palindrome around it. Then we can count all the palindromic substrings, find the longest one, and answer many other questions.

The easy method expands outwards from each centre one pair of letters at a time. On a string like `aaaa...a` every expansion runs to the border of the string, and the total time is $O(n^2)$. **Manacher's algorithm** does it in $O(n)$ by noticing that palindromes are _mirror-symmetric_, so what we computed for a centre on the left side of a big palindrome tells us about the mirror centre on the right.

We use two arrays. `d1[i]` is the number of odd palindromes centred at the letter $i$ (equivalently, the radius including the centre letter). `d2[i]` is the number of even palindromes whose centre is the gap just before letter $i$. For `"aabaa"`:

```
 index :   0  1  2  3  4
 letter:   a  a  b  a  a
 d1    :   1  1  3  1  1      (at index 2: "b", "aba", "aabaa")
 d2    :   0  1  0  0  1      (before index 1: "aa"; before index 4: "aa")
```

The total number of palindromic substrings is $\sum d1 + \sum d2 = 7 + 2 = 9$: the five single letters, `aa` twice, `aba` and `aabaa`.

## 7.2 The mirror idea

Remember the **rightmost palindrome** we have found so far, as the window `[l, r]` (the palindrome that reaches farthest to the right). When we move to a new centre $i$ and $i \le r$, we are inside that palindrome, so $i$ has a mirror image $j = l + r - i$ on the left side. Everything to the left of the centre of the big palindrome is the reverse of what is to the right. Therefore the palindrome at $i$ is at least as large as the palindrome at $j$, as long as it stays inside `[l, r]`:

```
 window [l .................. r]
        ...j.....c.....i...         c = centre of the big palindrome
 d1[i] starts at min(d1[j], r - i + 1)
```

We cap the value by `r - i + 1` because beyond $r$ we know nothing (the mirror argument stops working). Then we try to extend the palindrome by comparing letters on both sides, but only the letters beyond $r$ need comparing, and every successful comparison moves $r$ to the right. As before, $r$ only increases and is at most $n$, so the total work is $O(n)$.

For even palindromes the same idea applies, but the mirror of the gap before $i$ is the gap before $l + r - i + 1$, hence the "+ 1" in the code.

## 7.3 Manacher in code

```python
def manacher(s):
    n = len(s)
    d1 = [0] * n
    l, r = 0, -1
    for i in range(n):
        k = 1 if i > r else min(d1[l + r - i], r - i + 1)
        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1
        d1[i] = k
        if i + k - 1 > r:
            l, r = i - k + 1, i + k - 1
    d2 = [0] * n
    l, r = 0, -1
    for i in range(n):
        k = 0 if i > r else min(d2[l + r - i + 1], r - i + 1)
        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1
        d2[i] = k
        if i + k - 1 > r:
            l, r = i - k, i + k - 1
    return d1, d2


assert manacher("aabaa") == ([1, 1, 3, 1, 1], [0, 1, 0, 0, 1])
assert manacher("abacaba")[0] == [1, 2, 1, 4, 1, 2, 1]
assert manacher("abacaba")[1] == [0, 0, 0, 0, 0, 0, 0]
assert manacher("") == ([], [])
```

```cpp
pair<vector<int>, vector<int>> manacher(const string& s) {
    int n = s.size();
    vector<int> d1(n, 0), d2(n, 0);
    for (int i = 0, l = 0, r = -1; i < n; i++) {
        int k = (i > r) ? 1 : min(d1[l + r - i], r - i + 1);
        while (i - k >= 0 && i + k < n && s[i - k] == s[i + k]) k++;
        d1[i] = k;
        if (i + k - 1 > r) {
            l = i - k + 1;
            r = i + k - 1;
        }
    }
    for (int i = 0, l = 0, r = -1; i < n; i++) {
        int k = (i > r) ? 0 : min(d2[l + r - i + 1], r - i + 1);
        while (i - k - 1 >= 0 && i + k < n && s[i - k - 1] == s[i + k]) k++;
        d2[i] = k;
        if (i + k - 1 > r) {
            l = i - k;
            r = i + k - 1;
        }
    }
    return {d1, d2};
}
```

## 7.4 Counting palindromic substrings fast

Now the count is a single sum. For `"abacaba"`, `d1` is `[1, 2, 1, 4, 1, 2, 1]` (sum 12) and `d2` is all zeros, so the string has 12 palindromic substrings. This is exactly the problem _Count Palindromic Substrings, Fast_.

```python
def count_all_palindromes(s):
    d1, d2 = manacher(s)
    return sum(d1) + sum(d2)


assert count_all_palindromes("aaa") == 6
assert count_all_palindromes("abc") == 3
assert count_all_palindromes("abacaba") == 12
assert count_all_palindromes("abbab") == 8
```

```cpp
long long count_all_palindromes(const string& s) {
    auto [d1, d2] = manacher(s);
    long long total = 0;
    for (int v : d1) total += v;
    for (int v : d2) total += v;
    return total;
}
```

Time $O(n)$, space $O(n)$. (The answer can be as large as about $n^2/2$, which is why the C++ total is a `long long`.)

## 7.5 The longest palindromic substring in linear time

The same arrays give the longest palindromic substring: an odd palindrome of radius `d1[i]` has length $2\,d1[i] - 1$ and starts at $i - d1[i] + 1$; an even palindrome with `d2[i]` has length $2\,d2[i]$ and starts at $i - d2[i]$. We take the longest, and on equal lengths the earliest start.

```python
def longest_palindrome_linear(s):
    d1, d2 = manacher(s)
    best_len, best_start = 0, 0
    for i in range(len(s)):
        for length, start in ((2 * d1[i] - 1, i - d1[i] + 1), (2 * d2[i], i - d2[i])):
            if length > best_len or (length == best_len and length > 0 and start < best_start):
                best_len, best_start = length, start
    return s[best_start:best_start + best_len]


assert longest_palindrome_linear("babad") == "bab"
assert longest_palindrome_linear("cbbd") == "bb"
assert longest_palindrome_linear("abacaba") == "abacaba"
assert longest_palindrome_linear("") == ""
```

```cpp
string longest_palindrome_linear(const string& s) {
    auto [d1, d2] = manacher(s);
    int best_len = 0, best_start = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        int lens[2] = {2 * d1[i] - 1, 2 * d2[i]};
        int starts[2] = {i - d1[i] + 1, i - d2[i]};
        for (int t = 0; t < 2; t++) {
            if (lens[t] > best_len || (lens[t] == best_len && lens[t] > 0 && starts[t] < best_start)) {
                best_len = lens[t];
                best_start = starts[t];
            }
        }
    }
    return s.substr(best_start, best_len);
}
```

## 7.6 Check yourself

1. What are `d1` and `d2` for the string `"aaa"`?
2. Why do we cap the starting value of `k` with `r - i + 1`?
3. Why is the total running time linear although there is a `while` loop inside the `for` loop?
4. How many palindromic substrings does `"abbab"` contain?

# Chapter 8. Smallest rotation

## 8.1 The problem

A **rotation** of a string moves some letters from the front to the back, so `"bca"` has the rotations `bca`, `cab`, `abc`. Among all rotations, which one comes first in dictionary order (the **lexicographically smallest**)? For `"bca"` it is `"abc"`; for `"cabcab"` it is `"abcabc"`.

The easy way is to build all $n$ rotations and take the minimum. That is $O(n^2)$ time, since each rotation is a string of length $n$.

```python
def smallest_rotation_slow(s):
    if not s:
        return ""
    return min(s[i:] + s[:i] for i in range(len(s)))


assert smallest_rotation_slow("bca") == "abc"
assert smallest_rotation_slow("cabcab") == "abcabc"
assert smallest_rotation_slow("") == ""
```

```cpp
string smallest_rotation_slow(const string& s) {
    int n = s.size();
    if (n == 0) return "";
    string best = s;
    for (int i = 1; i < n; i++) best = min(best, s.substr(i) + s.substr(0, i));
    return best;
}
```

## 8.2 Two candidates racing

Write the string twice, `t = s + s`, so that every rotation is a window of length $n$ of $t$ (we met this trick in the strings step). Keep two candidate start positions, `i` and `j`, and a counter `k` for how many letters we have compared so far. We compare `t[i + k]` and `t[j + k]`:

- if they are equal, increase `k`;
- if `t[i + k] > t[j + k]`, then the candidate `i` is worse than `j`. In fact, every start `i, i+1, ..., i+k` is worse than the corresponding start `j, j+1, ..., j+k` (they have the same first letters up to that point and then lose), so none of them can ever be the answer and we skip all of them: `i += k + 1`;
- if `t[i + k] < t[j + k]`, symmetric: `j += k + 1`.

After a skip we restart with `k = 0`, and we make sure `i` and `j` are different. When one of them goes past the end (index $n$ or more) or `k` reaches $n$ (the two candidates give the same rotation, which happens when the string is periodic), the smaller of the two is the answer. For `"bca"`, the doubled string is `bcabca`:

```
 i=0, j=1, k=0: b vs c -> b < c, so j loses: j += 1 -> j=2
 i=0, j=2, k=0: b vs a -> b > a, so i loses: i += 1 -> i=1
 i=1, j=2, k=0: c vs a -> c > a, so i loses: i += 1 -> i=2, equals j, so j=3
 j=3 is not < n=3, stop. The answer starts at min(i, j) = 2:  "abc"
```

Every skip moves `i` or `j` forward by at least one, and the pointers together never move beyond $2n$ steps, while each comparison step either increases `k` or triggers a skip that pays for the `k` comparisons we have done. So the time is $O(n)$ and the space is $O(n)$ for the doubled string. This is exactly the problem _Lexicographically Smallest Rotation_.

```python
def least_rotation(s):
    n = len(s)
    if n == 0:
        return ""
    t = s + s
    i, j, k = 0, 1, 0
    while i < n and j < n and k < n:
        a, b = t[i + k], t[j + k]
        if a == b:
            k += 1
            continue
        if a > b:
            i += k + 1
        else:
            j += k + 1
        if i == j:
            j += 1
        k = 0
    start = min(i, j)
    return t[start:start + n]


assert least_rotation("bca") == "abc"
assert least_rotation("cabcab") == "abcabc"
assert least_rotation("aaaa") == "aaaa"
assert least_rotation("") == ""
assert least_rotation("bbaaba") == smallest_rotation_slow("bbaaba")
```

```cpp
string least_rotation(const string& s) {
    int n = s.size();
    if (n == 0) return "";
    string t = s + s;
    int i = 0, j = 1, k = 0;
    while (i < n && j < n && k < n) {
        char a = t[i + k], b = t[j + k];
        if (a == b) {
            k++;
            continue;
        }
        if (a > b) i += k + 1;
        else j += k + 1;
        if (i == j) j++;
        k = 0;
    }
    int start = min(i, j);
    return t.substr(start, n);
}
```

## 8.3 Another route: Lyndon words

There is a second, beautiful way to solve the same problem. A **Lyndon word** is a non-empty string that is strictly smaller than all of its own rotations (equivalently, smaller than all its proper suffixes). `"aab"` and `"ab"` are Lyndon words, `"aba"` is not (its rotation `aab` is smaller), `"aa"` is not (a rotation equals it). A known theorem says every string can be cut into Lyndon words in exactly one way if we ask the pieces to be in non-increasing order: `"banana"` is `b`, `an`, `an`, `a`. This cutting is the **Lyndon factorization**, and **Duval's algorithm** finds it in $O(n)$ time.

For the smallest rotation: factorise `s + s` and take the start of the factor that begins in the first copy of $s$ and reaches into the second copy. That start is the beginning of the smallest rotation. Here is Duval's algorithm, with a small change that remembers where the current group of equal factors begins:

```python
def lyndon_factors(s):
    n = len(s)
    out = []
    i = 0
    while i < n:
        j, k = i + 1, i
        while j < n and s[k] <= s[j]:
            k = i if s[k] < s[j] else k + 1
            j += 1
        while i <= k:
            out.append(s[i:i + j - k])
            i += j - k
    return out


def least_rotation_lyndon(s):
    n = len(s)
    if n == 0:
        return ""
    t = s + s
    i, best = 0, 0
    while i < n:
        best = i
        j, k = i + 1, i
        while j < 2 * n and t[k] <= t[j]:
            k = i if t[k] < t[j] else k + 1
            j += 1
        while i <= k:
            i += j - k
    return t[best:best + n]


assert lyndon_factors("banana") == ["b", "an", "an", "a"]
assert lyndon_factors("abab") == ["ab", "ab"]
assert least_rotation_lyndon("bca") == "abc"
assert least_rotation_lyndon("cabcab") == "abcabc"
assert least_rotation_lyndon("bbaaba") == smallest_rotation_slow("bbaaba")
```

```cpp
vector<string> lyndon_factors(const string& s) {
    int n = s.size();
    vector<string> out;
    int i = 0;
    while (i < n) {
        int j = i + 1, k = i;
        while (j < n && s[k] <= s[j]) {
            k = (s[k] < s[j]) ? i : k + 1;
            j++;
        }
        while (i <= k) {
            out.push_back(s.substr(i, j - k));
            i += j - k;
        }
    }
    return out;
}

string least_rotation_lyndon(const string& s) {
    int n = s.size();
    if (n == 0) return "";
    string t = s + s;
    int i = 0, best = 0;
    while (i < n) {
        best = i;
        int j = i + 1, k = i;
        while (j < 2 * n && t[k] <= t[j]) {
            k = (t[k] < t[j]) ? i : k + 1;
            j++;
        }
        while (i <= k) i += j - k;
    }
    return t.substr(best, n);
}
```

Both methods are linear. The two-candidate version of the previous section is shorter and is the one to remember for the smallest rotation; Duval's algorithm is worth knowing because it solves a whole family of problems about Lyndon words.

## 8.4 Check yourself

1. What are all the rotations of `"abc"`, and which is the smallest?
2. In the two-candidate race, why can we skip all of `i, i+1, ..., i+k` after a loss?
3. What is the Lyndon factorization of `"aab"`?
4. What does it mean when `k` reaches `n` in the race?

# Chapter 9. Suffix arrays

## 9.1 Sorting all suffixes

The **suffix array** of a string $s$ answers: "if I write down all the suffixes of $s$ and sort them in dictionary order, where do they start?" The answer is a list of start positions. For `"banana"` the suffixes are:

```
 start 0: banana
 start 1: anana
 start 2: nana
 start 3: ana
 start 4: na
 start 5: a
```

Sorted in dictionary order: `a` (5), `ana` (3), `anana` (1), `banana` (0), `na` (4), `nana` (2). So the suffix array is `[5, 3, 1, 0, 4, 2]`. Having all suffixes in order is useful because strings that share a long beginning are _neighbours_ in the list, which makes searching, finding repeats and counting distinct pieces easy.

The simplest way to build it is to sort the start positions using the suffix itself as the key. This works, but each comparison can cost $O(n)$, so the total can be $O(n^2 \log n)$, and the copies of suffixes need $O(n^2)$ memory in Python.

```python
def suffix_array_slow(s):
    return sorted(range(len(s)), key=lambda i: s[i:])


assert suffix_array_slow("banana") == [5, 3, 1, 0, 4, 2]
assert suffix_array_slow("aaaa") == [3, 2, 1, 0]
assert suffix_array_slow("") == []
```

```cpp
vector<int> suffix_array_slow(const string& s) {
    int n = s.size();
    vector<int> sa(n);
    iota(sa.begin(), sa.end(), 0);
    sort(sa.begin(), sa.end(), [&](int a, int b) {
        return s.compare(a, string::npos, s, b, string::npos) < 0;
    });
    return sa;
}
```

## 9.2 Prefix doubling

The fast method sorts in rounds, each time looking at twice as many letters. Give every suffix a **rank**: its place in the order when only its first $k$ letters are used (suffixes with the same first $k$ letters get the same rank). To go from $k$ to $2k$ letters, notice that the first $2k$ letters of the suffix starting at $i$ are the first $k$ letters of suffix $i$ followed by the first $k$ letters of suffix $i + k$. So the pair `(rank[i], rank[i + k])` is a perfect key for comparing by $2k$ letters! If $i + k$ is beyond the end, the second part is "nothing", which should come before every letter, so we use $-1$.

Start with $k = 1$ (the rank is the letter itself) and keep doubling until all ranks are different, which needs at most about $\log_2 n$ rounds. Here is `"banana"`, listing the ranks of the suffixes starting at positions 0 to 5:

```
 after sorting by 2 letters:  order [5, 1, 3, 0, 2, 4]   ranks [2, 1, 3, 1, 3, 0]
     (ba=2, an=1, na=3, an=1, na=3, a=0:  suffixes 1 and 3 tie on "an", 2 and 4 tie on "na")
 after sorting by 4 letters:  order [5, 3, 1, 0, 4, 2]   ranks [3, 2, 5, 1, 4, 0]
     all ranks different: done. Suffix array = [5, 3, 1, 0, 4, 2]
```

```python
def suffix_array_doubling(s):
    n = len(s)
    if n == 0:
        return []
    rank = [ord(c) for c in s]
    sa = list(range(n))
    k = 1
    while True:
        def key(i):
            return (rank[i], rank[i + k] if i + k < n else -1)

        sa.sort(key=key)
        new_rank = [0] * n
        for t in range(1, n):
            new_rank[sa[t]] = new_rank[sa[t - 1]] + (key(sa[t - 1]) < key(sa[t]))
        rank = new_rank
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa


assert suffix_array_doubling("banana") == [5, 3, 1, 0, 4, 2]
assert suffix_array_doubling("aaaa") == [3, 2, 1, 0]
assert suffix_array_doubling("mississippi") == suffix_array_slow("mississippi")
assert suffix_array_doubling("") == []
```

```cpp
vector<int> suffix_array_doubling(const string& s) {
    int n = s.size();
    if (n == 0) return {};
    vector<int> sa(n), rnk(n), tmp(n);
    iota(sa.begin(), sa.end(), 0);
    for (int i = 0; i < n; i++) rnk[i] = (unsigned char)s[i];
    for (int k = 1;; k <<= 1) {
        auto key = [&](int i) {
            return make_pair(rnk[i], i + k < n ? rnk[i + k] : -1);
        };
        sort(sa.begin(), sa.end(), [&](int a, int b) { return key(a) < key(b); });
        tmp[sa[0]] = 0;
        for (int t = 1; t < n; t++) {
            tmp[sa[t]] = tmp[sa[t - 1]] + (key(sa[t - 1]) < key(sa[t]) ? 1 : 0);
        }
        rnk = tmp;
        if (rnk[sa[n - 1]] == n - 1) break;
    }
    return sa;
}
```

There are $O(\log n)$ rounds, and each round sorts $n$ pairs in $O(n \log n)$, so this takes $O(n \log^2 n)$ time and $O(n)$ memory, which is plenty for strings of tens of thousands of letters. This is exactly the problem _Suffix Array_. (If you need more speed, the sort of each round can be replaced by a counting sort, because the keys are small whole numbers; sorting first by the second part and then, stably, by the first part brings the total to $O(n \log n)$.)

## 9.3 The LCP array

Neighbours in the suffix array share long beginnings, and we can record exactly how long. The **LCP array** (longest common prefix) stores, for each neighbouring pair, the length of the common beginning. Let `lcp[t]` be the common prefix length of the suffixes `sa[t-1]` and `sa[t]` (with `lcp[0] = 0`). For `"banana"` the sorted suffixes `a, ana, anana, banana, na, nana` have neighbours sharing 1, 3, 0, 0 and 2 letters, so `lcp = [0, 1, 3, 0, 0, 2]`.

Computing every pair from scratch would be slow, but **Kasai's trick** uses one observation: if the suffix starting at $i$ has a common prefix of length $h$ with its predecessor in the order, then the suffix starting at $i + 1$ has a common prefix of at least $h - 1$ with _its_ predecessor (chop the first letter off both). So we process the suffixes in text order $i = 0, 1, 2, \dots$ and carry $h$ along, lowering it by one each step; in total $h$ can rise at most $2n$ times. The time is $O(n)$.

```python
def lcp_array(s, sa):
    n = len(s)
    rank = [0] * n
    for t, p in enumerate(sa):
        rank[p] = t
    lcp = [0] * n
    h = 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rank[i]] = h
            if h > 0:
                h -= 1
        else:
            h = 0
    return lcp


assert lcp_array("banana", [5, 3, 1, 0, 4, 2]) == [0, 1, 3, 0, 0, 2]
assert lcp_array("aaaa", [3, 2, 1, 0]) == [0, 1, 2, 3]
assert lcp_array("", []) == []
```

```cpp
vector<int> lcp_array(const string& s, const vector<int>& sa) {
    int n = s.size();
    vector<int> rnk(n), lcp(n, 0);
    for (int t = 0; t < n; t++) rnk[sa[t]] = t;
    int h = 0;
    for (int i = 0; i < n; i++) {
        if (rnk[i] > 0) {
            int j = sa[rnk[i] - 1];
            while (i + h < n && j + h < n && s[i + h] == s[j + h]) h++;
            lcp[rnk[i]] = h;
            if (h > 0) h--;
        } else {
            h = 0;
        }
    }
    return lcp;
}
```

## 9.4 What the two arrays tell us

With the suffix array and the LCP array, two classic questions are one line each.

The longest substring that occurs twice is the largest LCP value. If a substring occurs at two places, the two suffixes starting there both begin with it, and so does every suffix sorted between them; in particular two neighbours share it. Conversely, two neighbours that share $L$ letters show a substring of length $L$ occurring twice. For `"banana"` the largest value is 3 (`"ana"`), the same answer as with hashing in Chapter 6, but with no risk of collisions.

The number of **distinct** substrings: each suffix of length $L$ contributes $L$ prefixes, but those that it shares with the previous suffix in the order were already counted, so we subtract the LCP. In total the count is

$$\frac{n(n+1)}{2} - \sum_t \text{lcp}[t].$$

For `"banana"`: $21 - 6 = 15$.

```python
def suffix_array_facts(s):
    sa = suffix_array_doubling(s)
    lcp = lcp_array(s, sa)
    return max(lcp, default=0), len(s) * (len(s) + 1) // 2 - sum(lcp)


def distinct_by_brute(s):
    return len({s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)})


assert suffix_array_facts("banana") == (3, 15)
assert suffix_array_facts("aaaa") == (3, 4)
assert suffix_array_facts("abcd") == (0, 10)
assert suffix_array_facts("banana")[1] == distinct_by_brute("banana")
```

```cpp
pair<int, long long> suffix_array_facts(const string& s) {
    int n = s.size();
    vector<int> sa = suffix_array_doubling(s);
    vector<int> lcp = lcp_array(s, sa);
    int longest = 0;
    long long sum = 0;
    for (int v : lcp) {
        longest = max(longest, v);
        sum += v;
    }
    return {longest, (long long)n * (n + 1) / 2 - sum};
}
```

Together, the suffix array (about $O(n \log^2 n)$ with the simple method) and the LCP array (linear) give both answers without any hashing.

## 9.5 Check yourself

1. What is the suffix array of `"abab"`?
2. Why is the pair `(rank[i], rank[i + k])` enough to compare two suffixes by their first $2k$ letters?
3. What does the LCP array of a string tell us about the neighbours in the suffix array?
4. How many distinct substrings does `"aaa"` have, and how does the formula get it?

# Chapter 10. Splitting at the letters that are too rare

## 10.1 A different kind of trick

The last problem of this page is about letter counts. Given a string $s$ of lower-case letters and a number $k$, find the length of the longest substring in which **every letter that appears occurs at least $k$ times**. For `s = "aaabb"` and `k = 3` the answer is 3 (`"aaa"`, because in `"aaabb"` the letter `b` appears only twice). For `"ababbc"` and `k = 2` the answer is 5 (`"ababb"`, where `a` appears twice and `b` three times).

Checking every substring would cost $O(n^2)$ substrings times the counting cost, which is too slow. The key observation is about the letters that are **too rare**. Count the letters of the whole string. If a letter appears fewer than $k$ times in the whole string, no valid substring can contain it, because the substring can never have more copies than the whole string does. So such a letter is a _wall_: the answer lies entirely inside one of the pieces between walls.

## 10.2 Divide at the walls

This gives a clean recursion. For the current piece of the string, count its letters. If no letter is too rare, the whole piece is valid and its length is a candidate answer. Otherwise cut the piece at every too-rare letter and solve each part the same way; the answer is the best over the parts. After cutting at a rare letter, counts inside a part can drop, so new rare letters may appear and new cuts follow.

For `"ababbc"` with $k = 2$: the letter `c` appears once in total, so it is a wall. The left part is `"ababb"`: `a` twice and `b` three times, nothing is too rare, so the answer is its length, 5. For `"aaabb"` with $k = 3$: the letter `b` (twice) is a wall; the left part is `"aaa"` with `a` three times, so the answer is 3. This is exactly the problem _Longest Substring With Each Letter at Least K Times_.

How fast is it? Every time we cut, at least one of the 26 letters is removed from the piece for good (it was too rare, and it is gone), so the recursion is at most 26 levels deep. At each level the pieces together contain at most $n$ letters, which we count once. The total is $O(26\,n)$ time, plus $O(26)$ stack depth.

```python
def longest_all_frequent(s, k):
    def solve(lo, hi):
        if hi - lo < k:
            return 0
        counts = {}
        for i in range(lo, hi):
            counts[s[i]] = counts.get(s[i], 0) + 1
        rare = {ch for ch, c in counts.items() if c < k}
        if not rare:
            return hi - lo
        best = 0
        start = lo
        for i in range(lo, hi + 1):
            if i == hi or s[i] in rare:
                best = max(best, solve(start, i))
                start = i + 1
        return best

    return solve(0, len(s))


assert longest_all_frequent("aaabb", 3) == 3
assert longest_all_frequent("ababbc", 2) == 5
assert longest_all_frequent("abc", 2) == 0
assert longest_all_frequent("aaaa", 1) == 4
assert longest_all_frequent("", 1) == 0
```

```cpp
int solve_range(const string& s, int k, int lo, int hi) {
    if (hi - lo < k) return 0;
    int counts[26] = {0};
    for (int i = lo; i < hi; i++) counts[s[i] - 'a']++;
    bool rare[26];
    bool any_rare = false;
    for (int c = 0; c < 26; c++) {
        rare[c] = counts[c] > 0 && counts[c] < k;
        if (rare[c]) any_rare = true;
    }
    if (!any_rare) return hi - lo;
    int best = 0, start = lo;
    for (int i = lo; i <= hi; i++) {
        if (i == hi || rare[s[i] - 'a']) {
            best = max(best, solve_range(s, k, start, i));
            start = i + 1;
        }
    }
    return best;
}

int longest_all_frequent(const string& s, int k) {
    return solve_range(s, k, 0, (int)s.size());
}
```

## 10.3 A second way: a window with a fixed number of letters

Here is another route that does not recurse. Suppose we _decide in advance_ that the substring should contain exactly $u$ distinct letters, for $u = 1, 2, \dots, 26$. For a fixed $u$ we can slide a window over the string with two pointers: extend the right end, and if the window has more than $u$ distinct letters, shrink the left end until it has at most $u$. While sliding we track how many distinct letters the window has and how many of them already reach $k$ copies. Whenever the window has exactly $u$ distinct letters and all $u$ of them reach $k$, its length is a candidate. The answer is the best candidate over all 26 values of $u$.

```python
def longest_by_window(s, k):
    best = 0
    for u in range(1, 27):
        cnt = [0] * 26
        left = 0
        distinct = 0
        enough = 0
        for right in range(len(s)):
            c = ord(s[right]) - ord("a")
            if cnt[c] == 0:
                distinct += 1
            cnt[c] += 1
            if cnt[c] == k:
                enough += 1
            while distinct > u:
                d = ord(s[left]) - ord("a")
                if cnt[d] == k:
                    enough -= 1
                cnt[d] -= 1
                if cnt[d] == 0:
                    distinct -= 1
                left += 1
            if distinct == u and enough == u:
                best = max(best, right - left + 1)
    return best


assert longest_by_window("aaabb", 3) == 3
assert longest_by_window("ababbc", 2) == 5
assert longest_by_window("abc", 2) == 0
assert longest_by_window("aabbcc", 1) == 6
```

```cpp
int longest_by_window(const string& s, int k) {
    int best = 0, n = s.size();
    for (int u = 1; u <= 26; u++) {
        int cnt[26] = {0};
        int left = 0, distinct = 0, enough = 0;
        for (int right = 0; right < n; right++) {
            int c = s[right] - 'a';
            if (cnt[c] == 0) distinct++;
            cnt[c]++;
            if (cnt[c] == k) enough++;
            while (distinct > u) {
                int d = s[left] - 'a';
                if (cnt[d] == k) enough--;
                cnt[d]--;
                if (cnt[d] == 0) distinct--;
                left++;
            }
            if (distinct == u && enough == u) best = max(best, right - left + 1);
        }
    }
    return best;
}
```

Each of the 26 passes visits every letter at most twice, so this also takes $O(26\,n)$ time, with only $O(1)$ extra memory. Both versions are correct; the divide-at-the-walls version is shorter to explain, and the window version has no recursion. The same two-way thinking ("cut at what cannot appear" and "fix the number of distinct letters") shows up in many string problems.

## 10.4 Check yourself

1. In `"aabcc"` with $k = 2$, which letter is a wall, and what is the answer?
2. Why can a letter that is too rare in the whole string never be in a valid substring?
3. Why is the recursion at most 26 levels deep?
4. In the window version, why do we need to loop over $u$ from 1 to 26?

# Sources and credit

Ideas for the prefix function, the Z-function, string hashing and Rabin-Karp, Manacher's algorithm, the suffix array (prefix doubling and the LCP array) and the Lyndon factorization (including the smallest cyclic shift) were adapted from the articles of the same names on cp-algorithms.com (https://cp-algorithms.com). The text here was rewritten for beginners with new examples and traces, and the code was written separately. Like the original articles, this page is shared under the Creative Commons Attribution-ShareAlike 4.0 licence.
