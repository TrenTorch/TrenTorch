> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Stacks and queues)

This page teaches two of the simplest containers in programming, the stack and the queue, and shows how far they can take you. They look almost too easy: a stack lets you touch only the newest item, a queue only the oldest. Yet that small restriction solves bracket matching, calculators, "next bigger value" questions, histograms, and sliding-window problems.

The page is a staircase. **Chapter 1 is deliberately gentle**: plates and a line of people, a few lines of code, nothing clever. Each chapter after it adds one new idea, and the ideas build on each other. The middle chapters introduce the **monotonic stack**, the single most useful trick of the topic, and the last chapters introduce queues, the two-stack queue, and the **monotonic deque**. By the end you will be able to solve every question in the step. Every code example is shown in Python and in C++, so pick whichever you like.

# Chapter 1. What a stack is

## 1.1 A pile of plates

Think about a pile of plates in a kitchen. You put a clean plate on top, and when you need one you take the top plate. You never pull one out of the middle. The plate you added last is the first to leave. This rule is called **last in, first out**, or LIFO for short, and a container that follows it is a **stack**.

A stack needs only a few operations. **Push** puts an item on top. **Pop** removes the top item and gives it to you. **Top** (or "peek") shows the top item without removing it. And we sometimes ask whether the stack is empty. Each of these takes $O(1)$ time, meaning the cost does not grow with the number of items.

```
push 1, push 2, push 3, then pop:

   |   |     |   |     | 3 |     |   |
   |   |     | 2 |     | 2 |     | 2 |
   | 1 |     | 1 |     | 1 |     | 1 |
   +---+     +---+     +---+     +---+
   push 1    push 2    push 3    pop gives 3
```

## 1.2 A stack in code

We do not need a special class. In Python a plain list works: `append` pushes, `pop()` removes and returns the last element, and `stack[-1]` is the top. In C++ a `vector` does the same with `push_back`, `pop_back` and `back()` (there is also a ready-made `stack` type, but the vector is just as easy and lets us look inside when we want to).

One rule is worth burning into memory: **never pop or peek an empty stack**. In Python that is an `IndexError`, in C++ it is undefined behaviour. Most stack bugs are a missing "is the stack empty?" check.

As a first small job, let us reverse a word. Push every letter, then pop them all. Because the last letter pushed is the first popped, the word comes out backwards.

```python
def reverse_with_stack(text):
    stack = []
    for ch in text:
        stack.append(ch)
    out = []
    while stack:
        out.append(stack.pop())
    return "".join(out)


assert reverse_with_stack("stack") == "kcats"
assert reverse_with_stack("") == ""
```

```cpp
string reverseWithStack(const string& text) {
    vector<char> stack;
    for (char ch : text) {
        stack.push_back(ch);
    }
    string out;
    while (!stack.empty()) {
        out.push_back(stack.back());
        stack.pop_back();
    }
    return out;
}
```

The loop `while stack:` in Python means "while the stack is not empty", because an empty list counts as false.

## 1.3 Stacks remember the past

Why is "newest first" so useful? Because many problems ask us to deal with the **most recent unfinished thing**. The classic example is the undo button in a text editor. Each action is pushed on a stack of history; "undo" pops the latest action and forgets it.

Here is a tiny history machine. The commands are words; any word other than `undo` is an action that gets recorded, and `undo` removes the latest recorded action (doing nothing if there is none).

```python
def apply_commands(commands):
    history = []
    for word in commands:
        if word == "undo":
            if history:
                history.pop()
        else:
            history.append(word)
    return history


assert apply_commands(["draw", "paint", "undo", "erase"]) == ["draw", "erase"]
assert apply_commands(["undo", "draw"]) == ["draw"]
```

```cpp
vector<string> applyCommands(const vector<string>& commands) {
    vector<string> history;
    for (const string& word : commands) {
        if (word == "undo") {
            if (!history.empty()) {
                history.pop_back();
            }
        } else {
            history.push_back(word);
        }
    }
    return history;
}
```

Notice the pattern: scan the input from left to right, push things as they arrive, and sometimes pop the top when a later item "cancels" or "completes" it. Almost everything in the next chapters is this pattern in disguise. The cost is $O(n)$ for $n$ commands, because each item is pushed once and popped at most once.

## 1.4 Check yourself

1. Which item does `pop` remove from a stack: the oldest or the newest?
2. Why must we check that the stack is not empty before reading its top?
3. In the undo machine, what does the stack hold after `["a", "b", "undo", "undo", "undo"]`?
4. Why does a scan that pushes each item once and pops each at most once take $O(n)$ time?

# Chapter 2. Matching and cancelling

## 2.1 Brackets that must match

Here is the first real problem. A string has only the brackets `(`, `)`, `[`, `]`, `{`, `}`. It is **valid** if every opening bracket is closed by the same kind of bracket, in the right order. So `([])` is valid but `([)]` is not: the `[` is still open when the `)` tries to close the `(`.

Scan from left to right. An opening bracket must wait for its partner, so push it. A closing bracket must match the **most recently opened** bracket that is still waiting, and that is exactly the top of the stack. If the top is the matching opener, pop it. If the stack is empty or the top is a different kind, the string is invalid. At the very end, the stack must be empty, otherwise some opener never got closed.

Trace of `([)]`: push `(`, push `[`; now `)` arrives but the top is `[`, which does not match, so the answer is no.

This is exactly the problem _Valid Brackets_. It takes $O(n)$ time and up to $O(n)$ space.

```python
def is_valid(s):
    partner = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in partner:
            if not stack or stack[-1] != partner[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)
    return not stack


assert is_valid("([])") is True
assert is_valid("([)]") is False
assert is_valid("((") is False
assert is_valid(")") is False
assert is_valid("") is True
```

```cpp
bool isValid(const string& s) {
    unordered_map<char, char> partner = {{')', '('}, {']', '['}, {'}', '{'}};
    vector<char> stack;
    for (char ch : s) {
        if (partner.count(ch)) {
            if (stack.empty() || stack.back() != partner[ch]) {
                return false;
            }
            stack.pop_back();
        } else {
            stack.push_back(ch);
        }
    }
    return stack.empty();
}
```

## 2.2 Neighbours that cancel

Brackets cancel in pairs. Plenty of other problems cancel too. Imagine repeatedly deleting two equal neighbouring letters from `abbaca`: `bb` goes, leaving `aaca`; then `aa` goes, leaving `ca`. Done naively this needs many passes over the string.

The stack does it in one pass. The stack always holds the string we have built so far with no cancellable pair in it. When a new letter arrives, compare it with the top: if they are equal they cancel, so pop; otherwise push. Because the new letter can only form a pair with its immediate left neighbour, which is the top, one comparison is enough. Cascades such as the `aa` that appears after `bb` is deleted happen automatically.

This is exactly the problem _Remove Adjacent Duplicates_.

```python
def remove_adjacent(s):
    stack = []
    for ch in s:
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)
    return "".join(stack)


assert remove_adjacent("abbaca") == "ca"
assert remove_adjacent("azxxzy") == "ay"
assert remove_adjacent("aa") == ""
```

```cpp
string removeAdjacent(const string& s) {
    string stack;
    for (char ch : s) {
        if (!stack.empty() && stack.back() == ch) {
            stack.pop_back();
        } else {
            stack.push_back(ch);
        }
    }
    return stack;
}
```

In C++ a `string` is itself a perfectly good stack of characters: it has `push_back`, `pop_back` and `back`. The cost is $O(n)$ time and space.

## 2.3 Typing with a backspace key

A text editor is a stack of letters, and the backspace key is a pop. A `#` in the input means backspace: it deletes the previous character, or does nothing if the text is empty. To know what the text looks like after all the typing, simulate it: push letters, and pop when you see `#`.

Two strings are the same after typing if their simulated results are equal, so we just compare them. For `ab#c` we get `a`, `ab`, then backspace gives `a`, then `ac`. For `ad#c` we get `ac` as well, so the answer is yes.

This is exactly the problem _Backspace String Compare_. (A cleverer solution reads both strings from the back using two pointers and $O(1)$ space; the stack version is the one to master first.)

```python
def type_text(s):
    stack = []
    for ch in s:
        if ch == "#":
            if stack:
                stack.pop()
        else:
            stack.append(ch)
    return "".join(stack)


def same_after_typing(s, t):
    return type_text(s) == type_text(t)


assert type_text("ab#c") == "ac"
assert type_text("###") == ""
assert same_after_typing("ab#c", "ad#c") is True
assert same_after_typing("ab", "a#b#") is False
```

```cpp
string typeText(const string& s) {
    string stack;
    for (char ch : s) {
        if (ch == '#') {
            if (!stack.empty()) {
                stack.pop_back();
            }
        } else {
            stack.push_back(ch);
        }
    }
    return stack;
}

bool sameAfterTyping(const string& s, const string& t) {
    return typeText(s) == typeText(t);
}
```

## 2.4 Walking through folders

