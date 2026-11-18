> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Strings)

This page teaches you how to think about strings in coding problems: how to read them, build them, scan them, compare them and turn them into numbers and back. It assumes only that you can write a loop and a small function. A **string** is simply text stored as a row of characters, like `"hello"`, and almost every programme you will ever write touches one.

The page is a staircase. **Chapter 1 is gentle**: what a string is, how to look inside it, how to cut it into words. Each next chapter adds one new idea (a counter, runs of equal letters, two pointers, counting letters, rotations, numbers hidden in text, a zigzag pattern, very big numbers, and finally palindromes that grow from the middle), and the problems slowly get harder. By the last chapter you will be able to solve every string question of this step. Every code example is shown in Python and in C++, so pick whichever language you like.

# Chapter 1. Looking inside a string

## 1.1 A string is a row of characters

Think of a string as a row of boxes, each box holding one **character** (a letter, a digit, a space or a symbol). The boxes are numbered starting from 0. This number is called the **index** of the character. For `"hello"` the picture is:

```
 index:   0   1   2   3   4
 char:    h   e   l   l   o
 from end: -5  -4  -3  -2  -1   (Python only)
```

The length of the string is the number of boxes, here 5, so the last index is always `length - 1`. In Python `s[0]` is the first character and `s[-1]` is the last one. In C++ you write `s[0]` and `s.back()` (or `s[s.size() - 1]`). Reading an index that does not exist is a classic bug, so always ask yourself: "what if the string is empty?"

```python
def first_and_last(s):
    if len(s) == 0:
        return ""
    return s[0] + s[-1]


assert first_and_last("hello") == "ho"
assert first_and_last("a") == "aa"
assert first_and_last("") == ""
```

```cpp
string first_and_last(string s) {
    if (s.size() == 0) return "";
    return string(1, s[0]) + s.back();
}
```

One more fact that surprises beginners: in Python a string **cannot be changed in place**. You can read `s[0]`, but writing `s[0] = "j"` is an error. We say strings are **immutable**. To "change" a string you build a new one. In C++ a `string` can be changed in place (`s[0] = 'j'` works), but the habit of building a fresh result is still the safest one.

## 1.2 Slices and building new strings

A **slice** is a piece of a string. In Python `s[a:b]` means "the characters from index `a` up to but not including index `b`". So `"hello"[1:4]` is `"ell"`. In C++ the same thing is `s.substr(a, b - a)`: you give the start and the _length_. A slice with a step of -1, `s[::-1]`, reads the string backwards.

Often we build a result letter by letter. In Python the clean way is to collect the pieces in a list and join them once at the end with `"".join(pieces)`. (Gluing with `+=` inside a loop can copy the whole string again and again.) In C++ `result += ch` is already efficient.

```python
def middle(s):
    if len(s) < 2:
        return ""
    return s[1:-1]


def double_letters(s):
    pieces = []
    for ch in s:
        pieces.append(ch)
        pieces.append(ch)
    return "".join(pieces)


assert middle("hello") == "ell"
assert middle("a") == ""
assert double_letters("abc") == "aabbcc"
assert "hello"[::-1] == "olleh"
```

```cpp
string middle(string s) {
    if (s.size() < 2) return "";
    return s.substr(1, s.size() - 2);
}

string double_letters(string s) {
    string result;
    for (char ch : s) {
        result += ch;
        result += ch;
    }
    return result;
}
```

Both functions visit each character once, so they take $O(n)$ time for a string of length $n$.

## 1.3 Words and the reverse-words problem

A **word** is a run of characters that are not spaces. Many problems say "split the sentence into words", and extra spaces make this fiddly: `"  hello   world  "` still has just two words. The safe way is to walk through the string with a position `i`, skip spaces, then read until the next space.

```python
def words_of(s):
    words = []
    i, n = 0, len(s)
    while i < n:
        while i < n and s[i] == " ":
            i += 1
        start = i
        while i < n and s[i] != " ":
            i += 1
        if i > start:
            words.append(s[start:i])
    return words


assert words_of("  hello   world  ") == ["hello", "world"]
assert words_of("") == []
assert words_of("one") == ["one"]
```

```cpp
vector<string> words_of(string s) {
    vector<string> words;
    int i = 0, n = s.size();
    while (i < n) {
        while (i < n && s[i] == ' ') i++;
        int start = i;
        while (i < n && s[i] != ' ') i++;
        if (i > start) words.push_back(s.substr(start, i - start));
    }
    return words;
}
```