A file path such as `/a/./b/../../c/` is a sequence of moves. Each name steps into a folder, a single dot `.` means "stay here", and two dots `..` mean "go up to the parent folder". So the folders we are inside form a stack: a name is pushed, `..` pops (if there is anywhere to go up to), and `.` or an empty piece between two slashes does nothing.

Split the path at the slashes and process the pieces. For `/a/./b/../../c/` the pieces are `a`, `.`, `b`, `..`, `..`, `c` (plus empty ones). The stack goes `[a]`, `[a]`, `[a, b]`, `[a]`, `[]`, `[c]`. Join what is left with slashes and put a `/` in front: `/c`. Going up from the root does nothing, so `/../` simplifies to `/`.

This is exactly the problem _Simplify a File Path_.

```python
def simplify_path(path):
    stack = []
    for part in path.split("/"):
        if part == "" or part == ".":
            continue
        if part == "..":
            if stack:
                stack.pop()
        else:
            stack.append(part)
    return "/" + "/".join(stack)


assert simplify_path("/a/./b/../../c/") == "/c"
assert simplify_path("/../") == "/"
assert simplify_path("/home//foo/") == "/home/foo"
```

```cpp
string simplifyPath(const string& path) {
    vector<string> stack;
    stringstream ss(path);
    string part;
    while (getline(ss, part, '/')) {
        if (part.empty() || part == ".") {
            continue;
        }
        if (part == "..") {
            if (!stack.empty()) {
                stack.pop_back();
            }
        } else {
            stack.push_back(part);
        }
    }
    string result;
    for (const string& name : stack) {
        result += "/" + name;
    }
    return result.empty() ? "/" : result;
}
```

The same shape again: scan, push, and pop when something cancels. Time and space are $O(n)$.

## 2.5 Check yourself

1. In bracket matching, what should happen when a closing bracket arrives and the stack is empty?
2. Why must the stack be empty at the end of the bracket check?
3. Why is one comparison with the top enough when removing adjacent equal letters?
4. What does `/a/b/../..` simplify to?

# Chapter 3. Calculators

## 3.1 Operators after their numbers

Normally we write arithmetic like `(2 + 1) * 3`, with the operator between its two numbers. There is another way, **reverse Polish notation** (RPN, or postfix): the operator goes after its two numbers. The same sum is written `2 1 + 3 *`. It has a wonderful property: it needs no brackets and no rules about which operator goes first. A stack evaluates it directly.

Read the tokens from left to right. A number is pushed. An operator takes the **two most recent numbers**, which are the top two items of the stack, combines them, and pushes the result back. Careful with the order for `-` and `/`: the number popped first is the _right-hand_ one. For `2 1 + 3 *`: push 2, push 1; `+` pops 1 and 2 and pushes 3; push 3; `*` pops 3 and 3 and pushes 9. The answer is the only value left.

The problem says division truncates toward zero, so $7 / -2 = -3$ (not $-4$, which is what Python's `//` would give). We divide the absolute values and fix the sign. C++'s `/` on integers already truncates toward zero.

This is exactly the problem _Evaluate Reverse Polish Notation_. It takes $O(n)$ time.

```python
def eval_rpn(tokens):
    stack = []
    for tok in tokens:
        if tok in ("+", "-", "*", "/"):
            b = stack.pop()
            a = stack.pop()
            if tok == "+":
                stack.append(a + b)
            elif tok == "-":
                stack.append(a - b)
            elif tok == "*":
                stack.append(a * b)
            else:
                q = abs(a) // abs(b)
                stack.append(q if (a < 0) == (b < 0) else -q)
        else:
            stack.append(int(tok))
    return stack[0]


assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
assert eval_rpn(["7", "-2", "/"]) == -3
```

```cpp
int evalRPN(const vector<string>& tokens) {
    vector<int> stack;
    for (const string& tok : tokens) {
        if (tok == "+" || tok == "-" || tok == "*" || tok == "/") {
            int b = stack.back();
            stack.pop_back();
            int a = stack.back();
            stack.pop_back();
            if (tok == "+") {
                stack.push_back(a + b);
            } else if (tok == "-") {
                stack.push_back(a - b);
            } else if (tok == "*") {
                stack.push_back(a * b);
            } else {
                stack.push_back(a / b);
            }
        } else {
            stack.push_back(stoi(tok));
        }
    }
    return stack.back();
}
```

Notice the test `tok in (...)` checks the whole token, so the token `-2` (a negative number) is correctly treated as a number, not as the operator `-`.

## 3.2 Plus, minus, times and divide

Now the ordinary way of writing: `3 + 2 * 2`. Multiplication must happen first, so the answer is 7, not 10. There are no brackets yet.

Here is a lovely trick. Think of the expression as a **sum of terms**: `3 + 2*2` is the term `3` plus the term `2*2`. Addition and subtraction only combine finished terms; multiplication and division work _inside_ a term. So we keep a stack of finished terms, a subtracted term being stored as a negative number. When we see `*` or `/` we update the term on top of the stack. At the end, the answer is the sum of the stack.

To do that we read a number, and then apply the operator that came **before** it (the "pending operator"; it starts as `+`). If the pending operator is `+`, push the number; if `-`, push its negative; if `*`, replace the top by top times number; if `/`, replace the top by top divided by number (truncating toward zero). We act on a number when we reach the next operator or the end of the string.

Trace of `3+2*2`: pending `+`, number 3 gives `[3]`. Pending `+`, number 2 gives `[3, 2]`. Pending `*`, number 2 changes the top to `4`, giving `[3, 4]`. The sum is 7.

This is exactly the problem _Basic Calculator_.

```python
def calculate(s):
    stack = []
    num = 0
    op = "+"
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)
        if (not ch.isdigit() and ch != " ") or i == len(s) - 1:
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            else:
                prev = stack.pop()
                q = abs(prev) // num
                stack.append(q if prev >= 0 else -q)
            op = ch
            num = 0
    return sum(stack)


assert calculate("3+2*2") == 7
assert calculate(" 3/2 ") == 1
assert calculate("14-3/2") == 13
assert calculate("0-5/2") == -2
```

```cpp
int calculate(const string& s) {
    vector<int> stack;
    int num = 0;
    char op = '+';
    for (int i = 0; i < (int)s.size(); i++) {
        char ch = s[i];
        if (isdigit(ch)) {
            num = num * 10 + (ch - '0');
        }
        if ((!isdigit(ch) && ch != ' ') || i == (int)s.size() - 1) {
            if (op == '+') {
                stack.push_back(num);
            } else if (op == '-') {
                stack.push_back(-num);
            } else if (op == '*') {
                stack.back() *= num;
            } else {
                stack.back() /= num;
            }
            op = ch;
            num = 0;
        }
    }
    int total = 0;
    for (int x : stack) {
        total += x;
    }
    return total;
}
```

The scan is $O(n)$ and the stack holds at most one entry per term. (With a little care you can keep only the last term instead of a whole stack, but the stack is clearer.)

## 3.3 Brackets and minus signs

Add round brackets: `1 + (4 + 5 + 2) - 3`. A bracket starts a fresh little sum that must be finished before the outer sum continues. "Finish the inner thing first, then come back to the outer thing" is exactly what a stack is for.

We keep two running pieces of information: `total`, the sum so far at the current level, and `sign`, which is +1 or -1 depending on the last `+` or `-` we saw. A number `num` is added as `sign * num` when the next operator or bracket arrives. When we meet `(`, we have to put the outer work on hold: push the pair `(total, sign)` and start the inside with `total = 0` and `sign = +1`. When we meet `)`, finish the inner sum, then pop the saved pair and combine: `total = saved_total + saved_sign * inner_total`. The saved sign is the sign that stood in front of the bracket, which is how `-(2+3)` becomes `-5`, and how a leading minus sign inside a bracket (as in `1-(-2)`) is handled naturally: a `-` just sets the sign, wherever it appears.

Trace of `1-(2+3)`: total 1, then `-` sets sign to -1. At `(` we push `(1, -1)` and start fresh. Inside, total becomes 2 and then 5. At `)` we pop `(1, -1)` and compute $1 + (-1)\cdot 5 = -4$.

This is exactly the problem _Calculator With Brackets_. One pass, so $O(n)$ time; the stack depth is the bracket nesting depth.

```python
def calc_brackets(s):
    total = 0
    sign = 1
    num = 0
    stack = []
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch in "+-":
            total += sign * num
            num = 0
            sign = 1 if ch == "+" else -1
        elif ch == "(":
            stack.append((total, sign))
            total = 0
            sign = 1
        elif ch == ")":
            total += sign * num
            num = 0
            saved_total, saved_sign = stack.pop()
            total = saved_total + saved_sign * total
            sign = 1
    return total + sign * num


assert calc_brackets("1-(2+3)") == -4
assert calc_brackets("(1+(4+5+2)-3)+(6+8)") == 23
assert calc_brackets("-(2+3)") == -5
assert calc_brackets("1-(-2)") == 3
```

```cpp
int calcBrackets(const string& s) {
    int total = 0;
    int sign = 1;
    int num = 0;
    vector<pair<int, int>> stack;
    for (char ch : s) {
        if (isdigit(ch)) {
            num = num * 10 + (ch - '0');
        } else if (ch == '+' || ch == '-') {
            total += sign * num;
            num = 0;
            sign = (ch == '+') ? 1 : -1;
        } else if (ch == '(') {
            stack.push_back({total, sign});
            total = 0;
            sign = 1;
        } else if (ch == ')') {
            total += sign * num;
            num = 0;
            auto [savedTotal, savedSign] = stack.back();
            stack.pop_back();
            total = savedTotal + savedSign * total;
            sign = 1;
        }
    }
    return total + sign * num;
}
```

Spaces fall through every branch and are ignored. After `)` we reset `sign` to 1, because the bracket is now a finished number inside the outer sum.

## 3.4 Check yourself

1. In RPN, which popped number is the left operand of `-`: the first one popped or the second?
2. Why does `3 + 2 * 2` need a stack of terms rather than a plain running total?
3. When the calculator meets `(`, what exactly is pushed, and why?
4. What is the value of `10-(2+3)-1`?

# Chapter 4. Stacks that remember more

## 4.1 A stack with a minimum

Sometimes each item on the stack carries extra information. Suppose we want a stack that supports push, pop, top, and also "what is the smallest value in the stack right now?" all in $O(1)$.

Scanning the whole stack for the smallest would take $O(n)$. Keeping one variable `smallest` fails when we pop the smallest: we would not know the next smallest. The clean solution is to store, alongside every item, the minimum of everything **at or below** that item. Then the minimum of the current stack is simply the extra number stored with the top item. When we pop, the extra number goes away with the item, and the previous one is exactly right again.

```
pushes 5, 3, 7, 3:     items:  5  3  7  3
                       mins:   5  3  3  3
pop -> items 5 3 7, mins 5 3 3, minimum is now 3 (still correct)
pop -> items 5 3,   mins 5 3,   minimum is now 3
pop -> items 5,     mins 5,     minimum is now 5
```

We use two parallel lists, one for items and one for minimums. Each operation is $O(1)$.

This is exactly the problem _Stack With Minimum_. The sheet gives the operations as text, so we also write a small runner that executes them and collects the answers of `top` and `get_min`.

```python
class MinStack:
    def __init__(self):
        self.items = []
        self.mins = []

    def push(self, x):
        self.items.append(x)
        if self.mins:
            self.mins.append(min(x, self.mins[-1]))
        else:
            self.mins.append(x)

    def pop(self):
        self.items.pop()
        self.mins.pop()

    def top(self):
        return self.items[-1]

    def get_min(self):
        return self.mins[-1]


def run_min_stack(ops):
    stack = MinStack()
    results = []
    for op in ops:
        if op.startswith("push"):
            stack.push(int(op.split()[1]))
        elif op == "pop":
            stack.pop()
        elif op == "top":
            results.append(stack.top())
        else:
            results.append(stack.get_min())
    return results


assert run_min_stack(["push 5", "push 3", "get_min", "pop", "top", "get_min"]) == [3, 5, 5]
assert run_min_stack(["push 2", "push 2", "pop", "get_min"]) == [2]
```

```cpp
struct MinStack {
    vector<int> items;
    vector<int> mins;

    void push(int x) {
        items.push_back(x);
        if (mins.empty()) {
            mins.push_back(x);
        } else {
            mins.push_back(min(x, mins.back()));
        }
    }

    void pop() {
        items.pop_back();
        mins.pop_back();
    }

    int top() { return items.back(); }

    int getMin() { return mins.back(); }
};

vector<int> runMinStack(const vector<string>& ops) {
    MinStack stack;
    vector<int> results;
    for (const string& op : ops) {
        if (op.rfind("push", 0) == 0) {
            stack.push(stoi(op.substr(5)));
        } else if (op == "pop") {
            stack.pop();
        } else if (op == "top") {
            results.push_back(stack.top());
        } else {
            results.push_back(stack.getMin());
        }
    }
    return results;
}
```

## 4.2 Nested repeats

Now a puzzle whose rule is `k[text]`: the text inside the brackets is repeated `k` times, and brackets can nest. So `3[a2[c]]` means: `a` followed by `cc`, all repeated three times, giving `accaccacc`.

This is brackets again, but we carry data. Whenever we see `[`, the string we were building before it must wait, along with the number `k` that told us how many times to repeat what comes next. So we push the pair `(string_so_far, k)` and start a fresh string. When we see `]`, the fresh string is the finished inside; pop the pair and set `current = string_before + current * k`. Digits build up `k` (it may have several digits, as in `12[ab]`), and letters are appended to the current string.

Trace of `3[a2[c]]`: read 3, then `[`: push `("", 3)`, current is empty. Read `a`: current is `a`. Read 2, then `[`: push `("a", 2)`, current is empty. Read `c`: current is `c`. Read `]`: pop `("a", 2)`, current becomes `a` + `cc` = `acc`. Read `]`: pop `("", 3)`, current becomes `accaccacc`.

This is exactly the problem _Decode a String_. Time is proportional to the length of the output, and the stack depth is the nesting depth.

```python
def decode(s):
    stack = []
    current = ""
    k = 0
    for ch in s:
        if ch.isdigit():
            k = k * 10 + int(ch)
        elif ch == "[":
            stack.append((current, k))
            current = ""
            k = 0
        elif ch == "]":
            before, times = stack.pop()
            current = before + current * times
        else:
            current += ch
    return current


assert decode("3[a2[c]]") == "accaccacc"
assert decode("2[ab]3[c]") == "ababccc"
assert decode("2[x]y") == "xxy"
assert decode("10[z]") == "zzzzzzzzzz"
```

```cpp
string decode(const string& s) {
    vector<pair<string, int>> stack;
    string current;
    int k = 0;
    for (char ch : s) {
        if (isdigit(ch)) {
            k = k * 10 + (ch - '0');
        } else if (ch == '[') {
            stack.push_back({current, k});
            current = "";
            k = 0;
        } else if (ch == ']') {
            auto [before, times] = stack.back();
            stack.pop_back();
            string repeated;
            for (int i = 0; i < times; i++) {
                repeated += current;
            }
            current = before + repeated;
        } else {
            current += ch;
        }
    }
    return current;
}
```

## 4.3 Collisions along a line

In a row of asteroids, a positive number moves right and a negative number moves left, all at the same speed. When two meet, the smaller one explodes (both explode if equal). Asteroids moving the same way never meet. Which ones survive?

Process them left to right and keep a stack of survivors so far. A new asteroid can only collide with the last survivor, and only if that survivor goes right while the new one goes left. In every other case the two move apart or in the same direction, so the new one is simply pushed. When a left-mover meets a right-mover on top of the stack, compare sizes: if the top is smaller, it explodes (pop) and the new one keeps going to meet the next survivor; if they are equal, both vanish; if the top is bigger, the new one explodes.

Trace of `[10, 2, -5]`: push 10; push 2; now -5 meets 2, and 2 is smaller, so pop it; -5 meets 10, and -5 is smaller, so it explodes. The survivors are `[10]`.

This is exactly the problem _Asteroid Collision_. Each asteroid is pushed once and popped at most once, so the cost is $O(n)$.

```python
def collide(asteroids):
    stack = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            if stack[-1] < -a:
                stack.pop()
            elif stack[-1] == -a:
                stack.pop()
                alive = False
            else:
                alive = False
        if alive:
            stack.append(a)
    return stack


assert collide([10, 2, -5]) == [10]
assert collide([8, -8]) == []
assert collide([-2, -1, 1, 2]) == [-2, -1, 1, 2]
assert collide([1, 2, 3, -10]) == [-10]
```

```cpp
vector<int> collide(const vector<int>& asteroids) {
    vector<int> stack;
    for (int a : asteroids) {
        bool alive = true;
        while (alive && a < 0 && !stack.empty() && stack.back() > 0) {
            if (stack.back() < -a) {
                stack.pop_back();
            } else if (stack.back() == -a) {
                stack.pop_back();
                alive = false;
            } else {
                alive = false;
            }
        }
        if (alive) {
            stack.push_back(a);
        }
    }
    return stack;
}
```

Notice the new shape: the `while` loop pops **several** items for one new arrival. That shape, "pop while the top loses to the newcomer", is the heart of the next chapter.

## 4.4 Check yourself

1. In the minimum stack, why does popping an item also pop the matching entry in the minimum list?
2. What do we push on the stack when `decode` meets `[`, and what do we do with it at `]`?
3. In the asteroid problem, which pairs of neighbours can never collide?
4. Why does one new asteroid sometimes pop several survivors?

# Chapter 5. The monotonic stack

## 5.1 The next bigger value

Here is a question that sounds simple. For every number in a list, find the first number to its right that is **strictly bigger**, or report `-1` if there is none. For `[3, 1, 4, 2, 5]` the answers are `[4, 4, 5, 5, -1]`: after 3 comes 1 and then 4, so 4 is the first bigger one, and so on.

The direct method starts at each position and scans to the right until it finds a bigger value. It is correct, but in the worst case (a list that only decreases, like `[5, 4, 3, 2, 1]`) every scan walks to the end, so the total is $O(n^2)$ steps. For a list of 100,000 numbers that is billions of steps. We want $O(n)$.

```python
def next_greater_slow(nums):
    n = len(nums)
    answer = [-1] * n
    for i in range(n):
        for j in range(i + 1, n):
            if nums[j] > nums[i]:
                answer[i] = nums[j]
                break
    return answer


assert next_greater_slow([3, 1, 4, 2, 5]) == [4, 4, 5, 5, -1]
```

```cpp
vector<int> nextGreaterSlow(const vector<int>& nums) {
    int n = nums.size();
    vector<int> answer(n, -1);
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (nums[j] > nums[i]) {
                answer[i] = nums[j];
                break;
            }
        }
    }
    return answer;
}
```

## 5.2 A waiting room

Flip the question around. Instead of each number searching to its right, let each number **wait** until a bigger one shows up, and let the bigger one tell everyone who was waiting. Scan from left to right and keep a stack called the waiting room. It holds the positions (indices) of numbers that have not yet found a bigger value.

When a new number $x$ arrives, look at the top of the waiting room. If the top number is smaller than $x$, then $x$ is the first bigger value to its right, so we record the answer for it and remove it. Keep doing this while the top is smaller than $x$. Then $x$ itself joins the waiting room.

Why is this correct? Think about what the waiting room looks like. Whenever a number is added, everything smaller than it has just left, so the numbers that remain are all **at least as big**. Therefore the waiting room, read from bottom to top, never increases: it is a non-increasing sequence. A stack whose contents are always sorted this way is called a **monotonic stack** ("monotonic" means moving in one direction only). The biggest waiting number is at the bottom, the smallest at the top, so if the top is not smaller than $x$, nothing below it is either, and we can stop. That is the key fact that makes the scan quick.

Trace on `[2, 1, 2, 4, 3]` (the stack shows indices, but we write the values):

```
read 2:  waiting [2]
read 1:  1 is not bigger than 2          waiting [2, 1]
read 2:  bigger than 1 -> answer for 1 is 2; 2 is not bigger than 2   waiting [2, 2]
read 4:  bigger than 2 -> answer 4; bigger than 2 -> answer 4          waiting [4]
read 3:  not bigger than 4                                            waiting [4, 3]
end:     4 and 3 never got a bigger value -> -1, -1
answers (by position): [4, 2, 4, -1, -1]
```

Why is it fast? Every index enters the waiting room exactly once and leaves at most once. The inner `while` loop may pop many items at one step, but over the whole scan the total number of pops is at most $n$. So the whole thing is $O(n)$ time and $O(n)$ space. When a cost is spread out like this, with some steps cheap and a few expensive but a small total, it is called **amortised** analysis.

This is exactly the problem _Next Greater Element_.

```python
def next_greater(nums):
    answer = [-1] * len(nums)
    waiting = []
    for i, x in enumerate(nums):
        while waiting and nums[waiting[-1]] < x:
            answer[waiting.pop()] = x
        waiting.append(i)
    return answer


assert next_greater([3, 1, 4, 2, 5]) == [4, 4, 5, 5, -1]
assert next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
assert next_greater([5, 4, 3]) == [-1, -1, -1]
assert next_greater([]) == []
```

```cpp
vector<int> nextGreater(const vector<int>& nums) {
    int n = nums.size();
    vector<int> answer(n, -1);
    vector<int> waiting;
    for (int i = 0; i < n; i++) {
        while (!waiting.empty() && nums[waiting.back()] < nums[i]) {
            answer[waiting.back()] = nums[i];
            waiting.pop_back();
        }
        waiting.push_back(i);
    }
    return answer;
}
```

We store **indices**, not values, because with an index we can both read the value (`nums[i]`) and write the answer into the right slot of `answer`. Storing indices is the habit to build for every monotonic-stack problem.

## 5.3 Counting the days until

A small change turns this into a different question: for each day's temperature, how many days must you wait for a warmer day? For `[73, 74, 75, 71, 69, 72, 76, 73]` the answers are `[1, 1, 4, 2, 1, 1, 0, 0]`.

It is the same waiting room. The only difference is what we write when a day $j$ gets answered by day $i$: not the temperature, but the **distance** $i - j$. Days that never get answered stay at 0, which is just the default. This is the reason to store indices: the distance needs them.

This is exactly the problem _Daily Temperatures_.

```python
def days_until_warmer(temps):
    answer = [0] * len(temps)
    waiting = []
    for i, t in enumerate(temps):
        while waiting and temps[waiting[-1]] < t:
            j = waiting.pop()
            answer[j] = i - j
        waiting.append(i)
    return answer


assert days_until_warmer([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
assert days_until_warmer([30, 40, 50]) == [1, 1, 0]
assert days_until_warmer([50, 40, 30]) == [0, 0, 0]
```

```cpp
vector<int> daysUntilWarmer(const vector<int>& temps) {
    int n = temps.size();
    vector<int> answer(n, 0);
    vector<int> waiting;
    for (int i = 0; i < n; i++) {
        while (!waiting.empty() && temps[waiting.back()] < temps[i]) {
            int j = waiting.back();
            waiting.pop_back();
            answer[j] = i - j;
        }
        waiting.push_back(i);
    }
    return answer;
}
```

## 5.4 Going around a circle

Now imagine the list is a circle: after the last element comes the first again. For `[1, 2, 1]` the last `1` looks onward to the first `1` and then to the `2`, so its answer is 2. The first `1` is answered by the 2 right next to it, and the `2` itself has no bigger number anywhere on the circle, so its answer is `-1`.

The trick: pretend the list is written twice in a row, `[1, 2, 1, 1, 2, 1]`, and scan through all $2n$ positions, reading the value at `i % n`. During the first pass we push indices as usual. During the second pass we only **answer** the waiting numbers and push nothing new, because every index was already pushed in the first pass. A number that is still waiting at the end has looked at everything, wrapped around, so it truly has no bigger number.

This is exactly the problem _Next Greater Element in a Circle_. It takes $O(n)$ time: two passes, each index pushed once and popped at most once.

```python
def next_greater_circular(nums):
    n = len(nums)
    answer = [-1] * n
    waiting = []
    for i in range(2 * n):
        x = nums[i % n]
        while waiting and nums[waiting[-1]] < x:
            answer[waiting.pop()] = x
        if i < n:
            waiting.append(i)
    return answer


assert next_greater_circular([1, 2, 1]) == [2, -1, 2]
assert next_greater_circular([5, 4, 3, 6]) == [6, 6, 6, -1]
assert next_greater_circular([2, 2]) == [-1, -1]
```

```cpp
vector<int> nextGreaterCircular(const vector<int>& nums) {
    int n = nums.size();
    vector<int> answer(n, -1);
    vector<int> waiting;
    for (int i = 0; i < 2 * n; i++) {
        int x = nums[i % n];
        while (!waiting.empty() && nums[waiting.back()] < x) {
            answer[waiting.back()] = x;
            waiting.pop_back();
        }
        if (i < n) {
            waiting.push_back(i);
        }
    }
    return answer;
}
```

## 5.5 Check yourself

1. Why is the waiting room always sorted from big (bottom) to small (top)?
2. Why do we store indices on the stack instead of values?
3. A single new number can pop many items. Why is the total work still $O(n)$?
4. In the circular version, why do we push indices only in the first pass?

# Chapter 6. Spans, rectangles and contributions

## 6.1 Looking to the left

The waiting room can also look **backwards**. Instead of "the next bigger to my right", ask "the previous bigger to my left". We scan left to right again, but this time the stack holds candidates for being the answer for future numbers. When a new number arrives, we remove from the top every number that is not bigger than it (for any later number, the new one is at least as big and also closer, so those old ones can never be the nearest bigger value again). After the removals, the top, if any, is the nearest number to the left that is bigger. Then we push the new number.

A neat use is the **span** of a stock price: the number of consecutive days, ending today and counting today, on which the price was at most today's price. If $p$ is the position of the previous strictly bigger price (or $-1$ if there is none), the span of day $i$ is $i - p$.

For prices `[5, 3, 4, 6, 2]`: day 0 has span 1; day 1 (price 3) has span 1 since 5 is bigger; day 2 (price 4) removes the 3 and stops at 5, so its span is $2 - 0 = 2$; day 3 (price 6) removes 4 and 5 and has no bigger price before it, so its span is $3 - (-1) = 4$; day 4 (price 2) has span 1. The spans are `[1, 1, 2, 4, 1]`.

This is exactly the problem _Stock Span_. It runs in $O(n)$ time by the same amortised argument as before.

```python
def stock_span(prices):
    stack = []
    spans = []
    for i, p in enumerate(prices):
        while stack and prices[stack[-1]] <= p:
            stack.pop()
        previous = stack[-1] if stack else -1
        spans.append(i - previous)
        stack.append(i)
    return spans


assert stock_span([5, 3, 4, 6, 2]) == [1, 1, 2, 4, 1]
assert stock_span([100, 80, 60, 70, 60, 75, 85]) == [1, 1, 1, 2, 1, 4, 6]
assert stock_span([7, 7, 7]) == [1, 2, 3]
```

```cpp
vector<int> stockSpan(const vector<int>& prices) {
    vector<int> stack;
    vector<int> spans;
    for (int i = 0; i < (int)prices.size(); i++) {
        while (!stack.empty() && prices[stack.back()] <= prices[i]) {
            stack.pop_back();
        }
        int previous = stack.empty() ? -1 : stack.back();
        spans.push_back(i - previous);
        stack.push_back(i);
    }
    return spans;
}
```

## 6.2 The largest rectangle in a histogram

A histogram is a row of bars, each 1 wide, with given heights. What is the biggest rectangle that fits inside the bars? A rectangle inside a histogram has a height equal to its shortest bar, so a useful way to look at it: fix a bar $i$ and ask for the widest rectangle of height `heights[i]` that contains bar $i$. It stretches left and right until it meets a bar **shorter** than bar $i$. So for every bar we need the nearest shorter bar on the left and the nearest shorter bar on the right: two "nearest smaller" questions, which the monotonic stack answers.

We can do both at once. Keep a stack of indices with **increasing** heights. When bar $i$ arrives and the top of the stack is not shorter than it, the top bar can stretch no further to the right: bar $i$ is its right boundary. Its left boundary is the stack entry just below it. The width is the gap between the two boundaries, exclusive: `i - left - 1`. We pop it and record `height * width`. After the scan, we add a fake bar of height 0 at the end, which forces everything left on the stack to be popped.

Trace on `[2, 4, 3, 5, 1]`:

```
i=2 (3): top 4 is not shorter -> pop 4: left boundary is bar 0, width 1, area 4
i=4 (1): pop 5: left boundary is bar 2, width 1, area 5
         pop 3: left boundary is bar 0, width 3, area 9
         pop 2: no left boundary, width 4, area 8
end (0): pop 1: no left boundary, width 5, area 5
best = 9   (the bars 4, 3, 5 give height 3 and width 3)
```

This is exactly the problem _Largest Rectangle in a Histogram_. Each bar is pushed and popped once: $O(n)$ time.

```python
def largest_rectangle(heights):
    stack = []
    best = 0
    for i in range(len(heights) + 1):
        h = heights[i] if i < len(heights) else 0
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best


assert largest_rectangle([2, 4, 3, 5, 1]) == 9
assert largest_rectangle([2, 1, 5, 6, 2, 3]) == 10
assert largest_rectangle([3, 3, 3]) == 9
assert largest_rectangle([]) == 0
```

```cpp
int largestRectangle(const vector<int>& heights) {
    vector<int> stack;
    int best = 0;
    int n = heights.size();
    for (int i = 0; i <= n; i++) {
        int h = (i < n) ? heights[i] : 0;
        while (!stack.empty() && heights[stack.back()] >= h) {
            int height = heights[stack.back()];
            stack.pop_back();
            int left = stack.empty() ? -1 : stack.back();
            best = max(best, height * (i - left - 1));
        }
        stack.push_back(i);
    }
    return best;
}
```

If two bars have the same height, the first is popped with a width that is too small. This is harmless, because the later of the two is popped afterwards with the full width.

## 6.3 Rectangles inside a grid

A grid of 0s and 1s hides histograms. Process the grid row by row and keep, for every column, the number of consecutive 1s ending at the current row (the height of the "bar" of ones standing on this row). If the cell is 0 the height resets to 0; otherwise it grows by 1. Then each row is a histogram, and the largest rectangle of ones whose bottom edge lies on this row is exactly the largest rectangle in that histogram. The answer is the best over all rows.

For the grid `[[1,1],[1,1],[0,1]]` the row histograms are `[1,1]`, `[2,2]` and `[0,3]`, with best areas 2, 4 and 3. The answer is 4 (the 2-by-2 block).

This is exactly the problem _Maximal Rectangle of Ones_. For a grid with $r$ rows and $c$ columns it costs $O(r \cdot c)$ time, since each row is handled in $O(c)$.

```python
def maximal_rectangle(matrix):
    if not matrix:
        return 0
    heights = [0] * len(matrix[0])
    best = 0
    for row in matrix:
        for j, cell in enumerate(row):
            heights[j] = heights[j] + 1 if cell == 1 else 0
        best = max(best, largest_rectangle(heights))
    return best


assert maximal_rectangle([[1, 1], [1, 1], [0, 1]]) == 4
assert maximal_rectangle([[0, 0], [0, 0]]) == 0
assert maximal_rectangle([[1, 0, 1, 1]]) == 2
```

```cpp
int maximalRectangle(const vector<vector<int>>& matrix) {
    if (matrix.empty()) {
        return 0;
    }
    vector<int> heights(matrix[0].size(), 0);
    int best = 0;
    for (const vector<int>& row : matrix) {
        for (int j = 0; j < (int)row.size(); j++) {
            heights[j] = (row[j] == 1) ? heights[j] + 1 : 0;
        }
        best = max(best, largestRectangle(heights));
    }
    return best;
}
```

(The function `largest_rectangle` is the one from the section before.)

## 6.4 Counting by contribution

A different way to use "nearest smaller" boundaries: summing over **all subarrays**. Take the list `[3, 1, 2, 4]`. There are ten subarrays, and we want the sum of the minimum of each: `3, 1, 2, 4, 1, 1, 2, 1, 1, 1`, which adds up to 17. Listing them all takes $O(n^2)$ time at best.

The idea is to ask, instead, for each element: _in how many subarrays am I the minimum?_ If element $i$ is the minimum of exactly $c_i$ subarrays, the answer is $\sum_i a_i \cdot c_i$. Element $i$ is the minimum of a subarray if the subarray lies inside the stretch where nothing is smaller than it. Suppose that stretch reaches `L` positions to the left (counting $i$ itself) and `R` positions to the right (counting $i$ itself). A subarray picks any of the `L` left ends and any of the `R` right ends, so $c_i = L \cdot R$. The numbers `L` and `R` are "distance to the nearest smaller", which the monotonic stack gives us.

One detail needs care: **ties**. In `[2, 5, 2]` a subarray like `[2, 5, 2]` has two elements equal to its minimum, and we must count it only once. The rule: on the left stop at a _strictly smaller_ element, and on the right stop at a _smaller or equal_ element. Then each subarray is credited to its rightmost minimum, once. In the code below, the left pass pops while the top is greater than or equal to the new element, and the right pass pops while the top is strictly greater.

The answer is asked modulo $10^9 + 7$ because it can be huge; in Python integers never overflow, in C++ we use `long long`.

This is exactly the problem _Sum of Subarray Minimums_. Two linear passes: $O(n)$ time.

```python
def sum_subarray_mins(arr):
    mod = 10**9 + 7
    n = len(arr)
    left = [0] * n
    right = [0] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = i - (stack[-1] if stack else -1)
        stack.append(i)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = (stack[-1] if stack else n) - i
        stack.append(i)
    total = 0
    for i in range(n):
        total += arr[i] * left[i] * right[i]
    return total % mod


assert sum_subarray_mins([3, 1, 2, 4]) == 17
assert sum_subarray_mins([2, 5, 2]) == 15
assert sum_subarray_mins([7]) == 7
```

```cpp
int sumSubarrayMins(const vector<int>& arr) {
    const long long mod = 1000000007LL;
    int n = arr.size();
    vector<long long> left(n), right(n);
    vector<int> stack;
    for (int i = 0; i < n; i++) {
        while (!stack.empty() && arr[stack.back()] >= arr[i]) {
            stack.pop_back();
        }
        left[i] = i - (stack.empty() ? -1 : stack.back());
        stack.push_back(i);
    }
    stack.clear();
    for (int i = n - 1; i >= 0; i--) {
        while (!stack.empty() && arr[stack.back()] > arr[i]) {
            stack.pop_back();
        }
        right[i] = (stack.empty() ? n : stack.back()) - i;
        stack.push_back(i);
    }
    long long total = 0;
    for (int i = 0; i < n; i++) {
        total = (total + arr[i] % mod * left[i] % mod * right[i]) % mod;
    }
    return (int)total;
}
```

## 6.5 Check yourself

1. In the stock span, why do we pop prices that are less than or equal to today's price?
2. For a bar of height 4 with nearest shorter bars at positions 1 and 6, what is the widest rectangle of height 4 through it?
3. Why does the maximal-rectangle method treat each row as a histogram?
4. Why do the left and right passes use `>=` and `>` (one strict, one not) in the contribution method?

# Chapter 7. Stacks that choose

## 7.1 Removing digits to get a smaller number

Here is a greedy puzzle. Given a number written as a string of digits, delete exactly $k$ digits so that the number that remains is as small as possible. For `3254` and $k = 2$ the answer is `24`.

What should we delete? Compare two numbers of the same length digit by digit from the left: the first difference decides. So we want the **leftmost digits to be as small as possible**. When a digit is followed by a smaller digit, deleting the bigger one makes the number smaller (the position gets a smaller digit). So scan left to right with a stack of kept digits. When a new digit arrives, while we still may delete and the top of the stack is **bigger** than the new digit, pop it (that is a deletion). Then push the new digit.

Trace of `3254`, $k = 2$: push 3; 2 arrives, 3 is bigger, pop 3 (one deletion used), push 2; 5 arrives, push; 4 arrives, 5 is bigger, pop 5 (second deletion used), push 4. Result: `24`.

Two cleanups remain. If the digits never decrease (like `112`), no pop happened and we still owe deletions: delete from the **end**, because those are the least important digits. And strip leading zeros, giving `0` if nothing is left (`10200` with $k = 1$ becomes `0200`, and then `200`).

This is exactly the problem _Remove K Digits_. It takes $O(n)$ time.

```python
def remove_k_digits(num, k):
    stack = []
    for d in num:
        while k > 0 and stack and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    if k > 0:
        stack = stack[:-k]
    result = "".join(stack).lstrip("0")
    return result or "0"


assert remove_k_digits("3254", 2) == "24"
assert remove_k_digits("10200", 1) == "200"
assert remove_k_digits("112", 1) == "11"
assert remove_k_digits("9", 1) == "0"
```

```cpp
string removeKDigits(const string& num, int k) {
    string stack;
    for (char d : num) {
        while (k > 0 && !stack.empty() && stack.back() > d) {
            stack.pop_back();
            k--;
        }
        stack.push_back(d);
    }
    stack.resize(stack.size() - k);
    size_t start = stack.find_first_not_of('0');
    if (start == string::npos) {
        return "0";
    }
    return stack.substr(start);
}
```

In the C++ code, `k` is at most the stack size at the end, so `resize` with `size - k` is safe (when `k` is already 0 it changes nothing).

## 7.2 Cars that cannot overtake

Cars drive on a one-lane road toward a target. A car that catches a slower one ahead cannot pass, so it slows down and follows it; they then arrive together as a **fleet**. How many fleets arrive?

Look at the cars from the one closest to the target backwards. For each car compute the time it would need if the road were free: $t = (\text{target} - \text{position}) / \text{speed}$. The car closest to the target leads the first fleet. The next car back arrives earlier or at the same time as the leader would, so it catches up and joins the fleet; or it needs longer, in which case it never catches up and starts a new fleet. In other words: going from front to back, a car starts a new fleet exactly when its time is **strictly larger** than the time of the fleet ahead of it. The fleet leaders' times form an increasing sequence, and the stack holds the fleet leaders. The answer is the number of fleets on the stack.

To avoid decimals we compare two times $d_1 / s_1$ and $d_2 / s_2$ by cross-multiplying: $d_1 \cdot s_2 > d_2 \cdot s_1$.

Example: target 10 with cars `[[8, 1], [5, 4], [0, 1]]` (position, speed). The times are 2, 1.25 and 10. The car at 8 leads (time 2). The car at 5 needs only 1.25 so it joins that fleet. The car at 0 needs 10, longer than 2, so it starts a second fleet. The answer is 2.

This is exactly the problem _Car Fleet_. Sorting costs $O(n \log n)$; the scan is $O(n)$.

```python
def car_fleet(target, cars):
    order = sorted(cars, reverse=True)
    fleets = []
    for position, speed in order:
        dist = target - position
        if not fleets or dist * fleets[-1][1] > fleets[-1][0] * speed:
            fleets.append((dist, speed))
    return len(fleets)


assert car_fleet(10, [[8, 1], [5, 4], [0, 1]]) == 2
assert car_fleet(12, [[10, 2], [8, 4], [0, 1], [5, 1], [3, 3]]) == 3
assert car_fleet(5, [[1, 1]]) == 1
```

```cpp
int carFleet(int target, vector<vector<int>> cars) {
    sort(cars.begin(), cars.end(), [](const vector<int>& a, const vector<int>& b) {
        return a[0] > b[0];
    });
    vector<pair<long long, long long>> fleets;
    for (const vector<int>& car : cars) {
        long long dist = target - car[0];
        long long speed = car[1];
        if (fleets.empty() || dist * fleets.back().second > fleets.back().first * speed) {
            fleets.push_back({dist, speed});
        }
    }
    return (int)fleets.size();
}
```

Only the top of the stack is ever looked at, so a single variable would do; we keep the stack to show that this too is the "decide against the top" pattern.

## 7.3 Check yourself

1. In _Remove K Digits_, why do we pop a digit when the next digit is smaller?
2. If no pop happens at all, which digits do we delete, and why?
3. In the car fleet example, why does the car at position 5 not create a new fleet?
4. Why can we compare two arrival times using only whole-number multiplication?

# Chapter 8. Queues

## 8.1 A line at the counter

A queue is the opposite of a stack. Think of people waiting at a ticket counter: the person who arrived first is served first. This rule is **first in, first out**, or FIFO. The operations are **enqueue** (join at the back), **dequeue** (leave from the front), and look at the front.

It is tempting to use a Python list with `append` and `pop(0)`. That works but is slow: removing the first element of a list makes every other element shift one place, so each `pop(0)` costs $O(n)$. The standard fix is `collections.deque` (say "deck", short for double-ended queue), where `append` and `popleft` both cost $O(1)$. In C++ the `queue` and `deque` types do the same job.

```
front                  back
  [A] [B] [C] [D]  <--- new arrivals join here
   ^
   next to be served
```

## 8.2 Counting in order

A queue shines when new items must be produced in the same order they were discovered. Here is a little puzzle: list the numbers that use only the digits 1 and 2, in increasing order: `1, 2, 11, 12, 21, 22, 111, ...`. Start the queue with `1` and `2`. Repeatedly take the front number, output it, and put two new numbers at the back: the front with a `1` appended and the front with a `2` appended. Because all numbers in the queue are processed from the shortest to the longest, and each number's children come after all the numbers already waiting, the output comes out in increasing order.

Now switch the digits to 0 and 1, start with just `1`, and you get the binary numbers: `1, 10, 11, 100, 101, ...`. This is exactly the problem _Binary Numbers From 1 to N_. The cost is $O(n)$ steps, each of which builds a string.

```python
from collections import deque


def digits_one_two(n):
    out = []
    queue = deque(["1", "2"])
    while len(out) < n:
        s = queue.popleft()
        out.append(s)
        queue.append(s + "1")
        queue.append(s + "2")
    return out


def binary_up_to(n):
    out = []
    queue = deque(["1"])
    for _ in range(n):
        s = queue.popleft()
        out.append(s)
        queue.append(s + "0")
        queue.append(s + "1")
    return out


assert digits_one_two(7) == ["1", "2", "11", "12", "21", "22", "111"]
assert binary_up_to(5) == ["1", "10", "11", "100", "101"]
assert binary_up_to(0) == []
```

```cpp
vector<string> digitsOneTwo(int n) {
    vector<string> out;
    queue<string> q;
    q.push("1");
    q.push("2");
    while ((int)out.size() < n) {
        string s = q.front();
        q.pop();
        out.push_back(s);
        q.push(s + "1");
        q.push(s + "2");
    }
    return out;
}

vector<string> binaryUpTo(int n) {
    vector<string> out;
    queue<string> q;
    q.push("1");
    for (int i = 0; i < n; i++) {
        string s = q.front();
        q.pop();
        out.push_back(s);
        q.push(s + "0");
        q.push(s + "1");
    }
    return out;
}
```

## 8.3 Candidates in a stream

Characters arrive one by one. After each arrival we must say which character is the **first that has appeared only once so far** (or `#` if there is none). For `abacb` the answers are `a, a, b, b, c`.

We keep two things: a count of how often each character has appeared, and a queue of characters in arrival order that are still _candidates_. When a character arrives, increase its count and add it to the back of the queue. Then clean the front: while the front character now has a count above 1, it is no longer unique, so remove it. After the cleaning, the front of the queue, if there is one, is the first character with count exactly 1. Why correct? A character is only ever removed once it is repeated, and a repeated character stays repeated forever, so no valid candidate is ever lost. The queue order is the order of first appearance.

Each character is enqueued once and dequeued at most once, so the total cost is $O(n)$.

This is exactly the problem _First Non-Repeating Character in a Stream_.

```python
def first_unique_stream(s):
    count = {}
    queue = deque()
    out = []
    for ch in s:
        count[ch] = count.get(ch, 0) + 1
        queue.append(ch)
        while queue and count[queue[0]] > 1:
            queue.popleft()
        out.append(queue[0] if queue else "#")
    return "".join(out)


assert first_unique_stream("abacb") == "aabbc"
assert first_unique_stream("aabc") == "a#bb"
assert first_unique_stream("zz") == "z#"
```

```cpp
string firstUniqueStream(const string& s) {
    unordered_map<char, int> count;
    queue<char> q;
    string out;
    for (char ch : s) {
        count[ch]++;
        q.push(ch);
        while (!q.empty() && count[q.front()] > 1) {
            q.pop();
        }
        out.push_back(q.empty() ? '#' : q.front());
    }
    return out;
}
```

## 8.4 Simulating a deck of cards

A queue also models a deck of cards perfectly: the top card is the front, and "move a card to the bottom" is dequeue followed by enqueue. Consider this trick. You arrange a deck. Then repeat: reveal the top card and set it aside, and if cards remain, move the next top card to the bottom. How must the deck be arranged so that the revealed cards come out in increasing order?

Solve it by thinking about **positions** instead of values. Make a queue of the positions `0, 1, 2, ...` in the order the process would visit them: the first position taken is the first revealed, then the next one is moved to the bottom, and so on. Simulate the process on these positions. The first revealed position must hold the smallest value, the second revealed position the next smallest, and so on. So sort the values, and as the simulation reveals a position, write the next smallest value there.

For four cards, simulate on positions `0, 1, 2, 3`: reveal 0, move 1 to the back (queue `2, 3, 1`); reveal 2, move 3 to the back (queue `1, 3`); reveal 1, move 3 to the back; reveal 3. The reveal order of positions is `0, 2, 1, 3`. With sorted values `1, 2, 3, 4` assigned in that order, position 0 gets 1, position 2 gets 2, position 1 gets 3, position 3 gets 4, so the deck is `[1, 3, 2, 4]`.

This is exactly the problem _Reveal Cards in Increasing Order_. It costs $O(n \log n)$ for the sort and $O(n)$ for the simulation.

```python
def reveal_order(deck):
    n = len(deck)
    positions = deque(range(n))
    result = [0] * n
    for value in sorted(deck):
        i = positions.popleft()
        result[i] = value
        if positions:
            positions.append(positions.popleft())
    return result


assert reveal_order([4, 1, 3, 2]) == [1, 3, 2, 4]
assert reveal_order([17, 13, 11, 2, 3, 5, 7]) == [2, 13, 3, 11, 5, 17, 7]
assert reveal_order([5]) == [5]
```

```cpp
vector<int> revealOrder(vector<int> deck) {
    int n = deck.size();
    deque<int> positions;
    for (int i = 0; i < n; i++) {
        positions.push_back(i);
    }
    sort(deck.begin(), deck.end());
    vector<int> result(n, 0);
    for (int value : deck) {
        int i = positions.front();
        positions.pop_front();
        result[i] = value;
        if (!positions.empty()) {
            positions.push_back(positions.front());
            positions.pop_front();
        }
    }
    return result;
}
```

## 8.5 Check yourself

1. Which end of a queue do new items join, and which end do they leave from?
2. Why is `list.pop(0)` a poor way to implement a queue in Python?
3. In the stream problem, why can a character that was removed from the queue never become the answer again?
4. In the card problem, why do we simulate positions instead of the values?

# Chapter 9. A queue built from two stacks

## 9.1 Reversing twice

Suppose all you have are stacks, and someone asks for a queue. A stack gives out the newest item first, a queue the oldest. Here is the key observation: if you pour one stack into another, the order **reverses**. Items pushed 1, 2, 3 sit as `1, 2, 3` from bottom to top. Pop them all and push each onto a second stack, and the second stack holds `3, 2, 1` from bottom to top, with 1 on top. The oldest item is now on top, ready to be popped, which is exactly the queue behaviour.

So we use two stacks. New items always go onto the **inbox**. Items are always taken from the **outbox**. When the outbox is empty and we need an item, we pour the whole inbox into it, which reverses the order and puts the oldest item on top.

The one rule you must not break is: **only pour when the outbox is empty**. If the outbox still has items and you pour more on top of them, the new (newer) items would be served before older ones, breaking the queue order.

Walk through it: push 1, 2, 3 (inbox `[1, 2, 3]`). Pop: the outbox is empty, so pour; the outbox becomes `[3, 2, 1]` with 1 on top, and we pop 1. Now push 4 (inbox `[4]`). Pop: the outbox is not empty, so no pouring, and we pop 2. The order 1, 2 is right, and 4 will wait its turn behind 3.

```python
class TwoStackQueue:
    def __init__(self):
        self.inbox = []
        self.outbox = []

    def push(self, x):
        self.inbox.append(x)

    def _refill(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def pop(self):
        self._refill()
        return self.outbox.pop()

    def peek(self):
        self._refill()
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox


q = TwoStackQueue()
q.push(1)
q.push(2)
q.push(3)
assert q.pop() == 1
q.push(4)
assert q.pop() == 2
assert q.peek() == 3
assert q.empty() is False
```

```cpp
struct TwoStackQueue {
    vector<int> inbox;
    vector<int> outbox;

    void push(int x) { inbox.push_back(x); }

    void refill() {
        if (outbox.empty()) {
            while (!inbox.empty()) {
                outbox.push_back(inbox.back());
                inbox.pop_back();
            }
        }
    }

    int pop() {
        refill();
        int x = outbox.back();
        outbox.pop_back();
        return x;
    }

    int peek() {
        refill();
        return outbox.back();
    }

    bool empty() { return inbox.empty() && outbox.empty(); }
};
```

## 9.2 Why it is fast on average

A single `pop` can be slow: if the inbox holds a million items, one pour moves a million items. So is this really $O(1)$? Yes, **on average**, and here is the argument. Follow one item through its whole life. It is pushed onto the inbox once, moved to the outbox at most once, and popped from the outbox once. That is at most three cheap operations per item, no matter how the calls are interleaved. If we perform $m$ operations, at most $m$ items ever exist, so the total work is at most about $3m$, and the average per operation is $O(1)$. This kind of reasoning, where an expensive step is paid for by many cheap ones, is called **amortised** analysis, and it is the same argument that made the monotonic stack linear.

The sheet gives the operations as text, so here is a small runner that executes them from an empty queue and collects the answers of `pop`, `peek` and `empty` (printing `1` for an empty queue and `0` otherwise).

This is exactly the problem _Queue Made of Two Stacks_.

```python
def run_queue_ops(ops):
    queue = TwoStackQueue()
    results = []
    for op in ops:
        if op.startswith("push"):
            queue.push(int(op.split()[1]))
        elif op == "pop":
            results.append(queue.pop())
        elif op == "peek":
            results.append(queue.peek())
        else:
            results.append(1 if queue.empty() else 0)
    return results


assert run_queue_ops(["push 1", "push 2", "peek", "pop", "empty"]) == [1, 1, 0]
assert run_queue_ops(["push 7", "pop", "empty"]) == [7, 1]
```

```cpp
vector<int> runQueueOps(const vector<string>& ops) {
    TwoStackQueue queue;
    vector<int> results;
    for (const string& op : ops) {
        if (op.rfind("push", 0) == 0) {
            queue.push(stoi(op.substr(5)));
        } else if (op == "pop") {
            results.push_back(queue.pop());
        } else if (op == "peek") {
            results.push_back(queue.peek());
        } else {
            results.push_back(queue.empty() ? 1 : 0);
        }
    }
    return results;
}
```

## 9.3 Check yourself

1. Why does pouring one stack into another reverse the order of the items?
2. What goes wrong if we pour the inbox into the outbox while the outbox still has items?
3. How many times can a single item move from the inbox to the outbox?
4. Why is the average cost per operation $O(1)$ even though one `pop` can cost $O(n)$?

# Chapter 10. The monotonic deque

## 10.1 A queue with two ends

A **deque** (double-ended queue) lets you add and remove at both ends: `append` and `pop` at the back, `appendleft` and `popleft` at the front. Python's `collections.deque` and C++'s `std::deque` do all four in $O(1)$. A deque can behave as a stack, as a queue, or as both at once. In this chapter we use both at once: we **pop from the back** (like a stack) to remove items that can no longer matter, and **pop from the front** (like a queue) to remove items that have grown too old.

## 10.2 Sliding window maximum

A window of size $k$ slides along a list, one step at a time. We want the maximum of every window. For `[5, 3, 4, 1, 2, 6]` and $k = 3$ the windows are `[5,3,4]`, `[3,4,1]`, `[4,1,2]`, `[1,2,6]`, with maximums `5, 4, 4, 6`.

Looking at every window from scratch costs $O(nk)$. Here is a smarter thought. Suppose the window contains `3` and then a bigger number `4` arrives to its right. The `3` is older (it leaves the window sooner) **and** smaller. It can never be the maximum of any window again, because every window that contains the `3` also contains the `4`. So we may throw the `3` away as soon as `4` arrives. In general, when a new number arrives, discard from the back every number that is smaller than or equal to it.

That keeps a deque of numbers (we store indices) that is decreasing from front to back, a monotonic deque, as in the waiting room of Chapter 5. Two facts follow. The **front is always the maximum** of the current window. And the only reason to remove from the front is age: when the index at the front has slid out of the window (its index is at most $i - k$), remove it.

Trace on `[5, 3, 4, 1, 2, 6]`, $k = 3$ (values shown, not indices):

```
read 5:  deque [5]
read 3:  deque [5, 3]
read 4:  4 beats 3 -> deque [5, 4]          window full: max 5
read 1:  deque [5, 4, 1], then 5 is too old -> [4, 1]     max 4
read 2:  2 beats 1 -> [4, 2]                max 4
read 6:  6 beats 2 and 4 -> [6]             max 6
```

Each index enters the deque once and leaves once, so the total is $O(n)$ time and $O(k)$ extra space.

This is exactly the problem _Sliding Window Maximum_.

```python
from collections import deque


def window_max(nums, k):
    window = deque()
    out = []
    for i, x in enumerate(nums):
        while window and nums[window[-1]] <= x:
            window.pop()
        window.append(i)
        if window[0] <= i - k:
            window.popleft()
        if i >= k - 1:
            out.append(nums[window[0]])
    return out


assert window_max([5, 3, 4, 1, 2, 6], 3) == [5, 4, 4, 6]
assert window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
assert window_max([9], 1) == [9]
```

```cpp
vector<int> windowMax(const vector<int>& nums, int k) {
    deque<int> window;
    vector<int> out;
    for (int i = 0; i < (int)nums.size(); i++) {
        while (!window.empty() && nums[window.back()] <= nums[i]) {
            window.pop_back();
        }
        window.push_back(i);
        if (window.front() <= i - k) {
            window.pop_front();
        }
        if (i >= k - 1) {
            out.push_back(nums[window.front()]);
        }
    }
    return out;
}
```

## 10.3 A window that grows and shrinks

Now the window does not have a fixed size. We want the longest stretch of the list in which the difference between its largest and smallest value is at most `limit`. This is the two-pointer ("sliding window") technique: a right end that moves forward one step at a time, and a left end that moves forward only when the stretch breaks the rule. If a stretch is too wide, any longer stretch containing it is too wide as well, so moving the left end forward is the only way to repair it.

The missing ingredient is knowing the largest and smallest value inside the current stretch quickly. We already have a tool for the maximum of a moving window: the monotonic deque. For the minimum we use a second deque that is _increasing_ (pop from the back while the back is greater than or equal to the new value). Use both: the front of the first deque is the maximum, the front of the second is the minimum.

At each step: add the new value to both deques; then, while the maximum minus the minimum is above `limit`, advance the left end by one, and remove from the front of a deque any index that has fallen to the left of the new left end. Record the width of the window.

For `[10, 1, 2, 4, 7, 2]` with `limit = 5`: the stretch `[2, 4, 7, 2]` has maximum 7 and minimum 2, difference 5, which is allowed, and no longer stretch works, so the answer is 4. Each index enters and leaves each deque once: $O(n)$ time.

This is exactly the problem _Longest Subarray Within a Limit_.

```python
def longest_within_limit(nums, limit):
    max_dq = deque()
    min_dq = deque()
    left = 0
    best = 0
    for right, x in enumerate(nums):
        while max_dq and nums[max_dq[-1]] <= x:
            max_dq.pop()
        max_dq.append(right)
        while min_dq and nums[min_dq[-1]] >= x:
            min_dq.pop()
        min_dq.append(right)
        while nums[max_dq[0]] - nums[min_dq[0]] > limit:
            left += 1
            if max_dq[0] < left:
                max_dq.popleft()
            if min_dq[0] < left:
                min_dq.popleft()
        best = max(best, right - left + 1)
    return best


assert longest_within_limit([10, 1, 2, 4, 7, 2], 5) == 4
assert longest_within_limit([8, 2, 4, 7], 4) == 2
assert longest_within_limit([4, 2, 2, 2, 4, 4, 2, 2], 0) == 3
```

```cpp
int longestWithinLimit(const vector<int>& nums, int limit) {
    deque<int> maxDq, minDq;
    int left = 0;
    int best = 0;
    for (int right = 0; right < (int)nums.size(); right++) {
        int x = nums[right];
        while (!maxDq.empty() && nums[maxDq.back()] <= x) {
            maxDq.pop_back();
        }
        maxDq.push_back(right);
        while (!minDq.empty() && nums[minDq.back()] >= x) {
            minDq.pop_back();
        }
        minDq.push_back(right);
        while (nums[maxDq.front()] - nums[minDq.front()] > limit) {
            left++;
            if (maxDq.front() < left) {
                maxDq.pop_front();
            }
            if (minDq.front() < left) {
                minDq.pop_front();
            }
        }
        best = max(best, right - left + 1);
    }
    return best;
}
```

## 10.4 Negative numbers and prefix sums

The last problem looks like a plain sliding window but is not: find the **shortest** non-empty stretch whose sum is **at least** $k$, when the numbers may be **negative**. With only positive numbers we could slide a window: grow it until the sum is big enough, then shrink it. With negatives that fails, because shrinking the window can increase the sum, so we cannot know when to stop.

A good way to handle sums of stretches is with **prefix sums**: let $P_j$ be the sum of the first $j$ numbers, with $P_0 = 0$. The sum of the stretch from position $i$ up to (not including) $j$ is $P_j - P_i$. Now the question becomes: find $i < j$ with $P_j - P_i \ge k$ and $j - i$ as small as possible.

Process $j$ from left to right and keep a deque of earlier indices $i$. Two rules keep the deque useful.

First, **front rule**: if $P_j - P_{\text{front}} \ge k$, we have found a valid stretch ending at $j$. Record its length, and remove that front index for good. Why can we forget it? Any later $j'$ pairing with it would give a longer stretch than the one we just found, so it can never help again.

Second, **back rule**: before adding $j$, remove from the back every index $i$ with $P_i \ge P_j$. Why? Index $j$ is later (so it gives shorter stretches) and has a smaller-or-equal prefix sum (so it makes $P_{j'} - P_j$ at least as big). It beats the old index in every future comparison. After this rule the prefix sums in the deque are increasing from front to back.

Trace on `[1, -1, 5, -2, 3]` with $k = 6$. The prefix sums are `0, 1, 0, 5, 3, 6`. Showing the prefix values in the deque: after $j=0$: `[0]`; $j=1$: `[0, 1]`; $j=2$ (value 0) removes `1` and `0` from the back: `[0]` (this is the new index 2); $j=3$: `[0, 5]`; $j=4$ (value 3) removes `5`: `[0, 3]`; $j=5$ (value 6): $6 - 0 = 6 \ge 6$, so we found the stretch from index 2 to 5, which has length 3 (the numbers `5, -2, 3`). The answer is 3.

This is exactly the problem _Shortest Subarray With Sum at Least K_. Every index enters and leaves the deque once: $O(n)$ time and space.

```python
def shortest_at_least_k(nums, k):
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, x in enumerate(nums):
        prefix[i + 1] = prefix[i] + x
    window = deque()
    best = n + 1
    for j in range(n + 1):
        while window and prefix[j] - prefix[window[0]] >= k:
            best = min(best, j - window.popleft())
        while window and prefix[window[-1]] >= prefix[j]:
            window.pop()
        window.append(j)
    return best if best <= n else -1


assert shortest_at_least_k([1, -1, 5, -2, 3], 6) == 3
assert shortest_at_least_k([2, -1, 2], 3) == 3
assert shortest_at_least_k([1, 2], 4) == -1
assert shortest_at_least_k([5], 5) == 1
```

```cpp
int shortestAtLeastK(const vector<int>& nums, int k) {
    int n = nums.size();
    vector<long long> prefix(n + 1, 0);
    for (int i = 0; i < n; i++) {
        prefix[i + 1] = prefix[i] + nums[i];
    }
    deque<int> window;
    int best = n + 1;
    for (int j = 0; j <= n; j++) {
        while (!window.empty() && prefix[j] - prefix[window.front()] >= k) {
            best = min(best, j - window.front());
            window.pop_front();
        }
        while (!window.empty() && prefix[window.back()] >= prefix[j]) {
            window.pop_back();
        }
        window.push_back(j);
    }
    return best <= n ? best : -1;
}
```

## 10.5 Check yourself

1. In the sliding window maximum, why can a smaller older number be discarded when a bigger newer one arrives?
2. What is the only reason to remove an element from the front of the deque?
3. Why does the longest-subarray method need two deques?
4. Why does the shortest-subarray method use prefix sums, and why does the usual shrinking window fail with negative numbers?