Now reversing the order of the words is easy: take the list, turn it around and glue the words together with a single space between them. This is exactly the problem _Reverse the Words_. (Python's built-in `s.split()` does what `words_of` does in one call, and `" ".join(...)` glues the words.)

```python
def reverse_sentence(s):
    words = words_of(s)
    words.reverse()
    return " ".join(words)


assert reverse_sentence("the sky is blue") == "blue is sky the"
assert reverse_sentence("  hello   world  ") == "world hello"
assert reverse_sentence("") == ""
```

```cpp
string reverse_sentence(string s) {
    vector<string> words = words_of(s);
    reverse(words.begin(), words.end());
    string result;
    for (int i = 0; i < (int)words.size(); i++) {
        if (i > 0) result += ' ';
        result += words[i];
    }
    return result;
}
```

The time and space are $O(n)$: each character is looked at a constant number of times and copied once into the answer.

## 1.4 Comparing column by column

The **prefix** of a string is its beginning: `"flo"` is a prefix of `"flower"`. To find the longest prefix shared by several words, imagine writing the words under each other and reading the picture **column by column**:

```
 f l o w e r
 f l o w
 f l i g h t
 ^ ^ ^
 same same differ -> stop
```

Column 0 is `f` in every word, column 1 is `l` in every word, but column 2 has `o`, `o`, `i`. So the answer is the first two columns: `"fl"`. We stop at the first column where some word is too short or has a different letter. Using the first word as the reference, the code is two small loops. This is exactly the problem _Longest Common Prefix_.

```python
def common_prefix(words):
    if len(words) == 0:
        return ""
    first = words[0]
    for i in range(len(first)):
        for w in words:
            if i >= len(w) or w[i] != first[i]:
                return first[:i]
    return first


assert common_prefix(["flower", "flow", "flight"]) == "fl"
assert common_prefix(["dog", "car"]) == ""
assert common_prefix(["same"]) == "same"
assert common_prefix([]) == ""
```

```cpp
string common_prefix(vector<string> words) {
    if (words.size() == 0) return "";
    string first = words[0];
    for (int i = 0; i < (int)first.size(); i++) {
        for (const string& w : words) {
            if (i >= (int)w.size() || w[i] != first[i]) return first.substr(0, i);
        }
    }
    return first;
}
```

In the worst case we look at every character of every word once, so the time is $O(S)$ where $S$ is the total number of characters. The extra space is only the answer.

## 1.5 Check yourself

1. What is the index of the last character of a string of length 7?
2. What does `"abcdef"[2:5]` give in Python, and what is the matching `substr` call in C++?
3. Why is the string `"  a  b "` made of exactly two words?
4. When comparing words column by column, when do you stop?

# Chapter 2. One pass with a counter

## 2.1 Keeping a running number

Many string problems can be solved by walking through the characters once while keeping a **counter**, a number we change as we go. The counter remembers just enough about everything we have seen so far.

The first example: how deeply are parentheses nested? Every `(` opens a new level and every `)` closes one. So the counter `depth` goes up by one on `(` and down by one on `)`. The answer is the largest value that `depth` ever reaches, so we keep a second variable `best`. Here is the string `(1+(2*3)+((8)/4))+1` and the depth after each character:

```
 char : ( 1 + ( 2 * 3 ) + ( ( 8 ) / 4 ) ) + 1
 depth: 1 1 1 2 2 2 2 1 1 2 3 3 2 2 2 1 0 0 0
```

The highest value is 3, so the answer is 3. This is exactly the problem _Maximum Nesting Depth_.

```python
def deepest_level(s):
    depth = 0
    best = 0
    for ch in s:
        if ch == "(":
            depth += 1
            if depth > best:
                best = depth
        elif ch == ")":
            depth -= 1
    return best


assert deepest_level("(1+(2*3)+((8)/4))+1") == 3
assert deepest_level("abc") == 0
assert deepest_level("()()") == 1
```

```cpp
int deepest_level(string s) {
    int depth = 0, best = 0;
    for (char ch : s) {
        if (ch == '(') {
            depth++;
            best = max(best, depth);
        } else if (ch == ')') {
            depth--;
        }
    }
    return best;
}
```

One pass, so $O(n)$ time and $O(1)$ extra space.

## 2.2 When the counter cannot go below zero

What if the parentheses are not balanced, like `"())(("`? We want the smallest number of parentheses to insert so that every `(` has a `)` after it. Keep a counter `open_count` of how many `(` are still waiting for a partner. When we see `)`, there are two cases. If something is waiting (`open_count > 0`), the `)` closes it. If nothing is waiting, this `)` can never be matched by anything before it, so we must insert a `(` in front of it: we add one to `need`.

At the end, every `(` still waiting needs a `)` inserted after it. Tracing `"())(("`:

```
 char   open_count   need
  (         1         0
  )         0         0
  )         0         1    nothing waiting -> one "(" must be inserted
  (         1         1
  (         2         1
```

At the end we have 2 unmatched `(` waiting and `need = 1`, so the answer is $1 + 2 = 3$. This is exactly the problem _Minimum Insertions to Balance Parentheses_. It is correct because each insertion fixes exactly one unmatched bracket, and we never matched a bracket that could not be matched.

```python
def insertions_needed(s):
    open_count = 0
    need = 0
    for ch in s:
        if ch == "(":
            open_count += 1
        elif open_count > 0:
            open_count -= 1
        else:
            need += 1
    return need + open_count


assert insertions_needed("())") == 1
assert insertions_needed("(((") == 3
assert insertions_needed("())((") == 3
assert insertions_needed("") == 0
```

```cpp
int insertions_needed(string s) {
    int open_count = 0, need = 0;
    for (char ch : s) {
        if (ch == '(') {
            open_count++;
        } else if (open_count > 0) {
            open_count--;
        } else {
            need++;
        }
    }
    return need + open_count;
}
```

Time $O(n)$, space $O(1)$.

## 2.3 Using the counter to decide what to keep

Sometimes the counter is not the answer but a tool to make a decision for each character. Take a valid string of parentheses such as `(()())(())`. It splits into **primitive groups**, the shortest balanced pieces: `(()())` and `(())`. We want to delete the outermost pair of each group.

Which brackets are outermost? An opening bracket is outermost when the depth _before_ it is 0. A closing bracket is outermost when the depth _after_ it is 0. So we keep every other bracket:

```
 char:   (   (   )   (   )   )   (   (   )   )
 depth:  0   1   1   1   1   0   0   1   1   0     (depth before "(" / after ")")
 keep:   no  yes yes yes yes no  no  yes yes no
```

Keeping the "yes" columns gives `()()` and `()`, joined to `()()()`. This is exactly the problem _Remove Outer Parentheses_.

```python
def strip_outer(s):
    kept = []
    depth = 0
    for ch in s:
        if ch == "(":
            if depth > 0:
                kept.append(ch)
            depth += 1
        else:
            depth -= 1
            if depth > 0:
                kept.append(ch)
    return "".join(kept)


assert strip_outer("(()())(())") == "()()()"
assert strip_outer("()()") == ""
assert strip_outer("((()))") == "(())"
```

```cpp
string strip_outer(string s) {
    string kept;
    int depth = 0;
    for (char ch : s) {
        if (ch == '(') {
            if (depth > 0) kept += ch;
            depth++;
        } else {
            depth--;
            if (depth > 0) kept += ch;
        }
    }
    return kept;
}
```

Notice the order: for `(` we test the depth first and then increase it, for `)` we decrease first and then test. That order is the whole trick. Time $O(n)$.

## 2.4 Scanning from the end

You do not have to scan from the left. Suppose `num` is a string of digits and you want the **largest odd number** that appears as a substring (a run of consecutive characters). A number is odd exactly when its last digit is odd. So a candidate must end at an odd digit. Among all candidates, a longer one is larger (it has more digits, assuming no leading zeros), and the longest candidate starts at the very front of `num`. So the best answer is the prefix of `num` that stops at the **last** odd digit.

For `"35427"` the last digit `7` is odd, so the answer is the whole string. For `"4206"` there is no odd digit, so the answer is `""`. For `"52"` we scan from the right: `2` is even, `5` is odd, so we cut after the `5` and get `"5"`. This is exactly the problem _Largest Odd Number in a String_.

```python
def last_odd_prefix(num):
    for i in range(len(num) - 1, -1, -1):
        if num[i] in "13579":
            return num[:i + 1]
    return ""


assert last_odd_prefix("52") == "5"
assert last_odd_prefix("4206") == ""
assert last_odd_prefix("35427") == "35427"
assert last_odd_prefix("3542") == "35"
```

```cpp
string last_odd_prefix(string num) {
    for (int i = (int)num.size() - 1; i >= 0; i--) {
        if (num[i] == '1' || num[i] == '3' || num[i] == '5' || num[i] == '7' || num[i] == '9') {
            return num.substr(0, i + 1);
        }
    }
    return "";
}
```

Time $O(n)$ (and usually much less, since we stop at the first odd digit from the right).

## 2.5 Check yourself

1. In `deepest_level`, why do we update `best` only after a `(`?
2. In `insertions_needed("))")`, what is `need` at the end?
3. Why does `strip_outer` test the depth before increasing it on `(`?
4. Why does a number stay odd or even depending only on its last digit?

# Chapter 3. Runs of equal letters

## 3.1 What a run is

A **run** is a stretch of the same character repeated: in `"aabcccccaaa"` the runs are `aa`, `b`, `ccccc` and `aaa`. Seeing a string as a list of runs is useful whenever a problem talks about "repeated characters" or "how many in a row".

To walk over runs we use two positions. `i` marks where the current run starts. We move `j` to the right while `s[j]` equals `s[i]`. When `j` stops, the run is `s[i:j]` and its length is `j - i`. Then the next run starts at `j`, so we set `i = j`. Each character is passed over by `j` exactly once, so the whole walk is $O(n)$.

```
 s = a a b c c c
     i j           s[j] == s[i], move j
     i   j         s[j] != s[i]  -> run "aa", length 2
         i j       next run starts here
```

## 3.2 Compressing runs

Write each run as the character followed by its length, and skip the length when it is 1. So `"aabcccccaaa"` becomes `"a2bc5a3"`. This is exactly the problem _Compress Repeated Characters_.

```python
def squeeze(s):
    out = []
    i = 0
    n = len(s)
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        out.append(s[i])
        if j - i > 1:
            out.append(str(j - i))
        i = j
    return "".join(out)


assert squeeze("aabcccccaaa") == "a2bc5a3"
assert squeeze("abc") == "abc"
assert squeeze("") == ""
assert squeeze("zzzzzzzzzzzz") == "z12"
```

```cpp
string squeeze(string s) {
    string out;
    int i = 0, n = s.size();
    while (i < n) {
        int j = i;
        while (j < n && s[j] == s[i]) j++;
        out += s[i];
        if (j - i > 1) out += to_string(j - i);
        i = j;
    }
    return out;
}
```

Time $O(n)$, space $O(n)$ for the answer. Note that a run of length 12 is written with two digits, `12`, which is why we convert the number to text with `str` (Python) or `to_string` (C++).

## 3.3 Reading a string aloud

Here is a playful use of the same loop. The **count-and-say** sequence starts with `"1"`. To get the next term, read the previous term aloud, run by run: "how many, then which digit". The term `"1"` is "one 1", so the next term is `"11"`. That is "two 1s", so the next is `"21"`. That is "one 2, one 1", so `"1211"`, and so on. The first terms, computed by running the code, are:

```
 term 1: 1
 term 2: 11
 term 3: 21
 term 4: 1211
 term 5: 111221
 term 6: 312211
 term 7: 13112221
```

The loop over runs is the same as before, but now we always write the length first and then the digit (even when the length is 1). We apply that step $n - 1$ times. This is exactly the problem _Count and Say_.

```python
def say_once(term):
    out = []
    i = 0
    n = len(term)
    while i < n:
        j = i
        while j < n and term[j] == term[i]:
            j += 1
        out.append(str(j - i))
        out.append(term[i])
        i = j
    return "".join(out)


def say_term(n):
    term = "1"
    for _ in range(n - 1):
        term = say_once(term)
    return term


assert say_once("1") == "11"
assert say_once("21") == "1211"
assert say_term(5) == "111221"
assert say_term(7) == "13112221"
```

```cpp
string say_once(string term) {
    string out;
    int i = 0, n = term.size();
    while (i < n) {
        int j = i;
        while (j < n && term[j] == term[i]) j++;
        out += to_string(j - i);
        out += term[i];
        i = j;
    }
    return out;
}

string say_term(int n) {
    string term = "1";
    for (int k = 1; k < n; k++) term = say_once(term);
    return term;
}
```

Each step costs time proportional to the length of the current term, and the terms grow by a factor of about 1.3 each step, so the total work is about the length of the last term. Only the first few dozen terms are ever asked for.

## 3.4 Check yourself

1. What is the run structure of `"aaabccdd"`?
2. Why do we set `i = j` after each run?
3. What is the compressed form of `"abbbbbbbbbbbb"` (one `a`, twelve `b`)?
4. Reading `"312211"` aloud, run by run, what is the next count-and-say term?

# Chapter 4. Two pointers from both ends

## 4.1 Palindromes with two fingers

A **palindrome** is a string that reads the same forwards and backwards, like `"level"` or `"abba"`. The easiest check uses two **pointers** (two index variables). Put one finger `i` on the first character and another finger `j` on the last. If `s[i]` and `s[j]` differ, the string is not a palindrome. If they are equal, move both fingers one step towards the middle and repeat. If the fingers meet or cross, every pair matched, so it is a palindrome.

```
 l e v e l
 i       j     l == l, ok
   i   j       e == e, ok
     ij        met in the middle -> palindrome
```

```python
def is_palindrome(s):
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True


assert is_palindrome("level")
assert is_palindrome("abba")
assert not is_palindrome("abca")
assert is_palindrome("")
```

```cpp
bool is_palindrome(string s) {
    int i = 0, j = (int)s.size() - 1;
    while (i < j) {
        if (s[i] != s[j]) return false;
        i++;
        j--;
    }
    return true;
}
```

Time $O(n)$ (at most $n/2$ comparisons), space $O(1)$. A shortcut in Python is `s == s[::-1]`, but it builds a whole reversed copy; the two-finger version uses no extra space.

## 4.2 Skipping characters we do not care about

Real texts are messy: `"A man, a plan, a canal: Panama"` is a palindrome only if we ignore spaces, commas and capital letters. We keep the same two fingers, with two extra rules. If the left finger is on something that is not a letter or digit, move it right without comparing. If the right finger is on such a character, move it left. Only when both fingers sit on letters or digits do we compare them, ignoring the case. This is exactly the problem _Valid Palindrome_.

```python
def is_clean_palindrome(s):
    i, j = 0, len(s) - 1
    while i < j:
        if not s[i].isalnum():
            i += 1
        elif not s[j].isalnum():
            j -= 1
        elif s[i].lower() != s[j].lower():
            return False
        else:
            i += 1
            j -= 1
    return True


assert is_clean_palindrome("A man, a plan, a canal: Panama")
assert not is_clean_palindrome("race a car")
assert is_clean_palindrome(".,")
```

```cpp
bool is_clean_palindrome(string s) {
    int i = 0, j = (int)s.size() - 1;
    while (i < j) {
        if (!isalnum((unsigned char)s[i])) {
            i++;
        } else if (!isalnum((unsigned char)s[j])) {
            j--;
        } else if (tolower((unsigned char)s[i]) != tolower((unsigned char)s[j])) {
            return false;
        } else {
            i++;
            j--;
        }
    }
    return true;
}
```

Every step moves at least one finger, so the time is $O(n)$ and the space is $O(1)$. We avoided creating a cleaned-up copy of the string, which is the other common way to do it.

## 4.3 Swapping from both ends

The same two fingers can also **swap**. Suppose we want to reverse only the vowels (`a e i o u`, either case) and leave all other characters where they are. Move the left finger right until it stands on a vowel, move the right finger left until it stands on a vowel, swap the two, and continue. In `"hello"` the vowels are `e` and `o`; swapping them gives `"holle"`. This is exactly the problem _Reverse the Vowels_.

Since Python strings cannot be changed, we first turn the string into a list of characters, swap inside the list and join at the end.

```python
def is_vowel(ch):
    return ch in "aeiouAEIOU"


def flip_vowels(s):
    chars = list(s)
    i, j = 0, len(chars) - 1
    while i < j:
        if not is_vowel(chars[i]):
            i += 1
        elif not is_vowel(chars[j]):
            j -= 1
        else:
            chars[i], chars[j] = chars[j], chars[i]
            i += 1
            j -= 1
    return "".join(chars)


assert flip_vowels("hello") == "holle"
assert flip_vowels("leetcode") == "leotcede"
assert flip_vowels("xyz") == "xyz"
```

```cpp
bool is_vowel(char ch) {
    return string("aeiouAEIOU").find(ch) != string::npos;
}

string flip_vowels(string s) {
    int i = 0, j = (int)s.size() - 1;
    while (i < j) {
        if (!is_vowel(s[i])) {
            i++;
        } else if (!is_vowel(s[j])) {
            j--;
        } else {
            swap(s[i], s[j]);
            i++;
            j--;
        }
    }
    return s;
}
```

Time $O(n)$, space $O(n)$ in Python for the list (the C++ version changes its own copy). The pattern "two fingers moving inwards, skipping what does not matter" appears again and again; remember it.

## 4.4 Check yourself

1. When do the two fingers stop in `is_palindrome`?
2. In `is_clean_palindrome`, why do we not compare when a finger sits on a comma?
3. After swapping two vowels, why do we move both fingers?
4. Is `"Madam"` a palindrome if we ignore the case?

# Chapter 5. Counting letters and sorting with a key

## 5.1 Counting with a table

To answer "how many times does each character appear?", keep a table with one cell per possible character and add one to the right cell for each character you read. When the text has only lower-case letters, there are 26 possible characters and a plain list works: the cell for `'a'` is index 0, for `'b'` index 1, and so on. The index of a letter is `ord(ch) - ord('a')` in Python and `ch - 'a'` in C++. (`ord` gives the number that a computer uses for a character; letters are numbered in alphabetical order, so subtracting the number of `'a'` gives 0 to 25.)

```python
def letter_counts(s):
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - ord("a")] += 1
    return counts


def are_anagrams(a, b):
    return letter_counts(a) == letter_counts(b)


assert letter_counts("banana")[0] == 3
assert letter_counts("banana")[1] == 1
assert letter_counts("banana")[13] == 2
assert are_anagrams("listen", "silent")
assert not are_anagrams("abc", "abd")
```

```cpp
vector<int> letter_counts(string s) {
    vector<int> counts(26, 0);
    for (char ch : s) counts[ch - 'a']++;
    return counts;
}

bool are_anagrams(string a, string b) {
    return letter_counts(a) == letter_counts(b);
}
```

Two words are **anagrams** (rearrangements of each other) exactly when their count tables are equal. Counting takes $O(n)$ time and $O(1)$ space, because the table always has 26 cells. If the characters can be anything (spaces, capitals, symbols), use a dictionary in Python (`counts[ch] = counts.get(ch, 0) + 1`) or a `map<char, int>` in C++ instead of a fixed list.

## 5.2 Sorting by something other than the value

Often we want to sort items not by themselves but by some measurement of them, called a **key**. You can sort words by length, people by age, letters by how often they appear. Python's `sorted(items, key=...)` and C++'s `sort` with a comparison function both do this.

Two keys at once are common: "first by this, and if there is a tie, by that". In Python a key can be a pair `(a, b)`, which Python compares first by `a`, then by `b`. For example, to sort words by length and then alphabetically, use `key=lambda w: (len(w), w)`. A minus sign in front of a number reverses its order, so `(-count, letter)` means "larger count first, then smaller letter first".

```python
def sort_words(words):
    return sorted(words, key=lambda w: (len(w), w))


def letters_by_frequency(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    return sorted(counts, key=lambda ch: (-counts[ch], ch))


assert sort_words(["pear", "fig", "apple", "kiwi"]) == ["fig", "kiwi", "pear", "apple"]
assert letters_by_frequency("tree") == ["e", "r", "t"]
assert letters_by_frequency("cccaaa") == ["a", "c"]
```

```cpp
vector<string> sort_words(vector<string> words) {
    sort(words.begin(), words.end(), [](const string& a, const string& b) {
        if (a.size() != b.size()) return a.size() < b.size();
        return a < b;
    });
    return words;
}

vector<char> letters_by_frequency(string s) {
    map<char, int> counts;
    for (char ch : s) counts[ch]++;
    vector<char> letters;
    for (auto& kv : counts) letters.push_back(kv.first);
    sort(letters.begin(), letters.end(), [&](char a, char b) {
        if (counts[a] != counts[b]) return counts[a] > counts[b];
        return a < b;
    });
    return letters;
}
```

Sorting $k$ distinct letters costs $O(k \log k)$, and counting costs $O(n)$.

## 5.3 Sorting the characters of a string

Now we can solve _Sort Characters by Frequency_. The statement asks for a string in which equal characters sit together, with the most frequent character first and ties broken alphabetically. In `"tree"` the letter `e` appears twice and `r`, `t` once, so the answer is `"eert"`.

The plan has three steps, and you have already seen each of them. First count how often each character appears. Second, order the distinct characters with the key `(-count, character)`, exactly like `letters_by_frequency` above. Third, walk through that order and write each character as many times as its count: a letter with count 3 is written three times in a row (in Python `ch * count`, in C++ `out.append(count, ch)`). Because we write the groups directly, we never sort the long string itself, so the cost is $O(n + k \log k)$ where $k \le n$ is the number of distinct characters.

## 5.4 Check yourself

1. Which table index does the letter `'d'` get?
2. Why are `"abc"` and `"cab"` anagrams but `"aab"` and `"abb"` not?
3. What does the key `(-count, ch)` do when two letters have the same count?
4. How many cells does the count table need if the string is made of lower-case letters only?

# Chapter 6. Rotations and the doubled string

## 6.1 What a rotation is

To **rotate** a string, take some characters from the front and move them to the back, keeping their order. Rotating `"abcde"` by 2 moves `"ab"` to the back and gives `"cdeab"`. Rotating by 0 changes nothing, and rotating by the full length also changes nothing.

```python
def rotate_left(s, k):
    return s[k:] + s[:k]


assert rotate_left("abcde", 2) == "cdeab"
assert rotate_left("abcde", 0) == "abcde"
assert rotate_left("abcde", 5) == "abcde"
```

```cpp
string rotate_left(string s, int k) {
    return s.substr(k) + s.substr(0, k);
}
```

A string of length $n$ has at most $n$ different rotations (one for each $k$ from 0 to $n-1$). The question "is `goal` a rotation of `s`?" can be answered the slow way: try all $n$ rotations and compare each with `goal`. That costs $O(n^2)$ time, since each rotation is a string of length $n$ to build and compare.

```python
def is_rotation_slow(s, goal):
    if len(s) != len(goal):
        return False
    for k in range(max(1, len(s))):
        if rotate_left(s, k) == goal:
            return True
    return False


assert is_rotation_slow("abcde", "cdeab")
assert not is_rotation_slow("abcde", "abced")
assert is_rotation_slow("", "")
```

```cpp
bool is_rotation_slow(string s, string goal) {
    if (s.size() != goal.size()) return false;
    for (int k = 0; k < max(1, (int)s.size()); k++) {
        if (rotate_left(s, k) == goal) return true;
    }
    return false;
}
```

## 6.2 The doubling trick

Here is a lovely idea. Write the string twice in a row: `"abcde"` becomes `"abcdeabcde"`. Look at it closely:

```
 a b c d e a b c d e
 ^^^^^^^^^               start 0 -> abcde
   ^^^^^^^^^             start 2 -> cdeab
     ^^^^^^^^^           start 3 -> deabc
```

Every window of length 5 in the doubled string is a rotation of the original, and every rotation appears as such a window. So `goal` is a rotation of `s` exactly when the two lengths are equal and `goal` appears as a **substring** (a run of consecutive characters) of `s + s`. We replaced "try all rotations" by "search inside one longer string". This is exactly the problem _Is It a Rotation?_.

```python
def is_rotation_fast(s, goal):
    return len(s) == len(goal) and goal in s + s


assert is_rotation_fast("abcde", "cdeab")
assert not is_rotation_fast("abcde", "abced")
assert not is_rotation_fast("ab", "abc")
assert is_rotation_fast("", "")
```

```cpp
bool is_rotation_fast(string s, string goal) {
    if (s.size() != goal.size()) return false;
    string doubled = s + s;
    return doubled.find(goal) != string::npos;
}
```

The length check matters: without it, `"ab"` would be found inside `"abab"` and wrongly look like a rotation of it, because it is only a piece. The doubled string has length $2n$ and building it costs $O(n)$. The searching step is a built-in operation. Python's `in` is fast in practice, but the plain guarantee for the worst case needs a proper string-matching algorithm, such as KMP, which is taught in the advanced strings page. The doubling trick also reappears there when we look for the alphabetically smallest rotation.

## 6.3 Check yourself

1. How many different rotations can a string of length 6 have at most?
2. Which window of `"abcdeabcde"` equals the rotation of `"abcde"` by 3?
3. Why do we compare the lengths first?
4. What is `rotate_left("hello", 2)`?

# Chapter 7. Numbers hidden in strings

## 7.1 Digits and their values

A digit character like `'7'` is not the number 7; it is a character. To get the value, subtract the character `'0'`: in Python `ord('7') - ord('0')` is 7, in C++ `'7' - '0'` is 7. This works because the digits `'0'` to `'9'` are stored with consecutive numbers.

To read a whole number from its digits, scan left to right and keep a running value. Each new digit **shifts** what we have one place to the left (multiply by 10) and adds itself. Reading `"472"`:

```
 start          value = 0
 read '4'       value = 0*10 + 4 = 4
 read '7'       value = 4*10 + 7 = 47
 read '2'       value = 47*10 + 2 = 472
```

## 7.2 Parsing a number with rules

The problem _String to Integer_ asks us to turn the start of a string into a number following clear rules: skip leading spaces, read an optional sign `+` or `-`, read digits until the first non-digit, and clamp the result into the range of a signed 32-bit integer, which is from $-2^{31}$ to $2^{31} - 1$. The way to write such code is to follow the rules in order, using one position `i` that only moves forward.

The only danger is a huge number. Python has no overflow, but in C++ an `int` that is too big gives garbage. So in C++ we keep the value in a `long long` (64 bits) and stop reading digits as soon as the value is bigger than $2^{31}$, because after that the answer is going to be clamped anyway. We use the same early stop in Python to keep numbers small.

```python
def parse_int(s):
    i, n = 0, len(s)
    while i < n and s[i] == " ":
        i += 1
    sign = 1
    if i < n and (s[i] == "+" or s[i] == "-"):
        if s[i] == "-":
            sign = -1
        i += 1
    value = 0
    while i < n and "0" <= s[i] <= "9":
        value = value * 10 + (ord(s[i]) - ord("0"))
        i += 1
        if value > 2**31:
            break
    value *= sign
    low, high = -(2**31), 2**31 - 1
    if value < low:
        return low
    if value > high:
        return high
    return value


assert parse_int("42") == 42
assert parse_int("   -42abc") == -42
assert parse_int("words 987") == 0
assert parse_int("-91283472332") == -2147483648
assert parse_int("91283472332") == 2147483647
assert parse_int("+") == 0
```

```cpp
int parse_int(string s) {
    int i = 0, n = s.size();
    while (i < n && s[i] == ' ') i++;
    int sign = 1;
    if (i < n && (s[i] == '+' || s[i] == '-')) {
        if (s[i] == '-') sign = -1;
        i++;
    }
    long long value = 0;
    while (i < n && s[i] >= '0' && s[i] <= '9') {
        value = value * 10 + (s[i] - '0');
        i++;
        if (value > (1LL << 31)) break;
    }
    value *= sign;
    long long low = -(1LL << 31), high = (1LL << 31) - 1;
    if (value < low) return (int)low;
    if (value > high) return (int)high;
    return (int)value;
}
```

Time $O(n)$, space $O(1)$. Notice that `"words 987"` gives 0: after the spaces, `w` is neither a sign nor a digit, so no digit is read at all.

## 7.3 Adding with a carry

You learned to add numbers on paper: write one under the other, add the last digits, write the last digit of the sum and **carry** the rest to the next column. We can do exactly the same with strings. Let us add the binary numbers `1010` and `1011` (that is 10 and 11, so the answer should be 21, which is `10101`). In binary each column adds at most $1 + 1 + 1 = 3$ (two digits and a carry); we write `total % 2` and carry `total // 2`.

```
   1 0 1 0
 + 1 0 1 1
 ---------
 column (from the right): digits + carry -> total -> write, carry
   1:  0 + 1 + 0 = 1  -> write 1, carry 0
   2:  1 + 1 + 0 = 2  -> write 0, carry 1
   3:  0 + 0 + 1 = 1  -> write 1, carry 0
   4:  1 + 1 + 0 = 2  -> write 0, carry 1
   5:  (nothing left) + carry 1 -> write 1
 written right to left: 1 0 1 0 1  = 10101
```

The loop keeps going while either number has digits left **or** a carry is left. We collect the written digits from right to left, so at the end we reverse them. This is exactly the problem _Add Binary Strings_.

```python
def add_bits(a, b):
    out = []
    i, j, carry = len(a) - 1, len(b) - 1, 0
    while i >= 0 or j >= 0 or carry > 0:
        total = carry
        if i >= 0:
            total += ord(a[i]) - ord("0")
            i -= 1
        if j >= 0:
            total += ord(b[j]) - ord("0")
            j -= 1
        out.append(str(total % 2))
        carry = total // 2
    return "".join(reversed(out))


assert add_bits("11", "1") == "100"
assert add_bits("1010", "1011") == "10101"
assert add_bits("0", "0") == "0"
```

```cpp
string add_bits(string a, string b) {
    string out;
    int i = (int)a.size() - 1, j = (int)b.size() - 1, carry = 0;
    while (i >= 0 || j >= 0 || carry > 0) {
        int total = carry;
        if (i >= 0) total += a[i--] - '0';
        if (j >= 0) total += b[j--] - '0';
        out += char('0' + total % 2);
        carry = total / 2;
    }
    reverse(out.begin(), out.end());
    return out;
}
```

Time $O(\max(n, m))$ for lengths $n$ and $m$. The same loop works for decimal numbers: just use 10 instead of 2.

## 7.4 Roman numerals to numbers

Roman numerals use the symbols $I=1$, $V=5$, $X=10$, $L=50$, $C=100$, $D=500$, $M=1000$. Usually we add them from the largest to the smallest: `XVI` is $10+5+1=16$. But if a small symbol stands directly **before** a bigger one, it is subtracted: `IV` is $5-1=4$ and `IX` is $10-1=9$.

So the rule for converting is simple: look at each symbol and the one after it. If the symbol is smaller than the next one, subtract its value; otherwise add it. For `MCMXCIV`:

```
 M  (1000)  next C is smaller      -> add   +1000
 C  (100)   next M is bigger       -> subtract -100
 M  (1000)  next X is smaller      -> add   +1000
 X  (10)    next C is bigger       -> subtract -10
 C  (100)   next I is smaller      -> add   +100
 I  (1)     next V is bigger       -> subtract -1
 V  (5)     last symbol            -> add   +5
 total = 1000 - 100 + 1000 - 10 + 100 - 1 + 5 = 1994
```

This is exactly the problem _Roman Numeral to Integer_.

```python
ROMAN_VALUE = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_value(s):
    total = 0
    for i in range(len(s)):
        v = ROMAN_VALUE[s[i]]
        if i + 1 < len(s) and v < ROMAN_VALUE[s[i + 1]]:
            total -= v
        else:
            total += v
    return total


assert roman_value("III") == 3
assert roman_value("IV") == 4
assert roman_value("MCMXCIV") == 1994
```

```cpp
int roman_char(char c) {
    switch (c) {
        case 'I': return 1;
        case 'V': return 5;
        case 'X': return 10;
        case 'L': return 50;
        case 'C': return 100;
        case 'D': return 500;
        default: return 1000;
    }
}

int roman_value(string s) {
    int total = 0, n = s.size();
    for (int i = 0; i < n; i++) {
        int v = roman_char(s[i]);
        if (i + 1 < n && v < roman_char(s[i + 1])) total -= v;
        else total += v;
    }
    return total;
}
```

Time $O(n)$.

## 7.5 Numbers to Roman numerals

The other direction uses a **greedy** idea: always take the biggest piece that still fits. To make the list of pieces easy, put the six subtractive forms into the table next to the plain symbols, in decreasing order: 1000 `M`, 900 `CM`, 500 `D`, 400 `CD`, 100 `C`, 90 `XC`, 50 `L`, 40 `XL`, 10 `X`, 9 `IX`, 5 `V`, 4 `IV`, 1 `I`. For each row, write the symbol as many times as the value fits in what is left, and subtract. For 1994:

```
 1000 fits once   -> M,  left 994
 900  fits once   -> CM, left 94
 90   fits once   -> XC, left 4
 4    fits once   -> IV, left 0           result: MCMXCIV
```

All the other rows fit zero times. This is exactly the problem _Integer to Roman Numeral_.

```python
ROMAN_TABLE = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
    (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def to_roman(num):
    out = []
    for value, symbol in ROMAN_TABLE:
        while num >= value:
            out.append(symbol)
            num -= value
    return "".join(out)


assert to_roman(3) == "III"
assert to_roman(58) == "LVIII"
assert to_roman(1994) == "MCMXCIV"
assert roman_value(to_roman(2024)) == 2024
```

```cpp
string to_roman(int num) {
    vector<pair<int, string>> table = {
        {1000, "M"}, {900, "CM"}, {500, "D"}, {400, "CD"}, {100, "C"}, {90, "XC"},
        {50, "L"}, {40, "XL"}, {10, "X"}, {9, "IX"}, {5, "V"}, {4, "IV"}, {1, "I"}};
    string out;
    for (auto& [value, symbol] : table) {
        while (num >= value) {
            out += symbol;
            num -= value;
        }
    }
    return out;
}
```

The table has a fixed size (13 rows) and the answer has a bounded number of symbols, so the time is $O(1)$ for the usual range up to 3999.

## 7.6 Check yourself

1. What is the value of the digit character `'8'` and how do you compute it?
2. Why does `parse_int` return 0 for `"+-5"`?
3. In binary addition, what are `total % 2` and `total // 2` when `total` is 3?
4. Why must `900` come before `500` in the Roman table?

# Chapter 8. Zigzag: simulating a pattern

## 8.1 The picture

Some problems describe a physical pattern and ask what you get when you read it differently. In _Zigzag Conversion_, we write the text down a number of rows, then back up diagonally, again and again. For `PAYPALISHIRING` with 3 rows:

```
 P   A   H   N
 A P L S I I G
 Y   I   R
```

Then we read it row by row: `PAHN` + `APLSIIG` + `YIR` = `PAHNAPLSIIGYIR`. We do not need to draw the picture. We only need to know, for each character of the text, **which row** it lands in. The row numbers for this example, computed by running the code, are:

```
 text: P A Y P A L I S H I R I N G
 row : 0 1 2 1 0 1 2 1 0 1 2 1 0 1
```

The row goes down 0, 1, 2, then bounces and goes up 1, then bounces at the top and goes down again.

## 8.2 Bouncing up and down

So keep a current `row` and a `step` that is `+1` (going down) or `-1` (going up). Put each character on its row's line, then move. When we reach the top row (0) the step becomes `+1`; when we reach the bottom row the step becomes `-1`. One row is a special case: there is nothing to bounce between, so the string stays as it is (the same holds when there are at least as many rows as characters).

```python
def zigzag_rows(s, rows):
    if rows == 1 or rows >= len(s):
        return s
    lines = [[] for _ in range(rows)]
    row, step = 0, 1
    for ch in s:
        lines[row].append(ch)
        if row == 0:
            step = 1
        elif row == rows - 1:
            step = -1
        row += step
    return "".join("".join(line) for line in lines)


assert zigzag_rows("PAYPALISHIRING", 3) == "PAHNAPLSIIGYIR"
assert zigzag_rows("PAYPALISHIRING", 4) == "PINALSIGYAHRPI"
assert zigzag_rows("AB", 1) == "AB"
```

```cpp
string zigzag_rows(string s, int rows) {
    if (rows == 1 || rows >= (int)s.size()) return s;
    vector<string> lines(rows);
    int row = 0, step = 1;
    for (char ch : s) {
        lines[row] += ch;
        if (row == 0) step = 1;
        else if (row == rows - 1) step = -1;
        row += step;
    }
    string result;
    for (const string& line : lines) result += line;
    return result;
}
```

Time $O(n)$, space $O(n)$. This is exactly the problem _Zigzag Conversion_.

## 8.3 Jumping with a formula

There is a second way, which is nice to know because it reads the answer directly without storing rows. One full "down and up" trip takes $2(\text{rows} - 1)$ characters; call it the **cycle**. In the first and last rows we meet exactly one character per cycle: positions $r, r + \text{cycle}, r + 2\,\text{cycle}, \dots$. In a middle row $r$ there is also a diagonal character in each cycle, at position $i + \text{cycle} - 2r$ after each regular position $i$. So for each row from top to bottom we jump along these positions.

```python
def zigzag_jumps(s, rows):
    if rows == 1 or rows >= len(s):
        return s
    cycle = 2 * (rows - 1)
    out = []
    for r in range(rows):
        i = r
        while i < len(s):
            out.append(s[i])
            if 0 < r < rows - 1:
                j = i + cycle - 2 * r
                if j < len(s):
                    out.append(s[j])
            i += cycle
    return "".join(out)


assert zigzag_jumps("PAYPALISHIRING", 3) == "PAHNAPLSIIGYIR"
assert zigzag_jumps("PAYPALISHIRING", 4) == zigzag_rows("PAYPALISHIRING", 4)
```

```cpp
string zigzag_jumps(string s, int rows) {
    int n = s.size();
    if (rows == 1 || rows >= n) return s;
    int cycle = 2 * (rows - 1);
    string out;
    for (int r = 0; r < rows; r++) {
        for (int i = r; i < n; i += cycle) {
            out += s[i];
            if (r > 0 && r < rows - 1) {
                int j = i + cycle - 2 * r;
                if (j < n) out += s[j];
            }
        }
    }
    return out;
}
```

Both ways run in $O(n)$. Use whichever you find easier to trust; the bouncing version is easier to get right under pressure.

## 8.4 Check yourself

1. How many rows does a zigzag need before the text simply stays unchanged?
2. For 4 rows, how long is one cycle?
3. Which two moments make `step` change direction?
4. In which rows of the formula version do we add a second, diagonal character?

# Chapter 9. Big numbers written as strings

## 9.1 Why numbers become strings

A 64-bit integer holds numbers up to about $9 \times 10^{18}$, which is only 19 digits. Problems with numbers of thousands of digits give them to us as strings, and we must do the arithmetic ourselves, digit by digit, like on paper. Addition with a carry (Chapter 7) was the first example. Multiplication is the second.

## 9.2 Schoolbook multiplication

On paper, to multiply $123 \times 45$ you multiply every digit of one number by every digit of the other and add the results in the right columns. A clean way to organise this: digit $i$ of the first number and digit $j$ of the second number (counting from the left, starting at 0) contribute their product to the column of position $i + j + 1$ in an answer array of length $\text{len}(a) + \text{len}(b)$. We first add up all the products into the columns, ignoring that columns can exceed 9, and only then do a single sweep from the right to fix the carries.

For $123 \times 45$ the array starts as `[0, 0, 0, 0, 0]`. After using the digit `3` of `123` with both digits of `45` it is `[0, 0, 0, 12, 15]`. After the digit `2` it is `[0, 0, 8, 22, 15]`, and after the digit `1` it is `[0, 4, 13, 22, 15]`. Now the carry sweep from the right: 15 leaves 5 and carries 1 into the next column, 22 + 1 = 23 leaves 3 and carries 2, and so on, giving `[0, 5, 5, 3, 5]`. After stripping the leading zero the answer is `5535`, and indeed $123 \times 45 = 5535$. This is exactly the problem _Multiply Big Numbers_.

```python
def multiply_digits(a, b):
    res = [0] * (len(a) + len(b))
    for i in range(len(a) - 1, -1, -1):
        x = ord(a[i]) - ord("0")
        for j in range(len(b) - 1, -1, -1):
            res[i + j + 1] += x * (ord(b[j]) - ord("0"))
    for k in range(len(res) - 1, 0, -1):
        res[k - 1] += res[k] // 10
        res[k] %= 10
    p = 0
    while p < len(res) - 1 and res[p] == 0:
        p += 1
    return "".join(str(d) for d in res[p:])


assert multiply_digits("123", "45") == "5535"
assert multiply_digits("0", "99999") == "0"
assert multiply_digits("999", "999") == "998001"
```

```cpp
string multiply_digits(string a, string b) {
    int n = a.size(), m = b.size();
    vector<long long> res(n + m, 0);
    for (int i = n - 1; i >= 0; i--) {
        for (int j = m - 1; j >= 0; j--) {
            res[i + j + 1] += (long long)(a[i] - '0') * (b[j] - '0');
        }
    }
    for (int k = n + m - 1; k > 0; k--) {
        res[k - 1] += res[k] / 10;
        res[k] %= 10;
    }
    int p = 0;
    while (p < n + m - 1 && res[p] == 0) p++;
    string out;
    for (; p < n + m; p++) out += char('0' + res[p]);
    return out;
}
```

The cost is $O(nm)$: one multiplication for each pair of digits. The array entries stay small (at most $81 \cdot \min(n, m)$ before carrying), so there is no overflow. Why do we strip zeros but keep at least one digit? So that `"0"` times anything gives `"0"`, not an empty string.

## 9.3 Using bigger digits

With two numbers of 20,000 digits there are $4 \times 10^8$ digit pairs, which is too slow in a scripting language. The fix is to treat several digits as one "super digit". If we cut each number into chunks of 4 decimal digits, we say the numbers are written in **base** $10^4$. Each chunk is between 0 and 9999, and a product of two chunks is below $10^8$, which still fits easily in a 64-bit integer. We need 4 times fewer chunks, so 16 times fewer multiplications.

The carry works exactly like before but with 10000 instead of 10, and when printing we must pad each chunk to 4 digits with zeros (a chunk of 7 inside the number must be printed as `0007`), except for the first chunk.

```python
def multiply_chunks(a, b):
    def chunks(x):
        return [int(x[max(0, k - 4):k]) for k in range(len(x), 0, -4)]

    A, B = chunks(a), chunks(b)
    res = [0] * (len(A) + len(B))
    for i in range(len(A)):
        carry = 0
        for j in range(len(B)):
            cur = res[i + j] + A[i] * B[j] + carry
            res[i + j] = cur % 10000
            carry = cur // 10000
        k = i + len(B)
        while carry > 0:
            cur = res[k] + carry
            res[k] = cur % 10000
            carry = cur // 10000
            k += 1
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return str(res[-1]) + "".join(str(v).zfill(4) for v in reversed(res[:-1]))


assert multiply_chunks("123", "45") == "5535"
assert multiply_chunks("0", "99999") == "0"
assert multiply_chunks("123456789", "987654321") == str(123456789 * 987654321)
assert multiply_chunks("10000", "10000") == "100000000"
```

```cpp
string multiply_chunks(string a, string b) {
    auto chunks = [](const string& x) {
        vector<long long> c;
        for (int k = (int)x.size(); k > 0; k -= 4) {
            int lo = max(0, k - 4);
            c.push_back(stoll(x.substr(lo, k - lo)));
        }
        return c;
    };
    vector<long long> A = chunks(a), B = chunks(b);
    vector<long long> res(A.size() + B.size(), 0);
    for (size_t i = 0; i < A.size(); i++) {
        long long carry = 0;
        for (size_t j = 0; j < B.size(); j++) {
            long long cur = res[i + j] + A[i] * B[j] + carry;
            res[i + j] = cur % 10000;
            carry = cur / 10000;
        }
        size_t k = i + B.size();
        while (carry > 0) {
            long long cur = res[k] + carry;
            res[k] = cur % 10000;
            carry = cur / 10000;
            k++;
        }
    }
    while (res.size() > 1 && res.back() == 0) res.pop_back();
    string out = to_string(res.back());
    for (int k = (int)res.size() - 2; k >= 0; k--) {
        string t = to_string(res[k]);
        out += string(4 - t.size(), '0') + t;
    }
    return out;
}
```

The time is still $O(nm)$ in the formal sense, but about 16 times smaller in practice. Python also has big integers built in: `int(a) * int(b)` multiplies even huge numbers quickly (it uses the cleverer Karatsuba method, with cost about $O(n^{1.585})$), and `str` turns the result back into text. Since Python 3.11 you may need to raise the safety limit on number-to-text conversion with `sys.set_int_max_str_digits(0)` for very long numbers. In C++ there are no built-in big integers, so you write the loops above.

## 9.4 Check yourself

1. Into which column of the answer array does the product of digit $i$ of `a` and digit $j$ of `b` go?
2. Why can we add the products first and carry only at the end?
3. In base $10^4$, how is the number 12,000,007 stored, least significant chunk first?
4. Why must a middle chunk be padded with zeros when printing?

# Chapter 10. Palindromes that grow from the middle

## 10.1 Expanding around a centre

Checking every substring of a string for being a palindrome takes far too long: there are about $n^2/2$ substrings, and checking each costs up to $n$, so the total is $O(n^3)$. There is a cleverer way based on one observation: **a palindrome is symmetric around its middle**. If we pick the middle first and grow outwards, we compare just one new pair of characters per step, and we stop at the first mismatch.

A palindrome of odd length has a character as its centre (`aba`, centre `b`), and a palindrome of even length has a gap between two characters as its centre (`abba`, centre between the two `b`). So a string of length $n$ has $n$ odd centres and $n - 1$ even centres, in total $2n - 1$.

```
 s = c b b d
 odd centre at index 1 ("b"):        compare c with b -> differ, stop. Longest: "b"
 even centre between index 1 and 2:  compare b with b -> equal, grow;
                                     compare c with d -> differ, stop. Longest: "bb"
```

To do it in code, write one helper `expand(s, l, r)` that starts with the window from `l` to `r` and moves `l` left and `r` right as long as the two characters are equal and still inside the string. It returns the length of the palindrome it found. For an odd centre at `c` we call `expand(s, c, c)`; for an even centre between `c` and `c + 1` we call `expand(s, c, c + 1)`.

```python
def expand(s, l, r):
    while l >= 0 and r < len(s) and s[l] == s[r]:
        l -= 1
        r += 1
    return r - l - 1


assert expand("abaa", 1, 1) == 3
assert expand("cbbd", 1, 2) == 2
assert expand("abc", 0, 1) == 0
```

```cpp
int expand(const string& s, int l, int r) {
    int n = s.size();
    while (l >= 0 && r < n && s[l] == s[r]) {
        l--;
        r++;
    }
    return r - l - 1;
}
```

When the loop stops, the window `l..r` has gone one step too far on each side, so the real palindrome is `l+1 .. r-1` and its length is $(r - 1) - (l + 1) + 1 = r - l - 1$. If the very first comparison fails (for an even centre between two different letters), the length is 0.

## 10.2 Counting all palindromic substrings

Counting palindromic substrings comes for free. If the longest palindrome around some centre has length $L$, then there are palindromes of every smaller size around that same centre too, because the inner part of a palindrome is also a palindrome. For an odd centre, lengths are $1, 3, 5, \dots, L$, which is $(L + 1) / 2$ palindromes. For an even centre, lengths are $2, 4, \dots, L$, which is $L / 2$ palindromes. So in the code below we add `(L + 1) // 2` for an odd centre and `L // 2` for an even centre.

For `"aaa"`, the three odd centres give maximal lengths 1, 3, 1 (that is 1, 2, 1 palindromes) and the two even centres give 2, 2 (1 and 1 palindromes), a total of $1 + 2 + 1 + 1 + 1 = 6$. Written out, those are `a`, `a`, `a`, `aa`, `aa`, `aaa`. This is exactly the problem _Count Palindromic Substrings_.

```python
def count_palindromes(s):
    total = 0
    for c in range(len(s)):
        total += (expand(s, c, c) + 1) // 2
        total += expand(s, c, c + 1) // 2
    return total


assert count_palindromes("abc") == 3
assert count_palindromes("aaa") == 6
assert count_palindromes("abba") == 6
assert count_palindromes("") == 0
```

```cpp
int count_palindromes(string s) {
    int total = 0;
    for (int c = 0; c < (int)s.size(); c++) {
        total += (expand(s, c, c) + 1) / 2;
        total += expand(s, c, c + 1) / 2;
    }
    return total;
}
```

There are $2n - 1$ centres and each expansion costs at most $O(n)$, so the worst case is $O(n^2)$, for example on `"aaaa...a"`. For typical strings it is much faster because expansions stop early. Space is $O(1)$.

## 10.3 The longest palindromic substring

To find the longest palindromic substring we run the same loop but remember the best one. For each centre we compute the length $L$; the start of that palindrome is `c - (L - 1) // 2` (for an odd centre `c` that is `c - (L-1)/2`, for an even centre between `c` and `c+1` it is `c - L/2 + 1`, and both equal `c - (L - 1) // 2`). If $L$ is strictly longer than the best so far, we replace the best. Using "strictly" makes the **earliest** palindrome win in case of a tie, because we move through the centres from left to right and, for a fixed length, an earlier centre means an earlier start. This is exactly the problem _Longest Palindromic Substring_.

For `"cbbd"` the lengths found are: centre 0 odd: 1, centre 0 even: 0, centre 1 odd: 1, centre 1 even: 2 (the palindrome `bb`), centre 2 odd: 1, centre 2 even: 0, centre 3 odd: 1. The best is `bb`, which starts at index $1 - (2 - 1) // 2 = 1$.

```python
def longest_palindrome(s):
    best_start, best_len = 0, 0
    for c in range(len(s)):
        for length in (expand(s, c, c), expand(s, c, c + 1)):
            if length > best_len:
                best_len = length
                best_start = c - (length - 1) // 2
    return s[best_start:best_start + best_len]


assert longest_palindrome("babad") == "bab"
assert longest_palindrome("cbbd") == "bb"
assert longest_palindrome("a") == "a"
assert longest_palindrome("") == ""
assert longest_palindrome("abacdfgdcaba") == "aba"
```

```cpp
string longest_palindrome(string s) {
    int best_start = 0, best_len = 0;
    for (int c = 0; c < (int)s.size(); c++) {
        int lens[2] = {expand(s, c, c), expand(s, c, c + 1)};
        for (int length : lens) {
            if (length > best_len) {
                best_len = length;
                best_start = c - (length - 1) / 2;
            }
        }
    }
    return s.substr(best_start, best_len);
}
```

The time is $O(n^2)$ in the worst case and the space is $O(1)$ besides the answer. That is fine for strings of a few thousand characters. For strings with hundreds of thousands of characters, a smarter algorithm is needed that never repeats a comparison: it is called Manacher's algorithm, and it is taught in the advanced strings page. It reuses the answers of centres we have already finished, because inside a big palindrome the left half is a mirror image of the right half.

## 10.4 Check yourself

1. How many centres (odd and even together) does a string of length 5 have?
2. What does `expand("abba", 1, 2)` return?
3. How many palindromic substrings does `"aaaa"` have?
4. Why does a strict "greater than" in `longest_palindrome` keep the earliest answer on a tie?
